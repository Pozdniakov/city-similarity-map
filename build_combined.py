"""Assemble the combined interactive page: geographic similarity network +
semantic chart with switchable layouts (MDS / UMAP / t-SNE), shared cutoff
slider, selection drawer and search.

Inputs:  output/layouts.json            (from make_layouts.py)
         data/city_index.csv            (city, region, token)
         data/similarity_matrix.csv     (full 124x124 cosine similarities)
         data/ne_110m_land.geojson      (world outline)
         cities.CITY_LATLON             (true coordinates)
Outputs: output/similarity_maps.html    (standalone, with doctype wrapper)
         docs/index.html                (GitHub Pages)
         <scratchpad>/semantic-city-map.html  (artifact copy, no wrapper)
"""

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

from cities import CITY_LATLON
from plot_geo_network import LAT0, LAT1, LON0, LON1, load_land

SCRATCH = ("/private/tmp/claude-501/-Users-ivan-projects-map-similarity-claude/"
           "3a5d67c2-b89d-4c28-9fcc-6545527253bd/scratchpad/semantic-city-map.html")

SLIDER_MIN = 0.30
SLIDER_MAX = 0.86
SLIDER_DEFAULT = 0.50


def main():
    idx = pd.read_csv("data/city_index.csv")
    Sdf = pd.read_csv("data/similarity_matrix.csv", index_col=0)
    names = list(Sdf.index)
    assert idx["city"].tolist() == names, "city order mismatch"

    cities = []
    for _, row in idx.iterrows():
        lat, lon = CITY_LATLON[row["city"]]
        cities.append({
            "n": row["city"], "r": row["region"], "t": row["token"],
            "lat": round(lat, 3), "lon": round(lon, 3),
        })

    S = Sdf.to_numpy()
    n = len(names)
    sims = [round(float(S[i, j]), 3) for i in range(n) for j in range(i + 1, n)]

    layouts = json.load(open("output/layouts.json"))
    assert all(len(layouts[k]["xy"]) == n for k in layouts)

    # teaching demo: three through-line cities (a close pair + a distant one)
    # with their real vectors and real pairwise cosines, reused by every card
    vecs = np.load("data/city_vectors.npy")
    trio = ["Sydney", "Melbourne", "New York"]
    ti = [names.index(c) for c in trio]
    demo = {
        "cities": trio,
        "vecs": [[round(float(v), 3) for v in vecs[i]] for i in ti],
        "sims": [[round(float(S[a, b]), 2) for b in ti] for a in ti],
    }
    print("demo sims:", {f"{trio[a]}-{trio[b]}": demo["sims"][a][b]
                         for a in range(3) for b in range(a + 1, 3)})

    # clustered heatmap: average-linkage hierarchy on d = 1 - cos with optimal
    # leaf ordering; export the leaf order and ready-to-draw dendrogram polylines
    D = 1.0 - S
    np.fill_diagonal(D, 0.0)
    Z = linkage(squareform((D + D.T) / 2.0, checks=False),
                method="average", optimal_ordering=True)
    dg = dendrogram(Z, no_plot=True)
    cluster = {
        "order": [int(i) for i in dg["leaves"]],
        "icoord": [[round(x, 1) for x in seg] for seg in dg["icoord"]],
        "dcoord": [[round(y, 3) for y in seg] for seg in dg["dcoord"]],
        "dmax": round(float(Z[:, 2].max()), 3),
    }
    print("cluster order head:", [names[i] for i in cluster["order"][:8]])

    data = {
        "cities": cities,
        "sims": sims,
        "layouts": layouts,
        "demo": demo,
        "cluster": cluster,
        "land": load_land("data/ne_110m_land.geojson"),
        "geometa": {"lon0": LON0, "lon1": LON1, "lat0": LAT0, "lat1": LAT1},
        "meta": {"min": SLIDER_MIN, "max": SLIDER_MAX, "default": SLIDER_DEFAULT},
    }
    payload = json.dumps(data, separators=(",", ":"))

    tpl = open("combined_template.html").read()
    assert "__DATA__" in tpl and tpl.count("<script>") == 1
    page = tpl.replace("__DATA__", payload)

    # Standalone / GitHub Pages build gets a proper <head> (lang, description,
    # Open Graph) that the artifact runtime supplies on its own. The scratch
    # copy stays a bare fragment, since the artifact platform wraps it.
    head = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Semantic City Map — 124 world cities by word2vec similarity</title>\n'
        '<meta name="description" content="A teaching demo: 124 world cities '
        'embedded by word2vec, compared by cosine similarity, and laid out with '
        'MDS / PCA / t-SNE / UMAP — a semantic map, a geographic link network, '
        'and a clustered similarity matrix.">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="124 world cities by word2vec similarity">\n'
        '<meta property="og:description" content="Can a computer sketch a map of '
        'the world from the news alone? An interactive teaching demo of embeddings, '
        'cosine similarity and dimensionality reduction.">\n'
        '<meta property="og:url" content="https://pozdniakov.github.io/city-similarity-map/">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '</head>\n<body>\n')
    standalone = head + page + "\n</body>\n</html>"
    os.makedirs("output", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    with open("output/similarity_maps.html", "w") as f:
        f.write(standalone)
    with open("docs/index.html", "w") as f:  # GitHub Pages
        f.write(standalone)
    with open(SCRATCH, "w") as f:
        f.write(page)
    print(f"cities {n}, sims {len(sims)}, layouts {list(layouts)}, "
          f"payload {len(payload)/1024:.0f} KB")
    print("Saved output/similarity_maps.html, docs/index.html and artifact copy")


if __name__ == "__main__":
    sys.exit(main())
