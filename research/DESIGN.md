# Conception — comment dire un tableau, un graphique ou un schéma

Date : 2026-11-02. S'appuie sur `STATE_OF_THE_ART.md`. Chaque règle est marquée **[V]** si une source la soutient,
**[P]** si c'est une pratique raisonnée que l'évaluation devra tester, **[NT]** si elle n'est pas testée ici.

## 1. Principes

1. **Structure, puis essentiel, puis détail à la demande.** [V] Lecteurs d'écran (JAWS annonce les dimensions), Olli,
   Chart Reader, études de Zong et Wang : vue d'ensemble d'abord, puis forage. La structure reste **brève** : L1 seul est
   « presque inutile » (Lundgard & Satyanarayan).
2. **Les chiffres et la tendance en langage courant priment.** [V] L2 + L3 sont les niveaux les plus utiles aux lecteurs
   aveugles ; l'interprétation (L4) n'est donnée que sur demande et annoncée comme une interprétation (63 % la refusent).
3. **Jamais un chiffre qui n'est pas dans la source.** [V] Les modèles de vision hallucinent. L'agent lit la table, la
   spécification ou le texte source ; s'il n'a qu'une image, il le dit et donne des ordres de grandeur étiquetés
   « approximatif ». Il sait dire « je ne peux pas le lire ».
4. **Petits blocs.** [V] Mémoire de travail d'environ 4 blocs (Cowan) ; 3 éléments par bloc par défaut (Google « Rule of
   three »), puis une pause et une offre de continuer. Les menus larges valent mieux que les imbriqués (Commarford) : on
   évite les sous-niveaux de sous-niveaux.
5. **Une idée par phrase, l'information clé en fin de phrase.** [V] W3C COGA ; Amazon « focal information at the end ».
6. **Normaliser avant de synthétiser.** [V] La lecture d'un nombre dépend du contexte (Zhang & Sproat) ; les moteurs se
   contredisent ; SSML ne normalise rien. L'agent écrit les nombres, unités, dates et symboles en mots selon la langue, et
   n'ajoute du SSML que si le moteur l'accepte.
7. **Repères sans encombrement.** [P] Le lecteur d'écran dit « liste de 4 éléments » ; la parole doit le remplacer par
   des ordinaux et des rappels d'en-tête, mais seulement quand l'auditeur risque de se perdre (JAWS laisse l'utilisateur
   régler la verbosité).
8. **Toujours proposer la suite, jamais l'imposer.** [P] Fin de chaque bloc : une question courte (« je continue ? »,
   « la colonne suivante ? »). Les commandes reconnues sont fixes : répète, reviens, suivant, ligne n, colonne X, résumé,
   détail, stop.

## 2. Ordre de lecture général (toutes figures)

| Étape | Contenu | Longueur cible [P] | Niveau |
|---|---|---|---|
| 0. Annonce | ce que c'est, son titre, sa taille (« un tableau de 4 colonnes et 12 lignes », « une courbe sur 10 ans ») | 1 phrase, ≤ 20 mots | L1 |
| 1. Message | ce que la figure dit, en une phrase de langage courant ; si une source le fournit (titre, légende, texte voisin), le reprendre | 1 phrase, ≤ 25 mots | L3 |
| 2. Chiffres clés | 2 à 3 valeurs qui soutiennent le message : extrêmes, total, écart | 1 à 3 phrases, un nombre par phrase | L2 |
| 3. Offre | « Je peux lire les détails ligne par ligne, une colonne, ou comparer deux éléments. » | 1 phrase | — |
| 4. Détail | selon la demande, par blocs de 3 à 4 éléments, en-tête rappelé à chaque bloc | blocs | L1/L2 |
| 5. Interprétation | seulement si demandée ; commence par « Interprétation : » ou « À mon avis » | ≤ 2 phrases | L4 |

Budget total avant la première offre : **≤ 60 mots, ≈ 25 secondes** à 150 mots/min. [P] Aucune source ne donne ce
chiffre ; il est fixé pour être mesuré.

## 3. Stratégie par type

### 3.1 Tableau

- **Annonce** : nombre de colonnes, de lignes (hors en-tête), nom des colonnes dans l'ordre, unité commune si elle existe.
  Au-delà de 6 colonnes : les 3 premières, puis « et n autres : … » à la demande. [P]
- **Message** : ce que le tableau compare (lignes = quoi, colonnes = quoi) et la lecture dominante (le plus grand, le
  plus petit, la somme, la tendance d'une colonne). [V] Wang 2024 : statistiques après la vue d'ensemble.
- **Détail par ligne** : « Ligne 3, Paris : population 2,1 millions ; superficie 105 kilomètres carrés. » L'en-tête de
  ligne d'abord, puis « nom de colonne + valeur », séparés par une pause. Jamais de valeur sans son en-tête quand la ligne a
  plus de 2 valeurs. [V] Les utilisateurs oublient le nom de colonne (Wang).
- **Détail par colonne** : « Colonne Population, de haut en bas : Paris 2,1 millions ; Lyon 0,5 million ; … » par blocs
  de 3 à 4.
- **Position** : « ligne 3 sur 12 » au début de chaque bloc, pas à chaque ligne. [P]
- **Cellules vides et symboles** : « vide », « non disponible », « zéro » ; un tiret se dit selon le sens (« quantité
  nulle », « non applicable ») ; une note de bas de page se dit « note » (NCAM). [V]
- **Taille** :
  - petit (≤ 4 colonnes et ≤ 6 lignes) : annonce + message + lecture complète par lignes sans attendre ;
  - moyen (≤ 8 colonnes, ≤ 30 lignes) : annonce + message + chiffres clés + offre ;
  - grand (au-delà) : annonce + message + chiffres clés + **proposer un sous-tableau** (filtrer, trier, les n premiers)
    avant toute lecture linéaire. [V] Zong : au plus 20–30 lignes parcourues ; Wang : sous-ensembles à la demande.
- **Tableaux à en-têtes multiples** : les scinder en plusieurs tableaux simples et dire combien il y en a (NCAM). [V]

### 3.2 Barres (simples, groupées, empilées)

- **Annonce** : type, ce que mesurent les barres, nombre de catégories, unité, et pour les barres groupées le nombre de
  séries (« trois barres par pays »).
- **Message** : le classement dominant (« les ventes sont les plus fortes en France, puis en Espagne ») ou l'écart.
- **Chiffres** : la plus haute, la plus basse, et l'écart ou le rapport (« presque le double »). [V] L2.
- **Détail** : toutes les barres si ≤ 6, dans l'ordre du graphique, en blocs de 3 ; sinon le top 3, le bas 3, et le
  reste à la demande. Empilées : par barre, le total puis les composantes ; ou par composante, à la demande.
- **Arrondir pour l'oreille** : la précision affichée est gardée si ≤ 3 chiffres significatifs, sinon on arrondit et on
  dit « environ ». [P] La valeur exacte reste disponible sur demande (« exactement 1 234,56 »).

### 3.3 Courbes (séries temporelles, nuages)

- **Annonce** : type, grandeur, période ou axe des x (« de 2015 à 2024, une valeur par an »), nombre de séries.
- **Message** : la tendance globale en langage courant (« augmente régulièrement », « chute puis se stabilise »), avec
  début et fin (« de 10 à 25 »). [V] L3 en langage courant.
- **Chiffres** : premier point, dernier point, pic et creux avec leur date. Pour plusieurs séries : la relation (« la
  courbe A reste au-dessus de B, l'écart se resserre »). [V]
- **Détail** : par segments (« de 2015 à 2018 : … »), jamais point par point au-delà de 8 points sans demande. [V]
  Highcharts : ne pas exposer tous les points d'une grande série.
- **Nuage de points** : nombre de points, corrélation en langage courant, valeurs extrêmes nommées si étiquetées. Pas de
  coefficient sans demande.

### 3.4 Camembert et anneau

- **Annonce** : type, ce que représente l'ensemble, nombre de parts.
- **Message** : la part dominante et si elle dépasse la moitié ; les parts se lisent du plus grand au plus petit, en
  pourcentage, et l'on dit la somme des « autres ». [P]
- **Détail** : toutes les parts si ≤ 6 ; sinon les 4 plus grandes et « les n autres totalisent x pour cent ».
- Les pourcentages se disent en entiers si la figure les donne ainsi ; on ne reconstruit pas de décimale.

### 3.5 Organigramme (hiérarchie)

- **Annonce** : type, sommet, nombre de niveaux, nombre de personnes ou d'unités.
- **Message** : qui dirige, combien de branches directes.
- **Détail** : en profondeur limitée : le sommet et ses enfants directs (bloc), puis par branche à la demande (« la
  branche Finance : … »). Dire « n subordonnés » plutôt que de les énumérer au-delà de 4. [V] Menus larges plutôt que
  profonds.

### 3.6 Diagramme de flux (processus, décision)

Schéma NCAM, adapté à la parole [V] :
1. **Annonce** : type, nombre d'étapes, nombre de décisions, nombre de points d'entrée et de sortie.
2. **Message** : ce que fait le processus en une phrase (« de la commande à la livraison »).
3. **Chemin principal** : le chemin le plus direct, étapes numérotées (« étape 1, …, étape 2, … »), chaque décision dite
   comme une question avec ses deux issues (« Si oui, étape 4 ; sinon, retour à l'étape 2 »).
4. **Branches et boucles** : « retour à l'étape n », « rejoint l'étape n » pour les fusions, dites explicitement.
5. **Détail** : une étape à la demande (« étape 3 : … ; elle vient de … ; elle mène à … »).
Les couleurs et formes ne se disent pas, sauf si elles portent du sens (une légende l'indique). [V]
Source de vérité : le graphe analysé (Mermaid, Graphviz, PlantUML, liste de nœuds et d'arêtes), jamais l'image seule. [V]

### 3.7 Diagramme de séquence

- **Annonce** : participants (dans l'ordre), nombre de messages.
- **Message** : le scénario en une phrase.
- **Détail** : les messages dans l'ordre, « de A à B : … », en blocs de 3 à 4 ; les boucles et alternatives annoncées
  comme dans le flux (« boucle tant que … », « alternative : si … »). [P]

### 3.8 Carte mentale et carte conceptuelle

- **Annonce** : le centre, le nombre de branches principales, la profondeur.
- **Message** : les branches principales nommées (≤ 6, sinon les 4 premières et le reste à la demande).
- **Détail** : une branche à la fois, du centre vers l'extérieur, en annonçant le nombre de sous-éléments. [P] TADA et
  Arboretum : navigation et questions nécessaires ; une seule description statique ne suffit pas.

### 3.9 Schéma libre (image sans structure fournie)

- Dire ce qu'on voit à coup sûr (type probable, titre, étiquettes lisibles), **étiqueter l'incertitude** (« je lis
  approximativement »), ne pas inventer de valeur, et proposer à l'utilisateur de fournir les données ou la source. [V]
  VizWiz, ChartHal.

## 4. Nombres, unités, dates, symboles (règles de prononciation)

Les règles complètes par langue sont dans le skill (`references/numbers-en.md`, `references/numbers-fr.md`). Décisions :

| Cas | Anglais | Français | Note |
|---|---|---|---|
| Décimale | 1,234.5 → « one thousand two hundred thirty-four point five » | 1 234,5 → « mille deux cent trente-quatre virgule cinq » | FR métropolitain : dire « virgule » ; l'OQLF l'omet au Québec. Choix : **virgule**, le plus sûr pour des données. [V] |
| Milliers | virgule = séparateur | espace (insécable) = séparateur ; « 1,5 » est une décimale | Détection par la locale, jamais par devinette. [V] |
| 10⁹ | billion | milliard | Faux ami ; jamais de traduction mot à mot. [V] |
| 10¹² | trillion | billion (rare) → préférer « mille milliards » | [P] |
| Pourcentage | « twelve percent » | « douze pour cent » | Point de pourcentage ≠ pour cent : « deux points » quand c'est un écart de taux. [P] |
| Intervalle | « from 10 to 15 » | « de 10 à 15 » | Jamais le tiret. [V] Cartesia |
| Négatif | « minus three » | « moins trois » | Jamais « tiret trois ». |
| Monnaie | « 12 euros », « 3 dollars 50 » | « 12 euros », « 3 dollars 50 » ; « 1,5 million d'euros » | Le code ISO (EUR, USD) se dit par le nom. [P] |
| Unités | en mots : « kilometres per hour », « milligrams per decilitre », « degrees Celsius » | « kilomètres par heure », « milligrammes par décilitre », « degrés Celsius » | Jamais l'abréviation brute. [V] Cartesia, ElevenLabs |
| Grands nombres | arrondis : « about 2.1 million » | « environ 2,1 millions » | Exact à la demande. [P] |
| Années | « twenty twenty-four » | « deux mille vingt-quatre » | Année ≠ quantité. [V] |
| Dates | « March 3rd, 2024 » (ordre explicite) | « le 3 mars 2024 » | Jamais 03/03/2024 tel quel. [V] ElevenLabs |
| Heures | « 2:30 p.m. » → « two thirty p m » | « 14 h 30 » → « quatorze heures trente » | |
| Ordinaux | « third » | « troisième » ; « premier » pour le 1er | |
| Acronymes | épeler si imprononçable (« G D P » → « gross domestic product » si connu) | « PIB » → « P I B » ou « produit intérieur brut » | Donner le développé une fois, puis le sigle. [P] |
| Symboles | ≥ « at least », ≤ « at most », ≈ « about », ± « plus or minus », → « leads to », × « times », Δ « change in » | « au moins », « au plus », « environ », « plus ou moins », « mène à », « fois », « variation de » | [P] |
| Fractions | « two thirds » | « deux tiers » | |
| Formules | ClearSpeak (en) / SimpleSpeak (fr) : « x squared plus one over two » | « x au carré plus un, sur deux » | MathCAT comme référence ; le skill couvre les cas simples. [V] |
| Formules chimiques | « H two O » | « H deux O » | Aucune source autoritaire ; donner le nom quand il est connu. [P] |
| Téléphone | groupes de 3-3-4 avec pauses | groupes de 2 avec pauses | [V] Elmers : les pauses aident le rappel. |
| Longues suites de chiffres | pause tous les 3 ou 4 chiffres | idem | [V] Elmers |

Précision à l'oreille [P] : garder au plus 3 chiffres significatifs dans le résumé ; toujours dire « environ » quand on a
arrondi ; donner l'exact à la demande.

## 5. SSML et repli texte

- **Trois sorties** : (a) texte parlé pré-normalisé, qui marche partout ; (b) SSML « sûr » : `speak`, `p`, `s`, `break`,
  `sub`, et `say-as` limité à `characters`, `date`, `time` (les nombres sont déjà en mots) ; (c) SSML « riche » par moteur (Azure :
  `unit`, `currency`, Math ; Polly : `unit`, `telephone` ; Google : `currency`, `unit`). [V] Table de capacités dans
  `references/ssml-engines.md`.
- Le texte pré-normalisé est **toujours** produit ; le SSML l'enveloppe sans dépendre de `say-as` pour la justesse : les
  nombres sont déjà en mots, `say-as` sert au rythme. [P] Ainsi un moteur qui supprime les balises reste correct.
- Pauses : 300 ms entre les cellules d'une ligne, 600 ms entre les lignes et entre les blocs, 1 s avant une question.
  [P] Valeurs à ajuster par l'évaluation. En repli texte : point-virgule entre cellules, point entre lignes, saut de
  ligne entre blocs. [P]
- Jamais de Markdown ni de symbole de tableau dans le flux parlé (`|`, `-`, `*`, `#`). [V]

## 6. Dialogue : commandes et réponses

| L'auditeur dit | L'agent fait |
|---|---|
| « continue », « suite », « oui » | bloc suivant, avec rappel de position |
| « répète » | redit le dernier bloc, à l'identique |
| « reviens », « précédent » | bloc précédent |
| « ligne 5 », « Paris » | la ligne demandée, avec tous ses en-têtes |
| « colonne Population » | la colonne, par blocs |
| « compare Paris et Lyon » | les deux lignes côte à côte, colonne par colonne |
| « le plus grand », « le minimum », « le total » | la statistique, avec l'en-tête |
| « résume » | retour à l'étape 1–2 |
| « détails », « tout » | lecture linéaire complète, par blocs, avec offres d'arrêt |
| « où en suis-je » | position courante : figure, ligne ou étape, en-tête |
| « pourquoi », « qu'est-ce que ça veut dire » | L4, annoncé comme interprétation |
| « stop » | s'arrête, sans question |

Dans un contexte sans dialogue (un seul tour, par exemple une réponse écrite destinée à une synthèse), le skill produit
les étapes 0 à 2 et, si la figure est petite, le détail complet ; sinon il termine par une phrase indiquant ce qu'on
peut demander. [P]

## 7. Représentation intermédiaire (pour les scripts)

Une structure JSON unique, produite depuis Markdown, CSV, HTML ou Mermaid, et consommée par le narrateur :

```json
{"kind": "table", "title": "…", "columns": [{"name": "Population", "unit": "millions"}], "rows": [["Paris", 2.1]],
 "row_header_col": 0, "lang": "fr", "notes": []}
{"kind": "flowchart", "nodes": [{"id": "A", "label": "…", "type": "process|decision|start|end"}],
 "edges": [{"from": "A", "to": "B", "label": "oui"}], "lang": "fr"}
```

Le narrateur applique la stratégie du § 3 à cette structure et produit le texte normalisé, puis le SSML. Les scripts
servent la **vérification** (chaque nombre prononcé existe dans la structure) autant que la génération. [P]

## 8. Critères d'évaluation (fixés avant les tests, voir `eval/PROTOCOL.md`)

1. **Exactitude des chiffres** : chaque nombre prononcé existe dans la source et porte la bonne unité et le bon en-tête
   (vérification automatique sur la représentation intermédiaire + lecture humaine).
2. **Ordre** : annonce → message → chiffres clés → offre, vérifié par motif.
3. **Longueur** : mots avant la première offre (cible ≤ 60), mots par bloc, nombre de nombres par phrase (cible 1).
4. **Prononçabilité** : zéro abréviation brute, zéro symbole, zéro tiret d'intervalle, zéro Markdown dans la sortie ;
   décimales et milliers conformes à la langue.
5. **Compréhension à l'écoute** [P] : trois questions par cas (« quelle est la plus grande valeur ? », « quelle
   tendance ? », « combien de lignes ? ») auxquelles un auditeur doit pouvoir répondre depuis le texte des étapes 0–2 seules.
   Faute d'auditeurs humains, un modèle juge différent de celui qui a produit répond aux questions à partir du texte
   seul ; c'est une approximation, dite comme telle.
6. **Comparaison** « sans skill » (même modèle, même consigne « lis ceci à voix haute ») contre « avec skill », sur les
   mêmes cas, mêmes critères.

## 9. Ce que cette conception ne couvre pas

- La sonification (tons) : hors périmètre ; le skill peut dire quand une sonification existe. [NT]
- Les langues autres que l'anglais et le français : l'architecture prévoit un fichier `numbers-<lang>.md` par langue et
  des gabarits de phrases par langue ; rien n'est écrit pour d'autres langues. [NT]
- La lecture d'images sans données : couverte seulement par la règle d'incertitude du § 3.9. [NT]
- Les auditeurs réels : l'évaluation est automatique et par modèle juge ; aucune étude utilisateur n'est menée ici. [NT]
