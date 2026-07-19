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

    # teaching demo: the real Paris vector (raw values) + real angles to two
    # reference cities for the cosine card
    vecs = np.load("data/city_vectors.npy")
    i_par = names.index("Paris")
    demo = {
        "name": "Paris",
        "vec": [round(float(v), 3) for v in vecs[i_par]],
        "pairs": [[c, round(float(S[i_par, names.index(c)]), 2)]
                  for c in ("Rome", "Beijing")],
    }
    print("demo cosines:", demo["pairs"])

    data = {
        "cities": cities,
        "sims": sims,
        "layouts": layouts,
        "demo": demo,
        "land": load_land("data/ne_110m_land.geojson"),
        "geometa": {"lon0": LON0, "lon1": LON1, "lat0": LAT0, "lat1": LAT1},
        "meta": {"min": SLIDER_MIN, "max": SLIDER_MAX, "default": SLIDER_DEFAULT},
    }
    payload = json.dumps(data, separators=(",", ":"))

    tpl = open("combined_template.html").read()
    assert "__DATA__" in tpl and tpl.count("<script>") == 1
    page = tpl.replace("__DATA__", payload)

    os.makedirs("output", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    standalone = "<!doctype html>\n<html>\n" + page + "\n</html>"
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
