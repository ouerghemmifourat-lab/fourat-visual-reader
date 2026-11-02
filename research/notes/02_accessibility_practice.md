# 02 - Accessibility practice: how blind / low-vision users consume tables and charts by ear

Compiled 2026-11-02. Every claim carries a URL fetched (F) or seen only in search results (S). "unverified" = not confirmed on a primary page. Quotes are under 15 words.

## 1. Screen readers on tables

| Reader | What is announced | Keys | Source |
|---|---|---|---|
| NVDA | Headers are read if "Report table row / column headers" is on in Document Formatting. Word/Excel need manual header setup. | Cell move: Ctrl+Alt+arrows; first/last col = Ctrl+Alt+Home/End; first/last row = Ctrl+Alt+PgUp/PgDn. Say all in row/column: NVDA+Ctrl+Alt+Right/Down. Read entire row/column (no caret move): NVDA+Ctrl+Alt+Left/Up. Set col/row headers (Word/Excel): NVDA+Shift+C / NVDA+Shift+R. Browse mode: T / Shift+T next/prev table. | NVDA User Guide (page title says 2026.3), https://download.nvaccess.org/documentation/userGuide.html (F). The exact "table with N columns and M rows" wording and the "Report table cell coordinates" option were in the unread part of the page: unverified. |
| JAWS | On entering a table: "table with seven columns and five rows" (dimensions); then column and row headers for the current cell. | T / Shift+T next/prev table; Windows+Alt+Down/Up next/prior row (Freedom Scientific keystrokes PDF, S); Ctrl+Alt+arrows for cells (third-party only, unverified); Esc leaves the table layer. | https://support.freedomscientific.com/teachers/lessons/7.3_Transcript-ReadingTables.htm (S only; direct fetch returned 403); https://www.freedomscientific.com/Content/Documents/Manuals/JAWS/Keystrokes.pdf (S). |
| VoiceOver (macOS) | "Grouping" gives "a summary of a table and its cells" while arrowing, without interacting. | VO+Cmd+= toggles grouping for one table; VO+Home/End first/last cell; VO+Cmd+Y / +Shift+Y next/prev column. Exact summary wording not given. | Apple, https://support.apple.com/en-euro/guide/voiceover/vo27958/mac (F). VO+Cmd+T next table: community guides only, https://dequeuniversity.com/screenreaders/voiceover-keyboard-shortcuts (S). |

Verbosity: JAWS offers high/medium/low verbosity; at high it adds wayfinding (start and end of regions); for tables it can include table size and whether row and column labels repeat for every cell (Zong et al. 2022, https://arxiv.org/pdf/2205.04917, F, citing JAWS docs). "More content is not always better" (same paper).

### What users complain about
- WebAIM Screen Reader Survey 10 (Dec 2023 - Jan 2024): "Complex data tables" ranked 10th among most problematic items; "Images with missing or improper descriptions" 6th; "Screens or parts of screens that change unexpectedly" 4th. https://webaim.org/projects/screenreadersurvey10/ (F).
- Large tables, 18 BLV users (Wang, Srinivasan, Kim, DIS 2024): difficulty comes from table size, getting lost, forgetting units and column names. Quote: "I sometimes have difficulties remembering the name of the row and column." Participants wanted an overview first, summary statistics, subsets on demand ("a simpler table"). https://pages.cs.wisc.edu/~yeaseulkim/assets/papers/2024_table.pdf (F, PDF read locally). Workaround seen: arrow left then right to hear the column name again.
- Zong et al. 2022 (13 BLV readers): at most, participants tabbed through 20-30 rows; 8 of 13 wanted to filter and sort without "wading line by line"; they want an overview then drill-down. Screen readers "explicitly linearize" reading, so users must remember prior output. https://arxiv.org/pdf/2205.04917 (F).
- Cell-by-cell navigation is "not suitable for large data" (search summary of small studies, papers not opened): https://www.sigaccess.org/2009/11/non-visual-navigation-of-excel-spreadsheet/ (S). Unverified.
- A 2023 study of 16 BLV people: 15 of 16 "could not meaningfully extract information from line charts" (secondary summary, unverified): https://a11y-paradise.onrender.com/reviews/69b2c5a7efe2ba05e36774d3 (S).

### Rules to adopt (from section 1)
1. Announce table size and header names before the first row (JAWS pattern).
2. Repeat the row and column label when the user may be lost; make repetition adjustable (JAWS verbosity).
3. Offer move-by-row and move-by-column plus "read whole row" / "read whole column" (NVDA model).
4. Offer a smaller derived table on demand (Wang et al.).
5. Keep a "where am I" command: row, column, header, unit.

## 2. Guidelines for describing charts and diagrams

### W3C WAI, Images Tutorial: Complex images
- https://www.w3.org/WAI/tutorials/images/complex/ (F). Updated 8 April 2026. Licence: (c) 2026 W3C, W3C permissive document rules; terms at "Permission to Use WAI Material" (exact licence name unverified).
- Rules: (1) two parts, a short description plus a long description; (2) the long description gives "values, relationships, and trends" in text; (3) show the long description in the main content for everyone; (4) summarise the image in nearby text (e.g. "The following graph shows that visitors were lost in the first quarter"); (5) aria-describedby flattens headings and tables, so use it for text only.

### W3C WAI, Tables Tutorial
- https://www.w3.org/WAI/tutorials/tables/ (F). Updated 16 Feb 2023. Same W3C licence note.
- Rules: "Header cells must be marked up with `<th>`"; scope/headers for multi-level headers; a caption names the topic; a summary gives orientation for complex tables.

### Cesal, "Writing Alt Text for Data Visualization" (Nightingale / Data Visualization Society)
- https://nightingaledvs.com/writing-alt-text-for-data-visualization (F). 23 July 2020, updated 5 Aug 2021. Licence: none stated, (c) Data Visualization Society.
- Rules: formula "Chart type of type of data where reason for including chart"; "There should be a point to every visual"; keep it short because alt text is read linearly; put a long description in HTML when possible; link the source outside the alt text.

### Datawrapper Academy
- https://www.datawrapper.de/academy/how-to-write-good-alternative-descriptions-for-your-data-visualization (F). Last updated 31 Mar 2021. Licence not stated.
- Rules: order = chart type (optional), data type, takeaway; do not repeat title, source or byline, since screen readers already read them; static charts get key data points; live charts get the highlighted values and trends and must be updated when the highlight changes.

### Lundgard and Satyanarayan, four levels of semantic content
- "Accessible Visualization via Natural Language Descriptions: A Four-Level Model", IEEE TVCG (VIS 2021, published 2022), MIT CSAIL. https://vis.csail.mit.edu/pubs/vis-text-model/ (F). DOI 10.1109/TVCG.2021.3114770. Licence: open-access PDF; the page says the corpus is released under an unnamed open-source licence (check before reuse).
- L1 chart construction (type, axes, encodings); L2 statistics and relations (extrema, comparisons); L3 perceived trends and patterns; L4 contextual and domain explanation.
- Findings (30 blind readers vs 90 sighted): blind readers ranked L2 and L3 most useful, L1 and L4 least; 63% did not want author editorialising (L4); about 40% wanted a mix of levels; L1-only descriptions called "almost useless".
- Rules: keep L1 brief, spend most words on L2 and L3, skip L4 unless asked, never present opinion as data.

### Zong et al., "Rich Screen Reader Experiences for Accessible Data Visualization" (EuroVis 2022)
- https://arxiv.org/pdf/2205.04917 (F). MIT, CMU, UCL; 13 BLV participants. Licence unverified (arXiv).
- Three design dimensions: structure, navigation, description (content, composition, verbosity). Hierarchical tree structure. Blind users share the sighted goal: "an initial holistic overview followed by comparing" and drilling down. A participant: "I always want more layers and details, but some charts had too much."
- Rules: overview first, then drill-down on demand; give location cues ("cursors and roadmaps"); let users set verbosity.

### Government Analysis Function (UK)
- "Data vis and accessibility - links to content and answers to questions", 19 May 2022 (archived page). https://analysisfunction.civilservice.gov.uk/blog/data-vis-and-accessibility-links-to-content-and-answers-to-questions (F). No licence stated.
- Rules: "the text alternative should be that message" when readers take away a message; if readers read values, give a marked-up table or data download; no placeholder alt such as "image description in body text below" (it causes "unnecessary auditory clutter"); order: headline, statistical title, chart, alt text, source, data link, footnotes.
- Companion post "Text descriptions for data visualisations", 13 April 2023, https://accessibility.blog.gov.uk/author/sean-snee-communicating-analysis-support-analysis-function (F, stub only, no rules). The Analysis Function Charts guidance and ONS pages themselves were not fetched: unverified. A third-party R package page (https://best-practice-and-impact.github.io/afcharts/articles/accessibility.html, S) says all plots need alt text.

### DIAGRAM Center (Benetech) / NCAM-WGBH Image Description Guidelines
- Intro page: https://www.wgbh.org/ncam-resources/2026-08-19/image-description-guidelines (F). Principles: "creating an accessible description differs greatly depending on the type of image"; brevity, focus on data, consistent language, accessible lists and tables, headers. Separate pages for Graphs, Tables, Illustrated and Relational diagrams. Licence not stated on the page; the Poet tool is called open source (licence unverified). The DIAGRAM site fetch failed (certificate error), so graph-specific pages were not read.
- Via a secondary summary (https://www.sigaccess.org/?p=1270, F, unverified against the original): graphs include title and axis labels, trends not already in the text, actual data points for simple charts, a data table for complex ones; flowcharts: diagram type, number of elements, connector types, overall shape, start and end points first, then details; complex flowcharts as nested lists.

### NCAM-WGBH, Effective Practices for Description of Science Content within Digital Talking Books
- Authors Gould, O'Connell, Freed; Dec 2008; NSF-funded; four-year research with describers, students and scientists with vision loss. Intro https://www.wgbh.org/ncam-resources/2026-08-11/effective-practices-for-description-of-science-content-introduction (F). Licence: "(c) 2008 GBH Educational Foundation", no open licence stated.
- The intro says a brief alt-tag does not convey the information inside a diagram (paraphrase).
- Tables page (F, https://www.wgbh.org/ncam-resources/2026-08-11/effective-practices-for-description-of-science-content-within-digital-talking-books-tables): splitting a multi-layer table "will aid in navigation and comprehension"; replace symbols with words ("Quantity zero" for a hyphen, "standard error" for a footnote marker); for a simple table put the caption and the question in the description, not the layout.

### Chartability
- https://chartability.fizz.studio/ (F). Elavsky, Bennett, Moritz, Computer Graphics Forum 41(3), 2022, DOI 10.1111/cgf.14522 (S, https://diglib.eg.org/handle/10.1111/cgf14522). Licence: CC-BY-SA 3.0 Unported (per site). 7 principles (POUR + CAF), about 50 heuristics, workbook at https://chartability.github.io/POUR-CAF/ (not opened). Specific screen-reader heuristics are unverified.
- Use: an audit checklist for our output (text alternative, data table, navigation), not a source of speech rules.

### Highcharts Accessibility module
- https://www.highcharts.com/docs/accessibility/accessibility-module-feature-overview (F). Product docs, no reuse licence stated.
- The first thing heard is an information region: title, chart type, axes, and the author description "if provided"; users can read point values, view a data table, hear sonification, get dynamic-update announcements; strings are translatable via `lang.accessibility`.
- From search (S, https://www.highcharts.com/docs/accessibility/configure-the-accessibility-module): per-point `valueDescriptionFormat`; individual points are not exposed on large series by default (`pointDescriptionEnabledThreshold`). Rule: do not read every point of a big series; summarise and offer sonification.

### Apple Audio Graphs
- https://developer.apple.com/documentation/accessibility/audio-graphs.md and https://developer.apple.com/documentation/accessibility/axchart.md (S only, not fetched). `AXChartDescriptor` holds title, axes, data points and a summary of key takeaways; the x-axis maps to pitch over time; reachable from the VoiceOver rotor; iOS 15+, macOS 12+. Details unverified.
- Zong et al. quote a researcher saying Apple's Data Comprehension reading all data is "very difficult ... play-or-stop" (F, arXiv above).

## 3. Flowcharts, org charts, diagrams

- NCAM Basic Flow Chart page (F): https://www.wgbh.org/ncam-resources/2026-08-11/effective-practices-for-description-of-science-content-within-digital-talking-books-basic-flow-chart. Licence as above (none open).
  Rules: (1) open with a short overview naming distinct elements and number of start points; (2) number each box and list possible next steps as sub-bullets: "Present the 'boxes' as numbers and the possible transitions as sub-bullets"; (3) multiple starts: one linear list per section; (4) state explicitly where separate lines merge; (5) loops: no special rule, the examples use "back to <step>" entries; (6) omit colours and line styles unless the content depends on them.
- DIAGRAM Center relational diagram samples (https://dcmpx.remotevs.com/org/diagramcenter/PL/accessible-image-sample-book/sample-4-relational-diagrams-accessible-image-sample-book.html): fetch failed (connection reset); it is a mirror anyway. Unverified.
- Mermaid: `accTitle:` one line and `accDescr:` single line or `accDescr { ... }` multi-line; renders SVG `<title>`, `<desc>`, `aria-labelledby`, `aria-describedby`, `aria-roledescription` (F, https://mermaid.js.org/config/accessibility.html). Rule: always supply both for every diagram; keep the title to one line. Docs licence not checked.
- PlantUML, Graphviz, DAISY: no dedicated screen-reader guidance found. Unverified / absent.
- RGAA 4.1.2 (French government), https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/#1.6 (F, partial): criterion 1.6 requires a "description détaillée" for informative images that need one, 1.7 requires it to be relevant, 1.9 groups image and caption in a figure; notes aria-describedby is poorly supported on img/object/canvas. The tables section (5) was not read. No licence stated on the page. French counterpart of the W3C tutorial.

## 4. Long content: progressive disclosure, skim then dive

- Zong et al. 2022 (F): users want an overview, then drill-down; hierarchy lets users move up and down levels; "details on demand" (citing Shneiderman). https://arxiv.org/pdf/2205.04917
- Wang et al. 2024 (F): users start with an overview or trend, then summary statistics, then subsets; they suggest on-demand smaller tables. https://pages.cs.wisc.edu/~yeaseulkim/assets/papers/2024_table.pdf
- Lundgard and Satyanarayan (F): combine levels, avoid L1-only. https://vis.csail.mit.edu/pubs/vis-text-model/
- NCAM (F): split complex tables into simpler ones.
- Google Assistant conversation design (S, secondary): lists of 2 to 10 items recommended (max 30); spoken prompts use end-focus, display prompts front-load; listen to each prompt in TTS. https://developers.google.cn/assistant/conversation-design/list and https://developers.google.cn/assistant/conversation-design/write-sample-dialogs. The search found no explicit "progressive disclosure" rule on Google's pages. Not fetched; the Assistant docs may be sunset: unverified.
- Rule set to adopt: say size and purpose first, then the headline finding, then ask whether to continue; chunk to roughly 2 to 10 items per turn (Google, S); keep a "where am I" cursor.

## 5. WHAT IS MISSING (spoken, interactive, conversational delivery)

1. All sources are static text (alt text, long description) or screen-reader keyboard navigation. None gives rules for text heard once, at fixed speed, with no way to re-scan. Only the Analysis Function mentions "auditory clutter", and only for one phrase.
2. No guideline sets a length budget in seconds or words for a spoken summary. Cesal and Datawrapper say "short" with no number.
3. No source says how to speak numbers, units, ranges, percentages, dates (for example "1,234.5", "-3", "10-20", "m2"), or how to use SSML breaks, `say-as`, emphasis. Screen readers leave this to pronunciation dictionaries. Our skill must define it.
4. No guidance on turn-taking: when to pause and ask "continue?", barge-in, "repeat", "go back", "skip to row 5", "read column Revenue".
5. No guidance on spoken wayfinding in a table: how often to repeat headers, how to say position ("row 3 of 12") without tiring the listener. Verbosity is a user setting, not a design rule (Zong et al.).
6. Lists, trees and nested flowchart lists rely on the screen reader announcing "list of 4 items" and nesting. Plain speech has no such markup; no source gives audio equivalents (earcons, spoken ordinals).
7. Sonification (Highcharts, Apple) is covered as an API; nothing says when to combine speech with tones or how to narrate a sonified chart.
8. Little evidence on generated descriptions: whether LLM-written summaries are trusted; Lundgard's 63% dislike of editorialising is the only hint. Hallucinated numbers and verification are not addressed.
9. French and other languages: only RGAA covers French, and it concerns markup, not wording. No French guidance on spoken table reading found (unverified that none exists).
10. Evidence base is small: studies of 12 to 30 participants, mostly desktop screen-reader users in the US/UK; phone-call or smart-speaker listeners and low-vision users who do not use screen readers are not studied here.

## Source reliability summary
Fetched and read: W3C complex images, W3C tables, Cesal, Datawrapper, Lundgard, Zong (PDF), Wang (PDF), WebAIM, NVDA guide (partial), Apple VoiceOver, Mermaid, NCAM intro/flow chart/tables, DIAGRAM intro, Analysis Function blog, Chartability, RGAA (partial), Highcharts overview.
Search results only: JAWS commands/transcript, Apple Audio Graphs, Highcharts configure page, Google conversation design, DIAGRAM graph pages, ONS pages.
