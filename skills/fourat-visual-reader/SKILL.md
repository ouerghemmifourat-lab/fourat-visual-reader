---
name: fourat-visual-reader
description: Turns tables, charts (bar, line, pie, scatter), flowcharts, org charts, sequence diagrams and mind maps into natural speech that is understandable by ear and ready for text-to-speech. Use whenever output will be spoken (voice agent, TTS, phone, smart speaker, screen-reader user, "read this aloud", "lis-moi ce tableau", "décris ce graphique", "explain this chart by voice"), or when writing SSML or alt text meant to be heard. Covers English and French: structure first, then the message and key figures, then detail on demand; numbers, units, dates, percentages and symbols spoken correctly per language; short sentences, pauses, no cell-by-cell dumps.
license: MIT
metadata:
  author: Fourat Ouerghemmi
  version: "0.1.0"
  languages: "en, fr"
---

# Fourat Visual Reader

Read a table, chart or diagram **for a listener**, not a viewer. A listener hears once, at fixed speed, cannot glance back,
and holds about four items in mind. Everything below follows from that.

## The method in one breath

**Announce → Message → Key figures → Offer → Detail on demand.** Short sentences, one number per sentence, groups of
three, a pause between groups. Numbers come from the data, never from guessing. Interpretation only when asked.

## Step 1 — Get the data, not the picture

- Prefer the underlying data: a Markdown/CSV/HTML table, a chart spec (Vega, Plotly, Chart.js), a Mermaid/Graphviz/
  PlantUML source, or the document text around the figure.
- If you only have an image, say so in the first sentence ("I'm reading this from the image, so values are approximate"),
  read only what is legible, and offer to work from the data if the user can provide it. Never invent a value.
- Run `scripts/vvr.py` when the input is machine-readable: it parses Markdown/CSV tables and Mermaid flowcharts into a
  JSON structure, produces the spoken text in English or French, and checks every spoken number against the data.

```bash
python scripts/vvr.py speak table.md --lang en            # announce + message + key figures + offer
python scripts/vvr.py speak table.md --lang fr --level full   # ...plus the rows, in groups of three
python scripts/vvr.py speak flow.mmd --kind flowchart --lang en --ssml   # SSML output
python scripts/vvr.py verify ir.json spoken.txt --lang fr  # numbers in the text that are not in the data
python scripts/vvr.py lint spoken.txt                       # digits, symbols, abbreviations, markdown left in speech
```

> The templates below are written with digits and symbols for brevity. When you speak them, every number, unit and
> symbol becomes words in the target language (Step 6 and the `numbers-*.md` references).

## Step 2 — Announce (one sentence, under 20 words)

Say what it is, its title, and its size, so the listener can decide how much to hear.

- Table: "A table with 4 columns and 12 rows: city, population, area and density."
- Chart: "A line chart of monthly revenue from January to December 2024, two series: online and stores."
- Diagram: "A flowchart with 7 steps and 2 decisions, from order received to delivery."

Over 6 columns or 6 series: name the first three, then "and 4 more". Do not read the full legend here.

## Step 3 — Message (one sentence, plain words)

What the figure says, as the author would summarise it. Use the caption or surrounding text when it exists. Describe
trends in everyday language ("rises steadily", "falls then levels off", "Paris is far ahead"), not statistics jargon.
Blind readers rank this level, with the key figures, as the most useful; a construction-only description is "almost
useless" to them.

## Step 4 — Key figures (two or three sentences, one number each)

The values that support the message: the largest and the smallest, the first and the last, the total, the gap. Give each
number with its label and unit: "The highest is Tokyo, 37 million." Keep the printed precision up to three significant
figures; beyond that, round and say "about"; keep the exact value for when it is requested.

## Step 5 — Offer, then detail only on request

End with one short question that names the options: "I can read it row by row, go through one column, or compare two
cities. What would you like?" In a single-turn setting (no dialogue), read small figures fully; for medium and large ones
the closing offer is still mandatory, as a sentence naming what can be asked ("Ask for a row, a column or a comparison
for more.").

When reading detail:
- **Groups of three or four**, then a pause. Start each group with the position: "Rows 4 to 6 of 12."
- **Every value with its header** when a row has more than two values: "Lyon: population 0.5 million; area 48 square
  kilometres." Listeners forget column names; the header is cheap, re-listening is not.
- Never dump a large table or every point of a long series. Offer a smaller table instead: top five, one column, a
  filter, a sort.
- Commands to honour: continue, repeat, back, row N / name, column X, compare A and B, maximum / minimum / total,
  summary, details, where am I, why (interpretation, labelled as such), stop. See [dialogue.md](references/dialogue.md).

## Per-type strategies

| Type | Lead with | Detail unit | Reference |
|---|---|---|---|
| Table | dimensions, column names, common unit; largest/smallest of the main numeric column | row (header + name:value pairs) | [tables.md](references/tables.md) |
| Bar chart | ranking and gap ("almost double") | bar, in chart order, all if ≤ 6 else top 3 / bottom 3 | [charts.md](references/charts.md) |
| Line chart | overall trend with first and last values; peak and trough with dates | time segments, never point by point beyond 8 points | [charts.md](references/charts.md) |
| Pie / donut | dominant share, whether it exceeds half | shares, largest to smallest, "the other N total X percent" | [charts.md](references/charts.md) |
| Scatter | number of points, relationship in plain words, named extremes | labelled points | [charts.md](references/charts.md) |
| Org chart | who leads, how many direct branches, depth | one branch at a time, "N reports" instead of listing beyond 4 | [diagrams.md](references/diagrams.md) |
| Flowchart | step and decision counts, entry and exit points, what the process does | numbered steps; decisions as questions with both outcomes; "back to step N" for loops; "joins step N" for merges | [diagrams.md](references/diagrams.md) |
| Sequence diagram | participants in order, number of messages, the scenario | "from A to B: message", groups of 3 to 4 | [diagrams.md](references/diagrams.md) |
| Mind map | centre, number of main branches | one branch at a time, outward | [diagrams.md](references/diagrams.md) |

## Speaking numbers, units, dates, symbols

Write them as words in the target language **before** any TTS. SSML `say-as` differs by engine and is not a safety net.
Full rules: [numbers-en.md](references/numbers-en.md), [numbers-fr.md](references/numbers-fr.md). The essentials:

| | English | French |
|---|---|---|
| 1,234.5 / 1 234,5 | one thousand two hundred thirty-four point five | mille deux cent trente-quatre virgule cinq |
| 10⁹ | billion | **milliard** (never "billion") |
| 12 % | twelve percent | douze pour cent |
| 10–15 | from 10 to 15 | de 10 à 15 |
| −3 | minus three | moins trois |
| km/h, mg/dL, °C | kilometres per hour, milligrams per decilitre, degrees Celsius | kilomètres par heure, milligrammes par décilitre, degrés Celsius |
| 2024 (year) | twenty twenty-four | deux mille vingt-quatre |
| 03/03/2024 | March third, twenty twenty-four | le trois mars deux mille vingt-quatre |
| ≥, ≈, ±, → | at least, about, plus or minus, leads to | au moins, environ, plus ou moins, mène à |
| GDP, PIB | spell out once then the acronym; spell letters only if unpronounceable | développer une fois, puis le sigle |
| empty cell, — | "no value", "not applicable", "zero" as the table means it | « vide », « non applicable », « zéro » |

Long digit strings (phone, IDs): groups of three or four with pauses. Decimals: at most two spoken decimals in a
summary; say "about" when rounding.

## Output formats

1. **Plain spoken text** (always): sentences end with a full stop; cells separated by semicolons; a blank line between
   groups; no Markdown, no `|`, `-`, `*`, `#`, no abbreviations, no bare digits where a word is safer.
2. **SSML** (when the engine accepts it): wrap the same text; `<break time="300ms"/>` between cells, `600ms` between
   rows and groups, `1s` before a question. Keep to `speak`, `p`, `s`, `break`, `sub`, `say-as` for `characters`,
   `date`, `time`. Engine differences and what each one ignores: [ssml-engines.md](references/ssml-engines.md).

## Honesty rules

- Every spoken number must exist in the source or be a plain derivation (sum, difference, ratio) that you state as such.
- Say "I can't tell from this" when the figure does not show it. Do not guess from an image.
- Mark interpretation: "My reading is that…" / « Mon interprétation : … ». Give it only when asked.
- Do not repeat the title, source and byline the host application already announces.

## Worked examples

Short English and French examples for every type, with the expected spoken output, are in
[examples.md](references/examples.md). Use them as templates for tone and length.
