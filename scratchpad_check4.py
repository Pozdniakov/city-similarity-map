import re,json,numpy as np
html=open('docs/index.html').read()
m=re.search(r'const DATA = (\{.*?\});', html, re.S)
DATA=json.loads(m.group(1))
cities=DATA['cities']
lat=np.array([c['lat'] for c in cities])
lon=np.array([c['lon'] for c in cities])
def corr(a,b): return float(np.corrcoef(a,b)[0,1])
def multiR(y,X):
    # multiple correlation of y on columns of X
    X1=np.column_stack([np.ones(len(y)),X])
    beta,_,_,_=np.linalg.lstsq(X1,y,rcond=None)
    pred=X1@beta
    return float(np.corrcoef(pred,y)[0,1])
for key in ['mds','pca','tsne','umap']:
    xy=np.array(DATA['layouts'][key]['xy']) if 'layouts' in DATA else np.array(DATA[key]['xy'])
    x=xy[:,0]; y=xy[:,1]
    ew=corr(x,lon); ns=corr(y,lat)
    Rlat=multiR(lat,xy); Rlon=multiR(lon,xy)
    print(f"{key:5s} E-W r(x,lon)={ew:+.3f}  N-S r(y,lat)={ns:+.3f}  | maxR(lat)={Rlat:.3f} maxR(lon)={Rlon:.3f}  metrics={DATA[key]['metrics'] if key in DATA else DATA['layouts'][key]['metrics']}")
