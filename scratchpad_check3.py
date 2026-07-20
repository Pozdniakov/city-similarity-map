import numpy as np, csv
V = np.load('data/city_vectors.npy')
cities=[]; regions=[]
with open('data/city_index.csv') as f:
    for row in csv.DictReader(f):
        cities.append(row['city']); regions.append(row['region'])
cities=np.array(cities); regions=np.array(regions)
Vn = V/np.linalg.norm(V,axis=1,keepdims=True)
S = Vn@Vn.T
def idx(name): return int(np.where(cities==name)[0][0])
us=['New York','Los Angeles','Chicago','Houston','Phoenix','Philadelphia','San Francisco','Boston','Seattle','Atlanta','Dallas','Denver','Miami','Washington DC']
us_idx=[idx(c) for c in us]
euro=[cities[i] for i in range(len(cities)) if regions[i]=='Europe']
print("European cities:",len(euro))
# For each euro city, mean and max cosine to US cities
rows=[]
for c in euro:
    i=idx(c)
    sims=[S[i,j] for j in us_idx]
    rows.append((c, np.mean(sims), np.max(sims), us[int(np.argmax(sims))]))
print("\n-- ranked by MEAN cos to US cities --")
for c,mn,mx,arg in sorted(rows,key=lambda r:-r[1])[:8]:
    print(f"  mean {mn:.4f}  max {mx:.4f} ({arg:12s})  {c}")
print("\n-- ranked by MAX cos to US cities --")
for c,mn,mx,arg in sorted(rows,key=lambda r:-r[2])[:8]:
    print(f"  max {mx:.4f} ({arg:12s})  mean {mn:.4f}  {c}")
