"""Seed-variability of geo-fidelity for each 2-D layout.

Geo-fidelity = Spearman(pairwise 2-D distances, great-circle distances). It is
alignment-free (rotation/scale preserve pairwise distances), so no Procrustes
step is needed here — we only need each layout's pairwise distances.

For t-SNE and UMAP we refit under N random seeds at the *shown* hyperparameters
and report the spread. PCA is deterministic; classical-init MDS (SMACOF) is
effectively deterministic, but we still sweep its random_state to confirm.

Outputs: output/intervals.json  and prints a table.
"""

import json

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.manifold import MDS, TSNE

from cities import CITY_LATLON

N_SEEDS = 12


def great_circle(names):
    lat = np.radians([CITY_LATLON[c][0] for c in names])
    lon = np.radians([CITY_LATLON[c][1] for c in names])
    dlat = lat[:, None] - lat[None, :]
    dlon = lon[:, None] - lon[None, :]
    a = (np.sin(dlat / 2) ** 2
         + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2)
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def geofid(X, gc_iu, iu):
    d = squareform(pdist(X))
    return float(spearmanr(d[iu], gc_iu).statistic)


def stats(vals):
    v = np.array(vals)
    return {
        "min": round(float(v.min()), 3),
        "max": round(float(v.max()), 3),
        "mean": round(float(v.mean()), 3),
        "sd": round(float(v.std(ddof=1)), 3),
        "seed42": round(float(vals[0]), 3),  # first seed is 42 (the shown run)
    }


def main():
    idx = pd.read_csv("data/city_index.csv")
    names = idx["city"].tolist()
    V = np.load("data/city_vectors.npy").astype(np.float64)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    iu = np.triu_indices(len(names), k=1)
    gc = great_circle(names)[iu]

    seeds = [42] + list(range(0, N_SEEDS - 1))

    # raw 300-d cosine distance vs great-circle (the baseline)
    S = np.clip(V @ V.T, -1.0, 1.0)
    D = 1.0 - S
    raw = float(spearmanr(D[iu], gc).statistic)

    # PCA — deterministic (sign flips don't change distances)
    pca = geofid(PCA(n_components=2, random_state=0).fit_transform(V), gc, iu)

    tsne_vals, umap_vals, mds_vals = [], [], []
    import umap
    for s in seeds:
        ts = TSNE(n_components=2, metric="cosine", perplexity=20, init="pca",
                  learning_rate="auto", random_state=s).fit_transform(V)
        tsne_vals.append(geofid(ts, gc, iu))
        um = umap.UMAP(n_components=2, metric="cosine", n_neighbors=15,
                       min_dist=0.3, random_state=s).fit_transform(V)
        umap_vals.append(geofid(um, gc, iu))
        md = MDS(n_components=2, dissimilarity="precomputed", random_state=s,
                 n_init=1, normalized_stress=False).fit_transform(D)
        mds_vals.append(geofid(md, gc, iu))
        print(f"seed {s:>2}: tsne {tsne_vals[-1]:.3f}  umap {umap_vals[-1]:.3f}  "
              f"mds {mds_vals[-1]:.3f}")

    out = {
        "n_seeds": len(seeds),
        "raw": round(raw, 3),
        "pca": round(pca, 3),
        "tsne": stats(tsne_vals),
        "umap": stats(umap_vals),
        "mds": stats(mds_vals),
    }
    with open("output/intervals.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
