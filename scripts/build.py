import json,math,re,sys,os
from shapely.geometry import shape
from shapely.ops import unary_union,polylabel
src,out=sys.argv[1],sys.argv[2]
ver=re.search(r'ver(\d{8})',src).group(1)
d=json.load(open(src,encoding='utf-8'))
def short(n):
 n=re.sub('(통합특별시|특별자치시|특별자치도|특별시|광역시)$','',n)
 if len(n)==4 and n[-1]=='도':return n[0]+n[2]
 return re.sub('도$','',n)
K,S={},{}
for f in d['features']:
 p=f['properties'];g=shape(f['geometry']).buffer(0)
 K.setdefault(short(p['sidonm']),[]).append(g)
 if p['sidonm']=='서울특별시':S.setdefault(p['sggnm'],[]).append(g)
def build(G,W,tol,mn):
 G={k:unary_union(v) for k,v in G.items()}
 b=unary_union(list(G.values())).bounds
 k=math.cos(math.radians((b[1]+b[3])/2))
 s=(W-20)/((b[2]-b[0])*k);H=(b[3]-b[1])*s+20
 P=lambda x,y:((x*k-b[0]*k)*s+10,(b[3]-y)*s+10)
 R=[]
 for nm in sorted(G):
  g=G[nm].simplify(tol,preserve_topology=True)
  ps=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
  out=''
  for pg in ps:
   for ring in [pg.exterior]+list(pg.interiors):
    q=[P(x,y) for x,y in ring.coords]
    xs=[a for a,_ in q];ys=[c for _,c in q]
    if (max(xs)-min(xs))*(max(ys)-min(ys))<mn:continue
    out+='M'+'L'.join('%.1f,%.1f'%a for a in q)+'Z'
  lp=polylabel(max(ps,key=lambda a:a.area),tolerance=tol/4);x,y=P(lp.x,lp.y)
  R.append({'k':nm,'d':out,'x':round(x/W*100,2),'y':round(y/H*100,2)})
 return {'w':W,'h':round(H,1),'r':R}
al={'광주':'전남광주','전남':'전남광주'} if '전남광주' in K else {}
D={'ver':ver,'src':'vuski/admdongkor '+ver,'alias':al,'kr':build(K,600,.004,4),'seoul':build(S,600,.0006,0)}
json.dump(D,open(out,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(ver,[r['k'] for r in D['kr']['r']],len(D['seoul']['r']))
