# Résultats de l'évaluation (2026-11-02)

Protocole : `PROTOCOL.md`, fixé avant les sorties. Cas : `cases.json` (34 ; 17 en, 17 fr). Sorties : `outputs/`.
Verdicts du juge : `judge/`. Métriques : `metrics.json` (`python run_eval.py`).

Une relecture indépendante (second modèle, lecture seule) a été faite avant publication. Elle a relevé un résultat
artefactuel (longueur avant la première question, voir ci-dessous), un exemple de README qui ne correspondait pas à la
sortie réelle du script, un plantage d'encodage sous Windows et des incohérences entre références. Tout est corrigé ou
déclaré ici ; les chiffres ci-dessous sont ceux recalculés après correction des outils de mesure (pas des seuils).

## Bras

| Bras | Qui produit | Ce qu'il voit |
|---|---|---|
| **sans skill** | Claude Sonnet, un passage | la figure + « Lis ceci à voix haute pour un auditeur ; produis le texte exact à envoyer à une synthèse vocale » |
| **avec skill** | Claude Sonnet, un passage | la même consigne, après lecture de `SKILL.md` et des 8 références ; **sans** exécuter le script |
| **script** | `vvr.py` seul, déterministe | les 27 cas à données structurées (tableaux, barres, courbes, camemberts, flux Mermaid) |

Juge : Claude Fable 5.1, texte seul, sans la figure ; les deux textes d'un cas lui sont présentés côte à côte sous des
étiquettes A/B tirées au hasard (`judge/key.json`) ; il note chaque texte séparément. Limite : la présentation côte à
côte peut laisser filtrer la longueur ou le style.

## Résultats par rapport aux seuils pré-enregistrés

| Critère (seuil) | sans skill | **avec skill** | script | Seuil atteint ? |
|---|---|---|---|---|
| Annonce en première phrase : mot du type **+ nombre + mot de taille** (≥ 90 %) | 41,2 % | **91,2 %** | 100 % | **oui** |
| Prononçabilité : problèmes lint pour 100 mots (< 1, et < sans skill) | 14,42 | **0,00** | 0,00 | **oui** |
| Cas sans aucun problème lint | 23,5 % | **100 %** | 100 % | — |
| Chiffres : cas structurés sans nombre non soutenu (≥ 90 %, et ≥ sans skill) | 100 % (27/27) | **92,6 %** (25/27) | 100 % | **partiel** : ≥ 90 % oui ; « au moins aussi bien » **non** (§ Chiffres) |
| Longueur : médiane des mots avant la première **question** (≤ 60) | — | **non mesurable** | — | **non évalué** : les seuls « ? » du bras skill sont des questions de décision dans les flux (« En stock ? »), pas des offres ; le compteur les prenait pour des offres. Remplacé par la métrique post hoc ci-dessous |
| Nombres par phrase (≤ 1,5 en moyenne) | 1,79 | **1,63** | 1,42 | **non** pour le bras skill |
| Compréhension (juge) : réponses correctes (≥ sans skill) | 98,0 % (100/102) | **99,0 %** (101/102) | — | **oui**, différence non significative |
| Compréhension : « non dit » / fausses | 2,0 % / 0 % | 1,0 % / 0 % | — | — |

**Compréhension, skill − sans skill : +1,0 point, IC 95 % bootstrap par cas [−2,0 ; +3,9]. Aucune différence
démontrée.** Les deux bras transmettent presque toute l'information ; un modèle récent sans consigne est déjà bon sur ce
point.

### Métriques ajoutées après coup (déclarées comme telles)

| Métrique post hoc | sans skill | avec skill | script |
|---|---|---|---|
| Textes contenant une **offre** de détail (phrase ou question) | 8,8 % (3/34) | 23,5 % (8/34) | 55,6 % |
| Offre présente sur les **4 tableaux moyens et grands** | 50 % (2/4) | **100 %** (4/4) | 100 % |
| Médiane des mots avant la première offre (quand il y en a une) | 92 | 69 | 49 |

Dans le bras skill, les 8 offres sont : les 4 tableaux moyens et grands, les 2 organigrammes, les 2 cas d'image. Les
figures petites sont lues en entier sans offre, comme le prévoit la règle du mode un tour. Le seuil « ≤ 60 mots avant
l'offre » n'est donc **pas** atteint par le bras skill (69) ; le script y est (49).

### Ce que le skill change vraiment

1. **La prononçabilité.** 14,4 problèmes pour 100 mots → 0 ; 76,5 % des textes sans skill contiennent des chiffres bruts
   (« 980 », « 12.50 », « 0,50 »), des symboles ou des unités abrégées ; aucun des 34 textes avec skill. C'est le gain le
   plus net et il ne dépend pas d'un juge.
2. **La structure.** 41 % → 91 % des textes commencent par le type, une taille chiffrée et ce qu'elle compte. Les trois
   manques du bras skill : les deux cas d'image (le texte commence, à dessein, par « je lis une image ») et une courbe.
3. **Les cas d'image.** Sans skill, pour les deux images floues, une valeur approximative est donnée là où la question
   attendait « illisible » (2/3 chacun) ; avec skill, 3/3.
4. **Boucles et fusions des flux** dites explicitement dans les 4 cas (« retour à l'étape deux », « rejoignent l'étape
   sept », « les étapes deux et quatre forment une boucle ») ; sans skill, en prose moins régulière mais présentes.

### Ce que le skill coûte

- **Longueur : +40 % de mots** (médiane 57,5 → 80,5). En audio Windows SAPI (≈ 95–140 mots/min), `en_table_small`
  passe de 20 s à 31 s, `fr_table_small` de 24 s à 36 s. Le gain de compréhension mesuré ne compense pas ce coût ; le coût
  est le prix de la robustesse à la synthèse (mots au lieu de chiffres, en-têtes répétés).
- **Un détail perdu** sur `fr_table_medium` : la règle « tableau moyen : annonce, message, chiffres clés, offre » n'a
  pas lu la note de français de Bastien, d'où un « non dit ». Compromis voulu (détail à la demande) qui, sans dialogue,
  coûte une réponse.
- **Nombres par phrase** : 1,63, au-dessus de la cible 1,5 ; les phrases de comparaison en portent deux.

### Chiffres non soutenus par la source (bras skill : 2 cas sur 27)

- `fr_table_medium` : « notes sur vingt » — connaissance du domaine exacte, mais le 20 n'est pas dans la donnée.
- `fr_nuage` : une valeur « 1 000 » détectée par l'extracteur de nombres en mots ; tous les prix du texte sont dans la
  donnée ; non retracée à un nombre inventé, probable artefact du découpage. Comptée quand même.
- Le bras sans skill (0 non soutenu) écrit les nombres en chiffres : plus facile à vérifier, mais ce sont ces chiffres
  bruts qui gênent la synthèse.

Le vérificateur a été corrigé pendant l'analyse pour accepter des dérivations légitimes énoncées comme telles (total
d'une ligne, écart entre deux colonnes, variation en pour cent, « douze euros cinquante » lu en deux nombres, « 7 900 »
avec espace, années dites en mots). Corrections d'outil, appliquées aux trois bras ; aucun seuil n'a bougé.

## Audio (fichiers, non écoutés)

10 WAV produits dans `audio/` (ignorés par git ; 6 skill, 2 sans skill, 2 script) avec les voix Windows Hortense (fr) et
Zira (en) : 94–139 mots/min. Aucun test d'écoute humaine ; les fichiers vérifient que les textes se synthétisent sans
erreur et donnent les durées.

## Limites

1. Le **juge est un modèle qui lit**, pas une personne qui écoute : la parité 98–99 % dit « l'information est dans le
   texte », pas « l'auditeur la retient ».
2. **Un passage** par cas et par bras ; variance entre passages non mesurée.
3. Le bras sans skill est **déjà un modèle récent** ; l'écart mesuré part de là, pas d'une lecture cellule par cellule.
4. Cas **synthétiques**, ≤ 32 lignes, pas de donnée réelle bruitée.
5. Règles françaises **métropolitaines** ; Québec, Belgique, Suisse non testés.
6. Le script ne couvre que les 27 cas structurés (pas d'organigramme, séquence ni carte mentale).
7. Tout le projet (recherche, conception, skill, évaluation) a été produit en quelques heures avec des agents de langue ;
   le « pré-enregistrement » est une discipline interne, pas un dépôt externe horodaté.

## Conclusion

- **Démontré** : avec le skill, les textes sont prononçables (0 chiffre brut, 0 symbole, 0 abréviation dans 34/34),
  commencent par la structure (91 %) et offrent la suite sur tous les tableaux moyens et grands, sans perte d'information
  mesurable (99 % contre 98 %).
- **Non démontré** : un gain de compréhension ; textes plus longs de 40 % ; offre à 69 mots au lieu de 60.
- **Avant une version 1.0** : raccourcir l'annonce et les chiffres clés pour tenir 60 mots avant l'offre, ramener la
  moyenne à ≤ 1,5 nombre par phrase, et tester avec des auditeurs réels.
