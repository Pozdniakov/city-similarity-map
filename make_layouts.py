"""Compute the three 2-D layouts for the semantic chart — MDS (from the existing
pipeline), UMAP and t-SNE (both on cosine distance over the same vectors) — each
rigidly aligned to geography, with per-layout label positions (adjustText) and
honest quality metrics.

Outputs: output/layouts.json
"""

import json
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text
from scipy.linalg import orthogonal_procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
from sklearn.manifold import TSNE

from cities import CITY_LATLON

RS = 42


def great_circle(names):
    """Pairwise great-circle distances (radians) between the cities."""
    lat = np.radians([CITY_LATLON[c][0] for c in names])
    lon = np.radians([CITY_LATLON[c][1] for c in names])
    dlat = lat[:, None] - lat[None, :]
    dlon = lon[:, None] - lon[None, :]
    a = (np.sin(dlat / 2) ** 2
         + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2)
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def knn_recall(S, X, k=10):
    n = len(S)
    d2 = squareform(pdist(X))
    hits = 0
    for i in range(n):
        true = set(np.argsort(-S[i])[1:k+1])
        emb = set(np.argsort(d2[i])[1:k+1])
        hits += len(true & emb)
    return hits / (n * k)


def align_to_geo(X, geo):
    """Center, scale to unit RMS, then rotate/reflect onto standardized geo."""
    Xc = X - X.mean(axis=0)
    Xc /= np.sqrt((Xc ** 2).sum(axis=1).mean())
    G = (geo - geo.mean(axis=0)) / geo.std(axis=0)
    R, _ = orthogonal_procrustes(Xc, G)
    return Xc @ R


def label_positions(X, names):
    """Run adjustText on an invisible figure to get non-overlapping label spots."""
    xr = X[:, 0].max() - X[:, 0].min()
    yr = X[:, 1].max() - X[:, 1].min()
    fig, ax = plt.subplots(figsize=(16, max(6.0, 16 * yr / xr)), dpi=100)
    ax.scatter(X[:, 0], X[:, 1], s=70)
    texts = [ax.text(x, y, n, fontsize=7.5) for (x, y), n in zip(X, names)]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # keep labels close to their points: modest repulsion, and pull each
        # label back toward its own marker so none drifts far (leader lines in
        # the page connect the few that still separate)
        adjust_text(texts, ax=ax, expand=(1.04, 1.10),
                    force_text=(0.2, 0.35), force_pull=(0.4, 0.4))
    pos = np.array([t.get_position() for t in texts])
    plt.close(fig)
    return pos


def main():
    idx = pd.read_csv("data/city_index.csv")
    names = idx["city"].tolist()
    V = np.load("data/city_vectors.npy").astype(np.float64)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    S = np.clip(V @ V.T, -1.0, 1.0)
    geo = np.array([[CITY_LATLON[c][1], CITY_LATLON[c][0]] for c in names])

    D = 1.0 - S
    np.fill_diagonal(D, 0.0)
    iu = np.triu_indices(len(S), k=1)
    gc = great_circle(names)[iu]  # true geographic distances

    layouts = {}

    # MDS: reuse the pipeline's coordinates (already geo-aligned, stress 0.347)
    mds_xy = pd.read_csv("data/mds_coordinates.csv")[["x", "y"]].to_numpy()
    layouts["mds"] = mds_xy

    # PCA: the classical linear baseline — project onto the two directions of
    # maximum variance; cannot capture nonlinear structure
    from sklearn.decomposition import PCA
    layouts["pca"] = align_to_geo(
        PCA(n_components=2, random_state=RS).fit_transform(V), geo)

    import umap
    um = umap.UMAP(n_components=2, metric="cosine", n_neighbors=15,
                   min_dist=0.3, random_state=RS)
    layouts["umap"] = align_to_geo(um.fit_transform(V), geo)

    ts = TSNE(n_components=2, metric="cosine", perplexity=20, init="pca",
              learning_rate="auto", random_state=RS)
    layouts["tsne"] = align_to_geo(ts.fit_transform(V), geo)

    out = {}
    for key, X in layouts.items():
        d_emb = squareform(pdist(X))
        m = {
            "recall10": round(knn_recall(S, X, 10), 3),
            # alignment-free: how well on-screen distances track great-circle
            # distances (Procrustes rotation/scale leaves pairwise distances
            # unchanged, so this measures recovered geography, not the fit)
            "geofid": round(float(spearmanr(d_emb[iu], gc).statistic), 2),
            "ew": round(float(np.corrcoef(X[:, 0], geo[:, 0])[0, 1]), 2),
            "ns": round(float(np.corrcoef(X[:, 1], geo[:, 1])[0, 1]), 2),
        }
        if key == "mds":
            m["stress1"] = round(float(np.sqrt(((d_emb - D) ** 2).sum()
                                               / (d_emb ** 2).sum())), 3)
        lpos = label_positions(X, names)
        out[key] = {
            "xy": [[round(float(x), 4), round(float(y), 4)] for x, y in X],
            "lxy": [[round(float(x), 4), round(float(y), 4)] for x, y in lpos],
            "metrics": m,
        }
        print(f"{key:>5}: {m}")

    with open("output/layouts.json", "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("Saved output/layouts.json")


if __name__ == "__main__":
    main()
