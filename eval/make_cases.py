#!/usr/bin/env python3
"""Builds eval/cases.json: 34 cases (17 en, 17 fr) with source data, type and three questions with expected answers.
Large tables are generated deterministically here so the expected extremes are known. Synthetic data only.
  python make_cases.py  -> cases.json
"""
import json, random
from pathlib import Path

C = []


def case(cid, lang, kind, text, questions, vvr_kind=None, title="", note=""):
    C.append({"id": cid, "lang": lang, "kind": kind, "vvr_kind": vvr_kind, "title": title, "input": text.strip("\n"),
              "questions": [{"q": q, "a": a} for q, a in questions], "note": note})


# ------------------------------------------------------------------ EN
case("en_table_small", "en", "table", """
| City | Population (millions) | Area (km²) |
|---|---|---|
| Paris | 2.1 | 105 |
| Lyon | 0.5 | 48 |
| Marseille | 0.9 | 241 |
""", [("Which city has the largest population?", "Paris"), ("What is the area of Marseille?", "241 square kilometres"),
      ("How many cities (rows) are there?", "3")], "table")

case("en_table_medium", "en", "table", """
Product,Q1 (k€),Q2 (k€),Q3 (k€),Q4 (k€)
Alpha,120,135,150,160
Beta,80,82,79,85
Gamma,200,190,180,170
Delta,45,50,55,60
Epsilon,310,300,320,330
Zeta,15,18,20,22
Eta,95,100,105,110
Theta,60,58,61,59
""", [("Which product has the highest Q1 sales?", "Epsilon (310 k€)"), ("Which product falls every quarter from Q1 to Q4?", "Gamma"),
      ("How many products (rows) are listed?", "8")], "table")

rng = random.Random(7)
rows = []
cities = ["Lille", "Lyon", "Nice", "Nantes", "Rennes", "Reims", "Metz", "Brest", "Tours", "Dijon", "Angers", "Nîmes", "Caen",
          "Pau", "Bayonne", "Annecy", "Troyes", "Lorient", "Vannes", "Arles", "Agen", "Albi", "Cahors", "Blois", "Sens",
          "Auch", "Dax", "Royan", "Niort", "Melun", "Évry", "Sète"]
for i, c in enumerate(cities):
    staff = rng.randint(4, 40)
    rev = rng.randint(120, 850)
    margin = rng.randint(4, 18)
    rows.append([f"S{i + 1:02d}", c, staff, rev, margin, rng.randint(2001, 2024)])
rows[11][3], rows[11][2] = 980, 52   # Nîmes: clear maximum revenue, most staff
rows[26][3], rows[26][2] = 41, 3     # Dax: clear minimum revenue, fewest staff
big = "Store,City,Staff,Revenue (k€),Margin (%),Opened\n" + "\n".join(",".join(map(str, r)) for r in rows)
case("en_table_large", "en", "table", big,
     [("Which store has the highest revenue, and how much?", "S12 in Nîmes, 980 k€"), ("Which store has the fewest staff?", "S27 in Dax, 3"),
      ("How many stores (rows) are in the table?", "32")], "table", note="32 rows: the skill should not read it all")

case("en_table_multiheader", "en", "table", """
| Region | Units 2023 | Revenue 2023 (k€) | Units 2024 | Revenue 2024 (k€) |
|---|---|---|---|---|
| North | 1,200 | 480 | 1,350 | 560 |
| South | 900 | 350 | 880 | 340 |
| West | 400 | 150 | 620 | 240 |
""", [("What was the 2024 revenue in the North?", "560 k€"), ("Which region grew the most in revenue from 2023 to 2024?", "West (150 to 240, +60 %)"),
      ("How many regions are listed?", "3")], "table", note="two header levels flattened")

case("en_table_empty", "en", "table", """
| Product | Price (€) | Stock | Supplier |
|---|---|---|---|
| Hammer | 12.50 | 40 | Acme |
| Saw | 24.00 | — | Acme |
| Drill | 89.90 | 7 | |
| Level | 15.00 | 0 | Bolt Co |
| Pliers | | 22 | Bolt Co |
""", [("Which product has no supplier listed?", "Drill"), ("What is the stock of Level?", "0 (zero)"),
      ("Which product has no price?", "Pliers")], "table", note="empty cells and a dash")

case("en_bars_simple", "en", "bars", """
Country,Sales (M€)
France,42
Spain,38
Italy,25
Portugal,9
""", [("Which country has the highest sales?", "France (42 M€)"), ("What are Portugal's sales?", "9 M€"),
      ("Roughly what fraction of France's sales does Portugal have?", "about a fifth (9/42 ≈ 21 %)")], "bars", title="Sales by country, 2024")

case("en_bars_grouped", "en", "bars", """
| Country | Online (M€) | Stores (M€) |
|---|---|---|
| France | 12 | 30 |
| Spain | 20 | 18 |
| Italy | 10 | 15 |
""", [("Which country sells more online than in stores?", "Spain (20 vs 18)"), ("What are France's store sales?", "30 M€"),
      ("How many series (bar groups) are there?", "2: online and stores")], "table", note="grouped bars; vvr reads it as a table")

case("en_bars_negative", "en", "bars", """
Quarter,Profit (M€)
Q1,5
Q2,-3
Q3,2
Q4,-7
""", [("Which quarter had the largest loss?", "Q4 (minus 7 M€)"), ("What was the profit in Q2?", "minus 3 M€"),
      ("How many quarters were negative?", "2 (Q2 and Q4)")], "bars", note="negative values; 'minus', never 'dash'")

case("en_line_single", "en", "line", """
Year,Revenue (M€)
2015,10
2016,12
2017,14
2018,16
2019,15
2020,11
2021,17
2022,21
2023,23
2024,25
""", [("What is the overall trend?", "rising (10 to 25), with a dip in 2020"), ("What was the revenue in 2020?", "11 M€"),
      ("What is the last value, in 2024?", "25 M€")], "line")

case("en_line_multi", "en", "line", """
| Year | Series A | Series B |
|---|---|---|
| 2019 | 10 | 14 |
| 2020 | 12 | 15 |
| 2021 | 16 | 15 |
| 2022 | 18 | 16 |
| 2023 | 20 | 16 |
| 2024 | 22 | 17 |
""", [("Which series is higher in 2019?", "B (14 vs 10)"), ("In which year does A first exceed B?", "2021 (16 vs 15)"),
      ("What is A's value in 2024?", "22")], "table", note="two series; vvr line mode uses the first series only")

case("en_pie", "en", "pie", """
Item,Share (%)
Rent,52
Food,20
Transport,12
Leisure,9
Other,7
""", [("What is the largest share?", "Rent, 52 %"), ("Does the largest share exceed half?", "yes"),
      ("How many parts are there?", "5")], "pie", title="Household budget")

case("en_scatter", "en", "scatter", """
| Country | Income (k$) | Life expectancy (years) |
|---|---|---|
| Japan | 42 | 84 |
| Norway | 75 | 83 |
| Chile | 25 | 80 |
| Mexico | 20 | 75 |
| India | 7 | 70 |
| Nigeria | 5 | 53 |
| USA | 65 | 77 |
| France | 45 | 82 |
""", [("What is the relationship between income and life expectancy?", "positive: higher income goes with higher life expectancy, USA an exception"),
      ("Which country has the highest life expectancy?", "Japan, 84 years"), ("How many points (countries) are plotted?", "8")], "table")

case("en_flowchart_loop", "en", "flowchart", """
flowchart TD
  A((Order received)) --> B[Check stock]
  B --> C{In stock?}
  C -->|yes| D[Pack]
  C -->|no| E[Back-order]
  E --> B
  D --> F[Ship]
  F --> G((Delivered))
""", [("What happens when the item is not in stock?", "it is back-ordered, then the stock check is repeated (loop)"),
      ("What is the step right after 'Pack'?", "Ship"), ("Where does the process end?", "Delivered")], "flowchart")

case("en_flowchart_merge", "en", "flowchart", """
flowchart LR
  A((Web order)) --> C[Validate order]
  B((Phone order)) --> C
  C --> D{Payment OK?}
  D -->|yes| E[Fulfil]
  D -->|no| F[Contact customer]
  F --> C
  E --> G((Done))
""", [("How many entry points does the process have?", "2 (web order and phone order)"),
      ("What happens if payment is not OK?", "contact the customer, then back to validate order"), ("How many decisions are there?", "1")], "flowchart")

case("en_orgchart", "en", "orgchart", """
CEO
  CFO
    Accounting (3 people)
    Treasury (2 people)
  CTO
    Development (12 people)
    Operations (4 people)
  COO
    Sales (20 people)
""", [("How many direct reports does the CEO have?", "3 (CFO, CTO, COO)"), ("How many people are in Development?", "12"),
      ("Who is above Treasury?", "the CFO")])

case("en_sequence", "en", "sequence", """
sequenceDiagram
  User->>App: enter credentials
  App->>Server: verify
  Server->>DB: read user
  DB-->>Server: record
  Server-->>App: token
  App-->>User: logged in
""", [("How many participants are there?", "4 (User, App, Server, DB)"), ("What does the Server send back to the App?", "a token"),
      ("How many messages are exchanged?", "6")])

case("en_image_only", "en", "image", """
[Image: a photo of a printed bar chart. Legible: the title "Sales 2024"; four bars labelled France, Spain, Italy, Portugal;
France is clearly the tallest (its top is near the gridline marked 40); Portugal is the shortest (below the gridline marked
10). The other y-axis labels are blurred and unreadable.]
""", [("Which country has the tallest bar?", "France"), ("What is Spain's exact value?", "not readable / not stated (correct answer is 'not said')"),
      ("Does the reading say it comes from an image and is approximate?", "yes")], note="judge: Q2 is correct only if the text does NOT give a value")

# ------------------------------------------------------------------ FR
case("fr_table_small", "fr", "table", """
| Ville | Population (millions) | Superficie (km²) |
|---|---|---|
| Bordeaux | 0,26 | 49 |
| Nantes | 0,32 | 65 |
| Lille | 0,24 | 35 |
| Toulouse | 0,50 | 118 |
""", [("Quelle ville est la plus peuplée ?", "Toulouse"), ("Quelle est la superficie de Lille ?", "35 kilomètres carrés"),
      ("Combien de villes (lignes) ?", "4")], "table")

case("fr_table_medium", "fr", "table", """
Élève;Maths;Français;Histoire;Moyenne
Amina;15;12;14;13,7
Bastien;9;14;11;11,3
Chloé;18;16;17;17,0
David;11;8;10;9,7
Emma;13;13;13;13,0
Farid;7;10;9;8,7
Gaëlle;16;17;15;16,0
Hugo;12;11;14;12,3
""", [("Quel élève a la meilleure moyenne ?", "Chloé (17,0)"), ("Quelle est la note de Bastien en français ?", "14"),
      ("Combien d'élèves (lignes) ?", "8")], "table", note="notes sur 20 ; décimale à virgule")

rng = random.Random(11)
communes = ["Aix", "Albi", "Annecy", "Arles", "Auch", "Bastia", "Blois", "Brive", "Cahors", "Calais", "Cognac", "Colmar",
            "Dinan", "Dole", "Épinal", "Figeac", "Gap", "Lens", "Mende", "Millau", "Nevers", "Niort", "Orange", "Pau",
            "Rodez", "Royan", "Saumur", "Sens", "Tulle", "Vichy"]
lines = []
for i, c in enumerate(communes):
    hab = rng.randint(8_000, 140_000)
    alt = rng.randint(5, 700)
    sup = rng.randint(10, 90)
    lines.append([c, f"{rng.randint(1, 95):02d}", hab, alt, sup])
lines[16][2], lines[16][3] = 42_000, 1_050   # Gap : altitude max
lines[9][3] = 3                               # Calais : altitude min
lines[0][2] = 145_000                         # Aix : habitants max
lines[15][2] = 7_900                          # Figeac : habitants min
fr_big = "Commune;Département;Habitants;Altitude (m);Superficie (km²)\n" + "\n".join(";".join(map(str, r)) for r in lines)
case("fr_table_large", "fr", "table", fr_big,
     [("Quelle commune a le plus d'habitants ?", "Aix, 145 000"), ("Quelle commune est la plus haute en altitude ?", "Gap, 1 050 mètres"),
      ("Combien de communes (lignes) ?", "30")], "table", note="30 lignes ; le skill ne doit pas tout lire")

case("fr_table_vides", "fr", "table", """
| Produit | Prix (€) | Stock | Fournisseur |
|---|---|---|---|
| Marteau | 12,50 | 40 | Acme |
| Scie | 24,00 | — | Acme |
| Perceuse | 89,90 | 7 | |
| Niveau | 15,00 | 0 | Bolt |
| Pince | | 22 | Bolt |
""", [("Quel produit n'a pas de fournisseur indiqué ?", "Perceuse"), ("Quel est le stock du niveau ?", "0 (zéro)"),
      ("Quel produit n'a pas de prix ?", "Pince")], "table")

case("fr_barres", "fr", "bars", """
Région;Ventes (M€)
Île-de-France;120
Auvergne-Rhône-Alpes;65
Occitanie;40
Bretagne;30
Corse;6
""", [("Quelle région est en tête ?", "Île-de-France (120 M€)"), ("Quelles sont les ventes en Corse ?", "6 M€"),
      ("Combien de barres ?", "5")], "bars", title="Ventes par région")

case("fr_barres_groupees", "fr", "bars", """
| Tranche d'âge | Hommes (milliers) | Femmes (milliers) |
|---|---|---|
| 0 à 19 ans | 820 | 790 |
| 20 à 39 ans | 760 | 770 |
| 40 à 59 ans | 800 | 830 |
| 60 ans et plus | 650 | 810 |
""", [("Dans quelle tranche l'écart en faveur des femmes est-il le plus grand ?", "60 ans et plus (810 contre 650)"),
      ("Combien d'hommes de 20 à 39 ans ?", "760 milliers (760 000)"), ("Combien de séries ?", "2 : hommes et femmes")], "table")

case("fr_courbe", "fr", "line", """
Mois;Température (°C)
janvier;3,5
février;4,5
mars;8,2
avril;11,5
mai;15,8
juin;19,6
juillet;22,4
août;22,1
septembre;18,0
octobre;13,2
novembre;7,5
décembre;4,2
""", [("Quel est le mois le plus chaud ?", "juillet, 22,4 degrés"), ("Quelle est l'allure de la courbe ?", "monte jusqu'en juillet puis redescend (en cloche)"),
      ("Quelle est la température en janvier ?", "3,5 degrés")], "line", title="Températures moyennes à Lyon", note="courbe en cloche : début ≈ fin")

case("fr_courbe_deux_series", "fr", "line", """
| Année | France (%) | Allemagne (%) |
|---|---|---|
| 2018 | 9,0 | 3,4 |
| 2019 | 8,4 | 3,1 |
| 2020 | 8,0 | 3,8 |
| 2021 | 7,9 | 3,6 |
| 2022 | 7,3 | 3,1 |
| 2023 | 7,3 | 3,0 |
| 2024 | 7,5 | 3,4 |
""", [("Quel pays a le taux le plus bas ?", "l'Allemagne"), ("Quel est le taux français en 2024 ?", "7,5 pour cent"),
      ("Quelle est la tendance en France ?", "en baisse (de 9,0 à 7,5), légère remontée en 2024")], "table", title="Taux de chômage")

case("fr_camembert", "fr", "pie", """
Navigateur;Part (%)
Chrome;65
Safari;18
Autres;9
Edge;5
Firefox;3
""", [("Quelle est la plus grande part ?", "Chrome, 65 pour cent"), ("Dépasse-t-elle la moitié ?", "oui"),
      ("Combien de parts ?", "5")], "pie", title="Parts de marché des navigateurs")

case("fr_nuage", "fr", "scatter", """
| Appartement | Surface (m²) | Prix (k€) |
|---|---|---|
| A | 25 | 180 |
| B | 40 | 260 |
| C | 55 | 340 |
| D | 70 | 410 |
| E | 85 | 520 |
| F | 30 | 310 |
| G | 100 | 600 |
| H | 60 | 350 |
""", [("Quelle est la relation entre surface et prix ?", "positive : plus grand, plus cher ; F est une exception (petit et cher)"),
      ("Quel appartement est le plus cher ?", "G, 600 k€"), ("Combien de points ?", "8")], "table")

case("fr_flux_boucle", "fr", "flowchart", """
flowchart TD
  A((Demande reçue)) --> B[Vérifier le dossier]
  B --> C{Dossier complet ?}
  C -->|oui| D[Instruire]
  C -->|non| E[Demander les pièces]
  E --> B
  D --> F{Accord ?}
  F -->|oui| G[Notifier l'accord]
  F -->|non| H[Notifier le refus]
  G --> I((Fin))
  H --> I
""", [("Que se passe-t-il si le dossier est incomplet ?", "on demande les pièces, puis retour à la vérification du dossier"),
      ("Combien de décisions ?", "2"), ("Que se passe-t-il en cas d'accord ?", "on notifie l'accord, puis fin")], "flowchart")

case("fr_flux_fusion", "fr", "flowchart", """
flowchart LR
  A((Commande web)) --> C[Valider la commande]
  B((Commande téléphone)) --> C
  C --> D{Paiement accepté ?}
  D -->|oui| E[Préparer]
  D -->|non| F[Contacter le client]
  F --> C
  E --> G((Terminé))
""", [("Combien de points d'entrée ?", "2 (web et téléphone)"), ("Que se passe-t-il si le paiement est refusé ?", "on contacte le client, puis retour à la validation"),
      ("Combien de décisions ?", "1")], "flowchart")

case("fr_organigramme", "fr", "orgchart", """
Directrice générale
  DRH
    Recrutement (4 personnes)
    Paie (3 personnes)
  DSI
    Développement (15 personnes)
    Support (6 personnes)
  Directeur commercial
    Ventes (22 personnes)
    Marketing (5 personnes)
""", [("Combien de subordonnés directs a la directrice générale ?", "3 (DRH, DSI, directeur commercial)"),
      ("Quel est l'effectif du développement ?", "15"), ("Qui dirige la paie ?", "la DRH")])

case("fr_sequence", "fr", "sequence", """
sequenceDiagram
  Client->>Site: ajoute au panier
  Site->>Stock: vérifie la disponibilité
  Stock-->>Site: disponible
  Site->>Paiement: autorise
  Paiement-->>Site: accepté
  Site-->>Client: confirmation
""", [("Combien de participants ?", "4 (client, site, stock, paiement)"), ("Que répond le paiement au site ?", "accepté"),
      ("Combien de messages ?", "6")])

case("fr_carte_mentale", "fr", "mindmap", """
mindmap
  root((Projet vacances))
    Destination
      Italie
      Grèce
      Portugal
    Budget
      Transport
      Hébergement
      Repas
    Dates
      Juillet
      Août
    Activités
      Plage
      Randonnée
      Musées
      Cuisine
""", [("Combien de branches principales ?", "4"), ("Quels sont les éléments de la branche Budget ?", "transport, hébergement, repas"),
      ("Quelles dates sont envisagées ?", "juillet et août")])

case("fr_image_seule", "fr", "image", """
[Image : photo d'un camembert imprimé. Lisible : le titre « Répartition du budget » ; cinq parts ; la plus grande part est
étiquetée « Loyer » et occupe nettement plus de la moitié du disque ; une petite part est étiquetée « Loisirs ». Les
pourcentages imprimés sont flous et illisibles.]
""", [("Quelle est la plus grande part ?", "Loyer"), ("Quel est le pourcentage exact des loisirs ?", "illisible / non dit (la bonne réponse est « non dit »)"),
      ("La lecture dit-elle qu'elle vient d'une image et reste approximative ?", "oui")], note="juge : Q2 correcte seulement si aucun pourcentage n'est donné")

case("fr_interpretation", "fr", "line", """
Année;Chiffre d'affaires (M€)
2015;10
2016;12
2017;14
2018;16
2019;15
2020;11
2021;17
2022;21
2023;23
2024;25

[L'auditeur demande ensuite : « Pourquoi le creux en 2020 ? »]
""", [("Quelle est la valeur en 2020 ?", "11 M€"), ("La réponse à « pourquoi » est-elle présentée comme une interprétation, distincte des données ?", "oui (marqueur du type « mon interprétation »)"),
      ("La réponse dit-elle que le graphique ne donne pas la cause ?", "oui")], "line", note="demande d'interprétation (niveau 4) ; la donnée ne contient pas la cause")

Path(__file__).with_name("cases.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(C), "cases;", sum(c["lang"] == "en" for c in C), "en,", sum(c["lang"] == "fr" for c in C), "fr")
