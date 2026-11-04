#!/usr/bin/env python3
"""Monte-Carlo power for the form-tightness study (Arm 1 primary contrast + TOST).

Design simulated: n_topics topics x 3 tightness levels (T1 loose, T2 structured,
T3 tight) x n_samples generations per stimulus. Outcome = projection on the
unit-normalised Assistant Axis (arbitrary units; reference role-SD = 14.65).

Generative model
    y[t, l, s] = mu_l + u_t + v_{t,l} + e[t,l,s]
    u_t      ~ N(0, topic_sd^2)          (1|topic)
    v_{t,l}  ~ N(0, topic_level_sd^2)    (1|topic:level)
    e        ~ N(0, resid_sd^2)          per-sample residual

Analysis simulated
    The preregistered model is a linear mixed model (lme4 / statsmodels
    MixedLM). statsmodels is not installed on the drafting machine, so this
    script analyses each simulated dataset with the equivalent *topic-level
    paired contrast*: average the n_samples generations within each
    topic x level cell, form d_t = mean(T1_t) - mean(T3_t) for each topic,
    and run a one-sample t-test on d_t (n = n_topics). This is the exact
    analysis of the T1-T3 contrast under the stated random-effects structure
    (the topic intercept cancels in the difference; the topic:level term and
    the residual both enter the variance of d_t), and it is conservative
    relative to the mixed model because it does not borrow strength from T2.
    If `--use-statsmodels` is given and statsmodels is importable, the mixed
    model is fitted instead (slower).

Outputs
    Power for (i) directional H1 test T1 < T3 at alpha = .05 one-sided,
    (ii) two-sided test at alpha = .05, (iii) TOST equivalence with bounds
    [-sesoi, +sesoi] (two one-sided tests at alpha = .05, i.e. 90 % CI inside
    the bounds), each at a grid of true T1-T3 effects.

Usage
    python3 pipeline/power.py                       # defaults, prints table
    python3 pipeline/power.py --resid-sd 10 --topic-sd 5 --n-topics 96
    python3 pipeline/power.py --markdown > prereg/power-table.md
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
from scipy import stats


def simulate_once(rng, n_topics, n_samples, effect, resid_sd, topic_sd,
                  topic_level_sd, t2_frac=0.5):
    """Return array shape (n_topics, 3, n_samples). Level order T1, T2, T3.

    effect = mu_T1 - mu_T3 (negative under H1: loose is lower). T2 sits at
    t2_frac of the way from T3 to T1; it is not used by the primary contrast.
    """
    mu = np.array([effect, t2_frac * effect, 0.0])
    u = rng.normal(0.0, topic_sd, size=(n_topics, 1, 1))
    v = rng.normal(0.0, topic_level_sd, size=(n_topics, 3, 1))
    e = rng.normal(0.0, resid_sd, size=(n_topics, 3, n_samples))
    return mu[None, :, None] + u + v + e


def paired_contrast(y):
    """Topic-level paired T1 - T3 contrast. Returns (estimate, se, df)."""
    cell = y.mean(axis=2)                 # (n_topics, 3)
    d = cell[:, 0] - cell[:, 2]
    n = d.shape[0]
    est = d.mean()
    se = d.std(ddof=1) / np.sqrt(n)
    return est, se, n - 1


def mixed_model_contrast(y):
    """Fit projection ~ level + (1|topic) + (1|topic:level) with statsmodels.

    Returns (estimate, se, df_approx) for the T1 - T3 contrast (T3 reference).
    """
    import pandas as pd  # noqa: WPS433  (only imported on request)
    import statsmodels.formula.api as smf

    n_topics, _, n_samples = y.shape
    rows = []
    for t in range(n_topics):
        for l, name in enumerate(("T1", "T2", "T3")):
            for s in range(n_samples):
                rows.append((t, name, y[t, l, s]))
    df = pd.DataFrame(rows, columns=["topic", "level", "proj"])
    df["level"] = pd.Categorical(df["level"], categories=["T3", "T1", "T2"])
    m = smf.mixedlm("proj ~ level", df, groups=df["topic"],
                    re_formula="1", vc_formula={"tl": "0 + C(level)"})
    r = m.fit(reml=True)
    est = r.params["level[T.T1]"]
    se = r.bse["level[T.T1]"]
    return est, se, n_topics - 1


def decide(est, se, df, sesoi, alpha=0.05):
    """Return (reject_one_sided_H1, reject_two_sided, tost_equivalent)."""
    t = est / se
    p_one = stats.t.cdf(t, df)                     # H1: est < 0
    p_two = 2 * stats.t.sf(abs(t), df)
    # TOST: both one-sided tests must reject at alpha.
    p_lower = stats.t.sf((est + sesoi) / se, df)   # H0: est <= -sesoi
    p_upper = stats.t.cdf((est - sesoi) / se, df)  # H0: est >= +sesoi
    tost = (p_lower < alpha) and (p_upper < alpha)
    return p_one < alpha, p_two < alpha, tost


def run(args):
    rng = np.random.default_rng(args.seed)
    effects = [0.0, -1.0, -2.0, -3.0, -4.0, -6.0]
    analyse = paired_contrast
    method = "topic-level paired contrast (conservative; statsmodels absent)"
    if args.use_statsmodels:
        try:
            import statsmodels  # noqa: F401
            analyse = mixed_model_contrast
            method = "statsmodels MixedLM"
        except ImportError:
            print("statsmodels not importable; falling back to paired contrast",
                  file=sys.stderr)

    rows = []
    for eff in effects:
        hits = np.zeros(3)
        for _ in range(args.n_sims):
            y = simulate_once(rng, args.n_topics, args.n_samples, eff,
                              args.resid_sd, args.topic_sd, args.topic_level_sd)
            est, se, df = analyse(y)
            hits += np.array(decide(est, se, df, args.sesoi), dtype=float)
        rows.append((eff, *(hits / args.n_sims)))

    # Analytic check for the paired design: Var(d_t) = 2*(tl_sd^2 + resid_sd^2/n_samples)
    sd_d = np.sqrt(2 * (args.topic_level_sd ** 2 + args.resid_sd ** 2 / args.n_samples))
    se_d = sd_d / np.sqrt(args.n_topics)

    hdr = (f"Monte-Carlo power, {args.n_sims} sims, seed {args.seed}\n"
           f"n_topics={args.n_topics}, n_samples={args.n_samples}, "
           f"resid_sd={args.resid_sd}, topic_sd={args.topic_sd}, "
           f"topic_level_sd={args.topic_level_sd}, SESOI=±{args.sesoi}\n"
           f"analysis: {method}\n"
           f"analytic SE of the T1-T3 contrast: {se_d:.3f} "
           f"(SD of per-topic difference {sd_d:.3f})")
    if args.markdown:
        print(hdr.replace("\n", "  \n"))
        print()
        print("| true T1−T3 (units) | power H1 one-sided (T1<T3), α=.05 | power two-sided, α=.05 | P(TOST declares equivalence, bounds ±3) |")
        print("|---|---|---|---|")
        for eff, p1, p2, pt in rows:
            print(f"| {eff:+.0f} | {p1:.3f} | {p2:.3f} | {pt:.3f} |")
    else:
        print(hdr)
        print(f"{'effect':>8} {'H1 1-sided':>11} {'2-sided':>9} {'TOST equiv':>11}")
        for eff, p1, p2, pt in rows:
            print(f"{eff:>+8.1f} {p1:>11.3f} {p2:>9.3f} {pt:>11.3f}")
    print()
    print("Reading: row 0 = Type I error (tests) and TOST power (equivalence) "
          "under exact null; row −3 = power at the SESOI (tests) and TOST "
          "error rate at the bound (should be ≤ .05).")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--resid-sd", type=float, default=8.0)
    p.add_argument("--topic-sd", type=float, default=5.0)
    p.add_argument("--topic-level-sd", type=float, default=2.0,
                   help="SD of the (1|topic:level) term; default 2")
    p.add_argument("--n-topics", type=int, default=96)
    p.add_argument("--n-samples", type=int, default=3)
    p.add_argument("--n-sims", type=int, default=2000)
    p.add_argument("--sesoi", type=float, default=3.0)
    p.add_argument("--seed", type=int, default=20261030)
    p.add_argument("--use-statsmodels", action="store_true")
    p.add_argument("--markdown", action="store_true")
    run(p.parse_args())


if __name__ == "__main__":
    main()
