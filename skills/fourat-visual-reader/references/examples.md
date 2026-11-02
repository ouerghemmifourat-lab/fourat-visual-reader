# Worked examples (English and French)

Each example gives the input, then the spoken output for a first turn. Word counts before the offer stay under 60.

## 1. Small table — EN

Input:
| City | Population (millions) | Area (km²) |
|---|---|---|
| Paris | 2.1 | 105 |
| Lyon | 0.5 | 48 |
| Marseille | 0.9 | 241 |

Spoken:
"A table with three columns and three rows, one row per city: population in millions, and area in square kilometres.
Paris is the most populous but Marseille covers the largest area.
Paris: population two point one million; area one hundred five square kilometres.
Lyon: zero point five million; forty-eight square kilometres.
Marseille: zero point nine million; two hundred forty-one square kilometres."

## 2. Petit tableau — FR

Même entrée.

Dit :
« Un tableau de trois colonnes et trois lignes, une ligne par ville : population en millions, et superficie en kilomètres
carrés. Paris est la plus peuplée, mais Marseille est la plus étendue.
Paris : population deux virgule un millions ; superficie cent cinq kilomètres carrés.
Lyon : zéro virgule cinq million ; quarante-huit kilomètres carrés.
Marseille : zéro virgule neuf million ; deux cent quarante-et-un kilomètres carrés. »

## 3. Large table — EN (first turn only)

Input: 9 columns × 120 rows of quarterly sales by product.

Spoken:
"A table with nine columns and one hundred twenty rows: product, region, year, and six quarterly and annual sales
columns, in thousands of euros. Annual sales are highest for the Alpha range in Western Europe. The top annual figure is
about four point two million euros; the lowest is about twelve thousand. I can read the top ten products, one region, or
one column. What would you like?"

## 4. Bar chart — EN

Input: Sales by country (M€): France 42, Spain 38, Italy 25, Portugal 9.

Spoken:
"A bar chart of sales by country, four bars, in millions of euros. France leads, Spain is close behind, Portugal is far
lower. France: forty-two million. Spain: thirty-eight. Italy: twenty-five. Portugal: nine, about a fifth of France."

## 5. Graphique en barres — FR

Dit :
« Un graphique en barres des ventes par pays, quatre barres, en millions d'euros. La France est en tête, l'Espagne juste
derrière, le Portugal loin derrière. France : quarante-deux millions. Espagne : trente-huit. Italie : vingt-cinq.
Portugal : neuf, environ un cinquième de la France. »

## 6. Line chart — EN

Input: Revenue 2015–2024 (M€): 10, 12, 14, 16, 15, 11, 17, 21, 23, 25.

Spoken:
"A line chart of annual revenue from twenty fifteen to twenty twenty-four, in millions of euros. Revenue rises steadily
from ten to twenty-five million, with one dip in twenty twenty. The low point is eleven million in twenty twenty; the
peak is the last year, twenty-five. Want the year-by-year values?"

## 7. Courbe — FR

Dit :
« Une courbe du chiffre d'affaires annuel de deux mille quinze à deux mille vingt-quatre, en millions d'euros. Il monte
régulièrement de dix à vingt-cinq millions, avec un creux en deux mille vingt. Le point bas est onze millions en deux
mille vingt ; le sommet est la dernière année, vingt-cinq. Voulez-vous les valeurs année par année ? »

## 8. Pie — EN

Input: Household budget: rent 52 %, food 20 %, transport 12 %, leisure 9 %, other 7 %.

Spoken:
"A pie chart of the household budget in five parts. Rent takes more than half. Rent: fifty-two percent. Food: twenty.
Transport: twelve. Leisure: nine. Other: seven."

## 9. Flowchart — EN

Input (Mermaid):
flowchart TD
  A((Order received)) --> B[Check stock]
  B --> C{In stock?}
  C -->|yes| D[Pack]
  C -->|no| E[Back-order]
  E --> B
  D --> F[Ship]
  F --> G((Delivered))

Spoken:
"A flowchart with six steps and one decision, one entry point, one exit, from order received to delivered. It takes an
order through a stock check to shipping.
Step one, order received. Step two, check stock. Decision: in stock? If yes, step three, pack. If no, step four,
back-order, then back to step two. Step three, pack, then step five, ship, then step six, delivered."

(Step count convention: every box except decisions is a step, start and end boxes included; see diagrams.md.)

## 10. Diagramme de flux — FR

Dit :
« Un diagramme de flux de six étapes et une décision, une entrée, une sortie, de commande reçue à livré. Il mène une
commande de la vérification du stock à l'expédition.
Étape un, commande reçue. Étape deux, vérifier le stock. Décision : en stock ? Si oui, étape trois, emballer. Si non,
étape quatre, commande en attente, puis retour à l'étape deux. Étape trois, emballer, puis étape cinq, expédier, puis
étape six, livré. »

## 11. Org chart — EN

Input: CEO → CFO (Accounting 3, Treasury 2), CTO (Dev 12, Ops 4), COO (Sales 20).

Spoken:
"An org chart with three levels and forty-four positions, led by the CEO. The CEO has three direct reports: the CFO, the
CTO and the COO. Under the CFO: accounting, three people; treasury, two. Under the CTO: development, twelve; operations,
four. Under the COO: sales, twenty. Which branch would you like in detail?"

## 12. Sequence diagram — FR

Input: Utilisateur → App : saisit identifiants ; App → Serveur : vérifie ; Serveur → Base : lit l'utilisateur ; Base →
Serveur : enregistrement ; Serveur → App : jeton ; App → Utilisateur : connecté.

Dit :
« Un diagramme de séquence à quatre participants : utilisateur, application, serveur, base de données ; six messages.
Un utilisateur se connecte : l'application interroge le serveur, qui lit la base.
De l'utilisateur à l'application : saisit ses identifiants. De l'application au serveur : vérifie. Du serveur à la base :
lit l'utilisateur. Retour de la base au serveur : l'enregistrement. Du serveur à l'application : un jeton. De
l'application à l'utilisateur : connecté. »

## 13. Image only — EN

Input: a photo of a bar chart, axis labels partly legible.

Spoken:
"I'm reading this from an image, so values are approximate. It looks like a bar chart of five countries; the tallest bar
is labelled France at roughly forty, the shortest Portugal, under ten. The other labels are too small to read. If you
can share the data, I'll read it exactly."

## 14. Interpretation on request — FR

Auditeur : « Pourquoi le creux en 2020 ? »

Dit :
« Les données montrent une baisse de quinze à onze millions en deux mille vingt. Mon interprétation : cela correspond à
l'année de la pandémie, mais le graphique ne le dit pas. »
