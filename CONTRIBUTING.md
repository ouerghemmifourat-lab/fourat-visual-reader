# Contributing / Contribuer

**English** · [Français ci-dessous](#français)

## What helps most

1. **A new language.** Add `skills/voice-visual-reader/references/numbers-<lang>.md` (numbers, units, dates, symbols as
   spoken in that language), sentence templates in `scripts/vvr.py` (`T[...]`, `UNITS[...]`, `int_to_words`), and at least
   6 evaluation cases in `eval/make_cases.py` with expected answers. Say which rules are sourced and which are practice.
2. **Evaluation cases.** Real-world shapes we do not cover yet (histograms, Gantt, Sankey, maps…), with three questions each.
   Synthetic or public data only; nothing private, nothing medical about real people.
3. **Engine notes.** Corrections to `references/ssml-engines.md`, with the official URL and the date you checked.
4. **Bug reports on spoken output**: give the input, the language, the output you got and what a listener misunderstood.

## Rules

- Keep `SKILL.md` under 500 lines; put detail in `references/`.
- `python skills/voice-visual-reader/scripts/vvr.py selftest` must pass. The script is standard-library only.
- Every claim in `research/` carries a URL. Mark unverified items as such.
- Do not copy text from copyleft or unlicensed sources (see `research/STATE_OF_THE_ART.md` § 4).
- Measured improvements only: run `eval/run_eval.py` before and after, and report both numbers.

## Français

### Ce qui aide le plus

1. **Une nouvelle langue** : `references/numbers-<lang>.md`, les gabarits de phrases dans `scripts/vvr.py`, et au moins 6
   cas d'évaluation avec réponses attendues. Distinguer les règles sourcées des pratiques.
2. **Des cas d'évaluation** pour les figures non couvertes (histogrammes, Gantt, Sankey, cartes…), trois questions chacun.
   Données synthétiques ou publiques seulement ; rien de privé ni de médical sur des personnes réelles.
3. **Des notes sur les moteurs** : corrections de `references/ssml-engines.md`, avec l'URL officielle et la date.
4. **Des rapports de bogue sur la sortie parlée** : l'entrée, la langue, la sortie obtenue, ce qu'un auditeur a mal compris.

### Règles

- `SKILL.md` reste sous 500 lignes ; le détail va dans `references/`.
- `python skills/voice-visual-reader/scripts/vvr.py selftest` doit passer. Le script n'utilise que la bibliothèque standard.
- Toute affirmation de `research/` porte une URL ; l'incertain est marqué.
- Pas de copie de sources copyleft ou sans licence (voir `research/STATE_OF_THE_ART.md` § 4).
- Amélioration mesurée seulement : `eval/run_eval.py` avant et après, les deux chiffres dans la demande.
