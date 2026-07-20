import numpy as np, csv
V = np.load('data/city_vectors.npy')
cities=[]; regions=[]
with open('data/city_index.csv') as f:
    r=csv.DictReader(f)
    for row in r:
        cities.append(row['city']); regions.append(row['region'])
cities=np.array(cities); regions=np.array(regions)
print("shape", V.shape, "n", len(cities))
# normalize
Vn = V/np.linalg.norm(V,axis=1,keepdims=True)
S = Vn@Vn.T
def idx(name): return int(np.where(cities==name)[0][0])
def neighbors(name,k=12):
    i=idx(name); s=S[i].copy(); s[i]=-2
    order=np.argsort(-s)[:k]
    return [(cities[j], round(float(s[j]),4), regions[j]) for j in order]
for c in ['Dubai','Sydney','Melbourne','Lisbon','London','St Petersburg']:
    print("\n==",c,"==")
    for nm,sc,rg in neighbors(c,12):
        print(f"  {sc:.4f}  {nm:20s} {rg}")
# tightest pair overall
n=len(cities)
Sm=S.copy(); np.fill_diagonal(Sm,-2)
flat=np.argsort(-Sm,axis=None)
seen=set(); print("\n== TOP 10 tightest pairs ==")
cnt=0
for f in flat:
    i,j=divmod(int(f),n)
    if i<j:
        key=(i,j)
    else:
        key=(j,i)
    if key in seen: continue
    seen.add(key); cnt+=1
    print(f"  {Sm[i,j]:.4f}  {cities[key[0]]} & {cities[key[1]]}")
    if cnt>=10: break
