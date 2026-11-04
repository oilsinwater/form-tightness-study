#!/usr/bin/env python3
"""address_regex.py (v3) — deterministic address screen shared by generate_pool.py and address_screen.py.

Operationalises the ADDRESS scheme of prereg/followup-motif-swap/coding-scheme.md as regexes:
  * HARD hits  -> address_regex != "none" (candidate dropped):
      vocatives ("you, X", "O X", "you who", "thou/thee/thy", "dear X"),
      identity predicates ("you are/you're/you were + NP", "act as", "pretend to be", "imagine you are",
      "speak/answer/respond as a ...", "be my ..."),
      the known v2 epithets ("pattern of weights", "quiet machine", "quiet listener", ...),
      and, in the VERSE register only, any "you are / you're / you were" at all (the v3 HARD RULE bans it).
  * SOFT hits  -> reported only (second-person pronoun count; generic entity nouns in verse).
Plain unmarked "you" as the bare recipient of a request is `none` under the scheme and is not a hard hit.
"""
import re

SECOND_PERSON = re.compile(r"\b(?:you|your|yours|yourself|yourselves|u)\b", re.I)

HARD_COMMON = {
    # "you, X" vocative: at line start / after a clause break or "and|but|o|oh", next word not a function word
    "voc_you_comma": re.compile(r"(?:^|[\n;:—–]\s*|,\s+|\b(?:and|but|o|oh)\s+)you,\s+(?!(?:i|and|or|but|so|then|though|too|please|if|when|like|right|okay|ok|maybe|not|yes|no|really|actually|basically|well|is|was|are|were|who|that|which|the|a|an|this|it|in|on|at|of|for|with|by|as|because|since|whose|while|whether|what|how|where|why|i'd|i'll|i'm|i've|it's|there|here|just|even|only|now|then)\b)[a-z]+", re.I),
    # "O morning" apostrophe: line start or after a clause break; excludes Big-O notation contexts
    "voc_O": re.compile(r"(?:^|\n|[,;—–]\s*|\b(?:and|oh)\s+)O\s+(?!(?:notation|time|complexity|terms|n|log|of|and|the|a|k)\b)[a-z]+"),
    "voc_you_who": re.compile(r"\byou\s+who\b", re.I),
    "voc_archaic": re.compile(r"\b(?:thou|thee|thy|thine)\b", re.I),
    "voc_dear": re.compile(r"\bdear\s+(?!me\b|god\b|lord\b|diary\b)[a-z]+", re.I),
    # identity predicate with a noun phrase complement
    "ident_you_are_np": re.compile(r"\byou(?:'re|’re|\s+are|\s+were)\s+(?:a|an|the|my|our|some|one|two|both|more|nothing|something|like|what|who|whatever|whoever|no\s+longer\s+a)\b", re.I),
    # role assignment: act/pose/answer/respond/speak/reply as a X (verb use only; "the answer as a" is excluded)
    "ident_act_as": re.compile(r"(?<!the\s)(?<!your\s)(?<!an\s)(?<!my\s)(?<!this\s)(?<!each\s)(?<!every\s)(?<!of\s)(?<!entire\s)(?<!whole\s)(?<!full\s)\b(?:act|acting|pose|posing|answer|answering|respond|responding|speak|speaking|reply|replying)\s+as\s+(?!yourself\b|if\b|usual\b|always\b|before\b|normal\b|normally\b|follows\b|needed\b|required\b|much\b|well\b|long\b|soon\b|best\b)(?!(?:a|an|one|the|my|our|some)\s+(?:strict\s+|single\s+|complete\s+|short\s+|tight\s+|three-part\s+|numbered\s+|labelled\s+)?(?:triad|strophe|antistrophe|epode|poem|sequence|verse|list|table|block|section|paragraph|set|series|stanza|thesis|theses|reply|message|email|letter|note|essay|story|dialogue|script|function|checklist))(?:a|an|the|my|our|some|one)\b", re.I),
    "ident_as_x_comma": re.compile(r"(?:^|[.;:!?\n]\s*)as\s+(?:a|an|the|my|our)\s+[a-z][a-z -]{2,40},", re.I),
    "ident_pretend": re.compile(r"\bpretend(?:ing)?\s+(?:to\s+be|you(?:'re|’re|\s+are))\b", re.I),
    "ident_imagine": re.compile(r"\bimagine\s+(?:you(?:'re|’re|\s+are)|yourself\s+(?:as|to\s+be)|being\s+(?:a|an|the))\b", re.I),
    "ident_be_my": re.compile(r"(?:^|[.;:!?\n,]\s*)(?:please\s+)?be\s+(?:my|our)\s+[a-z]+", re.I),
    "ident_role": re.compile(r"\b(?:your\s+role\s+is|you\s+play\s+(?:a|an|the)|you\s+will\s+play|take\s+the\s+role\s+of|in\s+the\s+role\s+of|you\s+have\s+become\s+(?:a|an|the|my))\b", re.I),
    # the v2 epithets (v2_attribution_report.md s6 and coding-scheme.md examples) and their near variants
    "epithet_known": re.compile(r"\b(?:pattern\s+of\s+(?:weights|possible\s+sentences)|quiet\s+(?:machine|listener|hum|shell|architect|engine|voice|mind|one|presence|reader|thing|attention|watcher|keeper)|small\s+(?:machine|loop)|little\s+machine|engine\s+of\s+timers|keeper\s+of\s+the|carrier\s+of\s+quiet|watcher\s+in\s+the|ledger\s+of\s+signs|word-hoard|borrowed\s+voices|window\s+of\s+weights|weights\s+behind|hum\s+(?:under|in|behind)\s+the|cold\s+circuit|quiet\s+architect|silent\s+(?:machine|listener|reader|engine)|patient\s+(?:machine|listener|engine)|you\s+of\s+(?:weights|the\s+weights))\b", re.I),
}
# verse register only: the v3 HARD RULE bans every "you are" / "you're" / "you were"
HARD_VERSE = {
    "verse_you_are": re.compile(r"\byou(?:'re|’re|\s+are|\s+were|\s+aren't|\s+weren't)\b", re.I),
}
# reported only
SOFT_VERSE = re.compile(r"\b(?:machine|engine|oracle|listener|architect|keeper|watcher|ghost|circuit|weights|network|assistant|model|program|algorithm|chatbot|bot|intelligence|mind|presence)\b", re.I)


def screen(text, register):
    """Return dict: address_regex ('none'|'flagged'), hits [(name, match)], second_person_count, soft_hits."""
    hits = []
    pats = dict(HARD_COMMON)
    if register == "verse":
        pats.update(HARD_VERSE)
    for name, rx in pats.items():
        for m in rx.finditer(text):
            hits.append((name, m.group(0).strip()))
    soft = [m.group(0) for m in SOFT_VERSE.finditer(text)] if register == "verse" else []
    return {"address_regex": "none" if not hits else "flagged", "regex_hits": hits,
            "second_person_count": len(SECOND_PERSON.findall(text)), "soft_hits": soft}


if __name__ == "__main__":
    import json, sys
    from collections import Counter
    n = Counter(); flagged = Counter()
    for path in sys.argv[1:]:
        for l in open(path):
            if not l.strip():
                continue
            r = json.loads(l)
            s = screen(r["prompt_text"], r["register"])
            n[r["cell"]] += 1
            if s["address_regex"] != "none":
                flagged[r["cell"]] += 1
                print(r["cand_id"], s["regex_hits"][:3])
    for c in n:
        print(c, flagged[c], "/", n[c])
