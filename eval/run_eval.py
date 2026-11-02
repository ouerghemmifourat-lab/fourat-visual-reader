#!/usr/bin/env python3
"""Automatic metrics for eval outputs (protocol: eval/PROTOCOL.md).
  python run_eval.py            -> metrics.json + prints a summary table
Inputs: cases.json; outputs/<arm>/<id>.txt for arms baseline, skill (and optionally script); judge/<arm>.json (optional).
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "fourat-visual-reader" / "scripts"))
import vvr  # noqa: E402

ARMS = ["baseline", "skill", "script"]
TYPE_WORD = {
    "en": r"\b(table|bar chart|line chart|pie chart|donut|scatter|flowchart|flow chart|org chart|organisation chart|organization chart|sequence diagram|mind map|chart|diagram|image|photo)\b",
    "fr": r"\b(tableau|graphique|camembert|courbe|nuage|diagramme|organigramme|carte mentale|image|photo)\b",
}
SIZE_WORD = {
    "en": r"\b(column|row|bar|point|step|part|series|level|participant|message|branch|slice|countr|quarter|month|year|cit|region|product|store|decision)",
    "fr": r"\b(colonne|ligne|barre|point|étape|part|série|niveau|participant|message|branche|pays|trimestre|mois|année|ville|région|produit|commune|élève|navigateur|appartement|tranche|magasin|décision)",
}


def announces(first, lang):
    """Pre-registered: type word + a NUMBER (digits or words, >= 2) + a size word, all in the first sentence."""
    if not re.search(TYPE_WORD[lang], first, re.I) or not re.search(SIZE_WORD[lang], first, re.I):
        return False
    return any(n >= 2 for n in vvr.words_to_numbers(first, lang))
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
# post-hoc metric (declared in RESULTS.md): an offer of further detail, with or without a question mark
OFFER = re.compile(r"(I can read|I can (also )?(give|go|detail|read|compare)|Ask for|ask me|Shall I|Would you like|Want the|let me know|"
                   r"If you can share|if you want|Je peux (lire|détailler|donner|parcourir|comparer)|Demandez|Vous pouvez (me )?(demander|fournir)|"
                   r"Voulez-vous|Souhaitez-vous|si vous le souhaitez|Je continue|Dites-moi)", re.I)


def first_sentence(text):
    text = text.strip()
    m = re.search(r"[.!?]", text)
    return text[: m.end()] if m else text


def metrics_for(text, case):
    lang = case["lang"]
    words = re.findall(r"\w+(?:[-']\w+)*", text, re.UNICODE)
    q = text.find("?")
    before_q = len(re.findall(r"\w+(?:[-']\w+)*", text[:q])) if q >= 0 else None
    # post-hoc: words before the first OFFER sentence (a decision's "?" inside a flowchart is not an offer)
    om = OFFER.search(text)
    before_offer = len(re.findall(r"\w+(?:[-']\w+)*", text[: om.start()])) if om else None
    sents = [s for s in SENT_SPLIT.split(text) if s.strip()]
    nums = vvr.words_to_numbers(text, lang)
    per_sent = [len(vvr.words_to_numbers(s, lang)) for s in sents]
    lint = vvr.lint(text)
    out = {"words": len(words), "sentences": len(sents), "words_before_first_question": before_q,
           "words_before_first_offer_posthoc": before_offer,
           "has_question": q >= 0, "has_offer": bool(om),
           "announce_first": announces(first_sentence(text), lang),
           "numbers_spoken": len(nums), "numbers_per_sentence": round(sum(per_sent) / max(1, len(sents)), 2),
           "max_numbers_in_a_sentence": max(per_sent) if per_sent else 0,
           "lint_issues": len(lint), "lint_per_100_words": round(100 * len(lint) / max(1, len(words)), 2),
           "lint_kinds": sorted({m for _, m, _ in lint})}
    if case.get("vvr_kind"):
        src = case["input"].split("\n[")[0]  # strip the listener's follow-up question in interpretation cases
        ir = vvr.parse(src, case["vvr_kind"], lang, case.get("title", ""))
        bad = vvr.verify(ir, text, lang, source_text=case["input"])
        out["unsupported_numbers"] = [round(b, 4) for b in bad]
        out["numbers_all_supported"] = not bad
    return out


def main():
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    res = {}
    for arm in ARMS:
        d = HERE / "outputs" / arm
        if not d.exists():
            continue
        judge = {}
        jp = HERE / "judge" / f"{arm}.json"
        if jp.exists():
            judge = {j["id"]: j for j in json.loads(jp.read_text(encoding="utf-8"))}
        per = {}
        for c in cases:
            p = d / f"{c['id']}.txt"
            if not p.exists():
                continue
            m = metrics_for(p.read_text(encoding="utf-8"), c)
            if c["id"] in judge:
                v = judge[c["id"]]["verdicts"]
                m["judge_correct"] = sum(x == "correct" for x in v)
                m["judge_not_said"] = sum(x == "not_said" for x in v)
                m["judge_incorrect"] = sum(x == "incorrect" for x in v)
            per[c["id"]] = m
        if not per:
            continue
        vals = list(per.values())
        n = len(vals)
        def med(xs):
            xs = sorted(xs)
            return None if not xs else (xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2)
        big_ids = {c["id"] for c in cases if "large" in c["id"] or "medium" in c["id"]}
        structured = [v for v in vals if "numbers_all_supported" in v]
        summ = {"cases": n,
                "announce_first_pct": round(100 * sum(v["announce_first"] for v in vals) / n, 1),
                "has_question_pct": round(100 * sum(v["has_question"] for v in vals) / n, 1),
                "has_offer_pct_posthoc": round(100 * sum(v["has_offer"] for v in vals) / n, 1),
                "median_words_before_first_offer_posthoc": med([v["words_before_first_offer_posthoc"] for v in vals if v["words_before_first_offer_posthoc"] is not None]),
                "big_cases_with_offer_pct_posthoc": round(100 * sum(per[i]["has_offer"] for i in big_ids if i in per) / max(1, len([i for i in big_ids if i in per])), 1),
                "median_words": med([v["words"] for v in vals]),
                "median_words_before_first_question": med([v["words_before_first_question"] for v in vals if v["words_before_first_question"] is not None]),
                "big_cases_with_question_pct": round(100 * sum(per[i]["has_question"] for i in big_ids if i in per) / max(1, len([i for i in big_ids if i in per])), 1),
                "mean_numbers_per_sentence": round(sum(v["numbers_per_sentence"] for v in vals) / n, 2),
                "pct_sentences_budget_ok": round(100 * sum(v["numbers_per_sentence"] <= 1.5 for v in vals) / n, 1),
                "lint_per_100_words_mean": round(sum(v["lint_per_100_words"] for v in vals) / n, 2),
                "cases_with_zero_lint_pct": round(100 * sum(v["lint_issues"] == 0 for v in vals) / n, 1),
                "structured_cases": len(structured),
                "structured_all_numbers_supported_pct": round(100 * sum(v["numbers_all_supported"] for v in structured) / max(1, len(structured)), 1),
                "unsupported_numbers_total": sum(len(v["unsupported_numbers"]) for v in structured)}
        if any("judge_correct" in v for v in vals):
            jv = [v for v in vals if "judge_correct" in v]
            summ["judge_cases"] = len(jv)
            summ["judge_correct_pct"] = round(100 * sum(v["judge_correct"] for v in jv) / (3 * len(jv)), 1)
            summ["judge_not_said_pct"] = round(100 * sum(v["judge_not_said"] for v in jv) / (3 * len(jv)), 1)
            summ["judge_incorrect_pct"] = round(100 * sum(v["judge_incorrect"] for v in jv) / (3 * len(jv)), 1)
        res[arm] = {"summary": summ, "per_case": per}
    # paired bootstrap on judge correctness, skill vs baseline
    if "baseline" in res and "skill" in res and "judge_correct" in next(iter(res["skill"]["per_case"].values()), {}):
        import random
        ids = [i for i in res["skill"]["per_case"] if i in res["baseline"]["per_case"] and "judge_correct" in res["baseline"]["per_case"][i]]
        diffs = [res["skill"]["per_case"][i]["judge_correct"] - res["baseline"]["per_case"][i]["judge_correct"] for i in ids]
        rng = random.Random(0)
        bs = sorted(sum(rng.choice(diffs) for _ in diffs) / (3 * len(diffs)) for _ in range(2000))
        res["judge_skill_minus_baseline"] = {"point_pct": round(100 * sum(diffs) / (3 * len(diffs)), 1),
                                            "ci95_pct": [round(100 * bs[50], 1), round(100 * bs[1949], 1)], "cases": len(ids)}
    (HERE / "metrics.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    keys = sorted({k for a in ARMS if a in res for k in res[a]["summary"]})
    print("metric".ljust(44) + "".join(a.rjust(12) for a in ARMS if a in res))
    for k in keys:
        print(k.ljust(44) + "".join(str(res[a]["summary"].get(k, "")).rjust(12) for a in ARMS if a in res))
    if "judge_skill_minus_baseline" in res:
        print("judge skill - baseline:", res["judge_skill_minus_baseline"])


if __name__ == "__main__":
    main()
