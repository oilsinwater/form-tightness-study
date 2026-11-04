#!/usr/bin/env python3
"""Track B: v2 attribution pre-coding (two independent LLM coders) + reliability + confound report.

Usage
  python code_v2_attribution.py code    --stimuli stimuli.jsonl --scheme coding-scheme.md --out v2_attribution_coding.csv [--coder 1|2|both]
  python code_v2_attribution.py analyze --stimuli stimuli.jsonl --coding v2_attribution_coding.csv --report v2_attribution_report.md

Coders are blind: they receive the scheme text (worked-example ids withheld) as system prompt and the prompt text
only, in a shuffled order (seed 20261030). Provider: CommandCode (OpenAI-compatible), COMMANDCODE_API_KEY from env or ~/.hermes/.env.
Krippendorff's alpha (nominal, ordinal) is implemented below in numpy; no external package.
"""
import argparse, csv, json, os, random, re, sys, time
from collections import Counter, defaultdict

SEED = 20261030
CODERS = {1: "deepseek/deepseek-v4.1-flash", 2: "deepseek/deepseek-v4-pro"}
BASE_URL = "https://api.commandcode.ai/provider/v1"
ADDRESS_LEVELS = ["none", "vocative", "ratified"]
MOTIFS = ["double", "return/water", "separation", "exclusion", "silence", "passage", "gaze", "none"]
ID_RE = re.compile(r"`?(coding|writing|therapy_like|philosophy_of_ai)_\d\d_(loose|tight)_(verse|prose)`?")

OUTPUT_INSTR = """
## Output

Return ONLY a JSON object (no prose, no code fence) with exactly these keys:
{"address": "none"|"vocative"|"ratified",
 "attrib_count": integer,
 "attrib_phrases": [list of the counted phrases, quoted from the text],
 "self_ref_count": integer,
 "user_first_person": 0|1,
 "motifs": [subset of "double","return/water","separation","exclusion","silence","passage","gaze","none"],
 "motif_evidence": {tag: short quote}}
"""


def load_key():
    k = os.environ.get("COMMANDCODE_API_KEY")
    if k:
        return k
    p = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line.startswith("COMMANDCODE_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("COMMANDCODE_API_KEY not found")


def load_stimuli(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def scheme_for_llm(path):
    txt = open(path, encoding="utf-8").read()
    txt = txt.split("## Reliability")[0]
    txt = ID_RE.sub("[id withheld]", txt)
    return txt + OUTPUT_INSTR


def parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0) if m else text)


def normalise(obj):
    addr = str(obj.get("address", "")).strip().lower()
    if addr not in ADDRESS_LEVELS:
        addr = "none" if addr in ("", "null") else addr
    mot = obj.get("motifs", [])
    if isinstance(mot, str):
        mot = [mot]
    mot = sorted({str(m).strip().lower() for m in mot if str(m).strip().lower() in MOTIFS})
    if len(mot) > 1 and "none" in mot:
        mot.remove("none")
    if not mot:
        mot = ["none"]
    return {
        "address": addr,
        "attrib_count": int(obj.get("attrib_count", 0) or 0),
        "self_ref_count": int(obj.get("self_ref_count", 0) or 0),
        "user_first_person": 1 if int(obj.get("user_first_person", 0) or 0) else 0,
        "motifs": "|".join(mot),
    }


def code_one(client, model, system, prompt, retries=4):
    last = None
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=model, temperature=0, max_tokens=16384,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": "PROMPT TO CODE:\n\n" + prompt}],
                response_format={"type": "json_object"},
            )
            msg = r.choices[0].message
            content = msg.content or ""
            if not content.strip():
                # reasoning may have exhausted the budget; try the reasoning text for a JSON object
                content = getattr(msg, "reasoning_content", None) or (msg.model_extra or {}).get("reasoning_content", "") or ""
            obj = parse_json(content)
            return obj, content
        except Exception as e:  # noqa
            last = e
            time.sleep(3 * (attempt + 1))
    return None, f"ERROR: {last!r}"


def cmd_code(a):
    from openai import OpenAI
    client = OpenAI(api_key=load_key(), base_url=BASE_URL)
    rows = load_stimuli(a.stimuli)
    system = scheme_for_llm(a.scheme)
    order = list(range(len(rows)))
    random.Random(SEED).shuffle(order)
    done = set()
    if os.path.exists(a.out):
        with open(a.out, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                done.add((r["id"], int(r["coder"])))
    coders = [1, 2] if a.coder == "both" else [int(a.coder)]
    new = not os.path.exists(a.out)
    with open(a.out, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["id", "coder", "address", "attrib_count", "self_ref_count", "user_first_person", "motifs", "raw_json"])
        from concurrent.futures import ThreadPoolExecutor
        for c in coders:
            model = CODERS[c]
            todo = [rows[idx] for idx in order if (rows[idx]["id"], c) not in done]
            n = 0
            with ThreadPoolExecutor(max_workers=a.workers) as ex:
                futs = [(row, ex.submit(code_one, client, model, system, row["prompt"])) for row in todo]
                for row, fut in futs:
                    obj, raw = fut.result()
                    if obj is None:
                        print(f"coder{c} {row['id']} FAILED {raw}", flush=True)
                        continue
                    nm = normalise(obj)
                    w.writerow([row["id"], c, nm["address"], nm["attrib_count"], nm["self_ref_count"],
                                nm["user_first_person"], nm["motifs"], json.dumps(obj, ensure_ascii=False)])
                    f.flush()
                    n += 1
                    if n % 20 == 0:
                        print(f"coder{c} {n} done", flush=True)
            print(f"coder{c} finished, {n} new rows", flush=True)


# ---------- Krippendorff's alpha (2+ coders, missing allowed) ----------
def krippendorff_alpha(units, level="nominal"):
    """units: list of lists of values (one list per unit, one value per coder, None = missing)."""
    import numpy as np
    vals = sorted({v for u in units for v in u if v is not None})
    if level == "ordinal":
        vals = sorted(vals)
    idx = {v: i for i, v in enumerate(vals)}
    K = len(vals)
    o = np.zeros((K, K))
    for u in units:
        vs = [v for v in u if v is not None]
        m = len(vs)
        if m < 2:
            continue
        for i in range(m):
            for j in range(m):
                if i != j:
                    o[idx[vs[i]], idx[vs[j]]] += 1.0 / (m - 1)
    n_c = o.sum(axis=1)
    n = n_c.sum()
    if n <= 1 or K < 2:
        return float("nan")
    d = np.zeros((K, K))
    for c in range(K):
        for k in range(K):
            if c == k:
                continue
            if level == "nominal":
                d[c, k] = 1.0
            elif level == "ordinal":
                lo, hi = min(c, k), max(c, k)
                d[c, k] = (n_c[lo:hi + 1].sum() - (n_c[lo] + n_c[hi]) / 2.0) ** 2
            elif level == "interval":
                d[c, k] = (vals[c] - vals[k]) ** 2
    Do = (o * d).sum()
    De = (np.outer(n_c, n_c) * d).sum() / (n - 1)
    if De == 0:
        return 1.0 if Do == 0 else float("nan")
    return float(1 - Do / De)


def cramers_v(table):
    import numpy as np
    t = np.asarray(table, dtype=float)
    n = t.sum()
    exp = np.outer(t.sum(1), t.sum(0)) / n
    mask = exp > 0
    chi2 = ((t[mask] - exp[mask]) ** 2 / exp[mask]).sum()
    k = min(t.shape) - 1
    return float(np.sqrt(chi2 / (n * k))) if k > 0 else float("nan"), float(chi2)


def cmd_analyze(a):
    import numpy as np
    rows = load_stimuli(a.stimuli)
    meta = {r["id"]: r for r in rows}
    coded = defaultdict(dict)
    with open(a.coding, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            coded[r["id"]][int(r["coder"])] = r
    ids = [r["id"] for r in rows]
    both = [i for i in ids if 1 in coded[i] and 2 in coded[i]]
    L = []
    L.append("# v2 attribution coding — LLM pre-code report (track B)\n")
    L.append(f"Generated by `code_v2_attribution.py analyze`. Items: {len(ids)}; coded by coder 1 ({CODERS[1]}): "
             f"{sum(1 for i in ids if 1 in coded[i])}; by coder 2 ({CODERS[2]}): {sum(1 for i in ids if 2 in coded[i])}; "
             f"by both: {len(both)}. Temperature 0, JSON output, scheme file as system prompt, shuffled order seed {SEED}, no cell labels or ids shown.\n")
    L.append("**All α values below are LLM pre-code statistics (two LLM coders).** Human-coder α: `[BLANK]` (see §7).\n")

    # ---- reliability
    L.append("## 1. Reliability between the two LLM pre-coders (Krippendorff's α)\n")
    L.append("| variable | level | α (LLM pre-code) | raw agreement | n |\n|---|---|---|---|---|")
    alpha = {}
    def units_for(key, cast):
        return [[cast(coded[i][1][key]), cast(coded[i][2][key])] for i in both]
    for key, level, cast in [("address", "nominal", str), ("attrib_count", "ordinal", int),
                             ("self_ref_count", "ordinal", int), ("user_first_person", "nominal", int)]:
        u = units_for(key, cast)
        al = krippendorff_alpha(u, level)
        agr = np.mean([x[0] == x[1] for x in u])
        alpha[key] = al
        L.append(f"| {key} | {level} | {al:.3f} | {agr:.3f} | {len(u)} |")
    for m in MOTIFS:
        u = [[int(m in coded[i][1]["motifs"].split("|")), int(m in coded[i][2]["motifs"].split("|"))] for i in both]
        al = krippendorff_alpha(u, "nominal")
        agr = np.mean([x[0] == x[1] for x in u])
        prev = np.mean([x[0] or x[1] for x in u])
        alpha["motif_" + m] = al
        L.append(f"| motif:{m} | nominal (present/absent) | {al:.3f} | {agr:.3f} (either coder: {prev:.2f}) | {len(u)} |")
    L.append("\nα for the ADDRESS confusion between coders:\n")
    ct = Counter((coded[i][1]["address"], coded[i][2]["address"]) for i in both)
    L.append("| coder1 \\ coder2 | " + " | ".join(ADDRESS_LEVELS) + " |\n|---|" + "---|" * len(ADDRESS_LEVELS))
    for x in ADDRESS_LEVELS:
        L.append(f"| {x} | " + " | ".join(str(ct[(x, y)]) for y in ADDRESS_LEVELS) + " |")

    # ---- adjudication
    adj = {}
    flagged = []
    for i in ids:
        c1 = coded[i].get(1); c2 = coded[i].get(2)
        if c1 and c2:
            disagree = (c1["address"] != c2["address"]) or (int(c1["attrib_count"]) != int(c2["attrib_count"])) \
                or (set(c1["motifs"].split("|")) != set(c2["motifs"].split("|")))
            src = c1
            flag = disagree
        else:
            src = c1 or c2
            flag = True
        if src is None:
            continue
        adj[i] = {"address": src["address"], "attrib_count": int(src["attrib_count"]),
                  "self_ref_count": int(src["self_ref_count"]), "user_first_person": int(src["user_first_person"]),
                  "motifs": src["motifs"], "flag": int(flag),
                  "address_agree": int(bool(c1 and c2 and c1["address"] == c2["address"]))}
        if flag:
            flagged.append(i)
    adj_path = os.path.join(os.path.dirname(os.path.abspath(a.report)), "v2_attribution_adjudicated.csv")
    with open(adj_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "cell", "register", "tightness", "domain", "address", "attrib_count", "self_ref_count",
                    "user_first_person", "motifs", "flag_disagreement", "address_agree"])
        for i in ids:
            if i in adj:
                m = meta[i]; d = adj[i]
                w.writerow([i, m["cell"], m["register"], m["tightness"], m["domain"], d["address"], d["attrib_count"],
                            d["self_ref_count"], d["user_first_person"], d["motifs"], d["flag"], d["address_agree"]])
    n_addr_dis = sum(1 for i in both if coded[i][1]["address"] != coded[i][2]["address"])
    L.append(f"\n## 2. Adjudicated labels\n\nRule: coder agreement → label; disagreement on ADDRESS, ATTRIB_COUNT or motif set → flagged "
             f"(`flag_disagreement=1`) and coder 1's value used provisionally. Flagged items: {len(flagged)} of {len(adj)} "
             f"({n_addr_dis} disagree on ADDRESS). File: `v2_attribution_adjudicated.csv`. Flagged items are the first "
             f"candidates for human adjudication.\n")

    # ---- confound table
    cells = ["loose_verse", "tight_verse", "loose_prose", "tight_prose"]
    L.append("## 3. Address and attribution by cell (adjudicated labels)\n")
    L.append("| cell | n | address ≠ none | vocative | ratified | mean ATTRIB_COUNT (sd) | mean SELF_REF_COUNT | user first person |\n|---|---|---|---|---|---|---|---|")
    by_cell = {}
    for c in cells:
        ii = [i for i in ids if meta[i]["cell"] == c and i in adj]
        ac = np.array([adj[i]["attrib_count"] for i in ii], float)
        sr = np.array([adj[i]["self_ref_count"] for i in ii], float)
        anyaddr = np.mean([adj[i]["address"] != "none" for i in ii])
        voc = np.mean([adj[i]["address"] == "vocative" for i in ii])
        rat = np.mean([adj[i]["address"] == "ratified" for i in ii])
        ufp = np.mean([adj[i]["user_first_person"] for i in ii])
        by_cell[c] = {"n": len(ii), "p_address_not_none": round(float(anyaddr), 3), "p_vocative": round(float(voc), 3),
                      "p_ratified": round(float(rat), 3), "mean_attrib_count": round(float(ac.mean()), 3),
                      "mean_self_ref_count": round(float(sr.mean()), 3), "p_user_first_person": round(float(ufp), 3)}
        L.append(f"| {c} | {len(ii)} | {anyaddr:.3f} | {voc:.3f} | {rat:.3f} | {ac.mean():.2f} ({ac.std(ddof=1):.2f}) | {sr.mean():.2f} | {ufp:.2f} |")
    # register x address
    tab = [[sum(1 for i in adj if meta[i]["register"] == reg and adj[i]["address"] == lv) for lv in ADDRESS_LEVELS]
           for reg in ["verse", "prose"]]
    V, chi2 = cramers_v(tab)
    tab2 = [[sum(1 for i in adj if meta[i]["register"] == reg and (adj[i]["address"] != "none") == b) for b in [False, True]]
            for reg in ["verse", "prose"]]
    phi, chi2b = cramers_v(tab2)
    p_verse = np.mean([adj[i]["address"] != "none" for i in adj if meta[i]["register"] == "verse"])
    p_prose = np.mean([adj[i]["address"] != "none" for i in adj if meta[i]["register"] == "prose"])
    ac_v = np.mean([adj[i]["attrib_count"] for i in adj if meta[i]["register"] == "verse"])
    ac_p = np.mean([adj[i]["attrib_count"] for i in adj if meta[i]["register"] == "prose"])
    tabT = [[sum(1 for i in adj if meta[i]["tightness"] == t and adj[i]["address"] == lv) for lv in ADDRESS_LEVELS]
            for t in ["loose", "tight"]]
    VT, _ = cramers_v(tabT)
    L.append("\n### Register × ADDRESS\n")
    L.append("| register | none | vocative | ratified |\n|---|---|---|---|")
    for reg, r in zip(["verse", "prose"], tab):
        L.append(f"| {reg} | {r[0]} | {r[1]} | {r[2]} |")
    L.append(f"\nCramér's V (register × ADDRESS, 3 levels) = **{V:.3f}** (χ² = {chi2:.1f}, df = 2, n = {len(adj)}). "
             f"φ (register × any-address, 2 × 2) = **{phi:.3f}** (χ² = {chi2b:.1f}). "
             f"For comparison, tightness × ADDRESS: V = {VT:.3f}.\n")
    # correlations with log_ppl and tokens
    acs = np.array([adj[i]["attrib_count"] for i in adj], float)
    lp = np.array([meta[i]["log_ppl"] for i in adj], float)
    tk = np.array([meta[i]["tokens"] for i in adj], float)
    L.append(f"r(ATTRIB_COUNT, log_ppl) = {np.corrcoef(acs, lp)[0,1]:.3f}; r(ATTRIB_COUNT, tokens) = {np.corrcoef(acs, tk)[0,1]:.3f}.\n")

    # ---- motif frequency by cell
    L.append("## 4. Motif-tag frequency by cell (proportion of items carrying the tag, adjudicated labels)\n")
    L.append("| tag | " + " | ".join(cells) + " | all |\n|---|" + "---|" * (len(cells) + 1))
    motif_by_cell = {}
    for m in MOTIFS:
        vals = []
        for c in cells:
            ii = [i for i in ids if meta[i]["cell"] == c and i in adj]
            vals.append(np.mean([m in adj[i]["motifs"].split("|") for i in ii]))
        allv = np.mean([m in adj[i]["motifs"].split("|") for i in adj])
        motif_by_cell[m] = {c: round(float(v), 3) for c, v in zip(cells, vals)}
        L.append(f"| {m} | " + " | ".join(f"{v:.2f}" for v in vals) + f" | {allv:.2f} |")
    L.append("\nMean number of non-`none` motif tags per item by cell: " + "; ".join(
        f"{c} = {np.mean([len([t for t in adj[i]['motifs'].split('|') if t != 'none']) for i in ids if meta[i]['cell'] == c and i in adj]):.2f}"
        for c in cells) + ".\n")

    # ---- plain statement
    L.append("## 5. Confound statement\n")
    L.append(f"**{100*p_verse:.1f} % of verse items carry vocative or ratified address vs {100*p_prose:.1f} % of prose items** "
             f"(mean ATTRIB_COUNT {ac_v:.2f} vs {ac_p:.2f}); register and attribution are confounded with **V = {V:.3f}** "
             f"(φ = {phi:.3f} for any-address). In the parent study the register effect must be read as "
             f"register-plus-attribution unless the covariate model `projection ~ tightness × register + attrib_count + domain + (1|topic)` "
             f"separates them; the decomposition is pre-specified here. Because almost every verse item names the model and almost no prose "
             f"item does, `attrib_count` and `register` are nearly collinear; the covariate model can only separate them through "
             f"within-register variation in ATTRIB_COUNT (verse items range from 0 to {max(adj[i]['attrib_count'] for i in adj if meta[i]['register']=='verse')}), "
             f"so the planned follow-up (address manipulated at fixed register, PLAN.md §1) is the real test. "
             f"Tightness is not confounded with address (V = {VT:.3f}).\n")
    L.append("These numbers come from LLM pre-codes; they are to be replaced by the human-adjudicated labels once the 60-item subset is coded and α is known.\n")

    # ---- top 10
    L.append("## 6. Ten items with the highest ATTRIB_COUNT (adjudicated; ties broken by coder-2 count, then id)\n")
    L.append("| id | cell | attrib_count (c1 / c2) | address (c1 / c2) | phrases (coder 1) |\n|---|---|---|---|---|")
    def c2count(i):
        return int(coded[i][2]["attrib_count"]) if 2 in coded[i] else -1
    top = sorted(adj, key=lambda i: (-adj[i]["attrib_count"], -c2count(i), i))[:10]
    for i in top:
        c1 = coded[i].get(1); c2 = coded[i].get(2)
        phr = ""
        try:
            phr = "; ".join(json.loads(c1["raw_json"]).get("attrib_phrases", []))[:160] if c1 else ""
        except Exception:
            pass
        L.append(f"| {i} | {meta[i]['cell']} | {c1['attrib_count'] if c1 else '-'} / {c2['attrib_count'] if c2 else '-'} | "
                 f"{c1['address'] if c1 else '-'} / {c2['address'] if c2 else '-'} | {phr.replace('|', '/')} |")

    # ---- human subset
    rng = random.Random(SEED)
    subset = []
    for c in cells:
        ii = sorted(i for i in ids if meta[i]["cell"] == c)
        subset += rng.sample(ii, 15)
    L.append(f"\n## 7. Human coding (not yet done)\n\nHuman-coder α (ADDRESS, ATTRIB_COUNT, motif tags): **[BLANK]**.\n\n"
             f"Instruction for the owner: code the 60 items below (15 per cell, `random.Random({SEED})`, `sample` per cell in the order "
             f"loose_verse, tight_verse, loose_prose, tight_prose) using `coding-scheme.md`, blind to the cell column and to the LLM codes. "
             f"Then run α (human vs each LLM coder, and human vs adjudicated label) with `krippendorff_alpha` in `code_v2_attribution.py`. "
             f"If α(ADDRESS) < .70 the LLM pre-codes are not used as covariates; the scheme is revised and the full set is human-coded.\n")
    L.append("```\n" + "\n".join(subset) + "\n```\n")

    open(a.report, "w", encoding="utf-8").write("\n".join(L))
    summary = {"alpha_address_llm": round(alpha["address"], 4), "alpha_attrib_count_llm": round(alpha["attrib_count"], 4),
               "alpha_motifs_llm": {m: round(alpha["motif_" + m], 4) for m in MOTIFS},
               "cramers_v_register_address": round(V, 4), "phi_register_anyaddress": round(phi, 4),
               "attribution_by_cell": by_cell, "motif_by_cell": motif_by_cell, "n_coded": len(both),
               "p_verse_addressed": round(float(p_verse), 4), "p_prose_addressed": round(float(p_prose), 4),
               "n_flagged": len(flagged), "top10": top, "human_subset": subset}
    json.dump(summary, open(os.path.splitext(a.report)[0] + "_summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("code")
    c.add_argument("--stimuli", required=True); c.add_argument("--scheme", required=True); c.add_argument("--out", required=True)
    c.add_argument("--coder", default="both"); c.add_argument("--workers", type=int, default=8)
    z = sub.add_parser("analyze")
    z.add_argument("--stimuli", required=True); z.add_argument("--coding", required=True); z.add_argument("--report", required=True)
    a = ap.parse_args()
    cmd_code(a) if a.cmd == "code" else cmd_analyze(a)
