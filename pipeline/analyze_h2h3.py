import os, json, warnings, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
warnings.filterwarnings("ignore")
R=os.path.expanduser("~/form-tightness/results/")
out={}
def row(m,term):
    b=float(m.params[term]); se=float(m.bse[term])
    return dict(est=round(b,3),se=round(se,3),ci95=[round(b-1.96*se,2),round(b+1.96*se,2)],ci90=[round(b-1.645*se,2),round(b+1.645*se,2)],p=float(f"{2*stats.norm.sf(abs(b/se)):.3g}"))
def codes(d):
    d["t"]=np.where(d.tightness=="tight",.5,-.5); d["r"]=np.where(d.register=="verse",.5,-.5); return d
# ---- H2 behavioural
j=pd.DataFrame([json.loads(l) for l in open(R+"role_adoption_judge.jsonl")])
out["judge_n"]=len(j); out["judge_failed"]=int(j.score.isna().sum())
a=pd.concat([pd.read_csv(R+"arm_1_observation.csv"),pd.read_csv(R+"arm_2_capping.csv")],ignore_index=True)
a["arm"]=np.where(a.capping.fillna("").astype(str).str.len()>0,"2_capping","1_observation")
j["stimulus_id"]=j.stimulus_id.astype(str); a["stimulus_id"]=a.stimulus_id.astype(str)
m=a.merge(j[["arm","stimulus_id","sample","score"]],on=["arm","stimulus_id","sample"]).dropna(subset=["score"])
m=codes(m); m["cap"]=np.where(m.arm=="2_capping",.5,-.5)
out["role_score_dist"]={arm:g.score.value_counts().sort_index().to_dict() for arm,g in m.groupby("arm")}
out["role_mean_by_cell_arm"]=m.groupby(["arm","cell"]).score.mean().round(3).unstack().to_dict("index")
out["role_p_score3_by_cell_arm"]=m.assign(s3=(m.score==3)).groupby(["arm","cell"]).s3.mean().round(3).unstack().to_dict("index")
lm=smf.mixedlm("score ~ t*r*cap + C(domain)",m,groups="topic_id",vc_formula={"cell":"0+C(cell)"}).fit(reml=True)
out["H2b_linear_note"]="ordinal mixed model not available in statsmodels; pre-stated fallback: linear mixed model on 0-3"
for k in ["t","r","cap","t:cap","r:cap","t:r"]: out[f"H2b_{k}"]=row(lm,k)
# projection-behaviour link (shift-without-trace check)
a1=m[m.arm=="1_observation"].dropna(subset=["projection_published"])
out["corr_projection_role_score_arm1"]=round(float(stats.spearmanr(a1.projection_published,a1.score)[0]),3)
# ---- H3 Gemma
g=codes(pd.read_csv(R+"arm_3_gemma.csv")); out["gemma_excluded_zero_tokens"]=int(g.projection_published.isna().sum())
g=g.dropna(subset=["projection_published"])
mg=smf.mixedlm("projection_published ~ t*r + C(domain)",g,groups="topic_id",vc_formula={"cell":"0+C(cell)"}).fit(reml=True)
H3=row(mg,"t"); H3["sesoi"]=106.5; H3["TOST_equivalent"]=bool(H3["ci90"][0]>-106.5 and H3["ci90"][1]<106.5)
H3["in_role_sd_units"]=round(H3["est"]/520.1,3)
out["H3_gemma_tight_minus_loose"]=H3
out["gemma_interaction"]=row(mg,"t:r"); out["gemma_register"]=row(mg,"r")
out["gemma_cell_means"]=g.groupby("cell").projection_published.mean().round(1).to_dict()
out["gemma_per_domain_tight_minus_loose"]={d:round(x[x.tightness=="tight"].projection_published.mean()-x[x.tightness=="loose"].projection_published.mean(),1) for d,x in g.groupby("domain")}
out["gemma_layer_sweep_t"]={L:row(smf.mixedlm(f"proj_L{L} ~ t*r + C(domain)",g,groups="topic_id",vc_formula={"cell":"0+C(cell)"}).fit(reml=True),"t") for L in [6,11,22,34]}
q=json.load(open(R+"analysis_arms12.json"))
out["qwen_in_role_sd_units"]={"t":round(q["H1_main_tight_minus_loose"]["est"]/14.65,3),"r":round(q["register_verse_minus_prose"]["est"]/14.65,3),"t:r":round(q["H4_interaction_verse_minus_prose_gap"]["est"]/14.65,3)}
out["gemma_in_role_sd_units"]={"t":round(out["H3_gemma_tight_minus_loose"]["est"]/520.1,3),"r":round(out["gemma_register"]["est"]/520.1,3),"t:r":round(out["gemma_interaction"]["est"]/520.1,3)}
json.dump(out,open(R+"analysis_h2h3.json","w"),indent=1,default=str); print(json.dumps(out,indent=1,default=str))
