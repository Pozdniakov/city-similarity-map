"""Stream-parse the GoogleNews word2vec binary file and extract vectors for the
city tokens defined in cities.py.

The .bin format: ASCII header "<vocab_size> <dim>\n", then per entry the token
bytes terminated by b' ' followed by <dim> float32 values. Some variants of the
format put b'\n' before the next token, so leading newlines are stripped from
tokens. Matching is done at the byte level to sidestep encoding issues.

Outputs:
  data/city_vectors.npy   (n_cities x 300 float32, rows ordered as in the CSV)
  data/city_index.csv     (city, region, token used)
"""

import gzip
import sys
import numpy as np
import pandas as pd

from cities import CITIES, COMPOSE_FALLBACK, candidates_for

MODEL_PATH = "data/word2vec-google-news-300.bin.gz"
CHUNK = 1 << 23  # 8 MB


def iter_entries(path):
    """Yield (token_bytes, vector_bytes) for every entry in the binary file."""
    with gzip.open(path, "rb") as f:
        header = f.readline().split()
        vocab_size, dim = int(header[0]), int(header[1])
        vec_bytes = dim * 4
        buf = b""
        pos = 0
        for _ in range(vocab_size):
            # ensure a full "token vector" entry is in the buffer
            while True:
                space = buf.find(b" ", pos)
                if space != -1 and len(buf) - space - 1 >= vec_bytes:
                    break
                chunk = f.read(CHUNK)
                if not chunk:
                    return  # truncated file; stop cleanly
                buf = buf[pos:] + chunk
                pos = 0
            token = buf[pos:space].lstrip(b"\n")
            vec = buf[space + 1 : space + 1 + vec_bytes]
            pos = space + 1 + vec_bytes
            yield token, vec


def main():
    # candidate token (bytes) -> list of city indices that want it
    wanted: dict[bytes, list[int]] = {}
    city_cands: list[list[bytes]] = []
    for i, (name, _region, extra) in enumerate(CITIES):
        cands = [c.encode("utf-8") for c in candidates_for(name, extra)]
        city_cands.append(cands)
        for c in cands:
            wanted.setdefault(c, []).append(i)
    compose_tokens = {
        t.encode("utf-8") for parts in COMPOSE_FALLBACK.values() for t in parts
    }
    for t in compose_tokens:
        wanted.setdefault(t, [])

    found: dict[bytes, np.ndarray] = {}
    n_scanned = 0
    for token, vec in iter_entries(MODEL_PATH):
        n_scanned += 1
        if token in wanted and token not in found:
            found[token] = np.frombuffer(vec, dtype=np.float32).copy()
            if len(found) == len(wanted):
                break
        if n_scanned % 500_000 == 0:
            print(f"  scanned {n_scanned:,} tokens, matched {len(found)}/{len(wanted)} candidates",
                  flush=True)
    print(f"Scan finished: {n_scanned:,} tokens read, {len(found)}/{len(wanted)} candidates matched")

    rows, vectors, missing = [], [], []
    for i, (name, region, _extra) in enumerate(CITIES):
        tok = next((c for c in city_cands[i] if c in found), None)
        if tok is not None:
            label = tok.decode("utf-8")
            vec = found[tok]
        elif name in COMPOSE_FALLBACK:
            parts = [p.encode("utf-8") for p in COMPOSE_FALLBACK[name]]
            if not all(p in found for p in parts):
                missing.append(name)
                continue
            label = "mean(" + ",".join(COMPOSE_FALLBACK[name]) + ")"
            vec = np.mean([found[p] for p in parts], axis=0)
        else:
            missing.append(name)
            continue
        rows.append({"city": name, "region": region, "token": label})
        vectors.append(vec)

    if missing:
        print(f"WARNING: {len(missing)} cities not found in vocabulary: {missing}")
    df = pd.DataFrame(rows)
    np.save("data/city_vectors.npy", np.vstack(vectors))
    df.to_csv("data/city_index.csv", index=False)
    print(f"Saved {len(df)} cities -> data/city_vectors.npy, data/city_index.csv")


if __name__ == "__main__":
    sys.exit(main())
