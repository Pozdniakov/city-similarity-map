"""Step 2+3: pairwise word2vec cosine similarity between cities, conversion to
dissimilarity, and 2-D metric MDS (SMACOF) on the precomputed dissimilarities.

Inputs:  data/city_vectors.npy, data/city_index.csv  (from extract_vectors.py)
Outputs: data/similarity_matrix.csv
         data/dissimilarity_matrix.csv
         data/mds_coordinates.csv   (city, region, token, x, y)
"""

import numpy as np
import pandas as pd
from scipy.linalg import orthogonal_procrustes
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

from cities import CITY_LATLON

RANDOM_STATE = 42


def main():
    idx = pd.read_csv("data/city_index.csv")
    vecs = np.load("data/city_vectors.npy").astype(np.float64)
    assert len(idx) == len(vecs), "index/vector length mismatch"
    names = idx["city"].tolist()
    n = len(names)

    # cosine similarity
    V = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    S = np.clip(V @ V.T, -1.0, 1.0)

    # dissimilarity: d = 1 - cosine similarity
    D = 1.0 - S
    np.fill_diagonal(D, 0.0)
    D = (D + D.T) / 2.0  # enforce exact symmetry for SMACOF

    mds = MDS(
        n_components=2,
        metric="precomputed",
        metric_mds=True,
        init="classical_mds",  # deterministic classical-MDS start, then SMACOF refinement
        n_init=1,
        max_iter=3000,
        eps=1e-9,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        normalized_stress=False,
    )
    X = mds.fit_transform(D)

    # Kruskal stress-1: how faithfully 2-D distances reproduce the input
    # (denominator is the sum of squared *embedding* distances, per Kruskal 1964)
    d_emb = squareform(pdist(X))
    stress1 = np.sqrt(((d_emb - D) ** 2).sum() / (d_emb**2).sum())

    # --- Orient the map to real geography ---
    # An MDS solution is arbitrary up to rotation, reflection and translation.
    # Rather than a made-up convention, find the orthogonal transform (rotation
    # + optional reflection — NO scaling or shear, so every distance is
    # preserved exactly) that best maps the embedding onto each city's true
    # (longitude, latitude). Afterwards +x points ~east and +y points ~north.
    assert set(names) <= set(CITY_LATLON), "missing coordinates for some cities"
    geo = np.array([[CITY_LATLON[c][1], CITY_LATLON[c][0]] for c in names])  # (lon, lat)

    def geo_corr(Y):
        """Pearson r of (x vs longitude, y vs latitude) — cardinal correspondence."""
        return (float(np.corrcoef(Y[:, 0], geo[:, 0])[0, 1]),
                float(np.corrcoef(Y[:, 1], geo[:, 1])[0, 1]))

    # previous orientation (PCA + fixed New-York-left / Tokyo-up sign), kept only
    # to quantify how much the geographic alignment improves things
    name_to_i = {c: i for i, c in enumerate(names)}
    X_old = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(X)
    if X_old[name_to_i["New York"], 0] > 0:
        X_old[:, 0] *= -1
    if X_old[name_to_i["Tokyo"], 1] < 0:
        X_old[:, 1] *= -1
    ew_old, ns_old = geo_corr(X_old)

    # standardize the two geographic axes so E-W and N-S count equally: longitude
    # spans ~300 deg here vs latitude ~100 deg, and without this the fit just
    # chases longitude and ignores the (weaker) latitude signal
    Xc = X - X.mean(axis=0)
    G = (geo - geo.mean(axis=0)) / geo.std(axis=0)
    R, _ = orthogonal_procrustes(Xc, G)
    X = Xc @ R
    ew_new, ns_new = geo_corr(X)

    pd.DataFrame(S, index=names, columns=names).to_csv("data/similarity_matrix.csv")
    pd.DataFrame(D, index=names, columns=names).to_csv("data/dissimilarity_matrix.csv")
    out = idx.copy()
    out["x"] = X[:, 0]
    out["y"] = X[:, 1]
    out.to_csv("data/mds_coordinates.csv", index=False)

    print(f"{n} cities | raw SMACOF stress: {mds.stress_:.4f} | Kruskal stress-1: {stress1:.4f}")
    print("Geographic correspondence (Pearson r, arbitrary orientation -> geo-aligned):")
    print(f"  E-W  x vs longitude: {ew_old:+.2f} -> {ew_new:+.2f}")
    print(f"  N-S  y vs latitude:  {ns_old:+.2f} -> {ns_new:+.2f}")

    # sanity report: most/least similar pairs and a few nearest-neighbor spot checks
    iu = np.triu_indices(n, k=1)
    pairs = sorted(zip(S[iu], iu[0], iu[1]), reverse=True)
    print("\nTop 10 most similar pairs:")
    for s, i, j in pairs[:10]:
        print(f"  {names[i]:>16} - {names[j]:<16} {s:.3f}")
    print("Bottom 5 least similar pairs:")
    for s, i, j in pairs[-5:]:
        print(f"  {names[i]:>16} - {names[j]:<16} {s:.3f}")
    print("\nNearest neighbors (word2vec space):")
    for probe in ["Paris", "Tokyo", "Lagos", "San Francisco", "Dubai"]:
        if probe in name_to_i:
            i = name_to_i[probe]
            nn = np.argsort(-S[i])
            nbrs = [names[j] for j in nn if j != i][:5]
            print(f"  {probe:>16}: {', '.join(nbrs)}")


if __name__ == "__main__":
    main()
