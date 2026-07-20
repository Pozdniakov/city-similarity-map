import numpy as np, csv
from itertools import combinations
V = np.load('data/city_vectors.npy')
cities=[]; regions=[]
with open('data/city_index.csv') as f:
    for row in csv.DictReader(f):
        cities.append(row['city']); regions.append(row['region'])
cities=np.array(cities); regions=np.array(regions)
Vn = V/np.linalg.norm(V,axis=1,keepdims=True)
S = Vn@Vn.T
n=len(cities)
iu,ju=np.triu_indices(n,1)
pair_cos=S[iu,ju]
print("num unique pairs:", len(pair_cos))
print("mean cos: %.4f" % pair_cos.mean())
print("max: %.4f  min: %.4f" % (pair_cos.max(), pair_cos.min()))
amin=pair_cos.argmin(); amax=pair_cos.argmax()
print("min pair:", cities[iu[amin]], "-", cities[ju[amin]], round(float(pair_cos[amin]),4))
print("max pair:", cities[iu[amax]], "-", cities[ju[amax]], round(float(pair_cos[amax]),4))
# Houston-Lisbon specifically
def idx(name): return int(np.where(cities==name)[0][0])
print("Houston-Lisbon cos: %.4f" % S[idx('Houston'),idx('Lisbon')])

# link counts at cutoffs
for c in [0.30,0.50,0.80,0.86]:
    print(f"pairs >= {c}: {(pair_cos>=c).sum()}")

# triangle inequality on d=1-cos
D = 1 - S
np.fill_diagonal(D,0)
viol=0; maxexcess=0; examples=[]
# For each triple i<j<k check all three triangle inequalities
# vectorize partially: loop over k as apex
for a,b,c in combinations(range(n),3):
    dab,dac,dbc=D[a,b],D[a,c],D[b,c]
    # check each side <= sum of other two
    for x,y,z in ((dab,dac,dbc),(dac,dab,dbc),(dbc,dab,dac)):
        if x > y+z:
            excess=x-(y+z)
            viol+=1
            if excess>maxexcess: maxexcess=excess
            examples.append((cities[a],cities[b],cities[c],round(excess,4)))
print("triangle violations (per-inequality count):", viol, "max excess: %.4f"%maxexcess)
# count of triples that have at least one violation
