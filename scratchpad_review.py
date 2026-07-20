import numpy as np, pandas as pd, itertools
V = np.load('data/city_vectors.npy')
idx = pd.read_csv('data/city_index.csv')
names = idx['city'].tolist()
print("shape:", V.shape, "n names:", len(names))
# normalize
Vn = V / np.linalg.norm(V, axis=1, keepdims=True)
S = Vn @ Vn.T
n = len(names)
def ci(name): return names.index(name)

# off-diagonal stats
iu = np.triu_indices(n, 1)
pairs = S[iu]
print("\n--- cosine matrix stats (7626 pairs) ---")
print("num pairs:", len(pairs))
print("max cos: %.4f" % pairs.max(), "  min cos: %.4f" % pairs.min(), "  mean: %.4f" % pairs.mean())
# which pairs
amax = np.argmax(pairs); amin = np.argmin(pairs)
print("max pair:", names[iu[0][amax]], "-", names[iu[1][amax]], "%.3f"%pairs[amax])
print("min pair:", names[iu[0][amin]], "-", names[iu[1][amin]], "%.3f"%pairs[amin])

def cos(a,b): return S[ci(a),ci(b)]
print("\n--- specific pairs ---")
for a,b in [("Sydney","Melbourne"),("Sydney","New York"),("Melbourne","New York"),
            ("Madrid","Barcelona"),("Tokyo","Lisbon"),("Lisbon","Madrid"),
            ("Houston","Lisbon")]:
    try:
        c = cos(a,b); import math
        print(f"{a}-{b}: cos={c:.3f}  angle={math.degrees(math.acos(max(-1,min(1,c)))):.1f}deg")
    except ValueError as e:
        print(f"{a}-{b}: NAME NOT FOUND ({e})")

print("\n--- Dubai top-10 nearest by cosine ---")
di = ci("Dubai")
order = np.argsort(-S[di])
cnt=0
for j in order:
    if j==di: continue
    print(f"  {names[j]:20s} {S[di,j]:.3f}")
    cnt+=1
    if cnt>=10: break
