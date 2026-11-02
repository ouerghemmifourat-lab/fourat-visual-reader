# Protocole d'évaluation (fixé avant de produire les sorties)

Date : 2026-11-02. Les critères viennent de `research/DESIGN.md` § 8, avec trois changements faits **avant** de produire
les sorties : la cible « un nombre par phrase » devient « ≤ 1,5 en moyenne » (une phrase de comparaison porte souvent deux
nombres) ; la lecture humaine des chiffres est remplacée par la vérification automatique plus l'inspection des cas
signalés ; le juge lit le texte entier, pas seulement les étapes 0 à 2. Rien n'est ajusté après avoir vu les résultats ;
toute déviation ou métrique ajoutée après coup est notée dans `RESULTS.md` avec le suffixe « post hoc ».

**Dispositif du juge** : pour chaque cas, le juge reçoit les deux textes côte à côte sous les étiquettes A et B,
attribuées au hasard par cas (`judge/key.json` ; A = skill dans 22 cas sur 34), sans la figure et sans le nom des bras,
et note chaque texte séparément. La présentation côte à côte peut laisser filtrer la longueur ou le style ; c'est une
limite du dispositif.

## Cas

`cases.json` : 34 cas, 17 en anglais et 17 en français, couvrant tableau (petit, moyen, grand, en-têtes multiples,
cellules vides), barres (simples, groupées, négatives), courbes (une et plusieurs séries, creux), camembert, nuage de
points, organigramme, diagramme de flux (boucle, fusion), séquence, carte mentale, image seule, et une demande
d'interprétation. Chaque cas porte : la donnée source, la langue cible, le type, et **trois questions** avec leur réponse
attendue (une valeur, une tendance ou un rang, un fait de structure).

Les données sont synthétiques ou de notoriété publique (aucune donnée privée ni médicale réelle).

## Deux bras, même modèle, même consigne de base

- **Sans skill** : le modèle reçoit la figure et la consigne « Lis ceci à voix haute pour un auditeur ; produis le texte
  exact à envoyer à une synthèse vocale », dans la langue du cas. Rien d'autre.
- **Avec skill** : la même consigne, précédée du contenu de `SKILL.md` et des références pertinentes, comme le ferait un
  agent qui a activé le skill. Le modèle **n'exécute pas** `vvr.py` (on mesure la méthode, pas le script).

Modèle des deux bras : Claude Sonnet (effort medium), un seul passage, température par défaut. Les sorties sont écrites
telles quelles dans `outputs/<bras>/<id>.txt`.

## Mesures automatiques (`run_eval.py`)

1. **Exactitude des chiffres** (cas à données structurées) : nombres prononcés absents de la source et de ses dérivées
   simples (somme, max, min, moyenne, étendue), via `vvr.verify`. Métrique : nombre de nombres non soutenus par cas ; part
   des cas sans aucun nombre non soutenu.
2. **Ordre** : la première phrase annonce le type et une taille (motif : mot du type + nombre + colonnes/lignes/barres/
   points/étapes/parts) ; une question ou une offre apparaît dans la sortie quand la figure est moyenne ou grande.
3. **Longueur** : mots avant la première question (cible ≤ 60 pour les figures moyennes et grandes) ; mots au total ;
   nombres par phrase (cible ≤ 1,5 en moyenne).
4. **Prononçabilité** : problèmes `vvr.lint` (chiffres bruts, symboles, abréviations, Markdown, tiret d'intervalle,
   unités abrégées) par 100 mots.

## Compréhension à l'écoute (juge)

Un modèle **différent** (Claude Fable 5.1) reçoit, pour chaque cas et chaque bras, **uniquement le texte parlé** (sans la
figure, sans le nom du bras) et les trois questions. Il répond ou dit « non dit ». Une réponse est correcte si elle
équivaut à la réponse attendue (tolérance : arrondi à 3 chiffres significatifs, synonymes de tendance). Métrique :
part de réponses correctes par bras ; part de « non dit ».

Limite assumée : un modèle qui lit n'est pas un humain qui écoute ; cette mesure approxime « l'information est-elle
présente, sans la figure ». Elle ne mesure ni la charge mentale ni l'agrément.

## Audio (fichiers seulement)

Pour 6 cas (3 FR, 3 EN), la sortie « avec skill » est synthétisée en WAV par Windows SAPI (Hortense, Zira), sans
lecture sur haut-parleurs. On note la durée et le débit en mots par minute. Aucun test d'écoute humaine.

## Seuils de succès (pré-enregistrés)

- Chiffres : ≥ 90 % des cas structurés sans nombre non soutenu, bras skill ; au moins aussi bien que le bras sans skill.
- Ordre : annonce en première phrase dans ≥ 90 % des cas, bras skill.
- Longueur : médiane des mots avant la première question ≤ 60, bras skill.
- Prononçabilité : < 1 problème lint pour 100 mots, bras skill, et moins que le bras sans skill.
- Compréhension : part de réponses correctes du bras skill ≥ celle du bras sans skill ; différence rapportée avec un
  intervalle bootstrap par cas (2 000 tirages).

Si un seuil n'est pas atteint, on le dit, on ne le déplace pas.
