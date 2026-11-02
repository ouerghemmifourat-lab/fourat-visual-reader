# voice-visual-reader

**An Agent Skill that teaches voice agents and text-to-speech pipelines to read tables, charts and diagrams aloud, in a
way a listener can follow.** English and French. · [Version française](#version-française)

A listener hears once, at fixed speed, cannot glance back, and holds about four items in mind. Most "read this chart"
output ignores that: it dumps cells, reads "1,234.5 km/h" as symbols, and never says what the figure is about. This skill
fixes the order and the wording:

**Announce → Message → Key figures → Offer → Detail on demand.** Short sentences, one number per sentence, groups of
three, numbers and units written as words in the target language, interpretation only when asked, and never a number
that is not in the data.

## Install

The skill follows the open [Agent Skills](https://agentskills.io/specification) format: one folder with a `SKILL.md`.

- **Claude Code / Claude.ai**: copy `skills/voice-visual-reader/` into your skills directory (for example
  `~/.claude/skills/`).
- **Other agents** (Codex, Cursor, custom LLM pipelines): give the model the content of `SKILL.md` when the output will be
  spoken; load the `references/` files it points to as needed. No dependency.

## Use

Ask anything that ends up spoken: "read me this table", "describe this chart for a voice note", "lis-moi ce tableau",
"écris le SSML de ce graphique". The skill triggers on voice, TTS, screen-reader, phone or SSML contexts.

The optional helper script needs only Python 3.9+ (standard library):

```bash
python skills/voice-visual-reader/scripts/vvr.py speak table.md --lang fr          # spoken text
python skills/voice-visual-reader/scripts/vvr.py speak flow.mmd --kind flowchart --ssml
python skills/voice-visual-reader/scripts/vvr.py verify ir.json spoken.txt --lang en  # numbers not in the data
python skills/voice-visual-reader/scripts/vvr.py lint spoken.txt                     # digits, symbols, abbreviations
python skills/voice-visual-reader/scripts/vvr.py selftest
```

It parses Markdown/CSV tables and Mermaid flowcharts, narrates tables, bar/line/pie charts and flowcharts in English or
French, writes SSML, and checks that every spoken number exists in the source.

### Example

Input:

| City | Population (millions) | Area (km²) |
|---|---|---|
| Paris | 2.1 | 105 |
| Lyon | 0.5 | 48 |
| Marseille | 0.9 | 241 |

Output of `vvr.py speak --lang en` (verbatim, `eval/outputs/script/en_table_small.txt`):

> A table with three columns and three rows: City, Population and Area.
>
> Paris has the largest Population; Lyon the smallest. Paris, Population: two point one million. Lyon: zero point five
> million.
>
> Paris: Population two point one million; Area one hundred five square kilometres. Lyon: Population zero point five
> million; Area forty-eight square kilometres. Marseille: Population zero point nine million; Area two hundred forty-one
> square kilometres.

The hand-written version in `references/examples.md` is shorter (announce, message, rows); the script adds the key-figures
block because it cannot judge when the message alone carries the point.

## What is in the repository

| Path | Content |
|---|---|
| `skills/voice-visual-reader/SKILL.md` | the method, under 150 lines |
| `skills/voice-visual-reader/references/` | tables, charts, diagrams, numbers (en, fr), SSML per engine, dialogue commands, worked examples |
| `skills/voice-visual-reader/scripts/vvr.py` | parser, narrator, SSML, number verifier, lint, self-test |
| `research/STATE_OF_THE_ART.md` | what exists (skills, repos, accessibility guidelines, research, TTS/SSML), every claim with a URL and licence; what is missing |
| `research/DESIGN.md` | the design, each rule marked sourced / practice / untested |
| `eval/` | pre-registered protocol, 34 cases (17 en, 17 fr) with expected answers, three arms (no skill, with skill, script), judge, metrics, `RESULTS.md` |

## Evidence and limits

Results of the controlled comparison are in [`eval/RESULTS.md`](eval/RESULTS.md). Read them with these limits in mind:
the judge is a language model reading the text, not a person listening; the evidence base in the literature is small
(studies of 6 to 30 blind readers, desktop screen readers, English); the bias-list and number rules for French follow
metropolitan usage (say "virgule"), Quebec usage differs. The script reads a unitless column as "header, value"
("Free beds: one") and cannot turn it into a counted noun phrase ("one free bed", "une chambre libre"), because that
needs the noun's number and, in French, its gender; the skill's prose templates leave that to the model. Nothing here
was tested with real listeners yet; that is the next step and contributions are welcome
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Licence

MIT. Ideas from the accessibility and visualisation research are cited in `research/`; no text was copied from
copyleft or unlicensed sources.

---

# Version française

**Un skill d'agent qui apprend aux agents vocaux et aux synthèses vocales à lire un tableau, un graphique ou un schéma
de manière compréhensible à l'oreille.** Anglais et français.

Un auditeur entend une fois, à vitesse fixe, ne peut pas revenir en arrière, et retient environ quatre éléments. La
plupart des lectures de figures l'ignorent : elles déversent les cellules, lisent « 1 234,5 km/h » comme des symboles et
ne disent jamais de quoi parle la figure. Ce skill fixe l'ordre et la formulation :

**Annoncer → Message → Chiffres clés → Offrir → Détail à la demande.** Phrases courtes, un nombre par phrase, blocs de
trois, nombres et unités écrits en mots dans la langue cible, interprétation seulement sur demande, et jamais un nombre
absent des données.

## Installation

Le skill suit le format ouvert [Agent Skills](https://agentskills.io/specification) : un dossier avec un `SKILL.md`.

- **Claude Code / Claude.ai** : copier `skills/voice-visual-reader/` dans le dossier des skills (par exemple
  `~/.claude/skills/`).
- **Autres agents** (Codex, Cursor, pipelines maison) : donner au modèle le contenu de `SKILL.md` quand la sortie sera
  parlée ; charger les fichiers de `references/` qu'il indique selon le besoin. Aucune dépendance.

## Utilisation

Toute demande dont la sortie sera entendue : « lis-moi ce tableau », « décris ce graphique pour une note vocale », « écris
le SSML de ce graphique ». Le skill se déclenche dans les contextes voix, synthèse vocale, lecteur d'écran, téléphone, SSML.

Le script d'aide, optionnel, ne demande que Python 3.9+ (bibliothèque standard) ; voir les commandes ci-dessus. Il analyse
les tableaux Markdown/CSV et les diagrammes de flux Mermaid, narre tableaux, barres, courbes, camemberts et flux en
français ou en anglais, écrit du SSML, et vérifie que chaque nombre prononcé existe dans la source.

## Preuves et limites

Les résultats de la comparaison contrôlée sont dans [`eval/RESULTS.md`](eval/RESULTS.md). À lire avec ces limites : le
juge est un modèle de langue qui lit le texte, pas une personne qui écoute ; la littérature repose sur de petites études
(6 à 30 lecteurs aveugles, lecteurs d'écran de bureau, anglais) ; les règles de nombres en français suivent l'usage
métropolitain (dire « virgule »), l'usage québécois diffère. Le script lit une colonne sans unité sous la forme
« en-tête, valeur » (« Lits libres : un ») et ne sait pas en faire un groupe nominal compté (« un lit libre », « une
chambre libre »), ce qui demande le nombre et le genre du nom ; les gabarits du skill laissent ce choix au modèle. Rien
n'a encore été testé avec de vrais auditeurs : c'est la prochaine étape, et les contributions sont bienvenues
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Licence

MIT. Les idées issues de la recherche en accessibilité et en visualisation sont citées dans `research/` ; aucun texte
n'a été copié de sources copyleft ou sans licence.
