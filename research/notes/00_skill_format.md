# Note 00 — Format Agent Skills (contraintes vérifiées)

Source : https://agentskills.io/specification (consultée le 2026-11-02).

- Un skill = un dossier contenant au minimum `SKILL.md` ; dossiers optionnels `scripts/`, `references/`, `assets/`.
- Frontmatter YAML obligatoire : `name` (1–64 caractères, minuscules, chiffres, tirets ; pas de tiret en début ou fin, pas
  de `--` ; **doit égaler le nom du dossier**) et `description` (1–1024 caractères ; dire **ce que fait** le skill **et quand**
  l'utiliser, avec des mots-clés déclencheurs).
- Optionnels : `license`, `compatibility` (≤ 500 car., seulement si exigences d'environnement), `metadata` (clés → chaînes),
  `allowed-tools` (expérimental).
- Chargement progressif : métadonnées (~100 tokens) toujours chargées ; corps de `SKILL.md` (< 5 000 tokens recommandés,
  **< 500 lignes**) chargé à l'activation ; `references/` et `scripts/` chargés à la demande.
- Références : chemins relatifs à la racine du skill, **un seul niveau** de profondeur depuis `SKILL.md`.
- Validation : `skills-ref validate ./my-skill` (https://github.com/agentskills/agentskills/tree/main/skills-ref).

Conséquence pour nous : `SKILL.md` porte la méthode (ordre de lecture, règles courtes, exemples) ; les règles de
prononciation par langue, les stratégies par type de figure et le SSML vont dans `references/` ; les conversions
(Markdown/CSV/Mermaid → structure → texte/SSML) dans `scripts/`, seulement si elles servent.

# Note 00b — TTS locale disponible (vérifié)

Windows SAPI via `System.Speech` (PowerShell, aucune installation) : voix Hortense (fr-FR), Zira (en-US), Hazel (en-GB).
`SpeakSsml` vers un fichier WAV fonctionne (test : 307 Ko générés, rien joué). Les voix « Desktop » SAPI ignorent une
partie du SSML (à mesurer : `say-as`, `break`, `prosody`).
