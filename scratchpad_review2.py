import numpy as np, pandas as pd, itertools
V = np.load('data/city_vectors.npy')
Vn = V / np.linalg.norm(V, axis=1, keepdims=True)
S = Vn @ Vn.T
n = S.shape[0]
D = 1 - S
np.fill_diagonal(D, 0)

# Triangle inequality violations over all C(124,3) triples for d=1-cos
viol = 0; max_excess = 0
for i,j,k in itertools.combinations(range(n),3):
    a,b,c = D[i,j], D[i,k], D[j,k]
    # check each side <= sum of other two
    for x,y,z in [(a,b,c),(b,a,c),(c,a,b)]:
        ex = x - (y+z)
        if ex > 1e-12:
            viol += 1
            if ex > max_excess: max_excess = ex
from math import comb
print("C(124,3) =", comb(124,3))
print("triangle-inequality violating triples (counting a violation if ANY side exceeds):")
# Recount: count triples with at least one violation
vt=0; mx=0
for i,j,k in itertools.combinations(range(n),3):
    a,b,c = D[i,j], D[i,k], D[j,k]
    exs = [a-(b+c), b-(a+c), c-(a+b)]
    m = max(exs)
    if m > 1e-12:
        vt+=1
        if m>mx: mx=m
print("  violating triples:", vt, " max excess: %.4f"%mx)

# link counts at cutoffs
iu = np.triu_indices(n,1)
pw = S[iu]
for cut in [0.30, 0.50, 0.80, 0.86]:
    print(f"cutoff {cut}: links = {(pw>=cut).sum()}")
# also exact default readout: strongest X% at 0.50
print("pct of pairs >= .50: %.1f%%" % (100*(pw>=0.50).mean()))
