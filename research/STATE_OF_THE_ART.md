# État de l'art — lire un tableau, un graphique ou un schéma à l'oreille

Date : 2026-11-02. Synthèse des quatre notes de `research/notes/` (01 dépôts et skills, 02 pratique de l'accessibilité,
03 littérature, 04 TTS/SSML/design vocal). Chaque affirmation porte une URL. Marques : **(F)** page lue, **(S)** vue
seulement dans des résultats de recherche, **non vérifié** = non confirmé sur une page primaire. Les chiffres sont
recopiés des sources ; aucun n'est inventé.

## 1. Ce qui existe déjà

### 1.1 Skills d'agents et dépôts publics (note 01)

| Ressource | URL | Licence | Fait | Ne fait pas (par rapport à notre but) |
|---|---|---|---|---|
| anthropics/skills (19 skills) | https://github.com/anthropics/skills | par skill, non vérifié | Format de référence `SKILL.md` | Rien sur tableaux, graphiques, voix, SSML |
| openai/skills (skill « speech ») | https://github.com/openai/skills | non vérifié | Lance une CLI TTS (clé OpenAI) | Enveloppe de synthèse, aucune règle de contenu |
| mgifford/accessibility-skills (charts-graphs, tables, mermaid…) | https://github.com/mgifford/accessibility-skills | **AGPL-3.0** (vérifié API) | Règles d'accessibilité web pour graphiques, tableaux, Mermaid | Texte alternatif écrit, pas de parole, de rythme, de SSML ni de prononciation. Licence virale : **ne rien copier** |
| accessibility-and-inclusive-visualization (vskill) | https://verified-skill.com/skills/openai/plugins/accessibility-and-inclusive-visualization/versions/1.0.0 | MIT en pied de page, non vérifié | Descriptions longues de graphiques, diagrammes UML | « Aucune mention d'audio, voix, SSML, sonification » |
| alt-text (E. Hvitfeldt, R/Quarto) | https://claudskills.com/skills/alt-text/SKILL.md | inconnue | Formule type + données + enseignement | Écrit, anglais seulement |
| Skills TTS communautaires (claude-speak, edge-tts, verging-ai/tts) | https://skills.cat/skills/leegonzales/aiskills/claude-speak ; https://claudskills.com/skills/edge-tts/ | inconnues | Lisent un texte à travers un moteur | Lecture seule, aucune restructuration pour l'oreille |
| Serveurs MCP TTS (SAPI, Kokoro, say, OpenAI) | https://pypi.org/project/text-to-speech-mcp/0.4.0/ ; https://enterprisedna.co/directories/mcp/mberg-kokoro-tts-mcp | MIT / Apache-2.0 d'après des listings, non vérifié | Parlent | Aucun avec SSML ni narration de tableau trouvé |
| **Olli** (umwelt-data) | https://github.com/umwelt-data/olli | **BSD-3** (vérifié) | Arbre textuel navigable au clavier avec niveaux de détail à partir d'une spécification Vega/Vega-Lite | Arbre visuel pour lecteur d'écran, pas de rythme vocal, de SSML ni de prononciation |
| **Chart2Music** | https://github.com/julianna-langston/chart2music | **MIT** (vérifié), actif (poussé 2026-10-27) | Sonification + lecteur d'écran + clavier ; plugin Chart.js traduit en fr | Audio non verbal dans un navigateur, pas de stratégie de résumé parlé |
| Highcharts accessibilité et sonification | https://www.highcharts.com/docs/accessibility/accessibility-module-feature-overview | propriétaire | Région d'information (titre, type, axes), tableau, sonification, pistes « speech » | Propriétaire ; aucune règle de prononciation ni de structure |
| Apple Audio Graphs | https://developer.apple.com/documentation/accessibility/audio-graphs | SDK propriétaire (S) | Titre, résumé, axes, séries pour VoiceOver | Fermé, applications natives seulement |
| mermaid-js/mermaid | https://github.com/mermaid-js/mermaid | **MIT** (vérifié) | Analyse et rend les diagrammes ; `accTitle` / `accDescr` | Aucun générateur de description trouvé |
| Constructeurs SSML (ssmd, ssml_builder, ssml-maker) | https://github.com/buchwandler/ssmd ; https://github.com/user3301/ssml_builder ; https://pypi.org/project/ssml-maker/ | MIT / sans licence claire / inconnue | Syntaxe SSML | Aucune logique de contenu |
| num2words | https://github.com/savoirfairelinux/num2words | **LGPL-2.1** (vérifié) | Nombres en mots, en, fr, fr_BE, fr_CH, ordinaux | Ni unités, ni pourcentages, ni intervalles. Un agrégateur signale un avis de sécurité MAL-2025-6794 sur PyPI : **non vérifié**, à contrôler avant toute dépendance |
| NeMo-text-processing | https://github.com/NVIDIA/NeMo-text-processing | Apache-2.0 | Normalisation de texte | Dépend de pynini, pas d'installation pip sous Windows ; langues fr/en non vérifiées |
| MathCAT (DAISY) | https://github.com/daisy/MathCAT | **MIT** | Parole mathématique, anglais et français ; règles ClearSpeak / SimpleSpeak | ClearSpeak indisponible en français d'après une note NVDA (https://app.semanticdiff.com/gh/nvaccess/nvda/commit/90ee3cd85df1985f9ec772dc23c343637c2666dc) |
| Chart-to-Text, VisText, ChartQA (données) | https://github.com/vis-nlp/Chart-to-text ; https://github.com/mitvis/vistext ; https://huggingface.co/datasets/ahmed-masry/ChartQA | **GPL-3.0** (dépôts) ; droits Statista/Pew non précisés | Résumés écrits en anglais | Pas pour l'oreille ; copyleft |
| ToTTo (données) | https://huggingface.co/datasets/google-research-datasets/totto | CC BY-SA 3.0 | Tableau → une phrase, cellules mises en avant | Écrit, anglais |

**Constat** : aucun skill, dépôt ni serveur MCP n'apprend à un agent à **dire** un tableau ou un graphique. Les briques
existent séparément (analyse Mermaid, arbre de niveaux d'Olli, say-as des moteurs, nombres en mots) ; personne ne les
assemble pour la parole.

### 1.2 Comment les personnes aveugles consomment déjà tableaux et graphiques (note 02)

- **Lecteurs d'écran sur les tableaux.** NVDA : déplacement cellule par cellule (Ctrl+Alt+flèches), lecture de toute la
  ligne ou colonne, annonce des en-têtes si l'option est active — https://download.nvaccess.org/documentation/userGuide.html (F).
  JAWS annonce les dimensions en entrant (« table with seven columns and five rows ») puis les en-têtes de chaque
  cellule — https://support.freedomscientific.com/teachers/lessons/7.3_Transcript-ReadingTables.htm (S, 403 à la lecture).
  VoiceOver donne « a summary of a table and its cells » par le regroupement — https://support.apple.com/en-euro/guide/voiceover/vo27958/mac (F).
- **Plaintes.** « Complex data tables » est le 10e problème le plus cité de l'enquête WebAIM 10 (2023-2024) —
  https://webaim.org/projects/screenreadersurvey10/ (F). Dix-huit utilisateurs aveugles (Wang, Srinivasan, Kim, DIS 2024)
  se perdent dans les grands tableaux et oublient unités et noms de colonnes ; ils veulent d'abord une vue d'ensemble,
  puis des statistiques, puis des sous-ensembles à la demande — https://pages.cs.wisc.edu/~yeaseulkim/assets/papers/2024_table.pdf (F).
  Treize lecteurs (Zong et al., EuroVis 2022) parcourent au plus 20 à 30 lignes et veulent filtrer et trier sans « wading
  line by line » — https://arxiv.org/pdf/2205.04917 (F).
- **Guides de description.** W3C WAI, images complexes : description courte + description longue donnant « values,
  relationships, and trends » — https://www.w3.org/WAI/tutorials/images/complex/ (F, mis à jour 2026-04-08).
  Cesal : « Chart type of type of data where reason for including chart » — https://nightingaledvs.com/writing-alt-text-for-data-visualization (F).
  Datawrapper : type, données, enseignement ; ne pas répéter titre et source — https://www.datawrapper.de/academy/how-to-write-good-alternative-descriptions-for-your-data-visualization (F).
  Analysis Function (UK) : le texte alternatif porte le **message** ; pas d'« auditory clutter » —
  https://analysisfunction.civilservice.gov.uk/blog/data-vis-and-accessibility-links-to-content-and-answers-to-questions (F).
  Chartability (CC BY-SA 3.0) : grille d'audit en 7 principes — https://chartability.fizz.studio/ (F).
  Highcharts : ne pas exposer chaque point d'une grande série (`pointDescriptionEnabledThreshold`) — https://www.highcharts.com/docs/accessibility/configure-the-accessibility-module (S).
- **Diagrammes de flux.** NCAM/WGBH (2008) : ouvrir par une vue d'ensemble (éléments, nombre de points de départ), puis
  numéroter les boîtes et donner les transitions en sous-puces, expliciter les fusions, omettre couleurs et styles de
  traits sauf s'ils portent du sens — https://www.wgbh.org/ncam-resources/2026-08-11/effective-practices-for-description-of-science-content-within-digital-talking-books-basic-flow-chart (F ; © GBH, pas de licence ouverte).
  Tableaux (même source) : scinder un tableau à plusieurs niveaux ; remplacer les symboles par des mots (« Quantity zero »
  pour un tiret). Mermaid : `accTitle` et `accDescr` — https://mermaid.js.org/config/accessibility.html (F).
  Rien trouvé pour PlantUML, Graphviz ou DAISY.
- **Français.** RGAA 4.1.2, critères 1.6–1.9 (description détaillée) — https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/#1.6 (F, partiel).
  Aucune consigne française sur la lecture **parlée** des tableaux trouvée (non vérifié qu'il n'en existe pas).

### 1.3 Littérature (note 03)

- **Les quatre niveaux de contenu** (Lundgard & Satyanarayan, IEEE TVCG 2022, https://arxiv.org/abs/2110.04406, F) :
  L1 construction (type, axes, codages) ; L2 statistiques (extrêmes, comparaisons) ; L3 tendances perçues en langage
  courant ; L4 contexte et domaine. Trente lecteurs aveugles ont classé **L2 et L3 les plus utiles**, L1 et L4 les
  moins ; **63 %** refusent l'interprétation de l'auteur (L4) ; 40 % veulent combiner les niveaux ; L1 seul est
  « almost useless ». Les 90 lecteurs voyants préfèrent L3 et L4.
- **Le résumé d'abord, le détail à la demande** est soutenu par Olli (https://vis.mit.edu/pubs/olli, S), Chart Reader
  (CHI 2023, co-conception de cinq mois avec 10 utilisateurs — https://www.microsoft.com/en-us/research/publication/chart-reader-accessible-visualization-experiences-designed-with-screen-reader-users/, F),
  VizAbility (UIST 2024, arbre + questions LLM, 6 participants aveugles seulement, 77 % de réponses « très bonnes » contre
  28 % pour GPT-4V — https://arxiv.org/html/2310.09611v4, F), VoxLens (CHI 2022, +122 % d'exactitude et −36 % de temps,
  21 utilisateurs — https://wildlab.cs.washington.edu/Publications_files/Sharif_CHI2022.pdf, S), Siu et al. (CHI 2022,
  description parlée + sonification de séries temporelles — https://hci.stanford.edu/publications/paper.php?id=473, S).
- **Les modèles de vision hallucinent les chiffres.** Chart-to-Text (ACL 2022) : les modèles « suffer from
  hallucinations and factual errors » — https://arxiv.org/abs/2203.06486 (F). Islam et al. 2024 : BLEU, BLEURT et CIDEr
  mesurent la fluidité, pas la vérité ; taux d'erreurs factuelles manuels de l'ordre de 5 à 27 % selon le modèle, valeurs
  **divergentes entre sources, non vérifiées** — https://arxiv.org/abs/2406.00257 (F). ChartCap propose un contrôle sans
  référence (régénérer le graphique depuis la légende) — https://arxiv.org/abs/2508.03164 (F). ChartHal : les questions
  sur une information absente du graphique provoquent le plus d'hallucinations — https://arxiv.org/abs/2509.17481 (F).
  VizWiz : beaucoup de questions d'utilisateurs aveugles sont sans réponse depuis l'image — https://arxiv.org/abs/1802.08218 (F).
- **Diagrammes.** FlowVQA (ACL 2024) : les modèles de vision échouent sur le raisonnement spatial et montrent un biais
  directionnel — https://arxiv.org/abs/2406.19237 (F). TADA (CHI 2024, 15 entretiens, 25 participants) et Arboretum (CHI
  2026) : la description statique ne suffit pas aux diagrammes nœuds-liens ; il faut questions, navigation et plusieurs
  représentations — https://arxiv.org/abs/2311.04502 (F), https://arxiv.org/abs/2601.19168 (F).
- **Tableaux.** ToTTo (CC BY-SA 3.0, https://arxiv.org/abs/2004.14373v3, S) ancre la phrase sur des cellules mises en
  avant. **Aucune étude évaluée par les pairs sur le résumé de tableaux pour la parole** n'a été trouvée.
- **Mémoire et parole.** Cowan 2001 : environ 4 blocs en mémoire de travail — https://pubmed.ncbi.nlm.nih.gov/11515286/ (S).
  Commarford et al. 2008 : les menus vocaux larges battent les menus profonds — https://stars.library.ucf.edu/facultybib2000/233 (S).
  Elmers et al. 2021 : une pause dans une suite de chiffres améliore le rappel ; aucun moteur testé ne l'insère seul —
  https://mikeyelmers.github.io/publications/elmers_ESSV2021_Presentation.pdf (S, tailles d'effet non obtenues).
  Zhang & Sproat 2019 : la lecture d'un nombre dépend du contexte — https://research.google/pubs/neural-models-of-text-normalization-for-speech-applications/ (S).
  Ould Ouali et al. 2025 : le SSML prédit par LLM améliore le naturel du français (MOS 3,20 → 3,87) mais la
  compréhension n'est pas mesurée — https://arxiv.org/abs/2508.17494 (F).

### 1.4 TTS, SSML et design vocal (note 04)

- **SSML 1.1 ne normalise pas les valeurs de `say-as`** : le W3C « does not enumerate the possible values » —
  https://www.w3.org/TR/speech-synthesis11/ (F). Chaque moteur a les siennes.
- **Prise en charge par moteur** (toutes pages officielles, F) :
  Polly, erreur sur une balise non prise en charge, `say-as` partiel en neural — https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html ;
  Google, jeu complet mais Chirp 3 HD n'accepte que `phoneme`, `p`, `s`, `sub`, `say-as` — https://docs.cloud.google.com/text-to-speech/docs/release-notes ;
  Azure, `say-as` le plus riche (cardinal, ordinal, fraction, date, time, currency, unit…) pour le français inclus, plus
  un domaine Math/MathML — https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation ;
  Alexa « removes unsupported tags » — https://developer.amazon.com/en-US/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html ;
  ElevenLabs : `break` ignoré par v3/v4, recommande d'« Expand all abbreviations to their full spoken forms » —
  https://elevenlabs.io/docs/best-practices/prompting/controls ;
  OpenAI TTS : aucune mention du SSML, style par `instructions` ; la page annonce l'arrêt de tts-1 et gpt-4o-mini-tts le
  2027-01-06 — https://developers.openai.com/api/docs/guides/text-to-speech ;
  Apple `AVSpeechUtterance(ssmlRepresentation:)` renvoie nil si le SSML est invalide — https://developer.apple.com/documentation/avfaudio/avspeechutterance/init(ssmlrepresentation:)-8zam9.md ;
  Windows System.Speech : SSML 1.0, exemple officiel avec `say-as type=` — https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis.speechsynthesizer.speakssml ;
  Piper et Coqui : SSML non confirmé — https://github.com/rhasspy/piper/issues/275, https://github.com/coqui-ai/TTS/issues/752.
- **Nombres en français.** OQLF : « zéro » et « virgule » ne se prononcent en principe pas (1,6 km → « un kilomètre
  six »), sauf risque de confusion ; « de » entre grandeur et unité (« dix millions de kilomètres ») —
  https://vitrinelinguistique.oqlf.gouv.qc.ca/25100/la-prononciation/prononciation-des-nombres/regles-generales-de-lecture-des-nombres (F ; usage québécois, l'usage métropolitain dit « virgule », S).
  Virgule décimale et espace insécable des milliers — https://vitrinelinguistique.oqlf.gouv.qc.ca/la-typographie/nombres (S).
  Faux ami **billion / milliard** : 10⁹ = « billion » en anglais, « milliard » en français — https://en.wikipedia.org/wiki/Long_and_short_scales (F).
- **Normalisation avant la synthèse.** Cartesia : intervalles et fractions peu fiables, écrire « 10 to 15 dollars »,
  « two thirds », unités en mots — https://docs.cartesia.ai/build-with-cartesia/capability-guides/text-normalization.md (F).
- **Densité.** Google Design « Rule of three » : dire 3 éléments, le reste à l'écran — https://design.google/library/rule-of-three (F).
  Amazon (2019) : l'information clé en fin de phrase, repères « first / second / third » —
  https://developer.amazon.com/en-US/blogs/alexa/alexa-skills-kit/2019/08/how-to-reduce-cognitive-load-for-voice-design (F).
  W3C COGA (brouillon 2026) : « Each list item should be a single idea. » — https://w3c.github.io/coga/research-modules/Conversational-Voice-Systems.html (F).
  Contre-point : la recherche IVR réfute la règle dure des « 5 éléments » (Commarford, S). Trois par bloc est un défaut,
  pas une loi.

## 2. Ce qui manque aujourd'hui

1. **Aucun skill ni outil ne dit un tableau, un graphique ou un diagramme** pour un auditeur. Tout l'existant vise le
   texte alternatif écrit ou la navigation clavier (notes 01, 02).
2. **Aucun budget de longueur parlée** (secondes ou mots) : les guides disent « court » sans chiffre (note 02).
3. **Aucune règle de prononciation unifiée en/fr** pour nombres, décimales, milliers, pourcentages, intervalles,
   négatifs, unités, dates, monnaies, symboles et acronymes. Les moteurs se contredisent et SSML ne normalise rien
   (notes 02, 04). Le faux ami milliard/billion n'est traité nulle part pour la parole.
4. **Aucune règle de tour de parole** : quand s'arrêter et demander « je continue ? », comment dire « répète »,
   « reviens », « ligne 5 », « lis la colonne Revenu », à quelle fréquence répéter les en-têtes (note 02).
5. **Aucun équivalent parlé des repères de structure** que le lecteur d'écran fournit (« liste de 4 éléments »,
   imbrication, position « ligne 3 sur 12 ») (note 02).
6. **Aucun narrateur de diagramme** : Mermaid et Graphviz s'analysent, mais rien ne transforme un graphe en parole ; les
   modèles de vision échouent sur les flux (notes 01, 03). Le seul guide (NCAM 2008) est écrit, non libre.
7. **Aucun jeu d'évaluation à l'oreille** : les corpus (Chart-to-Text, ToTTo) sont écrits, anglais, souvent GPL ou
   share-alike (notes 01, 03).
8. **Fiabilité des descriptions générées** : les modèles de vision hallucinent les chiffres ; seul le passage par la
   table de données et la vérification de chaque nombre sont défendables (note 03).
9. **Base de preuves mince** : études de 6 à 30 personnes, lecteurs d'écran de bureau, anglophones ; rien sur les
   auditeurs au téléphone ou sur enceinte, rien de comparatif en/fr (notes 02, 03).

## 3. Conséquences pour la conception (reprises dans DESIGN.md)

- Ordre : structure (L1, bref) → statistiques et tendance en langage courant (L2 + L3) → détail à la demande ;
  interprétation (L4) seulement si demandée et étiquetée comme telle.
- Les nombres viennent de la table de données ou de la spécification, jamais de l'image seule ; tout nombre prononcé
  doit exister dans la source ; savoir dire « je ne peux pas le lire ».
- Blocs de 3 à 4 éléments, une idée par phrase, pause entre les blocs, offre de continuer ; les menus larges valent mieux
  que les imbriqués.
- Normaliser nombres, unités, dates et symboles **avant** la synthèse, avec une locale explicite ; SSML quand le moteur le
  permet, texte pré-normalisé sinon ; table de capacités par moteur.
- Diagrammes : narrer depuis un graphe analysé (nœuds, arêtes), selon le schéma NCAM : vue d'ensemble, points de départ,
  boîtes numérotées, transitions, fusions explicites, boucles en « retour à l'étape n ».

## 4. Hygiène des licences pour la publication

- Réutilisables : idées et structures (citables) ; code MIT/BSD (Olli, Chart2Music, Mermaid, MathCAT) ; Chartability
  CC BY-SA 3.0 comme grille d'audit avec attribution.
- **À ne pas copier** : mgifford/accessibility-skills (AGPL-3.0) ; dépôts Chart-to-Text, VisText, ChartQA (GPL-3.0) ;
  données Statista/Pew (droits non précisés) ; NCAM/WGBH (© GBH, pas de licence ouverte : citer, ne pas reproduire).
- Dépendances : éviter num2words tant que l'avis MAL-2025-6794 n'est pas vérifié ; préférer un module maison minimal
  (en/fr) sous la licence du projet.

## 5. Limites de cette revue

Les PDF de VoxLens, Elmers et Find-and-Seek n'ont pas pu être lus (S) ; l'ACM DL et le site DIAGRAM Center ont refusé la
connexion ; les documents JAWS ont renvoyé 403. AutoChart, SeeChart, DiGVis et plusieurs licences restent non vérifiés.
Les comparatifs sonification contre parole n'ont pas de source primaire fiable. Rien n'a été cherché sur Graphviz et
PlantUML côté accessibilité au-delà d'un constat d'absence.
