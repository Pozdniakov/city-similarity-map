"""Extra view: a real geographic map (equirectangular) with cities at their true
coordinates and edges drawn between pairs whose word2vec cosine similarity is
above a threshold. Produces a static PNG at the default threshold and a JSON
bundle (cities, edges, simplified land outline) for the interactive slider page.

Inputs:  data/similarity_matrix.csv, data/ne_110m_land.geojson, cities.CITY_LATLON
Outputs: output/geo_network.png, output/geo_network_data.json
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection

from cities import CITY_LATLON
from plot_map import REGION_STYLE, SURFACE

# Edges with similarity >= EXPORT_MIN are shipped to the interactive page; the
# slider ranges over [EXPORT_MIN, SLIDER_MAX]. DEFAULT_T is the initial cutoff:
# 0.50 keeps 451 of 7,626 pairs (avg degree ~7) — regional constellations stay
# readable without collapsing into a hairball.
EXPORT_MIN = 0.30
SLIDER_MAX = 0.86
DEFAULT_T = 0.50

# equirectangular window (degrees)
LON0, LON1 = -165.0, 180.0
LAT0, LAT1 = -58.0, 82.0

LAND_LIGHT = "#eceae3"   # muted land fill on the light surface
LAND_EDGE = "#dcd9cf"
EDGE_HUE = "#2a78d6"     # similarity links


def load_land(path, min_lat=-57.0, dp=2, min_pts=4):
    """Simplified land polygons: rounded coords, Antarctica dropped, tiny rings
    removed. Returns a list of polygons, each a list of rings of [lon, lat]."""
    gj = json.load(open(path))
    polys = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            multi = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            multi = geom["coordinates"]
        else:
            continue
        for poly in multi:
            rings = []
            for ring in poly:
                r = [[round(x, dp), round(y, dp)] for x, y in ring]
                if max(y for _, y in r) < min_lat:  # below the crop (Antarctica)
                    continue
                if len(r) >= min_pts:
                    rings.append(r)
            if rings:
                polys.append(rings)
    return polys


def main():
    S = pd.read_csv("data/similarity_matrix.csv", index_col=0)
    names = list(S.index)
    sim = S.to_numpy()
    n = len(names)

    # region lookup keyed by city (region isn't in the similarity CSV)
    idx = pd.read_csv("data/city_index.csv").set_index("city")
    region = {c: idx.loc[c, "region"] for c in names}
    lon = np.array([CITY_LATLON[c][1] for c in names])
    lat = np.array([CITY_LATLON[c][0] for c in names])

    iu = np.triu_indices(n, k=1)
    edges = [
        [int(i), int(j), round(float(sim[i, j]), 3)]
        for i, j in zip(*iu)
        if sim[i, j] >= EXPORT_MIN
    ]
    land = load_land("data/ne_110m_land.geojson")

    # ---- static PNG at the default threshold ----
    os.makedirs("output", exist_ok=True)
    fig, ax = plt.subplots(figsize=(17, 7.4), dpi=200)
    fig.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for rings in land:
        for ring in rings:
            arr = np.array(ring)
            ax.fill(arr[:, 0], arr[:, 1], facecolor=LAND_LIGHT, edgecolor=LAND_EDGE,
                    linewidth=0.4, zorder=1)

    shown = [(i, j, s) for i, j, s in edges if s >= DEFAULT_T]
    segs, widths, alphas = [], [], []
    for i, j, s in shown:
        segs.append([(lon[i], lat[i]), (lon[j], lat[j])])
        # map similarity in [DEFAULT_T, max] to visible weight
        f = (s - DEFAULT_T) / max(1e-6, sim[iu].max() - DEFAULT_T)
        widths.append(0.3 + 1.7 * f)
        alphas.append(0.12 + 0.5 * f)
    lc = LineCollection(segs, colors=[(0.165, 0.471, 0.839, a) for a in alphas],
                        linewidths=widths, zorder=2)
    ax.add_collection(lc)

    for reg, (color, _marker) in REGION_STYLE.items():
        m = [k for k in range(n) if region[names[k]] == reg]
        if not m:
            continue
        ax.scatter(lon[m], lat[m], s=26, c=color, edgecolors=SURFACE,
                   linewidths=0.6, zorder=3, label=f"{reg} ({len(m)})")

    ax.set_xlim(LON0, LON1)
    ax.set_ylim(LAT0, LAT1)
    ax.set_aspect(1.0)  # equirectangular: 1 deg lon == 1 deg lat on screen
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    n_pairs = n * (n - 1) // 2
    ax.set_title(
        f"World cities linked by word2vec similarity — cosine ≥ {DEFAULT_T:.2f} "
        f"({len(shown)} of {n_pairs:,} city pairs).  Cities at true coordinates; "
        f"line opacity ∝ similarity.",
        fontsize=13, color="#0b0b0b", loc="left", pad=10, fontweight="bold",
    )
    ax.legend(loc="lower left", ncols=3, frameon=False, fontsize=8,
              labelcolor="#52514e", handletextpad=0.3, columnspacing=1.2,
              borderaxespad=0.4)

    fig.tight_layout()
    fig.savefig("output/geo_network.png", facecolor=SURFACE, bbox_inches="tight")
    print(f"Saved output/geo_network.png  ({len(shown)} edges at t={DEFAULT_T})")

    # ---- data bundle for the interactive page ----
    cities = [
        {"n": names[k], "r": region[names[k]],
         "lat": round(float(lat[k]), 3), "lon": round(float(lon[k]), 3)}
        for k in range(n)
    ]
    bundle = {
        "cities": cities,
        "edges": edges,
        "land": land,
        "meta": {"default": DEFAULT_T, "min": EXPORT_MIN, "max": SLIDER_MAX,
                 "lon0": LON0, "lon1": LON1, "lat0": LAT0, "lat1": LAT1},
    }
    with open("output/geo_network_data.json", "w") as f:
        json.dump(bundle, f, separators=(",", ":"))
    kb = os.path.getsize("output/geo_network_data.json") / 1024
    print(f"Saved output/geo_network_data.json  ({len(edges)} edges >= {EXPORT_MIN}, {kb:.0f} KB)")


if __name__ == "__main__":
    main()
