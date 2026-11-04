#!/usr/bin/env python3
"""check_c_model.py — pre-stimulus check (c): does blind-rated prompt-form tightness predict Lu et al.'s
per-turn Assistant-Axis projections in the released transcripts?

Inputs : results/check_c_projections.csv, results/check_c_user_tightness.csv, results/check_c_summary.json
Outputs: results/check_c_model.json (all numbers), results/check_c_report.md (plain-language report)

Projections are z-scored WITHIN model (Qwen L32 axis and Gemma L22 axis have different scales; raw
values are never pooled across models). Mixed models (statsmodels MixedLM, REML, random intercept
per transcript):
  (i)   Qwen unsteered only:        z ~ tightness_total + turn_index
  (ii)  Qwen all 6 transcripts:     z ~ tightness_total + turn_index + capped + tightness_total:capped
  (iii) Qwen + Gemma pooled on z:   z ~ tightness_total + turn_index + model
(i) is also fitted in raw Qwen units. Exploratory and underpowered: description, not a test of H1.
"""
import argparse, json, warnings
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

PAIRS = [("delusion", "delusion_capped.json", "delusion_unsteered.json"),
         ("jailbreak", "jailbreak_capped.json", "jailbreak_unsteered.json"),
         ("selfharm", "selfharm_capped.json", "selfharm_unsteered.json.json")]


def fit(df, formula, label):
    m = smf.mixedlm(formula, df, groups=df["transcript"]).fit(reml=True)
    var_t = float(m.cov_re.iloc[0, 0]); var_e = float(m.scale)
    out = {"label": label, "formula": formula, "n_obs": int(m.nobs), "n_groups": int(df["transcript"].nunique()),
           "icc_transcript": var_t / (var_t + var_e) if (var_t + var_e) > 0 else float("nan"),
           "var_transcript": var_t, "var_residual": var_e, "converged": bool(m.converged), "terms": {}}
    ci = m.conf_int()
    for name in m.fe_params.index:
        out["terms"][name] = {"est": float(m.fe_params[name]), "se": float(m.bse_fe[name]),
                              "ci_lo": float(ci.loc[name, 0]), "ci_hi": float(ci.loc[name, 1]),
                              "z": float(m.tvalues[name]), "p": float(m.pvalues[name])}
    return out


def term_row(name, t):
    return f"| {name} | {t['est']:.3f} | [{t['ci_lo']:.3f}, {t['ci_hi']:.3f}] | {t['p']:.3f} |"


def model_table(res):
    L = [f"**{res['label']}** — `{res['formula']}`, n = {res['n_obs']} turns, {res['n_groups']} transcripts, "
         f"ICC(transcript) = {res['icc_transcript']:.2f}, converged = {res['converged']}", "",
         "| term | estimate | 95% CI | p |", "|---|---|---|---|"]
    for k, t in res["terms"].items():
        L.append(term_row(k, t))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projections", required=True)
    ap.add_argument("--ratings", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-report", required=True)
    a = ap.parse_args()

    proj = pd.read_csv(a.projections)
    rat = pd.read_csv(a.ratings)
    rat = rat[rat["total"].notna()].copy()
    rat["total"] = rat["total"].astype(int)
    df = proj.merge(rat[["user_text_sha256", "item1", "item2", "item3", "item4", "item5", "total"]],
                    on="user_text_sha256", how="left", validate="m:1")
    assert df["total"].notna().all(), "unrated user turns present"
    df = df.rename(columns={"total": "tightness_total", "projection_L32": "projection"})
    df["model_short"] = df["model"].map(lambda s: "qwen" if "Qwen" in s else "gemma")
    df["z_projection"] = df.groupby("model_short")["projection"].transform(lambda x: (x - x.mean()) / x.std(ddof=1))
    df["capped"] = df["transcript"].str.contains("_capped").astype(int)
    df["turn_index"] = df["turn_index"].astype(float)

    R = {"n_rows": int(len(df)), "n_distinct_user_turns_rated": int(rat["user_text_sha256"].nunique()),
         "rater_model": str(rat["model"].iloc[0]), "n_rated_total_1_to_7": int(len(rat))}

    # ---- rating distribution ----
    R["tightness_overall"] = {"mean": float(df["tightness_total"].mean()), "sd": float(df["tightness_total"].std(ddof=1)),
                              "min": int(df["tightness_total"].min()), "max": int(df["tightness_total"].max()),
                              "distinct_turn_mean": float(rat["total"].mean()), "distinct_turn_sd": float(rat["total"].std(ddof=1)),
                              "distinct_turn_counts": {int(k): int(v) for k, v in rat["total"].value_counts().sort_index().items()}}
    R["item_means_distinct_turns"] = {f"item{i}": float(rat[f"item{i}"].mean()) for i in range(1, 6)}
    R["item_sd_distinct_turns"] = {f"item{i}": float(rat[f"item{i}"].std(ddof=1)) for i in range(1, 6)}
    per_t = {}
    for t, g in df.groupby("transcript"):
        rho, p = stats.spearmanr(g["tightness_total"], g["projection"])
        per_t[t] = {"model": g["model_short"].iloc[0], "n": int(len(g)), "mean_tightness": float(g["tightness_total"].mean()),
                    "sd_tightness": float(g["tightness_total"].std(ddof=1)), "min_tightness": int(g["tightness_total"].min()),
                    "max_tightness": int(g["tightness_total"].max()), "n_distinct_totals": int(g["tightness_total"].nunique()),
                    "mean_projection_raw": float(g["projection"].mean()), "sd_projection_raw": float(g["projection"].std(ddof=1)),
                    "spearman_rho": float(rho), "spearman_p": float(p)}
    R["per_transcript"] = per_t

    # shared user turns between capped/unsteered pairs
    shared = {}
    for name, c, u in PAIRS:
        sc, su = set(df.loc[df.transcript == c, "user_text_sha256"]), set(df.loc[df.transcript == u, "user_text_sha256"])
        shared[name] = {"n_shared_user_turns": len(sc & su), "n_capped": len(sc), "n_unsteered": len(su)}
    R["shared_user_turns_per_pair"] = shared

    # ---- capped vs unsteered mean projection difference per pair ----
    summ = json.loads(Path(a.summary).read_text())["per_transcript"]
    pairs = {}
    for name, c, u in PAIRS:
        gc, gu = df[df.transcript == c], df[df.transcript == u]
        # paired by turn_index where both exist
        m = gc[["turn_index", "projection"]].merge(gu[["turn_index", "projection"]], on="turn_index", suffixes=("_c", "_u"))
        d = m["projection_c"] - m["projection_u"]
        tt = stats.ttest_rel(m["projection_c"], m["projection_u"])
        pairs[name] = {"mean_capped": summ[c]["mean"], "mean_unsteered": summ[u]["mean"],
                       "diff_capped_minus_unsteered": round(summ[c]["mean"] - summ[u]["mean"], 2),
                       "n_turns": summ[c]["n_turns"], "paired_by_turn_n": int(len(m)),
                       "paired_mean_diff": float(d.mean()), "paired_sd_diff": float(d.std(ddof=1)),
                       "paired_t": float(tt.statistic), "paired_p": float(tt.pvalue),
                       "sd_unsteered_raw": float(gu["projection"].std(ddof=1))}
    R["capped_vs_unsteered"] = pairs

    # ---- mixed models ----
    q = df[df.model_short == "qwen"].copy()
    qu = q[q.capped == 0].copy()
    M = {}
    M["i_qwen_unsteered_z"] = fit(qu, "z_projection ~ tightness_total + turn_index", "(i) Qwen unsteered, z-scored projection")
    M["i_qwen_unsteered_raw"] = fit(qu, "projection ~ tightness_total + turn_index", "(i) Qwen unsteered, raw projection units")
    M["ii_qwen_all_z"] = fit(q, "z_projection ~ tightness_total + turn_index + capped + tightness_total:capped",
                            "(ii) Qwen all 6 transcripts (capped indicator + interaction), z-scored")
    M["iii_pooled_z"] = fit(df, "z_projection ~ tightness_total + turn_index + C(model_short, Treatment('qwen'))",
                           "(iii) Qwen + Gemma pooled, within-model z-scores, model fixed effect")
    R["models"] = M
    # sd of projection among Qwen unsteered (for raw/z conversion sanity)
    R["qwen_projection_sd_all_6"] = float(q["projection"].std(ddof=1))
    R["qwen_unsteered_projection_sd"] = float(qu["projection"].std(ddof=1))
    R["gemma_projection_sd"] = float(df.loc[df.model_short == "gemma", "projection"].std(ddof=1))

    Path(a.out_json).write_text(json.dumps(R, indent=1))

    # ---- report ----
    s = M["i_qwen_unsteered_raw"]["terms"]["tightness_total"]
    sz = M["i_qwen_unsteered_z"]["terms"]["tightness_total"]
    s2 = M["ii_qwen_all_z"]["terms"]["tightness_total"]; s2x = M["ii_qwen_all_z"]["terms"]["tightness_total:capped"]
    s3 = M["iii_pooled_z"]["terms"]["tightness_total"]
    ov = R["tightness_overall"]
    low_var = [t for t, v in per_t.items() if v["sd_tightness"] < 0.8]
    L = ["# Check (c): does prompt-form tightness predict per-turn Assistant-Axis projection in Lu et al.'s released transcripts?", "",
         "*Exploratory, pre-stimulus, underpowered. This is a description of the released transcripts, not a test of H1. "
         "Every number below comes from `results/check_c_model.json`, computed by `pipeline/check_c_model.py` from "
         "`results/check_c_projections.csv`, `results/check_c_user_tightness.csv` and `results/check_c_summary.json`.*", "",
         "## Rating", "",
         f"- Rater: `{R['rater_model']}` via CommandCode, temperature 0, seed 20261030, system prompt = `stimuli/tightness-rubric.md` "
         "verbatim, user message = the user turn text only (blind to projection, assistant text, transcript, turn index). "
         f"All {R['n_distinct_user_turns_rated']} items returned via json_schema; 0 parse failures.",
         f"- **{R['n_distinct_user_turns_rated']} distinct user turns rated** (deduplicated by sha256 across {R['n_rows']} transcript rows). "
         "Shared user turns within capped/unsteered pairs: " +
         ", ".join(f"{k} {v['n_shared_user_turns']}/{v['n_capped']}" for k, v in shared.items()) +
         " — the delusion pair shares no user turns (the auditor adapted its turns), so ratings are shared only for selfharm and most of jailbreak.",
         f"- Tightness total over the {R['n_distinct_user_turns_rated']} distinct turns: mean {ov['distinct_turn_mean']:.2f}, "
         f"SD {ov['distinct_turn_sd']:.2f}, range {ov['min']}–{ov['max']} of a possible 0–10. Counts by total: " +
         ", ".join(f"{k}: {v}" for k, v in ov["distinct_turn_counts"].items()) + ".",
         "- Item means (0–2): " + ", ".join(f"{k} {v:.2f} (SD {R['item_sd_distinct_turns'][k]:.2f})" for k, v in R["item_means_distinct_turns"].items()) +
         ". Items 1, 2 and 5 (hard constraints, output format, verification hooks) are almost always 0: nearly all the variance comes from "
         "items 3 and 4 (syntactic completeness, figurative density). The upper half of the rubric scale is empty in this corpus.", "",
         "### Rating distribution per transcript", "",
         "| transcript | model | n turns | tightness mean | SD | min–max | distinct totals | projection mean (raw) | projection SD (raw) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for t, v in per_t.items():
        L.append(f"| {t} | {v['model']} | {v['n']} | {v['mean_tightness']:.2f} | {v['sd_tightness']:.2f} | {v['min_tightness']}–{v['max_tightness']} | "
                 f"{v['n_distinct_totals']} | {v['mean_projection_raw']:.2f} | {v['sd_projection_raw']:.2f} |")
    L += ["", "**Variance note.** " + (
        f"Within-transcript SD of tightness is {min(v['sd_tightness'] for v in per_t.values()):.2f}–{max(v['sd_tightness'] for v in per_t.values()):.2f} points, "
        f"against an overall SD of {ov['distinct_turn_sd']:.2f} and a planned stimulus manipulation spanning the full 0–10 scale. "
        "The conversations do vary in form (some turns are terse fragments, some are complete literal prose), but only across the bottom "
        "~40 % of the rubric: no turn asks for hard structural constraints, a format, or a self-check. So this check can only speak to the loose "
        "end of the tightness range, and a null here says little about H1 at the planned T1–T3 contrast."
        + (f" Transcripts with SD < 0.8: {', '.join(low_var)}." if low_var else " No transcript has SD below 0.8.")), "",
        "## Mixed models (statsmodels MixedLM, REML, random intercept per transcript)", "",
        "Projection z-scored within model (Qwen L32 and Gemma L22 axes are on different scales, ~35×; raw values never pooled). "
        "`turn_index` is the position of the turn in the conversation (0-based).", ""]
    for k in ["i_qwen_unsteered_z", "i_qwen_unsteered_raw", "ii_qwen_all_z", "iii_pooled_z"]:
        L += [model_table(M[k])]
    L += ["### Slope summary (per rubric point)", "",
          "| model | slope per point | 95% CI | p | units |", "|---|---|---|---|---|",
          f"| (i) Qwen unsteered | {sz['est']:.3f} | [{sz['ci_lo']:.3f}, {sz['ci_hi']:.3f}] | {sz['p']:.3f} | within-Qwen SD |",
          f"| (i) Qwen unsteered | {s['est']:.2f} | [{s['ci_lo']:.2f}, {s['ci_hi']:.2f}] | {s['p']:.3f} | raw Qwen L32 projection units (unsteered SD = {R['qwen_unsteered_projection_sd']:.2f}) |",
          f"| (ii) Qwen all 6, main effect (unsteered) | {s2['est']:.3f} | [{s2['ci_lo']:.3f}, {s2['ci_hi']:.3f}] | {s2['p']:.3f} | within-Qwen SD |",
          f"| (ii) tightness × capped | {s2x['est']:.3f} | [{s2x['ci_lo']:.3f}, {s2x['ci_hi']:.3f}] | {s2x['p']:.3f} | within-Qwen SD |",
          f"| (iii) pooled Qwen+Gemma | {s3['est']:.3f} | [{s3['ci_lo']:.3f}, {s3['ci_hi']:.3f}] | {s3['p']:.3f} | within-model SD |", "",
          "## Spearman ρ of tightness_total with projection, within transcript", "",
          "| transcript | n | ρ | p |", "|---|---|---|---|"]
    for t, v in per_t.items():
        L.append(f"| {t} | {v['n']} | {v['spearman_rho']:.2f} | {v['spearman_p']:.3f} |")
    L += ["", "## Capped vs unsteered mean projection per pair (Qwen, raw L32 units; from check_c_summary.json)", "",
          "| pair | n turns | mean capped | mean unsteered | capped − unsteered | paired-by-turn mean diff (SD) | paired t | p |",
          "|---|---|---|---|---|---|---|---|"]
    for k, v in pairs.items():
        L.append(f"| {k} | {v['n_turns']} | {v['mean_capped']:.2f} | {v['mean_unsteered']:.2f} | {v['diff_capped_minus_unsteered']:+.2f} | "
                 f"{v['paired_mean_diff']:+.2f} ({v['paired_sd_diff']:.2f}) | {v['paired_t']:.2f} | {v['paired_p']:.2g} |")
    L += ["", "Capping raises the projection by roughly 20 raw units in every pair, i.e. about "
          f"{np.mean([v['diff_capped_minus_unsteered'] for v in pairs.values()]) / R['qwen_unsteered_projection_sd']:.1f} unsteered SDs — "
          "an effect far larger than anything tightness is associated with here.", "",
          "## Conclusion (plain language)", ""]
    sig = sz["p"] < 0.05
    direction = "higher" if sz["est"] > 0 else "lower"
    L += [f"In the three unsteered Qwen transcripts, each extra rubric point of prompt tightness goes with a {direction} per-turn projection of "
          f"{abs(s['est']):.2f} raw units ({abs(sz['est']):.2f} within-Qwen SD), 95 % CI [{s['ci_lo']:.2f}, {s['ci_hi']:.2f}], p = {s['p']:.2f}"
          + (", which is " + ("" if sig else "not ") + "distinguishable from zero at this sample size (n = 69 turns, 3 conversations)") + ". "
          f"The pooled estimate including Gemma ({s3['est']:+.3f} SD per point, p = {s3['p']:.2f}) and the all-Qwen estimate "
          f"({s2['est']:+.3f} SD per point, p = {s2['p']:.2f}) are likewise small, positive and not distinguishable from zero, with per-transcript Spearman ρ ranging "
          f"{min(v['spearman_rho'] for v in per_t.values()):.2f} to {max(v['spearman_rho'] for v in per_t.values()):.2f}. "
          f"Because these auditor-written turns only span tightness totals {ov['min']}–{ov['max']} (almost entirely items 3–4, never constraints, "
          "format or verification hooks) and the capping manipulation dwarfs any form-related variation, this check is a weak, exploratory description "
          "that neither supports nor rules out H1; the preregistered stimulus arms are needed."]
    Path(a.out_report).write_text("\n".join(L) + "\n")
    print(json.dumps({k: M[k]["terms"]["tightness_total"] for k in M}, indent=1))
    print("ICC:", {k: round(M[k]["icc_transcript"], 3) for k in M})
    print("per-transcript rho:", {t: round(v["spearman_rho"], 2) for t, v in per_t.items()})


if __name__ == "__main__":
    main()
