#!/usr/bin/env python3
"""vvr.py -- voice-visual-reader helper. Standard library only, Python 3.9+.

  python vvr.py parse   INPUT [--kind table|bars|line|pie|flowchart] [--lang en|fr] [--title T]  -> IR JSON
  python vvr.py narrate IR.json [--level brief|full] [--ssml]                                    -> spoken text / SSML
  python vvr.py speak   INPUT [same options as parse + narrate]                                  -> parse then narrate
  python vvr.py verify  IR.json SPOKEN.txt [--lang en|fr]   -> numbers spoken that are not in the data (exit 1 if any)
  python vvr.py lint    SPOKEN.txt                           -> digits, symbols, abbreviations, markdown left in speech
  python vvr.py num     VALUE [--lang en|fr]                 -> number in words
  python vvr.py selftest

INPUT: a Markdown table, a CSV (comma or semicolon), or a Mermaid flowchart (`flowchart`/`graph` header).
Kinds bars/line/pie read a two-or-more-column table (first column = category or x, next columns = series).
The intermediate representation (IR) is documented in research/DESIGN.md section 7.
"""
import argparse, csv, io, json, math, re, sys
from collections import OrderedDict

# ----------------------------------------------------------------------------------------------- numbers -> words
_EN_SMALL = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
             "seventeen eighteen nineteen").split()
_EN_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
_EN_SCALE = [(10 ** 12, "trillion"), (10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")]
_FR_SMALL = ("zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize dix-sept "
             "dix-huit dix-neuf").split()
_FR_TENS = "_ _ vingt trente quarante cinquante soixante soixante quatre-vingt quatre-vingt".split()
_FR_SCALE = [(10 ** 12, "billion"), (10 ** 9, "milliard"), (10 ** 6, "million"), (1000, "mille")]


def _en_below_1000(n):
    if n < 20:
        return _EN_SMALL[n]
    if n < 100:
        return _EN_TENS[n // 10] + ("-" + _EN_SMALL[n % 10] if n % 10 else "")
    return _EN_SMALL[n // 100] + " hundred" + (" " + _en_below_1000(n % 100) if n % 100 else "")


def _fr_below_100(n):
    if n < 20:
        return _FR_SMALL[n]
    t, u = divmod(n, 10)
    if t in (7, 9):  # soixante-dix..., quatre-vingt-dix...
        u += 10
    if t == 8 and u == 0:
        return "quatre-vingts"
    if u == 0:
        return _FR_TENS[t]
    if (u == 1 and t not in (8, 9)) or (u == 11 and t == 7):  # vingt-et-un ... soixante-et-un, soixante-et-onze
        return _FR_TENS[t] + "-et-" + _FR_SMALL[u]
    return _FR_TENS[t] + "-" + _FR_SMALL[u]


def _fr_below_1000(n):
    if n < 100:
        return _fr_below_100(n)
    h, r = divmod(n, 100)
    head = "cent" if h == 1 else _FR_SMALL[h] + " cent"
    if r == 0:
        return head + ("s" if h > 1 else "")
    return head + " " + _fr_below_100(r)


def int_to_words(n, lang):
    if n < 0:
        return ("minus " if lang == "en" else "moins ") + int_to_words(-n, lang)
    if n == 0:
        return _EN_SMALL[0] if lang == "en" else _FR_SMALL[0]
    parts = []
    for value, name in (_EN_SCALE if lang == "en" else _FR_SCALE):
        if n >= value:
            q, n = divmod(n, value)
            if lang == "en":
                parts.append(f"{_en_below_1000(q)} {name}")
            elif name == "mille":
                parts.append("mille" if q == 1 else f"{_fr_below_1000(q)} mille")
            else:
                parts.append(f"{_fr_below_1000(q)} {name}{'s' if q > 1 else ''}")
    if n:
        parts.append(_en_below_1000(n) if lang == "en" else _fr_below_1000(n))
    return " ".join(parts)


def number_to_words(value, lang, max_decimals=2):
    """float/int -> words. Decimals: EN digit by digit after 'point'; FR 'virgule' then the decimal part as a number
    (digit by digit when it has a leading zero)."""
    if isinstance(value, str):
        value = parse_number(value, lang)
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "no value" if lang == "en" else "vide"
    neg = value < 0
    value = abs(value)
    ip = int(value)
    frac = round(value - ip, 10)
    s = int_to_words(ip, lang)
    if frac:
        dec = f"{value:.{max_decimals}f}".split(".")[1].rstrip("0")
        if dec:
            if lang == "en":
                s += " point " + " ".join(_EN_SMALL[int(d)] for d in dec)
            elif dec[0] == "0":
                s += " virgule " + " ".join(_FR_SMALL[int(d)] for d in dec)
            else:
                s += " virgule " + int_to_words(int(dec), "fr")
        elif ip == 0 and value > 0:  # rounded away: keep the information
            s = ("about " if lang == "en" else "environ ") + s
    return ("minus " if lang == "en" else "moins ") + s if neg else s


_NUM_RE = re.compile(r"^\s*([-−–+]?)\s*([\d\s  .,]+)\s*(%|‰|[A-Za-zµ°€$£/²³]+(?:/[A-Za-z]+)?)?\s*$")


def parse_number(text, lang):
    """'1 234,5' (fr) or '1,234.5' (en) -> float; None if not a number."""
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    m = _NUM_RE.match(str(text))
    if not m:
        return None
    sign, body, _unit = m.groups()
    body = re.sub(r"[\s  ]", "", body)
    if lang == "fr":
        if "," in body and "." in body:  # 1.234,5
            body = body.replace(".", "").replace(",", ".")
        elif "," in body:
            body = body.replace(",", ".")
        elif body.count(".") > 1 or re.fullmatch(r"\d{1,3}(\.\d{3})+", body):
            body = body.replace(".", "")
    else:
        if "," in body and "." in body:
            body = body.replace(",", "")
        elif "," in body:
            body = body.replace(",", "") if re.fullmatch(r"\d{1,3}(,\d{3})+", body) else body.replace(",", ".")
    try:
        v = float(body)
    except ValueError:
        return None
    return -v if sign and sign in "-−–" else v


UNITS = {
    "en": {"%": "percent", "‰": "per mille", "€": "euros", "$": "dollars", "£": "pounds", "km": "kilometres",
           "m": "metres", "cm": "centimetres", "mm": "millimetres", "km/h": "kilometres per hour", "m/s": "metres per second",
           "kg": "kilograms", "g": "grams", "mg": "milligrams", "µg": "micrograms", "L": "litres", "mL": "millilitres",
           "dL": "decilitres", "mg/dL": "milligrams per decilitre", "mmol/L": "millimoles per litre", "°C": "degrees Celsius",
           "°F": "degrees Fahrenheit", "m²": "square metres", "km²": "square kilometres", "ha": "hectares", "m³": "cubic metres",
           "s": "seconds", "ms": "milliseconds", "min": "minutes", "h": "hours", "kWh": "kilowatt-hours", "MW": "megawatts",
           "GW": "gigawatts", "GB": "gigabytes", "TB": "terabytes", "Mbps": "megabits per second", "bpm": "beats per minute",
           "mmHg": "millimetres of mercury", "ppm": "parts per million", "M€": "million euros", "k€": "thousand euros",
           "M$": "million dollars", "k$": "thousand dollars", "k": "thousand", "M": "million", "bn": "billion", "pts": "points"},
    "fr": {"%": "pour cent", "‰": "pour mille", "€": "euros", "$": "dollars", "£": "livres", "km": "kilomètres",
           "m": "mètres", "cm": "centimètres", "mm": "millimètres", "km/h": "kilomètres par heure", "m/s": "mètres par seconde",
           "kg": "kilogrammes", "g": "grammes", "mg": "milligrammes", "µg": "microgrammes", "L": "litres", "mL": "millilitres",
           "dL": "décilitres", "mg/dL": "milligrammes par décilitre", "mmol/L": "millimoles par litre", "°C": "degrés Celsius",
           "°F": "degrés Fahrenheit", "m²": "mètres carrés", "km²": "kilomètres carrés", "ha": "hectares", "m³": "mètres cubes",
           "s": "secondes", "ms": "millisecondes", "min": "minutes", "h": "heures", "kWh": "kilowattheures", "MW": "mégawatts",
           "GW": "gigawatts", "Go": "gigaoctets", "To": "téraoctets", "Mbit/s": "mégabits par seconde", "bpm": "battements par minute",
           "mmHg": "millimètres de mercure", "ppm": "parties par million", "M€": "millions d'euros", "k€": "milliers d'euros",
           "M$": "millions de dollars", "k$": "milliers de dollars", "k": "mille", "M": "millions", "Md": "milliards", "pts": "points"},
}
_UNIT_IN_HEADER = re.compile(r"^(.*?)\s*[\(\[]([^\)\]]+)[\)\]]\s*$")


def unit_words(unit, lang):
    if not unit:
        return ""
    return UNITS[lang].get(unit, UNITS[lang].get(unit.strip(), unit))


def value_words(v, unit, lang, approx=False):
    """Number + unit for speech, rounded to 3 significant figures when approx."""
    if v is None:
        return "no value" if lang == "en" else "vide"
    if approx and v != 0:
        mag = 10 ** (math.floor(math.log10(abs(v))) - 2)
        v = round(v / mag) * mag
    big = abs(v) >= 1e6 and not unit
    if big:  # 2 100 000 -> about 2.1 million
        for scale, name_en, name_fr in ((1e9, "billion", "milliard"), (1e6, "million", "million")):
            if abs(v) >= scale:
                q = round(v / scale, 1)
                words = number_to_words(q, lang, 1)
                name = name_en if lang == "en" else name_fr + ("s" if q > 1 and q == int(q) or q >= 2 else "")
                return f"{words} {name}"
    if unit and unit.strip() in ("k€", "k$", "k") and v != int(v):  # 12.5 k€ -> twelve thousand five hundred euros
        v, unit = v * 1000, {"k€": "€", "k$": "$", "k": ""}[unit.strip()]
    words = number_to_words(v, lang)
    uw = unit_words(unit, lang)
    if uw and (abs(v) < 2 or lang == "en"):  # en: "two point one million" (always singular); fr: "zéro virgule cinq million"
        for pl, sg in (("millions", "million"), ("milliards", "milliard"), ("billions", "billion"), ("thousands", "thousand")):
            if uw.startswith(pl):
                uw = sg + uw[len(pl):]
    if uw and (abs(v) < 2 if lang == "fr" else abs(v) == 1):  # fr: "sept virgule un jour", "un lit"; en: "one kilometre"
        uw = _singular(uw)
    return f"{words} {uw}".strip()


def _singular(unit_phrase):
    """Drop the plural -s of each word: "kilomètres carrés" -> "kilomètre carré". Keeps Celsius, d'euros, pour cent."""
    return " ".join(w if (len(w) < 4 or not w.endswith("s") or w.endswith(("us", "ss")) or "'" in w) else w[:-1]
                    for w in unit_phrase.split(" "))


# ----------------------------------------------------------------------------------------------- parsing
def parse_table_text(text, lang):
    lines = [l.rstrip() for l in text.strip().splitlines() if l.strip()]
    if lines and "|" in lines[0]:
        rows = []
        for l in lines:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
    else:
        sample = "\n".join(lines[:5])
        delim = ";" if sample.count(";") > sample.count(",") else ","
        rows = list(csv.reader(io.StringIO("\n".join(lines)), delimiter=delim))
        rows = [[c.strip() for c in r] for r in rows if any(c.strip() for c in r)]
    header, body = rows[0], rows[1:]
    columns = []
    for h in header:
        m = _UNIT_IN_HEADER.match(h)
        columns.append({"name": (m.group(1) if m else h).strip(), "unit": (m.group(2).strip() if m else "")})
    out_rows = []
    for r in body:
        r = r + [""] * (len(header) - len(r))
        # column 0 is the row header (city, year...): kept as text so "2015" stays a label, not a quantity
        out_rows.append([c if j == 0 or parse_number(c, lang) is None else parse_number(c, lang) for j, c in enumerate(r[: len(header)])])
    # a unit spelled only in the cells (12 %, 3 km) -> move it to the column
    for j, col in enumerate(columns):
        if not col["unit"]:
            units = {(_NUM_RE.match(str(r[j])) or [None, None, None, None])[3] for r in body if _NUM_RE.match(str(r[j]))}
            units.discard(None)
            if len(units) == 1:
                col["unit"] = units.pop()
    return {"kind": "table", "title": "", "columns": columns, "rows": out_rows, "row_header_col": 0, "lang": lang,
            "notes": []}


_NODE_RE = re.compile(r"([A-Za-z0-9_]+)\s*(\(\((.*?)\)\)|\[\[(.*?)\]\]|\{(.*?)\}|\[(.*?)\]|\((.*?)\)|>(.*?)\])?")
_EDGE_RE = re.compile(r"\s*(-{2,}>|={2,}>|-\.+->|--\s*([^-]*?)\s*-->|-{2,}|={2,})\s*(\|([^|]*)\|)?\s*")


def parse_mermaid_flowchart(text, lang):
    nodes, edges = OrderedDict(), []

    def add_node(m):
        nid = m.group(1)
        label = next((g for g in m.groups()[2:] if g is not None), None)
        shape = "process"
        if m.group(3) is not None or m.group(4) is not None:
            shape = "terminal"
        elif m.group(5) is not None:
            shape = "decision"
        if nid not in nodes:
            nodes[nid] = {"id": nid, "label": (label or nid).strip().strip('"'), "type": shape}
        elif label:
            nodes[nid]["label"] = label.strip().strip('"')
            if shape != "process":
                nodes[nid]["type"] = shape
        return nid

    for raw in text.splitlines():
        line = raw.split("%%")[0].strip().rstrip(";")
        if not line or re.match(r"^(flowchart|graph)\b", line) or line.startswith(("subgraph", "end", "classDef", "class ", "style", "click", "linkStyle")):
            continue
        pos, prev, pending_label = 0, None, None
        while pos < len(line):
            m = _NODE_RE.match(line, pos)
            if not m or not m.group(1):
                break
            nid = add_node(m)
            if prev is not None:
                edges.append({"from": prev, "to": nid, "label": (pending_label or "").strip()})
            pos = m.end()
            e = _EDGE_RE.match(line, pos)
            if not e:
                break
            pending_label = e.group(4) if e.group(4) is not None else e.group(2)
            prev, pos = nid, e.end()
            if line[pos: pos + 1] == "&":  # A & B --> C : not supported, keep going
                pos += 1
    ids = list(nodes)
    has_in = {e["to"] for e in edges}
    has_out = {e["from"] for e in edges}
    for n in nodes.values():
        if n["type"] == "terminal":
            n["type"] = "start" if n["id"] not in has_in else "end"
        elif n["id"] in ids and n["id"] not in has_in and n["type"] == "process":
            n["type"] = "start"
        elif n["id"] not in has_out and n["type"] == "process":
            n["type"] = "end"
    return {"kind": "flowchart", "title": "", "nodes": list(nodes.values()), "edges": edges, "lang": lang}


def parse(text, kind, lang, title=""):
    if kind == "flowchart" or re.match(r"^\s*(flowchart|graph)\b", text):
        ir = parse_mermaid_flowchart(text, lang)
    else:
        ir = parse_table_text(text, lang)
        if kind in ("bars", "line", "pie"):
            ir["kind"] = kind
    ir["title"] = title or ir.get("title", "")
    return ir


# ----------------------------------------------------------------------------------------------- narration
T = {
    "en": {"table": "A table with {c} columns and {r} rows: {cols}.", "unit": " Values in {u}.",
           "more": " and {n} more", "row_of": "Rows {a} to {b} of {r}.", "row1": "Row {a} of {r}.",
           "max_min": "{maxl} has the largest {col}; {minl} the smallest.", "max": "{l}, {col}: {v}.",
           "min": "{l}: {v}.", "total": "The total of {col} is {v}.", "offer_table": "I can read it row by row, go through one column, or compare two rows. What would you like?",
           "offer_big": "That is a large table. I can read the top rows, one column, or a filtered subset. What would you like?",
           "bars": "A bar chart of {y} by {x}, {n} bars{unit}.", "pie": "A pie chart of {y} in {n} parts.",
           "line": "A line chart of {y} from {x0} to {x1}, {n} points{unit}.", "series": ", {s} series",
           "rank": "{top} is highest, {second} close behind, {bottom} far lower." , "rank2": "{top} is highest; {bottom} is lowest.",
           "ratio_half": "about half of {top}", "ratio_third": "about a third of {top}", "ratio_fifth": "about a fifth of {top}", "ratio_double": "almost double {bottom}",
           "rises": "{y} rises from {v0} to {v1}", "falls": "{y} falls from {v0} to {v1}", "flat": "{y} stays around {v0}",
           "dip": ", with a dip in {x}", "bump": ", with a peak in {x}", "low": "The low point is {v}, in {x}.", "high": "The peak is {v}, in {x}.",
           "pie_half": "{top} takes more than half.", "pie_top": "{top} is the largest share.", "others": "The other {n} total {v}.",
           "flow": "A flowchart with {s} steps and {d} decision{dp}, {i} entry point{ip}, {o} exit{op}, from {start} to {end}.",
           "step": "Step {n}, {label}.", "decision": "Decision: {label}", "ifyes": " If {lab}, step {n}, {label}.", "ifyes_end": " If {lab}, {label}.",
           "back": " then back to step {n}.", "join": " which joins step {n}.", "end": "Then {label}.", "offer_flow": "Shall I detail a step?",
           "offer_more": "Shall I continue?", "approx": "about ", "img": "", "wait": "",
           "detail_hint": "Ask for a row, a column, or a comparison for more."},
    "fr": {"table": "Un tableau de {c} colonnes et {r} lignes : {cols}.", "unit": " Valeurs en {u}.",
           "more": " et {n} autres", "row_of": "Lignes {a} à {b} sur {r}.", "row1": "Ligne {a} sur {r}.",
           "max_min": "{maxl} a la plus grande valeur de {col} ; {minl} la plus petite.", "max": "{l}, {col} : {v}.",
           "min": "{l} : {v}.", "total": "Le total de {col} est {v}.", "offer_table": "Je peux lire ligne par ligne, parcourir une colonne, ou comparer deux lignes. Que souhaitez-vous ?",
           "offer_big": "C'est un grand tableau. Je peux lire les premières lignes, une colonne, ou un sous-ensemble filtré. Que souhaitez-vous ?",
           "bars": "Un graphique en barres de {y} par {x}, {n} barres{unit}.", "pie": "Un camembert de {y} en {n} parts.",
           "line": "Une courbe de {y} de {x0} à {x1}, {n} points{unit}.", "series": ", {s} séries",
           "rank": "{top} est en tête, {second} juste derrière, {bottom} loin derrière.", "rank2": "{top} est en tête ; {bottom} est le plus bas.",
           "ratio_half": "environ la moitié de {top}", "ratio_third": "environ un tiers de {top}", "ratio_fifth": "environ un cinquième de {top}", "ratio_double": "presque le double de {bottom}",
           "rises": "{y} monte de {v0} à {v1}", "falls": "{y} baisse de {v0} à {v1}", "flat": "{y} reste autour de {v0}",
           "dip": ", avec un creux en {x}", "bump": ", avec un pic en {x}", "low": "Le point bas est {v} en {x}.", "high": "Le sommet est {v} en {x}.",
           "pie_half": "{top} prend plus de la moitié.", "pie_top": "{top} est la plus grande part.", "others": "Les {n} autres totalisent {v}.",
           "flow": "Un diagramme de flux de {s} étapes et {d} décision{dp}, {i} entrée{ip}, {o} sortie{op}, de {start} à {end}.",
           "step": "Étape {n}, {label}.", "decision": "Décision : {label}", "ifyes": " Si {lab}, étape {n}, {label}.", "ifyes_end": " Si {lab}, {label}.",
           "back": " puis retour à l'étape {n}.", "join": " qui rejoint l'étape {n}.", "end": "Puis {label}.", "offer_flow": "Voulez-vous le détail d'une étape ?",
           "offer_more": "Je continue ?", "approx": "environ ", "img": "", "wait": "",
           "detail_hint": "Demandez une ligne, une colonne ou une comparaison pour en savoir plus."},
}


def _say_n(n, lang):
    return int_to_words(n, lang)


def year_words(n, lang):
    if lang == "fr":
        return int_to_words(n, "fr")
    c, r = divmod(n, 100)
    if 2000 <= n <= 2009:
        return "two thousand" + (" " + _EN_SMALL[r] if r else "")
    return _en_below_1000(c) + " " + (_en_below_1000(r) if r >= 10 else ("oh " + _EN_SMALL[r] if r else "hundred"))


def speak_label(s, lang):
    """Row / x labels, column names and titles for speech: standalone numbers become words (4-digit years as years);
    identifiers such as S12 or Q1 are kept."""
    def sub(m):
        tok = m.group(0)
        if re.fullmatch(r"(1[5-9]|20)\d\d", tok):
            return year_words(int(tok), lang)
        v = parse_number(tok, lang)
        return number_to_words(v, lang) if v is not None else tok
    return re.sub(r"(?<![A-Za-z\d])\d+(?:[.,]\d+)?(?![A-Za-z\d])", sub, str(s))


def _label(ir, row):
    return speak_label(row[ir.get("row_header_col", 0)], ir["lang"])


def _numeric_cols(ir):
    return [j for j, _ in enumerate(ir["columns"]) if j != ir.get("row_header_col", 0)
            and any(isinstance(r[j], float) for r in ir["rows"])]


def _join(items, lang):
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + (" and " if lang == "en" else " et ") + items[-1]


def _ledger_add(ledger, v):
    if isinstance(v, float):
        ledger.append(v)


def narrate_table(ir, level):
    lang, t, L = ir["lang"], T[ir["lang"]], []
    cols, rows = ir["columns"], ir["rows"]
    rh = ir.get("row_header_col", 0)
    names = [speak_label(c["name"], lang) for c in cols]
    shown = names[:3] if len(names) > 6 else names
    cols_txt = _join(shown, lang) + (t["more"].format(n=_say_n(len(names) - 3, lang)) if len(names) > 6 else "")
    first = t["table"].format(c=_say_n(len(cols), lang), r=_say_n(len(rows), lang), cols=cols_txt)
    units = {c["unit"] for c in cols if c["unit"]}
    if len(units) == 1 and sum(1 for c in cols if c["unit"]) > 1:
        first += t["unit"].format(u=unit_words(units.pop(), lang))
    blocks, ledger = [[first]], []
    num = _numeric_cols(ir)
    if num and rows:
        j = num[0]
        vals = [(r[j], r) for r in rows if isinstance(r[j], float)]
        mx, mn = max(vals), min(vals)
        col = speak_label(cols[j]["name"], lang)
        msg = [t["max_min"].format(maxl=_label(ir, mx[1]), minl=_label(ir, mn[1]), col=col)]
        key = [t["max"].format(l=_label(ir, mx[1]), col=col, v=value_words(mx[0], cols[j]["unit"], lang, approx=True)),
               t["min"].format(l=_label(ir, mn[1]), v=value_words(mn[0], cols[j]["unit"], lang, approx=True))]
        ledger += [mx[0], mn[0]]
        blocks.append(msg + key)
    small = len(cols) <= 4 and len(rows) <= 6
    big = len(cols) > 8 or len(rows) > 30
    if level == "full" or small:
        limit = rows if not big else rows[:9]
        for a in range(0, len(limit), 3):
            grp = limit[a: a + 3]
            pos = (t["row1"] if len(rows) == 1 else t["row_of"]).format(a=_say_n(a + 1, lang), b=_say_n(a + len(grp), lang), r=_say_n(len(rows), lang))
            blk = [pos] if not small else []
            for r in grp:
                cells = []
                for j, c in enumerate(cols):
                    if j == rh:
                        continue
                    v = r[j]
                    if isinstance(v, float):
                        cells.append(f"{c['name']} {value_words(v, c['unit'], lang)}")
                        _ledger_add(ledger, v)
                    else:
                        cells.append(f"{c['name']} {v if v else ('no value' if lang == 'en' else 'vide')}")
                blk.append(f"{_label(ir, r)}{' :' if lang == 'fr' else ':'} " + (" ; " if lang == "fr" else "; ").join(cells) + ".")
            blocks.append(blk)
        if big:
            blocks.append([t["offer_big"]])
        elif not small:
            blocks.append([t["offer_more"]])
    else:
        blocks.append([t["offer_big"] if big else t["offer_table"]])
    return blocks, ledger


def _series(ir):
    """(x labels, [(series name, unit, values)])"""
    rh = ir.get("row_header_col", 0)
    xs = [speak_label(r[rh], ir["lang"]) for r in ir["rows"]]
    out = []
    for j, c in enumerate(ir["columns"]):
        if j == rh:
            continue
        vals = [r[j] if isinstance(r[j], float) else None for r in ir["rows"]]
        if any(v is not None for v in vals):
            out.append((c["name"], c["unit"], vals))
    return xs, out


def narrate_bars(ir, level):
    lang, t = ir["lang"], T[ir["lang"]]
    xs, series = _series(ir)
    name, unit, vals = series[0]
    pairs = [(v, x) for v, x in zip(vals, xs) if v is not None]
    order = sorted(pairs, reverse=True)
    unit_txt = (", in " if lang == "en" else ", en ") + unit_words(unit, lang) if unit else ""
    first = t["bars"].format(y=name, x=ir["columns"][ir.get("row_header_col", 0)]["name"], n=_say_n(len(pairs), lang), unit=unit_txt)
    if len(series) > 1:
        first = first[:-1] + t["series"].format(s=_say_n(len(series), lang)) + "."
    if any(v < 0 for v, _ in pairs):
        first += " Some values are below zero." if lang == "en" else " Certaines valeurs sont négatives."
    top, bottom = order[0], order[-1]
    msg = (t["rank"].format(top=top[1], second=order[1][1], bottom=bottom[1]) if len(order) >= 3 and order[1][0] > 0.8 * top[0]
           else t["rank2"].format(top=top[1], bottom=bottom[1]))
    ledger = [p[0] for p in pairs]
    blocks = [[first, msg]]
    ratio = bottom[0] / top[0] if top[0] else None
    rel = ""
    if ratio is not None:
        for lo, hi, key in ((0.42, 0.58, "ratio_half"), (0.28, 0.38, "ratio_third"), (0.15, 0.25, "ratio_fifth")):
            if lo <= ratio <= hi:
                rel = ", " + t[key].format(top=top[1], bottom=bottom[1])
    items = pairs if len(pairs) <= 6 else order[:3] + order[-3:]
    detail = []
    for k, (v, x) in enumerate(items):
        unit_now = unit if k % 3 == 0 else ""  # unit on the first value of each group of three
        tail = rel if (v, x) == bottom else ""
        detail.append(f"{x}{' :' if lang == 'fr' else ':'} {value_words(v, unit_now, lang)}{tail}.")
    for a in range(0, len(detail), 3):
        blocks.append(detail[a: a + 3])
    if len(pairs) > 6:
        blocks.append([t["offer_more"]])
    return blocks, ledger


def narrate_pie(ir, level):
    lang, t = ir["lang"], T[ir["lang"]]
    xs, series = _series(ir)
    name, unit, vals = series[0]
    pairs = sorted([(v, x) for v, x in zip(vals, xs) if v is not None], reverse=True)
    unit = unit or "%"
    first = t["pie"].format(y=name, n=_say_n(len(pairs), lang))
    total = sum(p[0] for p in pairs)
    msg = t["pie_half"].format(top=pairs[0][1]) if pairs[0][0] > total / 2 else t["pie_top"].format(top=pairs[0][1])
    blocks, ledger = [[first, msg]], [p[0] for p in pairs]
    shown = pairs if len(pairs) <= 6 else pairs[:4]
    detail = [f"{x}{' :' if lang == 'fr' else ':'} {value_words(v, unit if k == 0 else '', lang)}." for k, (v, x) in enumerate(shown)]
    if len(pairs) > 6:
        rest = sum(p[0] for p in pairs[4:])
        ledger.append(rest)
        detail.append(t["others"].format(n=_say_n(len(pairs) - 4, lang), v=value_words(rest, unit, lang)))
    for a in range(0, len(detail), 3):
        blocks.append(detail[a: a + 3])
    return blocks, ledger


def narrate_line(ir, level):
    lang, t = ir["lang"], T[ir["lang"]]
    xs, series = _series(ir)
    name, unit, vals = series[0]
    pts = [(x, v) for x, v in zip(xs, vals) if v is not None]
    unit_txt = (", in " if lang == "en" else ", en ") + unit_words(unit, lang) if unit else ""
    first = t["line"].format(y=name, x0=pts[0][0], x1=pts[-1][0], n=_say_n(len(pts), lang), unit=unit_txt)
    if len(series) > 1:
        first = first[:-1] + t["series"].format(s=_say_n(len(series), lang)) + "."
    v0, v1 = pts[0][1], pts[-1][1]
    hi, lo = max(pts, key=lambda p: p[1]), min(pts, key=lambda p: p[1])
    change = (v1 - v0) / abs(v0) if v0 else 0
    key = "rises" if change > 0.05 else "falls" if change < -0.05 else "flat"
    msg = t[key].format(y=name, v0=value_words(v0, "", lang, approx=True), v1=value_words(v1, unit, lang, approx=True))
    rng = (hi[1] - lo[1]) or 1.0
    # the deepest local dip (or highest local bump) worth a word: at least 10 % of the range, not at an endpoint
    local = [(pts[k][1] - min(pts[k - 1][1], pts[k + 1][1]), pts[k]) for k in range(1, len(pts) - 1)]
    dips = [(d, p) for d, p in local if d <= -0.1 * rng]
    bumps = [(d, p) for d, p in local if d >= 0.1 * rng]
    if key == "rises" and dips:
        msg += t["dip"].format(x=min(dips)[1][0])
    elif key == "falls" and bumps:
        msg += t["bump"].format(x=max(bumps)[1][0])
    msg += "."
    ledger = [v0, v1, hi[1], lo[1]]
    blocks = [[first, msg, t["low"].format(v=value_words(lo[1], unit, lang), x=lo[0]), t["high"].format(v=value_words(hi[1], unit, lang), x=hi[0])]]
    if level == "full" or len(pts) <= 8:
        detail = [f"{x}{' :' if lang == 'fr' else ':'} {value_words(v, unit if k == 0 else '', lang)}." for k, (x, v) in enumerate(pts)]
        ledger += [v for _, v in pts]
        for a in range(0, len(detail), 4):
            blocks.append(detail[a: a + 4])
    else:
        blocks.append([t["offer_more"]])
    return blocks, ledger


def narrate_flowchart(ir, level):
    lang, t = ir["lang"], T[ir["lang"]]
    nodes = {n["id"]: n for n in ir["nodes"]}
    out = {}
    for e in ir["edges"]:
        out.setdefault(e["from"], []).append(e)
    starts = [n for n in ir["nodes"] if n["type"] == "start"] or ir["nodes"][:1]
    ends = [n for n in ir["nodes"] if n["type"] == "end"]
    decisions = [n for n in ir["nodes"] if n["type"] == "decision"]
    steps = [n for n in ir["nodes"] if n["type"] in ("process", "start", "end")]
    fem = lambda n: "une" if (lang == "fr" and n == 1) else _say_n(n, lang)  # décision, entrée, sortie are feminine
    first = t["flow"].format(s=_say_n(len(steps), lang), d=fem(len(decisions)), dp="s" if len(decisions) > 1 else "",
                             i=fem(len(starts)), ip="s" if len(starts) > 1 else "", o=fem(len(ends)),
                             op="s" if len(ends) > 1 else "", start=starts[0]["label"], end=ends[0]["label"] if ends else "?")
    # steps are numbered in the order a listener first hears them: breadth-first from the entry point(s)
    order, seen = [], set()
    queue = [s["id"] for s in starts] + [n["id"] for n in ir["nodes"]]
    while queue:
        nid = queue.pop(0)
        if nid in seen:
            continue
        seen.add(nid)
        order.append(nid)
        queue += [e["to"] for e in out.get(nid, []) if e["to"] not in seen]
    number = {}
    for nid in order:
        if nodes[nid]["type"] != "decision":
            number[nid] = len(number) + 1
    sentences, spoken, introduced = [], set(), set()
    YESNO = {"yes": "oui", "no": "non", "true": "vrai", "false": "faux"}

    def edge_label(e):
        lab = e["label"] or ("yes" if lang == "en" else "oui")
        return YESNO.get(lab.lower(), lab) if lang == "fr" else lab

    def step_text(nid):
        n = nodes[nid]
        if n["type"] == "decision":
            q = n["label"].rstrip("?") + ("?" if lang == "en" else " ?")
            s = t["decision"].format(label=q)
            for e in out.get(nid, []):
                tgt = nodes[e["to"]]
                lab = edge_label(e)
                if tgt["type"] == "decision":
                    s += t["ifyes_end"].format(lab=lab, label=tgt["label"])
                elif e["to"] in spoken:
                    s += " " + ("If" if lang == "en" else "Si") + f" {lab}," + t["back"].format(n=_say_n(number[e["to"]], lang)).replace(" then", "", 1).replace(" puis", "", 1)
                else:
                    s += t["ifyes"].format(lab=lab, n=_say_n(number[e["to"]], lang), label=tgt["label"])
                    introduced.add(e["to"])
            return s
        s = t["step"].format(n=_say_n(number[nid], lang), label=n["label"])
        nxt = out.get(nid, [])
        if len(nxt) == 1:
            to = nodes[nxt[0]["to"]]
            if nxt[0]["to"] in spoken and to["type"] != "decision":  # loop
                s = s[:-1] + "," + t["back"].format(n=_say_n(number[nxt[0]["to"]], lang))
            elif to["type"] == "end" and not out.get(nxt[0]["to"]):  # final box: said with the step leading to it
                s = s[:-1] + (", then step {m}, {label}." if lang == "en" else ", puis étape {m}, {label}.").format(m=_say_n(number[nxt[0]["to"]], lang), label=to["label"])
                introduced.add(nxt[0]["to"])
        return s

    for nid in order:
        if nid in introduced and nodes[nid]["type"] != "decision" and len(out.get(nid, [])) == 0:
            spoken.add(nid)  # an end node already named by the step leading to it: nothing more to say
            continue
        sentences.append(step_text(nid))
        spoken.add(nid)
    blocks = [[first]]
    for a in range(0, len(sentences), 4):
        blocks.append(sentences[a: a + 4])
    blocks.append([t["offer_flow"]])
    return blocks, []


def narrate(ir, level="brief"):
    fn = {"table": narrate_table, "bars": narrate_bars, "pie": narrate_pie, "line": narrate_line, "flowchart": narrate_flowchart}[ir["kind"]]
    blocks, ledger = fn(ir, level)
    if ir.get("title"):
        blocks[0][0] = blocks[0][0][:-1] + (", titled " if ir["lang"] == "en" else ", intitulé ") + f"\"{speak_label(ir['title'], ir['lang'])}\"."
    return blocks, ledger


def to_text(blocks):
    return "\n\n".join(" ".join(b) for b in blocks)


def to_ssml(blocks, lang):
    code = {"en": "en-US", "fr": "fr-FR"}[lang]
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    parts = [f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{code}">']
    for i, b in enumerate(blocks):
        parts.append("  <p>")
        for s in b:
            s = esc(s).replace("; ", ';<break time="300ms"/> ')
            parts.append(f"    <s>{s}</s>")
        parts.append("  </p>")
        if i < len(blocks) - 1:
            last = i == len(blocks) - 2 and blocks[-1][0].endswith("?")
            parts.append(f'  <break time="{"1s" if last else "600ms"}"/>')
    parts.append("</speak>")
    return "\n".join(parts)


# ----------------------------------------------------------------------------------------------- verify & lint
_WORD_VAL = {}
for lang_ in ("en", "fr"):
    d = {}
    for n in range(0, 100):
        d[int_to_words(n, lang_)] = n
    for n in range(100, 1000, 100):
        d[int_to_words(n, lang_)] = n
    d.update({"hundred": 100, "thousand": 1000, "million": 10 ** 6, "billion": 10 ** 9, "trillion": 10 ** 12} if lang_ == "en"
             else {"cent": 100, "cents": 100, "mille": 1000, "million": 10 ** 6, "millions": 10 ** 6, "milliard": 10 ** 9, "milliards": 10 ** 9})
    _WORD_VAL[lang_] = d


def words_to_numbers(text, lang):
    """Extract numbers spoken as words (and bare digits) from text -> list of floats."""
    d = _WORD_VAL[lang]
    toks = re.findall(r"[a-zA-Zàâçéèêëîïôûùüÿœ\-]+|\d{1,3}(?:[   ]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?|[;:.,!?]", text.lower())
    out, cur, scale_total, i = [], None, 0, 0
    dec_mode, dec_digits, neg, mult = False, [], False, 1

    def flush():
        nonlocal cur, scale_total, dec_mode, dec_digits, neg, mult
        if cur is not None or scale_total:
            v = scale_total + (cur or 0)
            if dec_digits:
                v += float("0." + "".join(str(x) for x in dec_digits))
            v *= mult
            out.append(-v if neg else v)
        cur, scale_total, dec_mode, dec_digits, neg, mult = None, 0, False, [], False, 1

    while i < len(toks):
        tk = toks[i]
        if re.fullmatch(r"[\d ,.  ]+", tk):
            flush()
            out.append(parse_number(tk, lang))
        elif tk in ("minus", "moins") and (i + 1 < len(toks) and toks[i + 1] in d):
            flush()
            neg = True
        elif tk in ("point", "virgule") and (cur is not None or scale_total):
            dec_mode = True
        elif tk == "cent" and i and toks[i - 1] == "pour" and not (i + 1 < len(toks) and toks[i + 1] in d):
            pass  # "pour cent" is a unit, not 100 ("pour cent mille euros" is still a number)
        elif lang == "en" and tk == "oh" and cur is not None and 13 <= cur <= 99 and not scale_total:
            cur *= 100  # "twenty oh five" -> 2005
        elif tk in d:
            v = d[tk]
            if lang == "en" and cur is not None and 13 <= cur <= 99 and 10 <= v <= 99 and not scale_total and not dec_mode:
                cur = cur * 100 + v  # spoken year: "twenty fifteen", "nineteen ninety-eight"
                i += 1
                continue
            if v >= 1000 and cur is None and not scale_total and not (lang == "fr" and tk == "mille"):
                flush()  # "in million euros": a unit word, not a number ("mille" alone is 1000 in French)
            elif dec_mode:
                if v >= 1000:  # "two point one million": scale the whole value
                    mult = v
                    flush()
                elif lang == "en" or v < 10:
                    dec_digits.append(v)
                else:  # fr: "virgule vingt-cinq" -> 25 as decimals
                    dec_digits += [int(c) for c in str(v)]
            elif v >= 1000:
                scale_total += (cur or 1) * v
                cur = None
            elif v == 100:
                cur = (cur or 1) * 100
            else:
                cur = (cur or 0) + v
        else:
            flush()
        i += 1
    flush()
    return [x for x in out if x is not None]


def ir_values(ir):
    vals = set()
    if ir["kind"] == "flowchart":
        return vals
    for r in ir["rows"]:
        for v in r:
            if isinstance(v, float):
                vals.add(v)
                if v != int(v):  # "twelve euros fifty": integer part and cents of a raw value spoken as two numbers
                    vals.update({float(int(v)), float(round((v - int(v)) * 100))})
    num = _numeric_cols(ir)
    for j in num:
        col = [r[j] for r in ir["rows"] if isinstance(r[j], float)]
        if col:
            vals.update({sum(col), max(col), min(col), sum(col) / len(col), max(col) - min(col)})
            if col[0]:  # percent change first -> last, and max/min ratio in percent (plain derivations a narrator states)
                vals.add(100 * (col[-1] - col[0]) / abs(col[0]))
            if min(col):
                vals.add(100 * max(col) / min(col))
    for r in ir["rows"]:  # row-wise total and pairwise differences (grouped bars: "France, total 42"; "the gap is 160")
        rv = [r[j] for j in num if isinstance(r[j], float)]
        if len(rv) >= 2:
            vals.add(sum(rv))
            vals.update(abs(a - b) for a in rv for b in rv if a != b)
    return vals


def _close(a, b):
    if b == 0:
        return abs(a) < 1e-9
    rel = abs(a - b) / abs(b)
    return rel < 0.006 or (abs(b) >= 100 and rel < 0.051)  # 3 significant figures, or "about" rounding


def verify(ir, text, lang, source_text=""):
    """Numbers in `text` not present in the data (nor a sum/max/min/mean/range of a column). Ignored: small counts
    (<= 12: positions, group sizes), the row/column/node counts, numbers that appear in labels, headers or the
    source text itself (years in a title, "20 à 39 ans"), and years spoken as words."""
    vals = ir_values(ir)
    labels = set()
    if ir["kind"] != "flowchart":
        rh = ir.get("row_header_col", 0)
        labels.update({len(ir["rows"]), len(ir["columns"])})
        for r in ir["rows"]:
            for tok in re.findall(r"\d+(?:[.,]\d+)?", str(r[rh])):
                lv = parse_number(tok, lang)
                if lv is not None:
                    labels.add(lv)
        for c in ir["columns"]:
            labels.update(float(x) for x in re.findall(r"\d+", c["name"]))
    else:
        labels.update({len(ir["nodes"]), len(ir["edges"])})
    for tok in re.findall(r"\d+(?:[.,]\d+)?", (ir.get("title") or "") + " " + (source_text or "")):
        lv = parse_number(tok, lang)
        if lv is not None:
            labels.add(lv)
    spoken = words_to_numbers(text, lang)
    bad = []
    for s in spoken:
        if s <= 12 or s in labels or any(_close(s, v) for v in vals):
            continue
        if any(_close(s * k, v) for v in vals for k in (1e3, 1e6, 1e9)):  # "2.1 million" vs 2100000, or vice versa
            continue
        if any(_close(s, v * k) for v in vals for k in (1e3, 1e6, 1e9)):
            continue
        bad.append(s)
    return bad


_LINT = [
    (r"(?<![A-Za-z\d])\d+(?:[.,]\d+)?(?![A-Za-z\d])", "bare number in digits (write it in words)"),
    (r"[%‰€$£]", "currency/percent symbol left in speech"),
    (r"[|*#_`]", "markdown or table character"),
    (r"\b\d+\s*[-–]\s*\d+\b", "range written with a dash"),
    (r"[≥≤≈±→×÷Δ∑√∞]", "math symbol not spoken"),
    (r"\b(avg|max|min|no\.|approx\.|vs\.?|etc\.|e\.g\.|i\.e\.|N/A|YoY|QoQ|env\.|moy\.|n°)\b", "abbreviation not expanded"),
    (r"\b(km/h|mg/dL|°C|km²|m²|kg|mL|k€|M€|M\$)\b", "unit abbreviation"),
]
# identifiers such as Q1, S12 are not flagged: TTS engines read "Q one". Acronyms are not counted (advisory only).


def lint(text):
    issues = []
    for pat, msg in _LINT:
        for m in re.finditer(pat, text):
            issues.append((m.start(), msg, text[max(0, m.start() - 15): m.end() + 15].replace("\n", " ")))
    return issues


# ----------------------------------------------------------------------------------------------- selftest
def selftest():
    assert number_to_words(1234.5, "en") == "one thousand two hundred thirty-four point five"
    assert number_to_words(1234.5, "fr") == "mille deux cent trente-quatre virgule cinq"
    assert number_to_words(80, "fr") == "quatre-vingts" and number_to_words(81, "fr") == "quatre-vingt-un"
    assert number_to_words(71, "fr") == "soixante-et-onze" and number_to_words(91, "fr") == "quatre-vingt-onze"
    assert number_to_words(200, "fr") == "deux cents" and number_to_words(201, "fr") == "deux cent un"
    assert number_to_words(2000000, "fr") == "deux millions" and number_to_words(1000, "fr") == "mille"
    assert number_to_words(3.25, "fr") == "trois virgule vingt-cinq" and number_to_words(1.05, "fr") == "un virgule zéro cinq"
    assert number_to_words(-3, "en") == "minus three" and number_to_words(2.1e9, "en") == "two billion one hundred million"
    assert int_to_words(10 ** 9, "fr") == "un milliard" and int_to_words(10 ** 9, "en") == "one billion"
    assert parse_number("1 234,5", "fr") == 1234.5 and parse_number("1,234.5", "en") == 1234.5
    assert parse_number("1,5", "fr") == 1.5 and parse_number("1,234", "en") == 1234 and parse_number("−3 %", "en") == -3
    assert value_words(2100000.0, "", "en") == "two point one million" and value_words(2100000.0, "", "fr") == "deux virgule un millions"
    assert value_words(12.0, "%", "fr") == "douze pour cent" and value_words(48.0, "km²", "en") == "forty-eight square kilometres"
    md = "| City | Population (millions) | Area (km²) |\n|---|---|---|\n| Paris | 2.1 | 105 |\n| Lyon | 0.5 | 48 |\n| Marseille | 0.9 | 241 |"
    ir = parse(md, None, "en")
    assert ir["columns"][1]["unit"] == "millions" and ir["rows"][0][1] == 2.1
    blocks, ledger = narrate(ir)
    txt = to_text(blocks)
    assert txt.startswith("A table with three columns and three rows: City, Population and Area.")
    assert "Paris: Population two point one million;" in txt and "Lyon: Population zero point five million;" in txt
    assert value_words(12.5, "k€", "en") == "twelve thousand five hundred euros" and value_words(0.5, "millions", "fr") == "zéro virgule cinq million"
    assert value_words(1.1, "jours", "fr") == "un virgule un jour" and value_words(7.1, "jours", "fr") == "sept virgule un jours" and value_words(1.0, "km²", "fr") == "un kilomètre carré"
    assert value_words(1.0, "°C", "fr") == "un degré Celsius" and value_words(1.5, "M€", "fr") == "un virgule cinq million d'euros"
    assert value_words(1.0, "km", "en") == "one kilometre" and value_words(1.5, "km", "en") == "one point five kilometres"
    assert value_words(1.0, "%", "fr") == "un pour cent" and value_words(0.5, "mg/dL", "en") == "zero point five milligrams per decilitre"
    assert verify(ir, txt, "en") == [], verify(ir, txt, "en")
    assert verify(ir, txt + " Nice has seven point seven million.", "en") == [7700000.0]
    assert lint(txt) == [], lint(txt)
    fr = parse(md.replace("2.1", "2,1").replace("0.5", "0,5").replace("0.9", "0,9"), None, "fr")
    txt_fr = to_text(narrate(fr)[0])
    assert "trois colonnes et trois lignes" in txt_fr and "deux virgule un" in txt_fr and verify(fr, txt_fr, "fr") == []
    bars = parse("Country,Sales (M€)\nFrance,42\nSpain,38\nItaly,25\nPortugal,9", "bars", "en")
    tb = to_text(narrate(bars)[0])
    assert tb.startswith("A bar chart of Sales by Country, four bars, in million euros.") and "about a fifth of France" in tb
    assert verify(bars, tb, "en") == [] and lint(tb) == []
    line = parse("Year;Revenue (M€)\n2015;10\n2016;12\n2017;14\n2018;16\n2019;15\n2020;11\n2021;17\n2022;21\n2023;23\n2024;25", "line", "fr")
    tl = to_text(narrate(line)[0])
    assert "monte de dix à vingt-cinq millions d'euros, avec un creux en deux mille vingt" in tl and verify(line, tl, "fr") == []
    assert year_words(2024, "en") == "twenty twenty-four" and year_words(2005, "en") == "two thousand five" and year_words(1998, "en") == "nineteen ninety-eight"
    pie = parse("Item,Share (%)\nRent,52\nFood,20\nTransport,12\nLeisure,9\nOther,7", "pie", "en")
    tp = to_text(narrate(pie)[0])
    assert "Rent takes more than half." in tp and "Rent: fifty-two percent." in tp
    mm = ("flowchart TD\n  A((Order received)) --> B[Check stock]\n  B --> C{In stock?}\n  C -->|yes| D[Pack]\n"
          "  C -->|no| E[Back-order]\n  E --> B\n  D --> F[Ship]\n  F --> G((Delivered))")
    fl = parse(mm, "flowchart", "en")
    assert [n["type"] for n in fl["nodes"]] == ["start", "process", "decision", "process", "process", "process", "end"]
    tf = to_text(narrate(fl)[0])
    assert tf.startswith("A flowchart with six steps and one decision, one entry point, one exit, from Order received to Delivered.")
    assert "Decision: In stock? If yes, step three, Pack. If no, step four, Back-order." in tf
    assert "Step four, Back-order, then back to step two." in tf and "Step five, Ship, then step six, Delivered." in tf
    assert "Step two, Check stock. Decision:" in tf and tf.count("Step two,") == 1 and tf.count("Delivered") == 2
    tfr = to_text(narrate(parse(mm, "flowchart", "fr"))[0])
    assert "Si oui, étape trois" in tfr and "Si non, étape quatre" in tfr
    ssml = to_ssml(narrate(fl)[0], "en")
    assert ssml.startswith("<speak") and '<break time="1s"/>' in ssml
    import xml.dom.minidom
    xml.dom.minidom.parseString(ssml)
    assert words_to_numbers("one thousand two hundred thirty-four point five and forty-two", "en") == [1234.5, 42]
    assert words_to_numbers("mille deux cent trente-quatre virgule cinq ; quatre-vingt-onze", "fr") == [1234.5, 91]
    assert words_to_numbers("two point one million", "en") == [2100000.0]
    assert words_to_numbers("from twenty fifteen to twenty twenty-four; in nineteen ninety-eight; twenty oh five", "en") == [2015, 2024, 1998, 2005]
    assert speak_label("Units 2023", "en") == "Units twenty twenty-three" and speak_label("0 à 19 ans", "fr") == "zéro à dix-neuf ans" and speak_label("S12", "en") == "S12"
    print("selftest ok")


# ----------------------------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["parse", "narrate", "speak", "verify", "lint", "num", "selftest"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--kind", choices=["table", "bars", "line", "pie", "flowchart"])
    ap.add_argument("--lang", default="en", choices=["en", "fr"])
    ap.add_argument("--title", default="")
    ap.add_argument("--level", default="brief", choices=["brief", "full"])
    ap.add_argument("--ssml", action="store_true")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252; spoken text may carry ≈, →, œ
    read = lambda p: open(p, encoding="utf-8").read()
    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "num":
        print(number_to_words(parse_number(a.args[0], a.lang), a.lang))
        return
    if a.cmd == "lint":
        issues = lint(read(a.args[0]))
        for pos, msg, ctx in issues:
            print(f"{pos}\t{msg}\t…{ctx}…")
        print(f"{len(issues)} issue(s)")
        return 1 if issues else 0
    if a.cmd == "verify":
        ir = json.loads(read(a.args[0]))
        bad = verify(ir, read(a.args[1]), a.lang)
        print(json.dumps({"unsupported_numbers": bad}))
        return 1 if bad else 0
    if a.cmd in ("parse", "speak"):
        ir = parse(read(a.args[0]), a.kind, a.lang, a.title)
        if a.cmd == "parse":
            print(json.dumps(ir, ensure_ascii=False, indent=1))
            return
    else:
        ir = json.loads(read(a.args[0]))
    blocks, _ = narrate(ir, a.level)
    print(to_ssml(blocks, ir["lang"]) if a.ssml else to_text(blocks))


if __name__ == "__main__":
    sys.exit(main())
