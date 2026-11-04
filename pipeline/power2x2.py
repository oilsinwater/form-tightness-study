import numpy as np
rng=np.random.default_rng(20261030)
T,S,SIMS=96,3,4000
def sim(main,inter,resid=8.,tsd=5.,csd=2.):
    out=[]
    for _ in range(SIMS):
        topic=rng.normal(0,tsd,T)[:,None,None]
        # cells: [verse,prose] x [loose,tight]; effect coded
        reg=np.array([.5,-.5])[None,:,None]; tig=np.array([-.5,.5])[None,None,:]
        mu=topic+main*tig+inter*reg*tig+rng.normal(0,csd,(T,2,2))
        y=mu+rng.normal(0,resid/np.sqrt(S),(T,2,2))   # mean of S samples
        m=(y[:,:,1]-y[:,:,0]).mean(1)                    # tight-loose per topic
        i=(y[:,0,1]-y[:,0,0])-(y[:,1,1]-y[:,1,0])        # (t-l|verse)-(t-l|prose)
        out.append((m.mean(),m.std(ddof=1)/np.sqrt(T),i.mean(),i.std(ddof=1)/np.sqrt(T)))
    return np.array(out)
from scipy import stats
tc=stats.t.ppf(.95,T-1); t2=stats.t.ppf(.975,T-1)
print("| true tight−loose | one-sided power | two-sided power | P(TOST ±3) |")
for e in [0,1,2,3,4]:
    r=sim(e,0); est,se=r[:,0],r[:,1]
    print(f"| {e} | {np.mean(est/se>tc):.3f} | {np.mean(abs(est/se)>t2):.3f} | {np.mean((est-tc*se>-3)&(est+tc*se<3)):.3f} |")
print("\n| true interaction (verse − prose gap) | one-sided power |")
for e in [0,2,3,4,6]:
    r=sim(2,e); est,se=r[:,2],r[:,3]
    print(f"| {e} | {np.mean(est/se>tc):.3f} |")
r=sim(0,0); print("\nanalytic-ish SE main %.3f, interaction %.3f"%(r[:,1].mean(),r[:,3].mean()))
