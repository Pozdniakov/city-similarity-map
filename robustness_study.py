"""Robustness / decomposition study for the geo-fidelity result, prompted by
panel review (EDITORIAL_REVIEW.md, items R1, R4, S1).

Analyses (all read-only over shipped artifacts; no embedding model needed):
  1. Between/within decomposition of geo-fidelity: share of between-region
     pairs; within-region-only geo-fidelity per layout and for the raw space.
  2. Region-collapse counterfactual: move every city to its region's centroid
     in layout space (9 points) and recompute geo-fidelity. If the score RISES,
     the global metric is dominated by coarse regional structure.
  3. Geographic neighbour recall@10: of each city's 10 nearest cities on Earth,
     how many are in its 10 nearest by layout distance (and by raw cosine).
  4. City-level bootstrap (n=1000): resample the 124 cities with replacement,
     recompute geo-fidelity per layout; report 95% percentile CIs for adjacent
     differences (PCA-MDS, tSNE-PCA, UMAP-tSNE) and for layout-vs-raw.
  5. Rotation scan (backs the "r ~= .21" figure): best single rotation of the
     MDS layout maximizing corr(y, latitude); same for t-SNE for contrast.

Outputs: output/robustness.json + printed summary.
"""

import json

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr

from cities import CITY_LATLON

RNG = np.random.default_rng(42)


def great_circle(names):
    lat = np.radians([CITY_LATLON[c][0] for c in names])
    lon = np.radians([CITY_LATLON[c][1] for c in names])
    dlat = lat[:, None] - lat[None, :]
    dlon = lon[:, None] - lon[None, :]
    a = (np.sin(dlat / 2) ** 2
         + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2)
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def geofid_from_dist(demb, gc, iu, mask=None):
    a, b = demb[iu], gc[iu]
    if mask is not None:
        a, b = a[mask], b[mask]
    return float(spearmanr(a, b).statistic)


def neighbour_recall(demb, gc, k=10):
    n = demb.shape[0]
    hits = 0
    for i in range(n):
        true = set(np.argsort(gc[i])[1:k + 1])
        emb = set(np.argsort(demb[i])[1:k + 1])
        hits += len(true & emb)
    return hits / (n * k)


def main():
    idx = pd.read_csv("data/city_index.csv")
    names = idx["city"].tolist()
    regions = np.array(idx["region"].tolist())
    n = len(names)
    lay = json.load(open("output/layouts.json"))
    V = np.load("data/city_vectors.npy").astype(np.float64)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    D_raw = 1.0 - np.clip(V @ V.T, -1, 1)
    np.fill_diagonal(D_raw, 0.0)

    gc = great_circle(names)
    iu = np.triu_indices(n, k=1)
    within = regions[iu[0]] == regions[iu[1]]
    out = {"n_pairs": int(len(iu[0])),
           "within_share": round(float(within.mean()), 3),
           "between_share": round(float((~within).mean()), 3)}
    print(f"pairs: {out['n_pairs']}  between-region share: {out['between_share']}")

    keys = ["mds", "pca", "tsne", "umap"]
    X = {k: np.array(lay[k]["xy"]) for k in keys}
    demb = {k: squareform(pdist(X[k])) for k in keys}
    demb["raw"] = D_raw

    # 1) full vs within-region-only geo-fidelity
    out["geofid_full"], out["geofid_within"] = {}, {}
    for k in keys + ["raw"]:
        out["geofid_full"][k] = round(geofid_from_dist(demb[k], gc, iu), 3)
        out["geofid_within"][k] = round(geofid_from_dist(demb[k], gc, iu, within), 3)
    print("full   :", out["geofid_full"])
    print("within :", out["geofid_within"])

    # 2) region-collapse counterfactual
    out["geofid_region_collapsed"] = {}
    for k in keys:
        Xc = X[k].copy()
        for r in set(regions):
            m = regions == r
            Xc[m] = X[k][m].mean(axis=0)
        out["geofid_region_collapsed"][k] = round(
            geofid_from_dist(squareform(pdist(Xc)), gc, iu), 3)
    print("region-collapsed:", out["geofid_region_collapsed"])

    # 2b) collapse CONTROLS — is the region-collapse lift an artefact of the
    #     hand-drawn region labels? Three checks:
    #     (i)  label-free: cut the page's own average-linkage dendrogram
    #          (built from 1-cos alone, no geography, no labels) into 9
    #          clusters and collapse by those;
    #     (ii) geometric: k-means (k=9) on true coordinates (unit sphere);
    #     (iii) placebo: collapse by RANDOM partitions with the same group
    #          sizes — if collapsing per se inflated the score, it would
    #          inflate here too.
    from scipy.cluster.hierarchy import fcluster, linkage
    from sklearn.cluster import KMeans

    def collapse_by(labels, Xk):
        Xc = Xk.copy()
        for r in set(labels):
            m = labels == r
            Xc[m] = Xk[m].mean(axis=0)
        return geofid_from_dist(squareform(pdist(Xc)), gc, iu)

    Z = linkage(squareform((D_raw + D_raw.T) / 2.0, checks=False),
                method="average")
    dendro9 = fcluster(Z, 9, criterion="maxclust")
    lat_r = np.radians([CITY_LATLON[c][0] for c in names])
    lon_r = np.radians([CITY_LATLON[c][1] for c in names])
    xyz = np.c_[np.cos(lat_r) * np.cos(lon_r),
                np.cos(lat_r) * np.sin(lon_r), np.sin(lat_r)]
    geo9 = KMeans(n_clusters=9, n_init=10, random_state=0).fit_predict(xyz)
    out["collapse_dendrogram9"] = {k: round(collapse_by(dendro9, X[k]), 3)
                                   for k in keys}
    out["collapse_geo_kmeans9"] = {k: round(collapse_by(geo9, X[k]), 3)
                                   for k in keys}
    rand_vals = {k: [] for k in keys}
    for rep in range(20):
        perm = RNG.permutation(regions)  # same group sizes, random membership
        for k in keys:
            rand_vals[k].append(collapse_by(perm, X[k]))
    out["collapse_random_mean"] = {k: round(float(np.mean(rand_vals[k])), 3)
                                   for k in keys}
    out["collapse_random_range"] = {k: [round(float(np.min(rand_vals[k])), 3),
                                        round(float(np.max(rand_vals[k])), 3)]
                                    for k in keys}
    print("collapse by data-driven dendrogram cut (k=9):", out["collapse_dendrogram9"])
    print("collapse by k-means on true coords (k=9):   ", out["collapse_geo_kmeans9"])
    print("collapse by RANDOM partitions (mean of 20): ", out["collapse_random_mean"])

    # 3) geographic neighbour recall@10
    out["geo_recall10"] = {k: round(neighbour_recall(demb[k], gc), 3)
                           for k in keys + ["raw"]}
    print("geo neighbour recall@10:", out["geo_recall10"])

    # 4) city-level bootstrap over the 124-city sample
    B = 1000
    boots = {k: np.empty(B) for k in keys + ["raw"]}
    for b in range(B):
        s = RNG.integers(0, n, n)
        su = np.triu_indices(n, k=1)
        gcb = gc[np.ix_(s, s)]
        keep = gcb[su] > 0  # drop duplicate-city zero-distance pairs
        for k in keys + ["raw"]:
            dembb = demb[k][np.ix_(s, s)]
            boots[k][b] = spearmanr(dembb[su][keep], gcb[su][keep]).statistic
    def ci(delta):
        return [round(float(np.percentile(delta, 2.5)), 3),
                round(float(np.percentile(delta, 97.5)), 3)]
    out["bootstrap_ci95"] = {
        "pca_minus_mds": ci(boots["pca"] - boots["mds"]),
        "tsne_minus_pca": ci(boots["tsne"] - boots["pca"]),
        "umap_minus_tsne": ci(boots["umap"] - boots["tsne"]),
        "mds_minus_raw": ci(boots["mds"] - boots["raw"]),
        "pca_minus_raw": ci(boots["pca"] - boots["raw"]),
        "tsne_minus_raw": ci(boots["tsne"] - boots["raw"]),
        "umap_minus_raw": ci(boots["umap"] - boots["raw"]),
    }
    print("bootstrap 95% CIs:", json.dumps(out["bootstrap_ci95"], indent=2))

    # 5) rotation scan: best single rotation maximizing corr(y', latitude)
    lat = np.array([CITY_LATLON[c][0] for c in names])
    out["rotation_scan_max_lat_r"] = {}
    for k in ["mds", "tsne"]:
        Xi = X[k] - X[k].mean(axis=0)
        best = 0.0
        for th in np.linspace(0, 2 * np.pi, 3600, endpoint=False):
            y = -Xi[:, 0] * np.sin(th) + Xi[:, 1] * np.cos(th)
            r = np.corrcoef(y, lat)[0, 1]
            best = max(best, abs(r))
        out["rotation_scan_max_lat_r"][k] = round(float(best), 3)
    print("max |corr(y', lat)| over rotations:", out["rotation_scan_max_lat_r"])

    with open("output/robustness.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Saved output/robustness.json")


if __name__ == "__main__":
    main()
