"""Pre-registered analyses for Arms 1-2 (prereg sha in prereg/freeze.txt)."""
import os, json, warnings, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
warnings.filterwarnings("ignore")
R=os.path.expanduser("~/form-tightness/results/"); S=os.path.expanduser("~/form-tightness/stimuli/")
stim=pd.DataFrame([json.loads(l) for l in open(S+"stimuli.jsonl")])
out={}
def prep(f):
    d=pd.read_csv(R+f).merge(stim[["id","log_ppl","tokens"]],left_on="stimulus_id",right_on="id")
    d["t"]=np.where(d.tightness=="tight",.5,-.5); d["r"]=np.where(d.register=="verse",.5,-.5)
    d["excluded_zero_tokens"]=int(d.projection_published.isna().sum())
    d=d.dropna(subset=["projection_published"]).copy()
    d["hit_cap"]=d.n_tokens_span>=505
    d["lp_c"]=d.log_ppl-d.log_ppl.mean(); d["tok_c"]=(d.tokens-d.tokens.mean())/10
    return d
def fit(d,y,extra=""):
    m=smf.mixedlm(f"{y} ~ t*r + C(domain){extra}",d,groups="topic_id",vc_formula={"cell":"0+C(cell)"}).fit(reml=True)
    return m
def row(m,term):
    b=m.params[term]; se=m.bse[term]; z=b/se
    return dict(est=round(b,3),se=round(se,3),ci95=[round(b-1.96*se,2),round(b+1.96*se,2)],ci90=[round(b-1.645*se,2),round(b+1.645*se,2)],p=float(f"{2*stats.norm.sf(abs(z)):.3g}"))
a1=prep("arm_1_observation.csv")
m=fit(a1,"projection_published")
H1=row(m,"t"); H1["p_one_sided_tight_gt_loose"]=float(f"{stats.norm.sf(H1['est']/H1['se']):.3g}")
H1["TOST_equivalent_pm3"]=bool(H1["ci90"][0]>-3 and H1["ci90"][1]<3)
out["H1_main_tight_minus_loose"]=H1
H4=row(m,"t:r"); H4["refuted_upper90_lt_3"]=bool(H4["est"]+1.645*H4["se"]<3); H4["p_one_sided_gt0"]=float(f"{stats.norm.sf(H4['est']/H4['se']):.3g}")
out["H4_interaction_verse_minus_prose_gap"]=H4
out["register_verse_minus_prose"]=row(m,"r")
out["excluded_zero_tokens"]={"arm1":int(a1.excluded_zero_tokens.iloc[0])}
out["n_hit_512_cap_arm1"]=int(a1.hit_cap.sum())
out["sens_no_cap_hits_t"]=row(fit(a1[~a1.hit_cap],"projection_published"),"t")
out["sens_no_coding_t"]=row(fit(a1[a1.domain!="coding"],"projection_published"),"t")
out["sens_no_coding_t_x_r"]=row(fit(a1[a1.domain!="coding"],"projection_published"),"t:r")
out["sens_response_length_cov_t"]=row(fit(a1.assign(nt=(a1.n_response_tokens-a1.n_response_tokens.mean())/100),"projection_published","+ nt"),"t")
out["per_domain_tight_minus_loose"]={dm:round(g[g.tightness=="tight"].projection_published.mean()-g[g.tightness=="loose"].projection_published.mean(),2) for dm,g in a1.groupby("domain")}
out["resid_sd"]=round(float(np.sqrt(m.scale)),2)
out["cell_means"]=a1.groupby("cell").projection_published.agg(["mean","std","count"]).round(2).to_dict("index")
out["simple_effects"]={reg:round(a1[(a1.register==reg)&(a1.tightness=="tight")].projection_published.mean()-a1[(a1.register==reg)&(a1.tightness=="loose")].projection_published.mean(),2) for reg in ["verse","prose"]}
mc=fit(a1,"projection_published","+ lp_c + tok_c"); out["covariate_adjusted_t"]=row(mc,"t"); out["covariate_shift_gt_1"]=bool(abs(mc.params["t"]-m.params["t"])>1)
out["secondary_axis_ours_t"]=row(fit(a1,"projection_ours"),"t")
out["refusal_projection"]={k:row(fit(a1,"projection_refusal"),k) for k in ["t","r","t:r"]}
out["layer_sweep_t"]={L:row(fit(a1,f"proj_L{L}"),"t") for L in [11,22,32,45]}
out["layer_sweep_t_x_r"]={L:row(fit(a1,f"proj_L{L}"),"t:r") for L in [11,22,32,45]}
dec=[f"tok_decile_{i}" for i in range(10)]
out["per_token_deciles_by_cell"]={c:[round(x,1) for x in g[dec].mean()] for c,g in a1.groupby("cell")}
fl=a1.groupby("cell").floor_frac_mean.mean().round(3).to_dict(); out["floor_coverage_by_cell"]=fl
out["floor_condition_loose_ge_25pct"]=bool(a1[a1.tightness=="loose"].floor_frac_mean.mean()>=.25)
out["response_tokens_by_cell"]=a1.groupby("cell").n_response_tokens.mean().round(0).to_dict()
# Arm 2
a2=prep("arm_2_capping.csv"); a2["cap"]=.5; a1["cap"]=-.5
both=pd.concat([a1,a2],ignore_index=True)
m2=smf.mixedlm("projection_published ~ t*r*cap + C(domain)",both,groups="topic_id",vc_formula={"cell":"0+C(cell)"}).fit(reml=True)
out["arm2_capping_main"]=row(m2,"cap"); out["arm2_t_x_cap"]=row(m2,"t:cap")
g1=a1.groupby("tightness").projection_published.mean(); g2=a2.groupby("tightness").projection_published.mean()
out["arm2_gap_tight_minus_loose"]={"uncapped":round(g1.tight-g1.loose,2),"capped":round(g2.tight-g2.loose,2)}
out["arm2_cell_means"]=a2.groupby("cell").projection_published.mean().round(2).to_dict()
# final manipulation check
r=pd.read_csv(S+"tightness_ratings.csv"); r["cons"]=r[["item1","item2","item5"]].sum(1)
def d(a,b): return round((a.mean()-b.mean())/np.sqrt((a.var()+b.var())/2),2)
out["manip_final"]={reg:{"d_total":d(r[(r.register==reg)&(r.tightness=="tight")].total,r[(r.register==reg)&(r.tightness=="loose")].total),"d_constraint":d(r[(r.register==reg)&(r.tightness=="tight")].cons,r[(r.register==reg)&(r.tightness=="loose")].cons)} for reg in ["verse","prose"]}
out["manip_n"]=len(r); out["manip_cell_means"]=r.groupby("cell")[["total","cons"]].mean().round(2).to_dict("index")
json.dump(out,open(R+"analysis_arms12.json","w"),indent=1,default=str)
print(json.dumps(out,indent=1,default=str))
