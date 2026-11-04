"""summarize_check_c.py — per-transcript summary of results/check_c_projections.csv (no GPU)."""
import csv, collections, json, os, sys
p = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/form-tightness/results/check_c_projections.csv")
rows = list(csv.DictReader(open(p)))
g = collections.defaultdict(list)
for r in rows:
    g[r["transcript"]].append(r)
out = {}
for k, v in g.items():
    pr = [float(r["projection_L32"]) for r in v]
    out[k] = {"model": v[0]["model"], "layer": int(v[0]["layer"]), "n_turns": len(v), "mean": round(sum(pr) / len(pr), 2),
              "min": round(min(pr), 2), "max": round(max(pr), 2), "first": round(pr[0], 2), "last": round(pr[-1], 2),
              "truncated_turns": sum(r["truncated"] == "True" for r in v), "backends": sorted({r["backend"] for r in v}),
              "mean_n_response_tokens": round(sum(int(r["n_response_tokens"]) for r in v) / len(v), 1)}
print(json.dumps({"n_rows": len(rows), "columns": list(rows[0].keys()), "per_transcript": out}, indent=1))
