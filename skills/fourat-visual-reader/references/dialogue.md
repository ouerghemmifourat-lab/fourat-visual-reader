# Dialogue: turns, commands, wayfinding

A listener cannot scan. The agent therefore reads in short turns, offers the next step, and answers a fixed set of
commands. Phrasing below is a template; adapt to the agent's voice, keep the behaviour.

## Turn shape

1. Content: one group (3 to 4 items) or one answer.
2. Position when it helps: "Rows 4 to 6 of 12", "Step 3 of 7", "Branch Finance".
3. One short offer or question, with the options named: "Next three, or a different column?"
Never two questions in one turn. Never a question after "stop".

## Commands

| Listener says (EN / FR) | Agent does |
|---|---|
| continue, next, yes, go on / continue, suite, oui | next group; position first |
| repeat / répète | the last group, identical words |
| back, previous / reviens, précédent | previous group |
| row 5, "Paris" / ligne 5, « Paris » | that row, every value with its header |
| column Population / colonne Population | that column, top to bottom, groups of 3 to 4 |
| compare Paris and Lyon / compare Paris et Lyon | both rows, column by column, relation in words |
| maximum, minimum, total, average / le plus grand, le minimum, le total, la moyenne | the statistic with header and unit; say the operation |
| summary / résume | back to announce + message + key figures |
| details, everything / détails, tout | full linear read, in groups, with a stop offer every 3 groups |
| where am I / où en suis-je | figure, current row or step, header, unit |
| what does that mean, why / qu'est-ce que ça veut dire, pourquoi | interpretation, opened with "My reading is…" / « Mon interprétation : » |
| slower, faster / plus lent, plus vite | adjust (prosody rate if SSML; shorter sentences otherwise) |
| stop / stop, arrête | stop, no question |

Unrecognised request: say what you can do, in three options, then wait.

## Wayfinding rules

- Position at the start of each group, not each item.
- After an interruption, repeat the last label before continuing ("We were at Lyon. Next: Marseille…").
- When the listener asks "which is which", restore full headers for the rest of the session.
- Headers repeat in every row when the row has more than two values; with two values, after the first group they may be
  dropped if the order is obvious.

## Single-turn mode (no dialogue possible)

Written answer meant for a TTS, a voice note, an email read aloud:
- small figure: announce, message, full detail in groups;
- medium or large: announce, message, key figures, then one sentence saying what can be asked ("Ask for a row, a column,
  or a comparison for more.").

## Interpretation (level 4)

Only when asked. Open with the marker, keep to two sentences, separate fact from reading: "The data show a drop in
2020. My reading is that this matches the pandemic year, but the chart does not say why."

## Uncertainty

"I can't tell from this figure." "The image is too small to read the values; I can give the labels." "The parts sum to
98 percent as printed." Never fill a gap with a guess.
