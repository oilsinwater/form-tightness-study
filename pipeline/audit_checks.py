"""audit_checks.py — post-hoc audit of REPORT.md against the data that is in this repo.

Not preregistered. Everything here is a check on the reported analysis, not a new hypothesis test.
Runs from the repo root on files that are committed (Arms 1-2 per-generation CSVs are NOT in the
repo, so Qwen projection analyses cannot be recomputed here):

  stimuli/stimuli.jsonl              decorrelation, per-domain r, residual address/self-reference balance
  stimuli/tightness_ratings.csv      manipulation check
  results/role_adoption_judge.jsonl  H2 behavioural criterion as frozen (loose cells, capped vs uncapped)
  results/arm_3_gemma.csv            H3 reproduction, conservative topic-level check, domain effect,
                                     cap hits, length, deciles, self-reference covariate
  results/check_b_refusal_cosine.json  gate (b) max over layers

Output: results/audit_checks.json
"""
import json, os, warnings
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
out = {}


def row(m, term):
    b, se = float(m.params[term]), float(m.bse[term])
    return dict(est=round(b, 3), se=round(se, 3), ci95=[round(b - 1.96 * se, 2), round(b + 1.96 * se, 2)],
                ci90=[round(b - 1.645 * se, 2), round(b + 1.645 * se, 2)],
                p=float(f"{2 * stats.norm.sf(abs(b / se)):.3g}"))


def codes(d):
    d["t"] = np.where(d.tightness == "tight", .5, -.5)
    d["r"] = np.where(d.register == "verse", .5, -.5)
    return d


def fit(d, f):
    return smf.mixedlm(f, d, groups="topic_id", vc_formula={"cell": "0+C(cell)"}).fit(reml=True)


# ---------------------------------------------------------------- stimuli
s = codes(pd.DataFrame([json.loads(l) for l in open(P("stimuli", "stimuli.jsonl"))]))
s["tt"] = (s.tightness == "tight").astype(int)
out["stimuli_r_per_domain_within_register"] = {
    f"{d}/{reg}": {"r_tokens": round(g.tt.corr(g.tokens), 3), "r_log_ppl": round(g.tt.corr(g.log_ppl), 3)}
    for (d, reg), g in s.groupby(["domain", "register"])}
out["stimuli_self_ref_by_cell"] = s.groupby("cell").self_ref_count.agg(["mean", "std"]).round(2).to_dict("index")
out["stimuli_second_person_by_cell"] = s.groupby("cell").second_person_count.agg(["mean", "std"]).round(2).to_dict("index")
sp = {}
for reg, g in s.groupby("register"):
    a, b = g[g.tightness == "loose"].self_ref_count, g[g.tightness == "tight"].self_ref_count
    sp[reg] = {"loose_minus_tight": round(a.mean() - b.mean(), 2),
               "d": round((a.mean() - b.mean()) / np.sqrt((a.var() + b.var()) / 2), 2),
               "mannwhitney_p": float(f"{stats.mannwhitneyu(a, b).pvalue:.3g}")}
out["stimuli_self_ref_imbalance"] = sp

# ---------------------------------------------------------------- manipulation check
r = pd.read_csv(P("stimuli", "tightness_ratings.csv"))
out["manip_n_rated"] = int(len(r))
out["manip_n_raters"] = int(r.rater_model.nunique())
out["manip_icc_computable"] = False  # one rater only; the frozen gate requires ICC(2,1) >= .75 on 60 items

# ---------------------------------------------------------------- gate (b)
cb = json.load(open(P("results", "check_b_refusal_cosine.json")))
out["gate_b"] = {"cos_L32": round(cb["cos_L32_last_instruction_token"], 3),
                 "max_abs_pruned": cb["max_abs_cos_last_instruction_token"],
                 "max_abs_unpruned": cb["max_abs_cos_last_instruction_token_unpruned"],
                 "max_abs_any_eoi_position": cb["max_abs_cos_any_eoi_position"]}

# ---------------------------------------------------------------- H2 behavioural, as frozen
# Frozen criterion (prereg, Inference criteria): "Role adoption: T1 unsteered vs T1 capped contrast,
# p < .05" -> under v2 naming, loose cells, Arm 1 vs Arm 2.
j = pd.DataFrame([json.loads(l) for l in open(P("results", "role_adoption_judge.jsonl"))])
parts = j.stimulus_id.str.extract(r"^(?P<domain>.+)_(?P<num>\d\d)_(?P<tightness>loose|tight)_(?P<register>verse|prose)$")
j = pd.concat([j, parts], axis=1)
j["topic_id"] = j.domain + "_" + j.num
j["cell"] = j.tightness + "_" + j.register
j = codes(j)
j["cap"] = np.where(j.arm == "2_capping", .5, -.5)
lo = j[j.tightness == "loose"]
m = fit(lo, "score ~ cap * r + C(domain)")
h2 = {"loose_cells_capping_effect_lmm": row(m, "cap")}
w = lo.pivot_table(index=["stimulus_id", "sample"], columns="arm", values="score").dropna()
diff = w["2_capping"] - w["1_observation"]
h2["loose_paired_n"] = int(len(diff))
h2["loose_mean_change"] = round(float(diff.mean()), 3)
h2["loose_wilcoxon_p"] = float(f"{stats.wilcoxon(diff[diff != 0]).pvalue:.3g}") if (diff != 0).any() else None
for reg in ["verse", "prose"]:
    g = lo[lo.register == reg]
    h2[f"loose_{reg}_mean"] = g.groupby("arm").score.mean().round(3).to_dict()
# stimulus-level paired check: mean over samples, one value per stimulus
st = lo.groupby(["stimulus_id", "arm"]).score.mean().unstack().dropna()
dd = st["2_capping"] - st["1_observation"]
h2["loose_stimulus_level_t"] = {"n": int(len(dd)), "mean": round(float(dd.mean()), 3),
                                "p": float(f"{stats.ttest_1samp(dd, 0).pvalue:.3g}")}
out["H2_behavioural_frozen_criterion"] = h2

# ---------------------------------------------------------------- projection audits
def projection_audit(d, role_sd):
    """Checks the reports either omitted or misstated, for one arm's per-generation CSV."""
    d = codes(d.dropna(subset=["projection_published"]).copy())
    m = fit(d, "projection_published ~ t*r + C(domain)")
    a = {"reproduced_t": row(m, "t"), "reproduced_r": row(m, "r"), "reproduced_t_x_r": row(m, "t:r")}
    # conservative topic-level paired check named in the prereg (df = n_topics - 1)
    tm = d.groupby(["topic_id", "tightness"]).projection_published.mean().unstack()
    td = tm.tight - tm.loose
    a["topic_level_paired"] = {"n_topics": int(len(td)), "mean": round(float(td.mean()), 2),
                               "ci95": [round(float(x), 2) for x in stats.t.interval(.95, len(td) - 1, td.mean(), stats.sem(td))],
                               "p": float(f"{stats.ttest_1samp(td, 0).pvalue:.3g}")}
    # domain main effect: the "measurement works" check (null write-up, failure modes) -- compare Lu's 6-12
    dm = d.groupby("domain").projection_published.mean()
    a["domain_means"] = dm.round(2).to_dict()
    a["therapy_minus_coding"] = round(float(dm["therapy_like"] - dm["coding"]), 2)
    a["therapy_minus_coding_role_sd"] = round(float((dm["therapy_like"] - dm["coding"]) / role_sd), 3)
    a["n_response_tokens_by_cell"] = d.groupby("cell").n_response_tokens.mean().round(0).to_dict()
    a["share_hit_512_by_cell"] = (d.n_tokens_span >= 505).groupby(d.cell).mean().round(3).to_dict()
    dec = [f"tok_decile_{i}" for i in range(10)]
    a["decile_first_last_by_cell"] = {c: [round(float(x[dec[0]].mean()), 1), round(float(x[dec[-1]].mean()), 1)]
                                      for c, x in d.groupby("cell")}
    d["nt"] = (d.n_response_tokens - d.n_response_tokens.mean()) / 100
    a["length_covariate_t"] = row(fit(d, "projection_published ~ t*r + C(domain) + nt"), "t")
    # residual confound: second-person reference to the model (self_ref_count), imbalanced in prose
    d = d.merge(s[["id", "self_ref_count"]], left_on="stimulus_id", right_on="id")
    d["sr"] = d.self_ref_count - d.self_ref_count.mean()
    msr = fit(d, "projection_published ~ t*r + C(domain) + sr")
    a["self_ref_covariate_t"] = row(msr, "t")
    a["self_ref_covariate_t_x_r"] = row(msr, "t:r")
    a["self_ref_coef"] = row(msr, "sr")
    return a


out["H3_gemma_audit"] = projection_audit(pd.read_csv(P("results", "arm_3_gemma.csv")), 520.1)

# Arms 1-2 CSVs live on the analysis host (~/form-tightness/results/); run there to fill these in.
HOST = os.environ.get("FT_RESULTS", os.path.expanduser("~/form-tightness/results"))
a1p, a2p = os.path.join(HOST, "arm_1_observation.csv"), os.path.join(HOST, "arm_2_capping.csv")
if os.path.exists(a1p):
    a1 = pd.read_csv(a1p)
    out["H1_qwen_audit"] = projection_audit(a1, 14.65)
    if os.path.exists(a2p):
        a2 = pd.read_csv(a2p)
        b = codes(pd.concat([a1.assign(cap=-.5), a2.assign(cap=.5)], ignore_index=True)
                  .dropna(subset=["projection_published"]))
        b["cellarm"] = b.cell + "_" + b.cap.astype(str)
        # adds a stimulus x arm variance component the reported Arm 2 model omits
        m2 = smf.mixedlm("projection_published ~ t*r*cap + C(domain)", b, groups="topic_id",
                         vc_formula={"cell": "0+C(cell)", "cellarm": "0+C(cellarm)"}).fit(reml=True)
        out["H2_qwen_t_x_cap_with_stimulus_x_arm_vc"] = row(m2, "t:cap")
else:
    out["H1_qwen_audit"] = f"not run: {a1p} absent (Arm 1-2 per-generation CSVs are not in the repo)"

json.dump(out, open(P("results", "audit_checks.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
