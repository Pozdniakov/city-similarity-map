"""Empirical comparison of similarity->dissimilarity transforms for MDS.

Candidates (all monotone in each other, so nonmetric MDS would be identical):
  raw    d = 1 - cos          (squared chord / 2; semi-metric)
  chord  d = sqrt(2(1-cos))   (Euclidean distance between unit vectors; metric)
  angle  d = arccos(cos)      (geodesic on the unit sphere; metric)

For each: run the same deterministic SMACOF, then measure
  - stress-1 against its own target (scale-invariant),
  - kNN recall@k: fraction of each city's true top-k cosine neighbours that
    appear in its top-k 2-D neighbours (common reference for all),
  - Spearman r between 2-D distances and 1-cos (common reference),
  - Procrustes disparity of the layout vs the raw layout (how different the
    pictures actually are).
"""

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
from sklearn.manifold import MDS

RS = 42


def smacof(D):
    return MDS(n_components=2, metric="precomputed", metric_mds=True,
               init="classical_mds", n_init=1, max_iter=3000, eps=1e-9,
               random_state=RS, n_jobs=-1, normalized_stress=False).fit_transform(D)


def knn_recall(S, X, k):
    n = len(S)
    d2 = squareform(pdist(X))
    hits = 0
    for i in range(n):
        true = set(np.argsort(-S[i])[1:k+1])       # top-k by cosine (skip self)
        emb = set(np.argsort(d2[i])[1:k+1])        # top-k nearest in 2-D
        hits += len(true & emb)
    return hits / (n * k)


def main():
    idx = pd.read_csv("data/city_index.csv")
    V = np.load("data/city_vectors.npy").astype(np.float64)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    S = np.clip(V @ V.T, -1.0, 1.0)
    n = len(S)
    iu = np.triu_indices(n, k=1)

    targets = {
        "raw   1-cos": 1.0 - S,
        "chord sqrt(2(1-cos))": np.sqrt(np.clip(2.0 * (1.0 - S), 0, None)),
        "angle arccos(cos)": np.arccos(S),
    }
    ref = 1.0 - S

    layouts = {}
    print(f"{'transform':<22} {'stress1':>7} {'rec@5':>6} {'rec@10':>7} "
          f"{'spear_r':>8} {'vs_raw':>7}")
    for name, D in targets.items():
        D = D.copy()
        np.fill_diagonal(D, 0.0)
        D = (D + D.T) / 2.0
        X = smacof(D)
        layouts[name] = X
        d_emb = squareform(pdist(X))
        stress1 = np.sqrt(((d_emb - D) ** 2).sum() / (d_emb ** 2).sum())
        r5 = knn_recall(S, X, 5)
        r10 = knn_recall(S, X, 10)
        rho = spearmanr(d_emb[iu], ref[iu]).statistic
        disp = (procrustes(layouts["raw   1-cos"], X)[2]
                if name != "raw   1-cos" else 0.0)
        print(f"{name:<22} {stress1:7.4f} {r5:6.3f} {r10:7.3f} {rho:8.3f} {disp:7.4f}")

    # triangle-inequality violations of the raw transform
    rng = np.random.default_rng(0)
    viol = total = 0
    Draw = 1.0 - S
    for _ in range(200_000):
        i, j, k = rng.choice(n, 3, replace=False)
        total += 1
        if Draw[i, j] > Draw[i, k] + Draw[k, j] + 1e-12:
            viol += 1
    print(f"\ntriangle-inequality violations in 1-cos: {viol}/{total} "
          f"({100*viol/total:.2f}% of sampled triples)")


if __name__ == "__main__":
    main()
