"""ContinuousVI module for scRNA-seq data analysis.

This module provides classes and methods to train and utilize scVI models for
single-cell RNA-seq data. It supports the inclusion of continuous covariates
(e.g., pseudotime in trajectory analysis, aging or other continuous measurements) while correcting for batch
effects. The main classes are:

- ContinuousVI: Sets up the anndata object and trains multiple scVI models.
- TrainedContinuousVI: Manages one or more trained scVI models, provides methods
  for generating embeddings, sampling expression parameters, and performing
  regression analysis.
"""

from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import patsy
import pyro
import pyro.distributions as dist
import scanpy as sc
import scvi
import statsmodels.api as sm
import torch
from pyro.infer import MCMC, NUTS
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

from .continuous_harmony import run_continuous_harmony

if TYPE_CHECKING:
    from scvi.distributions import ZeroInflatedNegativeBinomial


class ContinuousVI:
    """ContinuousVI module for scRNA-seq data analysis.

    This class is responsible for configuring the input data (AnnData object)
    and training multiple scVI models to account for batch effects, label keys,
    and one optional continuous covariate. Use the `train` method to train
    multiple scVI models. The trained models can be accessed via the returned
    `TrainedContinuousVI` instance.
    """

    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
    ) -> None:
        """Initialize a ContinuousVI object.

        Parameters
        ----------
        adata : sc.AnnData
            The annotated data matrix with cells (observations) and genes (variables).
        batch_key : str
            The column name in `adata.obs` that contains batch information.
        label_key : str or None
            The column name in `adata.obs` that contains label or cell-type information.
            If None, no label covariate is used.
        continuous_key : str or None
            The column name in `adata.obs` that contains a single continuous covariate
            (e.g., pseudotime). If None, no continuous covariate is used.

        """
        self.adata: sc.AnnData = adata
        self.batch_key: str = batch_key
        self.label_key: str | None = label_key
        self.continuous_key: str | None = continuous_key

    def train(
        self,
        n_train: int = 5,
        n_latent: int = 30,
        max_epochs: int = 800,
        early_stopping: bool = True,
    ) -> TrainedContinuousVI:
        """Train multiple scVI models (n_train times) and return a TrainedContinuousVI object.

        This method sets up the scVI anndata configuration once per training run
        and trains `n_train` scVI models with the same hyperparameters but
        potentially different random initializations.

        Parameters
        ----------
        n_train : int, default=5
            The number of times to train scVI with the same setup.
        n_latent : int, default=30
            The dimensionality of the scVI latent space (z).
        max_epochs : int, default=800
            The maximum number of training epochs.
        early_stopping : bool, default=True
            Whether to apply early stopping based on validation loss improvements.

        Returns
        -------
        TrainedContinuousVI
            A TrainedContinuousVI object containing the trained scVI models,
            allowing further analysis and model usage.

        """
        _trained_models: list[scvi.model.SCVI] = []
        for _ in tqdm(
            range(n_train),
            desc="Training multiple scVI models",
            leave=False,
        ):
            scvi.model.SCVI.setup_anndata(
                self.adata,
                batch_key=self.batch_key,
                labels_key=self.label_key,
                continuous_covariate_keys=[self.continuous_key] if self.continuous_key else None,
            )
            model = scvi.model.SCVI(self.adata, n_latent=n_latent)
            model.train(max_epochs=max_epochs, early_stopping=early_stopping)
            _trained_models.append(model)
        return TrainedContinuousVI(
            adata=self.adata,
            batch_key=self.batch_key,
            label_key=self.label_key,
            continuous_key=self.continuous_key,
            trained_models=_trained_models,
        )


class TrainedContinuousVI:
    """TrainedContinuousVI manages one or more trained scVI models for scRNA-seq data.

    This class provides methods to:
    - Load or store multiple trained scVI models.
    - Calculate embeddings (UMAP, clusters) using the latent representation.
    - Perform regressions against the continuous covariate.
    - Sample parameters from the generative model (px).
    - Save the trained models to disk.
    """

    @overload
    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_models: list[scvi.model.SCVI],
    ) -> None: ...

    @overload
    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_model_path: Path | str,
    ) -> None: ...

    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_models: list[scvi.model.SCVI] | None = None,
        trained_model_path: Path | str | None = None,
    ) -> None:
        """Initialize a TrainedContinuousVI object with trained scVI models or a path to load them.

        Parameters
        ----------
        adata : sc.AnnData
            The annotated data matrix used for model training or inference.
        batch_key : str
            The column name in `adata.obs` for batch information.
        label_key : str or None
            The column name in `adata.obs` for label or cell-type information.
        continuous_key : str or None
            The column name in `adata.obs` for continuous covariate information.
        trained_models : list[scvi.model.SCVI], optional
            A list of scVI models that have already been trained.
        trained_model_path : Path or str, optional
            Path to a directory that contains one or more trained scVI models.
            If provided, the models at this path will be loaded instead of using
            `trained_models`.

        Raises
        ------
        ValueError
            If both `trained_models` and `trained_model_path` are None.

        """
        self.adata = adata
        self.batch_key: str = batch_key
        self.label_key: str | None = label_key
        self.continuous_key: str | None = continuous_key

        scvi.model.SCVI.setup_anndata(
            adata=adata,
            batch_key=batch_key,
            labels_key=label_key,
            continuous_covariate_keys=[continuous_key] if continuous_key is not None else None,
        )

        if trained_models is None and trained_model_path is None:
            raise ValueError(
                "`trained_models` or `trained_model_path` is required. Both are None.",
            )

        if trained_models is None and trained_model_path is not None:
            _trained_model_paths = [p for p in (trained_model_path if isinstance(trained_model_path, Path) else Path(trained_model_path)).rglob("*") if p.is_dir()]
            _trained_models: list[scvi.model.SCVI] = [scvi.model.SCVI.load(str(p), adata) for p in tqdm(_trained_model_paths, desc="Loading pre-trained models")]
        else:
            _trained_models = trained_models

        self.trained_models = _trained_models

        self._embeddings: TrainedContinuousVI.Embeddings | None = None

    @property
    def embeddings(self) -> TrainedContinuousVI.Embeddings:
        """Return the Embeddings object for visualizations and further downstream analyses.

        Returns
        -------
        TrainedContinuousVI.Embeddings
            An Embeddings object that provides methods such as `umap` for
            generating UMAP plots.

        Raises
        ------
        ValueError
            If embeddings have not been computed yet. Please call
            `calc_embeddings()` first.

        """
        if self._embeddings is None:
            raise ValueError(
                "No Embeddings object found. Please execute `calc_embeddings()` first.",
            )
        return self._embeddings

    def latent_coord(
        self,
        n_use_model: int = 0,
        use_clusteringbased_correction: bool = False,
    ) -> np.ndarray:
        """Return the latent coordinates from one of the trained scVI models.

        Parameters
        ----------
        n_use_model : int, default=0
            The index of the trained model in `self.trained_models` to use for
            obtaining the latent representation.

        Returns
        -------
        numpy.ndarray
            A 2D array of shape (n_cells, n_latent) containing the latent representation.

        """
        arr: np.ndarray = self.trained_models[n_use_model].get_latent_representation(
            adata=self.adata,
        )
        if use_clusteringbased_correction:
            if self.continuous_key is None:
                ho = run_continuous_harmony(
                    data_mat=arr.T,
                    meta_data=self.adata.obs,
                    vars_use=[self.batch_key],
                    remove_vars=[self.batch_key],
                )
            else:
                ho = run_continuous_harmony(
                    data_mat=arr.T,
                    meta_data=self.adata.obs,
                    vars_use=[self.batch_key, self.continuous_key],
                    remove_vars=[self.batch_key],
                )
            arr = ho.result().T
        return arr

    def calc_embeddings(
        self,
        resolution: float = 0.5,
        n_neighbors: int = 10,
        n_pcs: int = 30,
        n_use_model: int = 0,
        use_clusteringbased_correction: bool = False,
    ) -> TrainedContinuousVI:
        """Calculate embeddings and cluster labels using the latent space.

        This method:
        - Stores the latent coordinates in `adata.obsm["X_latent"]`.
        - Computes neighborhood graphs using `scanpy.pp.neighbors`.
        - Performs draw_graph, leiden clustering, paga, and UMAP embedding.
        - Creates an `Embeddings` object that can be used for plotting.

        Parameters
        ----------
        resolution : float, default=0.5
            Resolution parameter for the leiden clustering. Higher values lead to
            more granular clustering.
        n_neighbors : int, default=10
            Number of neighbors to use for building the k-NN graph.
        n_pcs : int, default=30
            Number of principal components to use for neighborhood computation (if applicable).
        n_use_model : int, default=0
            The index of the trained model to use when extracting latent coordinates.

        Returns
        -------
        TrainedContinuousVI
            The TrainedContinuousVI instance with updated embeddings in `adata.obsm`
            and a newly created `Embeddings` object (`self._embeddings`).

        """
        KEY_LATENT = "X_latent"
        KEY_CLUSTER = "clusters"
        self.adata.obsm[KEY_LATENT] = self.latent_coord(
            n_use_model,
            use_clusteringbased_correction,
        )
        sc.pp.neighbors(
            self.adata,
            n_neighbors=n_neighbors,
            n_pcs=n_pcs,
            use_rep=KEY_LATENT,
        )
        sc.tl.draw_graph(self.adata)
        sc.tl.leiden(
            self.adata,
            key_added=KEY_CLUSTER,
            resolution=resolution,
            directed=False,
        )
        sc.tl.paga(self.adata, groups=KEY_CLUSTER)
        sc.tl.umap(self.adata)
        self._embeddings = TrainedContinuousVI.Embeddings(self)
        return self

    def save(
        self,
        dir_path: Path | str,
        overwrite: bool = False,
    ) -> TrainedContinuousVI:
        """Save the trained models to the specified directory.

        Each model is saved in a subdirectory named `model_{i}` where `i`
        is the index of the model. For example, if there are 5 models in
        `self.trained_models`, subdirectories `model_0, model_1, ... model_4`
        will be created.

        Parameters
        ----------
        dir_path : Path or str
            The directory path where the models will be saved.
        overwrite : bool, default=False
            Whether to overwrite existing models at the target path if a
            model directory already exists.

        Returns
        -------
        TrainedContinuousVI
            The TrainedContinuousVI instance (self) for chained operations.

        """
        _base_path = dir_path if isinstance(dir_path, Path) else Path(dir_path)
        for n in tqdm(range(len(self.trained_models)), desc="Saving trained model."):
            _path = _base_path / Path(f"model_{n}")
            self.trained_models[n].save(_path, overwrite=overwrite)
        return self

        # def sample_px(self, transform_batch: int = 0, n_draws: int = 25, chunk_size: int | None = None, use_clusteringbased_correction: bool = False) -> torch.Tensor:
        # """Sample px (the distribution parameters for the gene expression) from trained models.

        # The px distribution is the Zero-Inflated Negative Binomial (ZINB) or
        # Negative Binomial in scVI, depending on configuration. This method samples
        # multiple times (`n_draws`) from each trained model's approximate posterior,
        # and returns the mean of those samples.

        # Parameters
        # ----------
        # transform_batch : int, default=0
        #     The batch index to condition on (i.e., as if all cells belonged to
        #     this batch).
        # n_draws : int, default=25
        #     Number of forward passes (draws) to sample px for each model. The
        #     final px mean is averaged over these samples.
        # use_clusteringbased_correction : bool, default=False
        #     Whether to apply clustering-based correction (e.g. continuous_harmony) to the
        #     latent space z before feeding into the generative model.
        # chunk_size : int or None
        #     If not None, process the data in chunks of this size (useful for very large
        #     data to avoid OOM). If None, all cells are processed at once.

        # Returns
        # -------
        # torch.Tensor
        #     A 2D tensor of shape (n_cells, n_genes) containing the average
        #     (across models and draws) of the px distribution means for each cell.

        # """
        # cont_obsm_key = "_scvi_extra_continuous_covs"
        # n_cells = self.adata.n_obs
        # x_ = torch.tensor(self.adata.X.toarray(), dtype=torch.float32) if hasattr(self.adata.X, "toarray") else torch.tensor(self.adata.X, dtype=torch.float32)
        # batch_index = torch.full((n_cells, 1), transform_batch, dtype=torch.int64)

        # if hasattr(self.adata.obsm[cont_obsm_key], "to_numpy"):
        #     cont_covs = torch.tensor(
        #         self.adata.obsm[cont_obsm_key].to_numpy(),
        #         dtype=torch.float32,
        #     )
        # else:
        #     cont_covs = torch.tensor(
        #         self.adata.obsm[cont_obsm_key],
        #         dtype=torch.float32,
        #     )

        # _px_mean_all: list[torch.Tensor] = []
        # for model in tqdm(self.trained_models):
        #     if model.module is None:
        #         raise ValueError("Model is none. Please execute the training process.")
        #     px_means_sample: list[torch.Tensor] = []
        #     for _ in tqdm(
        #         range(n_draws),
        #         leave=True,
        #         desc="sampling px distribution",
        #     ):
        #         with torch.no_grad():
        #             inf_out = model.module.inference(
        #                 x=x_,
        #                 batch_index=batch_index,
        #                 cont_covs=cont_covs,
        #                 cat_covs=None,
        #             )
        #             z_est: np.ndarray = inf_out["z"].cpu().numpy()
        #         if use_clusteringbased_correction:
        #             var_use = [self.batch_key, self.continuous_key] if self.continuous_key is not None else [self.batch_key]
        #             ho = run_continuous_harmony(
        #                 data_mat=z_est.T,
        #                 meta_data=self.adata.obs,
        #                 vars_use=var_use,
        #                 remove_vars=[self.batch_key],
        #             )
        #             z_est = ho.result().T
        #         with torch.no_grad():
        #             gen_out = model.module.generative(
        #                 z=z_est,
        #                 library=inf_out["library"],
        #                 batch_index=torch.full(
        #                     (n_cells, 1),
        #                     transform_batch,
        #                     dtype=torch.int64,
        #                 ),
        #                 cont_covs=cont_covs,
        #                 cat_covs=None,
        #             )
        #             px_data: ZeroInflatedNegativeBinomial = gen_out["px"]
        #             px_means_sample.append(px_data.mean.cpu().numpy())
        #     px_mean = torch.stack(px_means_sample, dim=-1).mean(dim=-1)
        #     _px_mean_all.append(px_mean)
        # return torch.stack(_px_mean_all, dim=-1).mean(dim=-1)

    def sample_px(
        self,
        transform_batch: int = 0,
        n_draw: int = 25,
        batch_size: int = 512,
        use_clusteringbased_correction: bool = False,
        mean: bool = True,
    ) -> torch.Tensor:
        """Sample px (distribution parameters for gene expression) from multiple trained models,
        optionally applying Harmony-based correction. The function processes cells in mini-batches
        and returns either the averaged px across draws or the entire stack of draws.

        Parameters
        ----------
        transform_batch : int, optional
            The batch index to condition on (i.e. as if all cells belonged to this batch).
        n_draw : int, optional
            Number of forward passes (draws) from each model.
            For each draw, px is sampled for each model, then averaged across models.
        batch_size : int, optional
            Mini-batch size for iterating over cells to avoid out-of-memory issues.
        use_clusteringbased_correction : bool, optional
            If True, apply clustering-based (e.g., Harmony) correction to the latent space z
            before the generative step.
        mean : bool, optional
            If True, return a 2D tensor of shape (n_cells, n_genes), obtained by averaging px
            over n_draw. If False, return a 3D tensor of shape (n_draw, n_cells, n_genes),
            storing each draw's px after averaging across models.

        Returns
        -------
        torch.Tensor
            - If mean=True, shape is (n_cells, n_genes).
            - If mean=False, shape is (n_draw, n_cells, n_genes), where the first dimension
            indexes each draw (already averaged across all models).

        """
        adata_local = self.adata
        n_cells = adata_local.n_obs
        n_genes = adata_local.n_vars
        cont_obsm_key = "_scvi_extra_continuous_covs"

        # Prepare X
        x_full = adata_local.X.toarray() if hasattr(adata_local.X, "toarray") else adata_local.X
        x_full_torch = torch.tensor(x_full, dtype=torch.float32)

        # Batch index
        batch_index_full = torch.full(
            (n_cells, 1),
            transform_batch,
            dtype=torch.int64,
        )

        # Continuous covariates
        if hasattr(adata_local.obsm[cont_obsm_key], "to_numpy"):
            cont_covs_full = torch.tensor(
                adata_local.obsm[cont_obsm_key].to_numpy(),
                dtype=torch.float32,
            )
        else:
            cont_covs_full = torch.tensor(
                adata_local.obsm[cont_obsm_key],
                dtype=torch.float32,
            )

        # Output buffer: (n_draw, n_cells, n_genes)
        px_samples = torch.zeros((n_draw, n_cells, n_genes), dtype=torch.float32)
        all_indices = np.arange(n_cells)

        for draw_i in range(n_draw):
            # Accumulator for average across models
            px_accum_for_draw = torch.zeros((n_cells, n_genes), dtype=torch.float32)
            n_models = len(self.trained_models)

            for model in self.trained_models:
                if model.module is None:
                    raise ValueError(
                        "One of the trained models has `module=None`. Ensure all are trained.",
                    )

                for start_idx in range(0, n_cells, batch_size):
                    end_idx = min(start_idx + batch_size, n_cells)
                    idx_batch = all_indices[start_idx:end_idx]

                    x_batch_torch = x_full_torch[idx_batch]
                    batch_idx_torch = batch_index_full[idx_batch]
                    cont_covs_batch_torch = cont_covs_full[idx_batch]

                    with torch.no_grad():
                        inf_out = model.module.inference(
                            x=x_batch_torch,
                            batch_index=batch_idx_torch,
                            cont_covs=cont_covs_batch_torch,
                            cat_covs=None,
                        )

                    z_est = inf_out["z"]
                    # Harmony-based correction (if needed)
                    if use_clusteringbased_correction:
                        # ユーザ定義関数 run_continuous_harmony を想定
                        # self.batch_key, self.continuous_key 等も設定済みと仮定
                        z_np: np.ndarray = z_est.cpu().numpy()
                        meta_data = adata_local.obs.iloc[idx_batch]
                        z_np_corrected = (
                            run_continuous_harmony(
                                data_mat=z_np.T,
                                meta_data=meta_data,
                                vars_use=[self.batch_key, self.continuous_key] if self.continuous_key else [self.batch_key],
                                remove_vars=[self.batch_key],
                            )
                            .result()
                            .T
                        )
                        z_est = torch.tensor(z_np_corrected, dtype=torch.float32)

                    with torch.no_grad():
                        gen_out = model.module.generative(
                            z=z_est,
                            library=inf_out["library"],
                            batch_index=batch_idx_torch,
                            cont_covs=cont_covs_batch_torch,
                            cat_covs=None,
                        )
                    px_data: ZeroInflatedNegativeBinomial = gen_out["px"]  # distribution
                    px_mean_batch = px_data.mean  # (batch_size, n_genes)

                    px_accum_for_draw[idx_batch] += px_mean_batch

            # Average across models
            px_accum_for_draw /= n_models
            # Save this draw
            px_samples[draw_i] = px_accum_for_draw

        if mean:
            # Return average over draws => shape=(n_cells, n_genes)
            return px_samples.mean(dim=0)
        # Return all draws => shape=(n_draw, n_cells, n_genes)
        return px_samples

    def plot_gene_expression(
        self,
        target_genes: list[str],
        transform_batch: str | None,
        mode: Literal["normalized", "px"] = "px",
        stabilize_log1p: bool = False,
        n_draws: int = 25,
        chunk_size: int = 512,
        use_clusteringbased_correction: bool = False,
    ) -> None:
        """Plot gene expression for the specified target_genes.

        Depending on the `mode`, we either:
        - (mode="normalized") use `get_normalized_expression`
        - (mode="px")         use `sample_px` (or sample_px_new) to obtain px-based expression

        Parameters
        ----------
        target_genes : list of str
            Genes to be plotted.
        mode : {"normalized", "px"}, default="normalized"
            If "normalized", uses get_normalized_expression from the model.
            If "px", uses sample_px (or sample_px_new) to obtain the distribution parameters for each gene.
        transform_batch : int or None, default=None
            Batch index used for expression generation.
        stabilize_log1p : bool, default=False
            If True, apply log1p transform to the gene expression before plotting.
        n_draws : int, default=25
            Number of draws for sampling px (if mode="px").
        chunk_size : int or None, default=None
            Chunk size for sample_px (if mode="px"), can help manage memory in large datasets.
        use_clusteringbased_correction : bool, default=False
            Whether to apply harmony-based correction for px (if mode="px").

        Returns
        -------
        None
            Displays a series of scatter plots with linear regression fits for each gene.

        """
        adata_local = self.adata

        # 連続変数
        x = adata_local.obs[self.continuous_key].to_numpy().reshape(-1, 1)

        # ---------------------------------------------------------------------
        # 1) Gene expression 取得
        # ---------------------------------------------------------------------
        if mode == "normalized":
            if transform_batch is None:
                # 最初のバッチを使用する
                transform_batch = adata_local.obs[self.batch_key].unique().tolist()[0]
            # get_normalized_expression を用いる
            # 複数モデルがある場合は平均
            expressions = []
            for model in tqdm(
                self.trained_models,
                desc="Collecting normalized expressions",
            ):
                expr = model.get_normalized_expression(
                    adata_local,
                    transform_batch=transform_batch,
                    n_samples=n_draws,
                    gene_list=target_genes,
                )
                # shape=(n_cells, len(target_genes)) 程度を想定
                expressions.append(expr)
            expression = np.mean(np.stack(expressions), axis=0)
            # => shape=(n_cells, len(target_genes))

        elif mode == "px":
            if transform_batch is None:
                # 最初のバッチを使用する
                use_transform_batch = 0
            else:
                use_transform_batch = list(
                    self.adata.obs[self.batch_key].cat.categories.unique(),
                ).index(transform_batch)
            # sample_px (or sample_px_new) を用いる
            # ここでは sample_px の例を示す (実装済みなら sample_px_new でも良い)
            # 複数モデルは内部で平均される実装の場合 => 直接呼び出し
            # もし内部で複数モデル平均をしないならここで平均してもよい
            px_2d = self.sample_px(
                transform_batch=use_transform_batch,
                n_draw=n_draws,
                batch_size=chunk_size,
                use_clusteringbased_correction=use_clusteringbased_correction,
            )
            # px_2d: shape=(n_cells, n_genes)
            # ここから target_genes の列を切り出す
            gene_indices = [np.where(adata_local.var_names == g)[0][0] for g in target_genes]
            expression = px_2d[:, gene_indices].cpu().numpy() if hasattr(px_2d, "cpu") else px_2d[:, gene_indices]
            # => shape=(n_cells, len(target_genes))

        else:
            raise ValueError("mode must be either 'normalized' or 'px'.")

        # オプションで log1p
        if stabilize_log1p:
            expression = np.log1p(expression)

        # ---------------------------------------------------------------------
        # 2) プロット
        # ---------------------------------------------------------------------
        n_genes = len(target_genes)
        ncols = 3
        nrows = math.ceil(n_genes / ncols)
        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(5 * ncols, 4 * nrows),
        )
        axes = np.ravel(axes)  # サブプロットを1次元にフラット化

        for i, gene in enumerate(target_genes):
            y = expression[:, i]

            # 線形回帰してみる (例)
            model_lin = LinearRegression()
            model_lin.fit(x, y)
            y_pred = model_lin.predict(x)

            ax = axes[i]
            ax.scatter(x, y, alpha=0.7, label="Gene Expression")
            ax.plot(x, y_pred, label="Regression Line", color="red")

            ax.set_xlabel(self.continuous_key)
            ax.set_ylabel("Gene Expression")
            ax.set_title(f"{gene} ({mode})")
            ax.legend()

        # 余ったサブプロットを非表示
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        plt.tight_layout()
        plt.show()

    def regression(
        self,
        transform_batch: int = 0,
        stabilize_log1p: bool = True,
        mode: Literal["ols", "poly2", "spline"] = "ols",
        n_samples: int = 25,
        batch_size: int = 512,
        spline_df: int = 5,
        spline_degree: int = 3,
        use_mcmc: bool = True,
        # use_clusteringbased_correction: bool = False,
    ) -> pd.DataFrame:
        """Perform gene-wise regression of scVI-imputed expression values (px) against a continuous covariate,
        optionally using a hierarchical Bayesian model (if `use_mcmc=True`), otherwise using
        frequentist regression (OLS, poly2, or spline) with multiple px draws.

        Parameters
        ----------
        transform_batch : int, optional
            Batch index to which all cells are 'transformed' when generating px.
        stabilize_log1p : bool, optional
            If True, applies log1p to the px values before regression.
        mode : {"ols", "poly2", "spline"}, optional
            Regression model to use.
        n_samples : int, optional
            - If `use_mcmc=False`, number of draws for frequentist regressions.
            - If `use_mcmc=True`, number of posterior samples (per chain) in MCMC.
        batch_size : int, optional
            Mini-batch size for sampling latent variables, useful for large datasets.
        spline_df : int, optional
            Degrees of freedom for spline basis if mode="spline".
        spline_degree : int, optional
            Polynomial degree for the spline if mode="spline".
        use_mcmc : bool, optional
            If True, performs hierarchical Bayesian regression with MCMC (Pyro).

        Returns
        -------
        pd.DataFrame
            DataFrame of regression results. The content depends on whether MCMC is used or not.

        """
        # -----------------------------------------------------------------------
        # (A) Basic checks / data prep
        # -----------------------------------------------------------------------
        if self.continuous_key is None:
            raise ValueError("continuous_key must not be None for regression.")
        if mode not in {"ols", "poly2", "spline"}:
            raise ValueError("Unsupported mode. Use 'ols', 'poly2', or 'spline'.")

        adata_local = self.adata.copy()
        continuous_values = adata_local.obs[self.continuous_key].astype(float).to_numpy()
        n_cells = adata_local.n_obs
        n_genes = adata_local.n_vars
        gene_names = adata_local.var_names.to_numpy()

        # -----------------------------------------------------------------------
        # (B) Sample px using sample_px_new (mean=False => keep all draws)
        # -----------------------------------------------------------------------
        px_samples_torch = self.sample_px(
            transform_batch=transform_batch,
            n_draw=n_samples,
            batch_size=batch_size,
            use_clusteringbased_correction=False,
            mean=False,  # get shape=(n_samples, n_cells, n_genes)
        )
        px_samples = px_samples_torch.cpu().numpy()  # convert to numpy
        # shape: (n_samples, n_cells, n_genes)

        # Optional log transform
        if stabilize_log1p:
            px_samples = np.log1p(px_samples)

        # -----------------------------------------------------------------------
        # (C) Design matrix
        # -----------------------------------------------------------------------
        if mode == "ols":
            X_design = sm.add_constant(continuous_values)
            design_cols = ["Intercept", "Slope"]
        elif mode == "poly2":
            X_design = np.column_stack([
                continuous_values**2,
                continuous_values,
                np.ones_like(continuous_values),
            ])
            design_cols = ["Coef_x2", "Coef_x1", "Intercept"]
        else:  # spline
            spline_frame = patsy.dmatrix(
                f"bs(x, df={spline_df}, degree={spline_degree}, include_intercept=True)",
                {"x": continuous_values},
                return_type="dataframe",
            )
            X_design = spline_frame.to_numpy()
            design_cols = list(spline_frame.columns)

        # Helper: compute summary stats
        def compute_stats(array_2d: np.ndarray) -> dict:
            """Computes mean, std, 2.5%, 97.5%, prob_positive along axis=0.
            array_2d shape = (n_samples, n_genes).
            """
            mean_ = array_2d.mean(axis=0)
            std_ = array_2d.std(axis=0)
            pct2_5 = np.percentile(array_2d, 2.5, axis=0)
            pct97_5 = np.percentile(array_2d, 97.5, axis=0)
            prob_pos = (array_2d > 0).mean(axis=0)
            return {
                "mean": mean_,
                "std": std_,
                "2.5pct": pct2_5,
                "97.5pct": pct97_5,
                "prob_positive": prob_pos,
            }

        # -----------------------------------------------------------------------
        # (D) If not use_mcmc => frequentist approach (OLS / poly2 / spline)
        # -----------------------------------------------------------------------
        if not use_mcmc:
            # n_samples draws => for each draw, fit OLS (or poly2/spline) on each gene
            n_params = X_design.shape[1]
            param_values = np.zeros((n_samples, n_genes, n_params), dtype=np.float32)
            r2_values = np.zeros((n_samples, n_genes), dtype=np.float32)

            def _fit_one_gene(task):
                s_idx, g_idx, y_ = task
                reg_res = sm.OLS(y_, X_design).fit()
                return s_idx, g_idx, reg_res.params, reg_res.rsquared

            tasks = []
            for s_idx in range(n_samples):
                current_px = px_samples[s_idx]  # shape=(n_cells, n_genes)
                for g_idx in range(n_genes):
                    y_vals = current_px[:, g_idx]
                    tasks.append((s_idx, g_idx, y_vals))

            # 並列実行(必要に応じて max_workers=... 変更)
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(_fit_one_gene, t) for t in tasks]
                for fut in tqdm(
                    as_completed(futures),
                    total=len(futures),
                    desc="Fitting regressions",
                    leave=True,
                ):
                    s_idx, g_idx, params, r2_val = fut.result()
                    param_values[s_idx, g_idx, :] = params
                    r2_values[s_idx, g_idx] = r2_val

            # 統計量まとめ
            parameters_summary = {}
            for param_idx, col_name in enumerate(design_cols):
                param_array = param_values[
                    :,
                    :,
                    param_idx,
                ]  # shape=(n_samples, n_genes)
                parameters_summary[col_name] = compute_stats(param_array)

            r2_summary = compute_stats(r2_values)

            # 出力整形
            output_dict = {"gene": gene_names}
            for col_name, stats_dict in parameters_summary.items():
                output_dict[f"{col_name}_mean"] = stats_dict["mean"]
                output_dict[f"{col_name}_std"] = stats_dict["std"]
                output_dict[f"{col_name}_2.5pct"] = stats_dict["2.5pct"]
                output_dict[f"{col_name}_97.5pct"] = stats_dict["97.5pct"]
                output_dict[f"{col_name}_prob_positive"] = stats_dict["prob_positive"]

            output_dict["r2_mean"] = r2_summary["mean"]
            output_dict["r2_std"] = r2_summary["std"]
            output_dict["r2_2.5pct"] = r2_summary["2.5pct"]
            output_dict["r2_97.5pct"] = r2_summary["97.5pct"]
            output_dict["r2_prob_positive"] = r2_summary["prob_positive"]

            regression_output = pd.DataFrame(output_dict)

            # 例: OLS/Poly2 の場合は係数でソート
            if mode == "ols" and "Slope_mean" in regression_output.columns:
                regression_output = regression_output.sort_values(
                    "Slope_mean",
                    ascending=False,
                )
            elif mode == "poly2" and "Coef_x1_mean" in regression_output.columns:
                regression_output = regression_output.sort_values(
                    "Coef_x1_mean",
                    ascending=False,
                )

            return regression_output.reset_index(drop=True)

        # -----------------------------------------------------------------------
        # (E) use_mcmc=True => Pyro による階層ベイズ回帰
        # -----------------------------------------------------------------------
        # ここでは 1 サンプル目 (px_samples[0]) などを使う例を示す
        # 本当に scVI の不確実性 (n_draw) まで反映させたい場合は、さらにモデルを拡張するなど検討が必要
        # -----------------------------------------------------------------------
        Y_data = px_samples[0]  # shape=(n_cells, n_genes)

        # 階層ベイズモデル (chunk 単位で遺伝子を分割)
        def hierarchical_model_chunk(x_torch: torch.Tensor, y_torch: torch.Tensor):
            """Hierarchical Bayesian linear model for a chunk of genes.

            param[g, d] ~ Normal(param_mean[d], param_sd[d])
            sigma[g]    ~ Exponential(1)
            y_{cell,g}  ~ Normal( (x_{cell} @ param[g]), sigma[g] )
            """
            n_cells_chunk, n_genes_chunk = y_torch.shape
            n_params_local = x_torch.shape[1]

            # Hyper-priors
            param_mean = pyro.sample(
                "param_mean",
                dist.Normal(
                    torch.zeros(n_params_local),
                    5.0 * torch.ones(n_params_local),
                ).to_event(1),
            )
            param_sd = pyro.sample(
                "param_sd",
                dist.Exponential(torch.ones(n_params_local)).to_event(1),
            )

            # gene-wise parameters
            param = pyro.sample(
                "param",
                dist.Normal(param_mean.unsqueeze(0), param_sd.unsqueeze(0)).expand([n_genes_chunk, n_params_local]).to_event(2),
            )
            sigma = pyro.sample(
                "sigma",
                dist.Exponential(1.0).expand([n_genes_chunk]).to_event(1),
            )

            param_t = param.transpose(0, 1)  # => shape=(n_params_local, n_genes_chunk)
            mu = x_torch @ param_t  # => (n_cells_chunk, n_genes_chunk)

            with pyro.plate("data", n_cells_chunk, dim=-2):
                pyro.sample("obs", dist.Normal(mu, sigma), obs=y_torch)

        # geneごとにチャンク分割
        n_threads = 1  # 並列数 (要調整)
        chunk_size = max(1, n_genes // n_threads) if n_threads > 0 else n_genes
        chunk_starts = range(0, n_genes, chunk_size)
        chunk_intervals = [(start, min(start + chunk_size, n_genes)) for start in chunk_starts]

        warmup_steps = 200  # MCMCウォームアップ (要調整)

        def run_mcmc_for_chunk(g_start: int, g_end: int) -> pd.DataFrame:
            g_slice = slice(g_start, g_end)
            Y_chunk = Y_data[:, g_slice]  # (n_cells, chunk_size)
            x_torch_chunk = torch.tensor(X_design, dtype=torch.float32)
            y_torch_chunk = torch.tensor(Y_chunk, dtype=torch.float32)

            nuts_kernel = NUTS(hierarchical_model_chunk)
            mcmc = MCMC(
                nuts_kernel,
                num_samples=n_samples,
                warmup_steps=warmup_steps,
                num_chains=1,  # for simplicity
            )
            mcmc.run(x_torch_chunk, y_torch_chunk)
            posterior = mcmc.get_samples()  # dict with ["param_mean", "param_sd", "param", "sigma"]

            # (n_samples, chunk_size, n_params)
            param_array = posterior["param"].cpu().numpy()
            sigma_array = posterior["sigma"].cpu().numpy()  # (n_samples, chunk_size)
            # R^2 用
            r2_array = np.zeros((n_samples, Y_chunk.shape[1]), dtype=np.float32)

            # R^2計算
            for s_idx in range(n_samples):
                param_s = param_array[s_idx]  # shape=(chunk_size, n_params)
                # 予測
                predicted_s = X_design @ param_s.T  # => (n_cells, chunk_size)
                for g_local in range(Y_chunk.shape[1]):
                    y_true = Y_chunk[:, g_local]
                    y_hat = predicted_s[:, g_local]
                    sse = np.sum((y_true - y_hat) ** 2)
                    sst = np.sum((y_true - y_true.mean()) ** 2)
                    r2_value = 1.0 - (sse / (sst + 1e-12))
                    r2_array[s_idx, g_local] = r2_value

            chunk_gene_names = gene_names[g_slice]
            records = []
            for g_local, gene_name in enumerate(chunk_gene_names):
                row = {"gene": gene_name}
                # param_array[:, g_local, :] => (n_samples, n_params)
                for d_idx, col_name in enumerate(design_cols):
                    samples_d = param_array[:, g_local, d_idx]
                    row[f"{col_name}_mean"] = samples_d.mean()
                    row[f"{col_name}_std"] = samples_d.std()
                    row[f"{col_name}_2.5pct"] = np.percentile(samples_d, 2.5)
                    row[f"{col_name}_97.5pct"] = np.percentile(samples_d, 97.5)
                    row[f"{col_name}_prob_positive"] = (samples_d > 0).mean()

                sigma_samples = sigma_array[:, g_local]
                row["sigma_mean"] = sigma_samples.mean()
                row["sigma_std"] = sigma_samples.std()
                row["sigma_2.5pct"] = np.percentile(sigma_samples, 2.5)
                row["sigma_97.5pct"] = np.percentile(sigma_samples, 97.5)
                row["sigma_prob_positive"] = (sigma_samples > 0).mean()

                # R^2
                r2_gene = r2_array[:, g_local]
                row["r2_mean"] = r2_gene.mean()
                row["r2_std"] = r2_gene.std()
                row["r2_2.5pct"] = np.percentile(r2_gene, 2.5)
                row["r2_97.5pct"] = np.percentile(r2_gene, 97.5)
                row["r2_prob_positive"] = (r2_gene > 0).mean()

                records.append(row)
            return pd.DataFrame(records)

        # 並列でチャンク処理
        results_list = []
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = []
            for start_i, end_i in chunk_intervals:
                fut = executor.submit(run_mcmc_for_chunk, start_i, end_i)
                futures.append(fut)

            for fut in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="MCMC chunks",
                leave=True,
            ):
                df_part = fut.result()
                results_list.append(df_part)

        df_out = pd.concat(results_list, axis=0).reset_index(drop=True)

        # ソート(ols相当でSlopeがあれば / poly2でCoef_x1があれば)
        if mode == "ols":
            if len(design_cols) > 1 and f"{design_cols[1]}_mean" in df_out.columns:
                df_out = df_out.sort_values(f"{design_cols[1]}_mean", ascending=False)
        elif mode == "poly2" and "Coef_x1_mean" in df_out.columns:
            df_out = df_out.sort_values("Coef_x1_mean", ascending=False)

        return df_out.reset_index(drop=True)

    class Embeddings:
        """Embeddings class for handling dimensional reductions and plotting.

        An instance of this class is created after calling `calc_embeddings()`
        on the parent `TrainedContinuousVI` object. Provides convenience methods
        for plotting UMAP or other embeddings with gene or metadata coloring.
        """

        def __init__(self, trained_vi: TrainedContinuousVI) -> None:
            """Construct an Embeddings object.

            Parameters
            ----------
            trained_vi : TrainedContinuousVI
                The parent TrainedContinuousVI instance containing the AnnData
                and trained models.

            """
            self.trained_vi = trained_vi

        def umap(
            self,
            color_by: list[str] | None = None,
            n_draw: int = 25,
            transform_batch: int | str | None = None,
            n_use_model: int = 0,
        ) -> TrainedContinuousVI.Embeddings:
            """Plot a UMAP embedding colored by genes or metadata.

            If `color_by` contains gene names that exist in `adata.var_names`,
            expression levels are sampled from the scVI models. If `color_by`
            contains column names that exist in `adata.obs`, those columns are used
            for coloring. The resulting AnnData (with X_umap, X_latent, etc.)
            is then plotted via `scanpy.pl.umap`.

            Parameters
            ----------
            color_by : list of str, optional
                A list of gene names (in `adata.var_names`) or column names (in `adata.obs`)
                by which to color the UMAP plot.
            n_draw : int, default=25
                Number of forward passes (draws) to estimate gene expression with scVI
                for coloring genes. Ignored for categorical obs coloring.
            transform_batch : int, str, or None, default=None
                The batch to condition on when estimating normalized gene expression.
                If None, no specific batch transformation is applied.
            n_use_model : int, default=0
                The index of the trained model to use when obtaining latent coordinates
                (if needed).

            Returns
            -------
            TrainedContinuousVI.Embeddings
                The Embeddings instance (self) for potential chaining.

            """
            unique_color_by: list[str] | None = list(dict.fromkeys(color_by)) if color_by is not None else None
            _target_vars: list[str] = []
            _target_obs: list[str] = []

            if unique_color_by is not None:
                for c in unique_color_by:
                    if c in self.trained_vi.adata.var_names:
                        _target_vars.append(c)
                    elif c in self.trained_vi.adata.obs.columns:
                        _target_obs.append(c)

                expression: np.ndarray | None = None
                if len(_target_vars) > 0:
                    expression = np.mean(
                        [
                            model.get_normalized_expression(
                                self.trained_vi.adata,
                                gene_list=_target_vars,
                                n_samples=n_draw,
                                transform_batch=transform_batch,
                            )
                            for model in tqdm(
                                self.trained_vi.trained_models,
                                desc="Sampling expression",
                                leave=True,
                            )
                        ],
                        axis=0,
                    )

                obs_df: pd.DataFrame = self.trained_vi.adata.obs[_target_obs] if len(_target_obs) > 0 else pd.DataFrame(index=self.trained_vi.adata.obs.index)
                vars_df: pd.DataFrame | None = None
                if len(_target_vars) > 0:
                    vars_df = self.trained_vi.adata.var[self.trained_vi.adata.var.index.isin(_target_vars)]

                _adata = sc.AnnData(
                    X=expression,
                    obs=obs_df,
                    var=vars_df,
                    obsm={
                        "X_latent": self.trained_vi.latent_coord(n_use_model),
                        "X_umap": self.trained_vi.adata.obsm["X_umap"],
                    },
                )
            if color_by is not None:
                sc.pl.umap(_adata, color=color_by)
            else:
                sc.pl.umap(_adata)

            return self
