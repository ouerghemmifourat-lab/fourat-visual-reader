# 03 - Research literature survey (chart/table/diagram -> speech)

Conventions: every item carries a URL I fetched (F) or only saw in search results (S). "unverified" = not confirmed on a primary page. Numbers are copied from the cited page; none invented. Survey date: 2026-11-02.

## 0. Take-aways for the SKILL.md (derived from the evidence below)
1. "Structure first, essentials, detail on demand" is supported by: the 4-level model (L1 construction is useful mainly combined with L2/L3), Olli / Chart Reader / VizAbility (overview then drill-down), TADA and Arboretum (questions and several representations beat one fixed description), Siu et al. (description before sonification, secondary source).
2. Lead with L2 (statistics: extrema, ranges) and L3 (overall trend in plain language). Blind readers ranked L2 and L3 most useful; 63% of blind participants wanted no editorializing (L4). Make L4 opt-in and labeled as interpretation.
3. Plain language beats statistical jargon for trends (some blind readers, Lundgard & Satyanarayan).
4. Never speak a number that was not in the source: VLM chart summaries hallucinate. Read from the data table/spec when available; check that every spoken number exists in the source (ChartCap, Islam et al., ChartHal).
5. Spoken lists: no hard "7+-2" rule. Cowan ~4 chunks; Commarford 2008 found broad menus beat deep ones. Group in chunks of ~3-4 with pauses, but avoid deep nested turns.
6. Numbers/units are a text-normalization problem (context decides the reading); normalize explicitly with a locale before the TTS (Zhang/Sproat). Pauses inside long digit strings help recall (Elmers et al.).
7. VizWiz shows many blind-user questions are unanswerable from the image: the agent must say "I cannot tell" instead of guessing.

## 1. Chart-to-text / chart summarization

### 1.1 Obeid & Hoque 2020 - Chart-to-Text (Statista, transformer)
- Jason Obeid, Enamul Hoque. INLG 2020 (ACL Anthology 2020.inlg-1.20), arXiv 2010.09142.
- URLs: https://arxiv.org/abs/2010.09142v2 (S), https://aclanthology.org/2020.inlg-1.20 (S)
- Findings: first neural chart-summary dataset; content selection 55.42% vs 8.49% for the base model (per abstract); motivated by visually impaired users.
- Licence: not checked (unverified).

### 1.2 Kantharaj et al. 2022 - Chart-to-Text benchmark
- Shankar Kantharaj, Rixie Tiffany Ko Leong, Xiang Lin, Ahmed Masry, Megh Thakkar, Enamul Hoque, Shafiq Joty. ACL 2022 (2022.acl-long.277), arXiv 2203.06486. (Author list from memory/search; "seven authors" confirmed, names unverified.)
- URL: https://arxiv.org/abs/2203.06486 (F)
- Findings: 44,096 charts from two sources (Statista, Pew); BLEU plus human evaluation; best models are fluent but "suffer from hallucinations and factual errors" and struggle with complex trends.
- Licence: arXiv page shows CC BY 4.0 for the paper. Repo https://github.com/vis-nlp/Chart-to-text (F) is GPL-3.0 and states no terms for the Statista/Pew source material: redistribution rights of the data unverified.

### 1.3 SciCap (Hsu, Giles, Huang)
- Findings of EMNLP 2021 (2021.findings-emnlp.277), arXiv 2110.11624. URL: https://arxiv.org/abs/2110.11624 (F)
- Findings: >2M figures from >290k CS arXiv papers (2010-2020); graph plots are 19.2% of figures; authors report "steep challenges". Captions are author-written, not accessibility-oriented (my inference).
- Licence: not stated on page (unverified).

### 1.4 AutoChart (Zhu et al., RANLP 2021)
- Not searched or fetched. Unverified, do not cite until checked.

### 1.5 VisText (Tang, Boggust, Satyanarayan)
- ACL 2023 (2023.acl-long.401, Outstanding Paper), arXiv 2307.05356. URL: https://arxiv.org/abs/2307.05356 (F)
- Findings: 12,441 chart-caption pairs; each chart as image + data table + scene graph. Captions: synthetic L1 (construction) and human L2/L3 (stats, trends) per https://github.com/mitvis/vistext (F). Prefix-tuning controls the semantic level. Six qualitative error categories.
- Licence: repo lists GPL-3.0; no separate dataset licence stated (F).

### 1.6 ChartQA (Masry, Long, Tan, Joty, Hoque)
- Findings of ACL 2022, arXiv 2203.10244. URL: https://arxiv.org/abs/2203.10244v1 (S)
- Findings: 9.6K human-written + 23.1K generated questions; complex reasoning remains hard.
- Licence: GPL-3.0 per HF card https://huggingface.co/datasets/ahmed-masry/ChartQA (F).

### 1.7 PlotQA (Methani, Ganguly, Khapra, Kumar)
- WACV 2020, arXiv 1909.00997. URL: https://arxiv.org/abs/1909.00997v3 (S)
- Findings: 28.9M QA pairs over 224,377 plots; 26% of questions have answers outside a fixed vocabulary (numeric). Reported accuracies differ between arXiv versions: unverified.
- Licence: not checked.

### 1.8 ChartX & ChartVLM (Xia et al.)
- arXiv 2402.12185 (v6 Apr 2025); published venue unverified. URL: https://arxiv.org/abs/2402.12185v6 (S)
- Findings: 18 chart types, 7 tasks (QA, description, summarization, redraw), 22 topics. ChartVLM predicts structured data first then reasons (supports "extract table, then verbalize").
- Licence: not checked.

### 1.9 Islam et al. 2024 - Are LVLMs up to chart comprehension?
- Mohammed Saidul Islam, Raian Rahman, Ahmed Masry, Md Tahmid Rahman Laskar, Mir Tafseer Nayeem, Enamul Hoque. arXiv 2406.00257 (v2 Oct 2024); published venue unverified.
- URLs: https://arxiv.org/abs/2406.00257 (F), https://arxiv.org/html/2406.00257v2 (F)
- Findings: fluent text with high-level insights but "hallucinations, factual errors, and data bias". Automatic metrics used: BLEU, BLEURT, CIDEr, BERTScore, perplexity (similarity/fluency, not truth); no metric-vs-human correlation reported. Manual check of 100 samples: factual-error rates about GPT-4V 5%, Claude-3 16%, Gemini 27% on the HTML page; an earlier search summary gave 4%/5%/17%. The sources conflict: treat exact values as unverified. FAVA average error counts per summary (Pew: Gemini 0.89, GPT-4V 0.92, Claude-3 1.76; Statista: 1.26 / 1.35 / 2.23).

### 1.10 ChartCap (Lim, Ahn, Kim)
- ICCV 2025 Highlight, arXiv 2508.03164. URL: https://arxiv.org/abs/2508.03164 (F)
- Findings: 565K real charts; captions restricted to what is visible in the chart; cycle-consistency human verification. Proposes the Visual Consistency Score (VCS): regenerate the chart from the caption and compare it to the original (reference-free hallucination metric). Fine-tuned models claim fewer hallucinations.
- Licence: not stated on page (unverified).

### 1.11 ChartHal (Wang et al.)
- arXiv 2509.17481 (Sep 2025). URL: https://arxiv.org/abs/2509.17481 (F)
- Findings: 1,062 human-validated samples; SOTA LVLMs hallucinate heavily; questions about information absent from, or contradicting, the chart trigger the most hallucinations. Page cites GPT-5 34.46% and o4-mini 22.79% accuracy (page wording ambiguous: unverified which model/metric).

Metric note: BLEU/BLEURT/CIDEr/BERTScore measure overlap or fluency, not truth (1.9). Factuality needs human audit, FAVA-style taxonomy or reconstruction checks (VCS). Skill rule: numbers come from the table; verify each spoken number against the source.

## 2. Accessible description for blind users

### 2.1 Lundgard & Satyanarayan - four-level model (primary source read)
- "Accessible Visualization via Natural Language Descriptions: A Four-Level Model of Semantic Content". Alan Lundgard, Arvind Satyanarayan. IEEE TVCG 2022 (IEEE VIS 2021), arXiv 2110.04406.
- URLs: https://arxiv.org/abs/2110.04406 (F), https://vis.mit.edu/pubs/vis-text-model/ (F)
- Built by grounded-theory analysis of 2,147 sentences from 120+ participants.
- Levels:
  - L1 Elemental and encoded properties: chart type, title, legend, encoding channels, axes and scales. Example: "Mortality rate is plotted on the vertical y-axis from 0 to 15%."
  - L2 Statistical concepts and relations: descriptive statistics, extrema, outliers, correlations, point-wise comparisons from the data.
  - L3 Perceptual and cognitive phenomena: overall trends, multi-series patterns, exceptions, gaps, in commonplace language (e.g. prices "seem to fluctuate but nevertheless increase"). Depends on a human perceiver.
  - L4 Contextual and domain-specific insights: explanations from events, social/political context, domain knowledge (e.g. attributing a 2008 drop to the financial crisis).
- Study: 30 blind + 90 sighted readers ranked one description per level for 15 charts (1 = least, 4 = most useful).
  - Blind: L2 and L3 most useful, L1 and L4 least; L3 vs L4 significant (p < 0.001). Sighted: L3 and L4 most useful.
  - L1 is bimodal (ranked most useful 101 times by blind, 87 by sighted readers).
  - 63% (n=19) of blind readers: avoid author interpretation (L4). 40% (n=12): best descriptions combine levels; one reader called L1 alone "almost useless" but valuable with L2/L3; some preferred layperson language to statistical terms.
  - 41% (n=37) of sighted readers valued L4; 4% asked to exclude it.
  - No significant differences by chart type, topic or difficulty.
- Open problems named by authors: conveying statistical ideas in non-statistical language (L3) is unsolved; let readers choose/combine levels; L4 mostly human work; English and canonical chart types only (other languages untested); co-develop with disabled readers. Limitation: exemplar descriptions curated by the authors; groups recruited and paid differently.

### 2.2 Tools and user studies
- VoxLens: Making Online Data Visualizations Accessible with an Interactive JavaScript Plug-In. Ather Sharif, Olivia H. Wang, Alida T. Muongchan, Katharina Reinecke, Jacob O. Wobbrock. CHI 2022. URL: https://wildlab.cs.washington.edu/Publications_files/Sharif_CHI2022.pdf (S; PDF unreadable by my fetch tool; ACM page 403). Voice-driven: summary, sonification, spoken questions. 21 screen-reader users (press says 22): +122% information-extraction accuracy and -36% interaction time vs conventional access (S). A later dissertation reports 164% / 50% (S; unverified which applies). No arXiv version found.
- Olli: An Extensible Visualization Library for Screen Reader Accessibility. Matthew Blanco, Jonathan Zong, Arvind Satyanarayan. IEEE VIS 2022 poster. URL: https://vis.mit.edu/pubs/olli (S). Chart as ARIA tree with levels of detail (overview then drill-down); Vega, Vega-Lite, Observable Plot.
- Chart Reader: Accessible Visualization Experiences Designed with Screen Reader Users. John R. Thompson, Jesse J. Martinez, Alper Sarikaya, Edward Cutrell, Bongshin Lee. CHI 2023, DOI 10.1145/3544548.3581186. URL: https://www.microsoft.com/en-us/research/publication/chart-reader-accessible-visualization-experiences-designed-with-screen-reader-users/ (F). Five-month co-design with 10 screen-reader users; findings organized by design dimension; open-source engine (https://github.com/microsoft/chart-reader, S).
- Supporting Accessible Data Visualization Through Audio Data Narratives. Alexa F. Siu, Gene S-H Kim, Sile O'Modhrain, Sean Follmer. CHI 2022, DOI 10.1145/3491102.3517678. URL: https://hci.stanford.edu/publications/paper.php?id=473 (S; fetch failed on certificate). Auto-generated spoken description + sonification of time series; 16 screen-reader users gained significantly more insights with narratives (S). A workshop summary says to play the description before the sonification (secondary, unverified).
- VizAbility: Enhancing Chart Accessibility with LLM-based Conversational Interaction. Joshua Gorniak, Yoon Kim, Donglai Wei, Nam Wook Kim (author list from search; unverified). UIST 2024 (DOI 10.1145/3654777.3676414 per S), arXiv 2310.09611. URL: https://arxiv.org/html/2310.09611v4 (F). Keyboard tree + LLM Q&A. Query taxonomy: analytical, visual, contextual, navigation. 979 real BLV questions; classification accuracy 87.39%; human rating "Very Good" 77.36% (82.50% Very Good + Good); GPT-4V baseline 27.96% Very Good. Only 6 BLV participants; users struggled to know which query types exist, so authors added cold-start suggestions and a raw data table. Authors' future work: customization, better benchmarks, vision models.
- Making Charts Speak: LLM-Based Conversational Chart QA for BLV Users (Das, Tarun, Mueller). Venue/year unverified. URL: https://researchr.org/publication/DasTM26-0 (S). Claims 98.1% on literacy benchmarks and 94% accuracy over 185 questions with 15 participants: abstract-level, unverified.
- VizWiz Grand Challenge: Answering Visual Questions from Blind People. Danna Gurari, Qing Li, Abigale J. Stangl, Anhong Guo, Chi Lin, Kristen Grauman, Jiebo Luo, Jeffrey P. Bigham. CVPR 2018, arXiv 1802.08218. URL: https://arxiv.org/abs/1802.08218 (F). >31,000 visual questions, spoken by blind users, 10 crowd answers each; low-quality images, conversational questions, many unanswerable. Dataset licence not stated on arXiv page (unverified).
- SeeChart: not found in my searches; omitted.

### 2.3 Audio / sonification vs verbal description
- No clean head-to-head found; evidence is task-dependent. A 2025 user-agency study (secondary summary, unverified) reports sonification valued for trends, text for specific values, tables for comparisons. Siu et al. combine both. A claimed "2026 Chundury et al." comparison of Olli / TactualPlot / Monarch appeared only on a third-party review site: unverified, do not cite.
- Skill implication: speech carries exact values and the L2/L3 gist; if sonification exists, speak the description first (weak evidence).

## 3. Table-to-text and tables read aloud
- ToTTo: A Controlled Table-To-Text Generation Dataset. Ankur P. Parikh et al. EMNLP 2020, arXiv 2004.14373. URL: https://arxiv.org/abs/2004.14373v3 (S). >100K Wikipedia tables with highlighted cells and a one-sentence description; the controlled setup anchors on highlighted cells (idea for us: tell the agent which cells matter). Licence CC BY-SA 3.0; 120,761 / 7,700 / 7,700 split (F https://huggingface.co/datasets/google-research-datasets/totto).
- Table-to-Text: Describing Table Region with Natural Language (WikiTableText). Junwei Bao, Duyu Tang, Nan Duan, et al. AAAI 2018, arXiv 1805.11234. URL: https://arxiv.org/abs/1805.11234v1 (S). 13,318 sentences for 4,962 tables; row-level description; BLEU-4 38.23. Licence not checked.
- Logical Natural Language Generation from Open-Domain Tables (LogicNLG). Wenhu Chen et al. ACL 2020 (2020.acl-main.708), arXiv 2004.10404. URL: https://huggingface.co/papers/2004.10404.md (S). Logical-inference sentences (comparisons, superlatives, counts) from Wikipedia tables; follow-up work says fidelity and control are weak (S via PLOG, https://arxiv.org/pdf/2205.12697v2.pdf). Licence not checked.
- Find and Seek: Assessing the Impact of Table Navigation on Information Look-up with a Screen Reader. ACM TACCESS 2020, DOI 10.1145/3342282 (authors not retrieved; Emory group). URL: https://www.cs.emory.edu/~kwil271/pdf/find_seek_taccess2020.pdf (S; fetch failed). Per secondary summary: controlled experiment, 21 screen-reader users; proper headers/structure matter; blank cells announced ambiguously. Unverified.
- Large-scale HTML table audit (49.28% of table elements used for layout; captions and header associations rare): third-party review site only (S): unverified, do not cite.
- Gap: I found no peer-reviewed work on summarizing tables specifically for speech output.

## 4. Diagrams, flowcharts, mind maps
- AI2D: A Diagram Is Worth A Dozen Images. Aniruddha Kembhavi et al. ECCV 2016, arXiv 1603.07396. URL: https://arxiv.org/pdf/1603.07396 (S). About 5,000 grade-school science diagrams, annotated with constituents and relations; 4,000 train / 1,000 test. Licence not stated in sources (unverified).
- FlowVQA: Mapping Multimodal Logic in Visual Question Answering with Flowcharts. Findings of ACL 2024, arXiv 2406.19237 (first author Singh; full author list unverified). URL: https://arxiv.org/abs/2406.19237 (F). 2,272 flowchart images, 22,413 QA pairs from three sources; tests information localization, decision-making, logical progression; open and proprietary VLMs struggle with visual/spatial reasoning and show directional bias. Skill implication: build the spoken flow from a parsed graph (nodes/edges), not from raw image reading. Page links CC BY 4.0 (dataset licence itself unverified).
- TADA: Making Node-link Diagrams Accessible to Blind and Low-Vision People. Yichun Zhao, Miguel A. Nacenta, Mahadeo A. Sukhai, Sowmya Somanath. CHI 2024 (Honourable Mention), arXiv 2311.04502. URL: https://arxiv.org/abs/2311.04502 (F). Interviews with 15 people; tablet system with tones + speech (mind maps, taxonomies); evaluated with 25 participants; users gained different perspectives and completed tasks.
- Nonvisual Support for Understanding and Reasoning about Data Structures (Arboretum). Brianna L. Wimer, Ritesh Kanchi, Kaija Frierson, Venkatesh Potluri, Ronald Metoyer, Jennifer Mankoff, Miya Natsuhara, Matt X. Wang. CHI 2026 (to appear), arXiv 2601.19168. URL: https://arxiv.org/abs/2601.19168 (F). Alt text describes appearance, not structure; tabular + navigable + tactile formats from a text spec; complementary representations help; tactile best for complex tasks.
- DiGVis (directed graphs for the visually challenged): search summary only, 28 participants, unverified.
- Gap: no dataset found for describing mind maps / concept maps aloud.

## 5. Spoken delivery
- Miller 1956, "The magical number seven, plus or minus two", Psychological Review 63:81-97, DOI 10.1037/h0043158. URL: https://pubmed.ncbi.nlm.nih.gov/8022966/ (S). Limit is in chunks; secondary summaries say ~7 digits, ~6 letters, ~5 words (unverified).
- Cowan 2001, "The magical number 4 in short-term memory", Behavioral and Brain Sciences 24(1):87-114, DOI 10.1017/S0140525X01003922. URL: https://pubmed.ncbi.nlm.nih.gov/11515286/ (S). Focus-of-attention capacity about 4 chunks. Skill rule: at most 3-4 items per spoken group, then pause.
- Commarford, Lewis, Smither, Gentzler 2008, "A comparison of broad versus deep auditory menu structures", Human Factors 50(1):77-89, DOI 10.1518/001872008X250665. URL: https://stars.library.ucf.edu/facultybib2000/233 (S). Broad IVR menus outperformed deep ones, more so for low working-memory users; challenges the "5 items or fewer" rule attributed to Miller. Implication: avoid many nested turns; give a short list then offer more.
- Wolters et al., "Reducing Working Memory Load in Spoken Dialogue Systems" (older users; fewer options per turn and confirmations). URL: https://era.ed.ac.uk/handle/1842/3956 (S). Details unverified.
- Elmers, Werner, Muhlack, Moebius, Trouvain: ESSV 2021 "Evaluating the Effect of Pauses on Number Recollection in Synthesized Speech"; related Interspeech 2021 "Take a Breath" (breath noises and sentence length). URLs: https://www.coli.uni-saarland.de/~trouvain/docs/Elmers_et_al_2021a.pdf (S; unreadable), https://mikeyelmers.github.io/publications/elmers_ESSV2021_Presentation.pdf (S). A silent pause inside a 7-digit sequence improved recall of the following digit; none of the TTS systems tested inserted such pauses automatically; shorter sentences were recalled better. Effect sizes not obtained: unverified. Closest evidence for SSML break use on numbers.
- Ould Ouali et al. 2025, "Improving French Synthetic Speech Quality via SSML Prosody Control", ICNLSP 2025 (pp. 302-314), arXiv 2508.17494. URL: https://arxiv.org/abs/2508.17494 (F). LLM-predicted SSML breaks/pitch/rate/volume for French: break placement 99.2% F1; MOS naturalness 3.20 to 3.87 (p < 0.005); 15 of 18 listeners preferred SSML output. Measures naturalness, not comprehension. French evidence.
- Zhang, Sproat et al., "Neural Models of Text Normalization for Speech Applications", Computational Linguistics 2019 (DOI 10.1162/COLI_a_00349). URL: https://research.google/pubs/neural-models-of-text-normalization-for-speech-applications/ (S). Same string reads differently by context ("123" as "one hundred twenty three" or "one twenty three"); neural models make occasional absurd errors, so finite-state covering grammars constrain them. Skill rule: normalize numbers, units, dates yourself with an explicit locale.
- Gorman & Sproat, "Minimally Supervised Number Normalization", TACL. URL: https://transacl.org/index.php/tacl/article/download/897/213/2738 (S). Hand-built number grammars for ~70 languages at Google; hard cases include Russian gender/case agreement.
- Gap: no study found testing SSML (rate, emphasis, say-as) on comprehension of tabular/chart content; no peer-reviewed unit-verbalization study for French located. (Practical note, not literature: French has regional forms soixante-dix / septante and decimal comma.)

## 6. OPEN PROBLEMS named by the literature
1. Conveying statistical ideas in non-statistical language (L3) is unsolved; reader-specific content needs and customizable level mix; L4 largely human. Source: https://vis.mit.edu/pubs/vis-text-model/
2. Hallucination and factual errors persist in chart captioning; automatic metrics do not measure truth. Sources: https://arxiv.org/abs/2203.06486, https://arxiv.org/abs/2406.00257, https://arxiv.org/abs/2508.03164, https://arxiv.org/abs/2509.17481
3. LLM chart QA for BLV users: small studies (6 participants in VizAbility), mishandled unanswerable/ambiguous queries, users not knowing what to ask; need benchmarks and vision-model integration. Source: https://arxiv.org/html/2310.09611v4
4. VLMs weak on flowchart spatial reasoning and show directional bias. Source: https://arxiv.org/abs/2406.19237
5. Static descriptions are inadequate for node-link diagrams; Q&A, navigation and multiple representations are needed. Sources: https://arxiv.org/abs/2311.04502, https://arxiv.org/abs/2601.19168
6. Non-English and non-canonical charts untested in the four-level work (Lundgard & Satyanarayan). I located no EN/FR comparative study.
7. Literature gaps I found (my search gaps, not proof of absence): speech-first table summarization; SSML effect on chart/table comprehension; end-to-end evaluation of voice agents reading charts.
8. Licence hygiene: Statista/Pew-derived data has unclear redistribution terms; ChartQA, VisText and Chart-to-Text repos are GPL-3.0 (copyleft); ToTTo is CC BY-SA 3.0 (share-alike). Check before bundling any data in the open-source skill.

## 7. Method caveats
- WebFetch could not read PDFs (VoxLens, Elmers) and some hosts (ACM DL 403, Stanford HCI certificate error); those items rely on search-result summaries and are flagged (S).
- Third-party review sites (e.g. a11y-paradise) were not treated as sources; items relying only on them are marked unverified.
- AutoChart, SeeChart, DiGVis, Wolters and several licences were not verified.
