"""Render the 2-D MDS map of cities as a static PNG, and export the data
(including the collision-adjusted label positions) for the interactive page.

Input:  data/mds_coordinates.csv, data/similarity_matrix.csv
Output: output/city_map.png, output/artifact_data.json
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text

# dataviz reference palette: fixed categorical slot order; slot 1 is reused for
# the 9th region with a different marker shape (composite encoding), and every
# point is direct-labeled, so identity never rides on color alone
REGION_STYLE = {
    "North America":              ("#2a78d6", "o"),
    "South America":              ("#1baf7a", "s"),
    "Europe":                     ("#eda100", "^"),
    "Middle East & North Africa": ("#008300", "D"),
    "Sub-Saharan Africa":         ("#4a3aa7", "v"),
    "South Asia":                 ("#e34948", "P"),
    "East Asia":                  ("#e87ba4", "X"),
    "Southeast Asia":             ("#eb6834", "p"),
    "Oceania":                    ("#2a78d6", "^"),
}
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"


def main():
    df = pd.read_csv("data/mds_coordinates.csv")
    os.makedirs("output", exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 12), dpi=200)
    fig.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for region, (color, marker) in REGION_STYLE.items():
        sub = df[df["region"] == region]
        if sub.empty:
            continue
        ax.scatter(
            sub["x"], sub["y"],
            s=70, c=color, marker=marker,
            edgecolors=SURFACE, linewidths=1.2,
            label=f"{region} ({len(sub)})", zorder=3,
        )

    texts = [
        ax.text(row.x, row.y, row.city, fontsize=7.5, color=INK_SECONDARY, zorder=4)
        for row in df.itertuples()
    ]
    adjust_text(
        texts, ax=ax,
        expand=(1.15, 1.3),
        arrowprops=dict(arrowstyle="-", color=INK_MUTED, lw=0.5, alpha=0.6),
    )

    # MDS axes are abstract — no meaningful units, so no ticks or spines
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(
        f"Semantic map of {len(df)} world cities",
        fontsize=17, color=INK_PRIMARY, loc="left", pad=18, fontweight="bold",
    )
    ax.text(
        0, 1.005,
        "Word2vec (Google News, 300d) cosine similarity → dissimilarity (1 − cos) → 2-D metric MDS, "
        "rotated to geography (→ east, ↑ north). E–W tracks longitude r=0.70; N–S latitude only r=0.17.",
        transform=ax.transAxes, fontsize=9.5, color=INK_MUTED, va="bottom",
    )
    leg = ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.01), ncols=3,
        frameon=False, fontsize=9, labelcolor=INK_SECONDARY,
        borderaxespad=0, handletextpad=0.4, columnspacing=1.4,
    )
    for h in leg.legend_handles:
        h.set_sizes([48])

    fig.tight_layout()
    fig.savefig("output/city_map.png", facecolor=SURFACE, bbox_inches="tight")
    print("Saved output/city_map.png")

    # export for the interactive page: coordinates, adjusted label positions,
    # and each city's top-5 nearest neighbors by cosine similarity
    S = pd.read_csv("data/similarity_matrix.csv", index_col=0)
    assert list(S.index) == df["city"].tolist()
    sim = S.to_numpy()
    cities = []
    for i, row in enumerate(df.itertuples()):
        order = np.argsort(-sim[i])
        nbrs = [[int(j), round(float(sim[i, j]), 3)] for j in order if j != i][:5]
        lx, ly = texts[i].get_position()
        cities.append({
            "n": row.city, "r": row.region, "t": row.token,
            "x": round(row.x, 4), "y": round(row.y, 4),
            "lx": round(float(lx), 4), "ly": round(float(ly), 4),
            "nb": nbrs,
        })
    data = {"cities": cities}
    with open("output/artifact_data.json", "w") as f:
        json.dump(data, f)
    print("Saved output/artifact_data.json")

    # self-contained interactive page (artifact_template.html with data injected)
    tpl = open("artifact_template.html").read()
    assert "__DATA__" in tpl
    with open("output/city_map.html", "w") as f:
        f.write("<!doctype html>\n<html>\n" + tpl.replace("__DATA__", json.dumps(data)) + "\n</html>")
    print("Saved output/city_map.html")


if __name__ == "__main__":
    main()
