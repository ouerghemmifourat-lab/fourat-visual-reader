# 01 - Public repos and agent-skill ecosystems survey

Date: 2026-11-02. Method: WebSearch + WebFetch (GitHub API for license/stars when possible). "unverified" = seen only in search snippets or aggregator pages, not on the primary repo page.

## A. Agent Skills / skill ecosystems

| # | Name | URL | License | Does | Does NOT do (vs. our goal) |
|---|------|-----|---------|------|-----------------------------|
| 1 | anthropics/skills (19 dirs: docx, pdf, pptx, xlsx, frontend-design, mcp-builder, skill-creator...) | https://github.com/anthropics/skills (listing: https://api.github.com/repos/anthropics/skills/contents/skills) | repo-level license field null (per-skill licenses; unverified) | Reference format and examples of SKILL.md | No chart/table/diagram description and no voice/TTS/SSML skill in the listing |
| 2 | openai/skills (Codex catalog; has a "speech" skill per aggregator) | https://github.com/openai/skills ; https://openskillindex.com/skills/openai-skills-speech | repo license field null (unverified per skill) | Catalog; speech skill runs a bundled TTS CLI (needs OpenAI key) | Backend wrapper only; no guidance on writing speakable tables/charts (subdirs .curated/.system not enumerated) |
| 3 | mgifford/accessibility-skills (skills: charts-graphs, mermaid, tables, image-alt-text, svg, audio-video, plain-language...) | https://github.com/mgifford/accessibility-skills | AGPL-3.0 (API-verified), 57 stars | Visual/screen-reader accessibility rules for charts, tables, Mermaid | Targets web text alternatives, not spoken delivery, pacing, SSML or number pronunciation. AGPL is viral: do not copy text into a permissive skill |
| 4 | accessibility-and-inclusive-visualization (listed under openai/plugins path; source anton-abyzov/vskill) | https://verified-skill.com/skills/openai/plugins/accessibility-and-inclusive-visualization/versions/1.0.0 | page footer says MIT, not explicitly tied to the skill (unverified) | 67-line SKILL.md: long descriptions for complex charts, UML/ERD/state diagram a11y | Explicitly no audio/voice/SSML/sonification mention |
| 5 | data-visualization-accessibility (community-access/accessibility-agents) | https://www.skills.sh/taylorarndt/a11y-agent-team/data-visualization-accessibility | not stated on page (unverified) | Chart audit: alt text, ARIA, keyboard, Highcharts/Chart.js/D3/Recharts specifics | No spoken/voice output rules |
| 6 | alt-text skill (Emil Hvitfeldt; chart type + data + insight pattern) | https://claudskills.com/skills/alt-text/SKILL.md | unknown (unverified) | 3-part alt text structure for R/Quarto | Written alt text only; not by-ear; not French |
| 7 | gsd-build/gsd-2 accessibility skill | https://ruleskill.com/skills/gsd-build-gsd-2-src-resources-skills-accessibility-skill-md | unknown (unverified) | General WCAG; bar chart alt text example | Generic |
| 8 | TTS skills: claude-speak (leegonzales/aiskills), edge-tts, qwen-tts, verging-ai/tts | https://skills.cat/skills/leegonzales/aiskills/claude-speak ; https://claudskills.com/skills/edge-tts/ ; https://skillstore.io/skills/verging-ai-tts | unknown (unverified) | Speak text through a TTS backend; verging listing says OpenAI TTS has no SSML/pronunciation overrides | Playback only; none teaches restructuring tables/charts for listening |
| 9 | mermaid accessibility skill (mgifford) | https://sharedcontext.ai/skills/external/mgifford/mermaid | AGPL-3.0 (same repo as #3) | Advice: accTitle/accDescr and a written description under the code block | No diagram-to-speech method |

Cursor rules or Codex AGENTS.md specifically for chart/table narration: not found.

## B. MCP servers (TTS)

| Name | URL | License | Does | Does NOT |
|------|-----|---------|------|----------|
| text-to-speech-mcp (Engr-FaizanAli; Windows SAPI, tool speak_text) | https://pypi.org/project/text-to-speech-mcp/0.4.0/ | MIT per search snippet (unverified) | Speak text | Plain text only |
| mberg/kokoro-tts-mcp | https://enterprisedna.co/directories/mcp/mberg-kokoro-tts-mcp | Apache-2.0 per directory listing (unverified) | Kokoro TTS | No SSML shown, no table logic |
| blacktop "say"; nakamurau1/tts-mcp (OpenAI) | https://playbooks.com/mcp/blacktop-say ; https://playbooks.com/mcp/nakamurau1-openai-tts | unknown | System/OpenAI TTS | Same |

No MCP server with SSML support or table/chart narration was found in the search results.

## C. Libraries and repos

| # | Name | URL | License | Does | Does NOT |
|---|------|-----|---------|------|----------|
| 10 | Chart2Music | https://github.com/julianna-langston/chart2music | MIT (API-verified), 37 stars, pushed 2026-10-27 | Sonification + screen reader + keyboard nav for Chart.js/D3/Plotly or static images; Chart.js plugin lists en, de, es, fr, it (https://npmjs.com/package/chartjs-plugin-chart2music) | Needs structured data in a browser; non-speech audio; no spoken summary strategy for voice agents |
| 11 | Olli (umwelt-data/olli; mitvis/olli redirects there) | https://github.com/umwelt-data/olli ; https://vis.mit.edu/pubs/olli | BSD-3-Clause (API-verified), 85 stars | Turns Vega/Vega-Lite/Observable Plot specs into a keyboard-navigable text tree with levels of detail (structure first, drill down) | Visual a11y tree, not audio pacing/SSML/number pronunciation; languages unverified |
| 12 | Highcharts Sonification Studio | https://github.com/highcharts/sonification-studio | NOASSERTION via API; search snippets conflict (BSD-3 on repo page vs MIT on Georgia Tech page); commercial use needs Highcharts license. Treat as unclear | Browser tool to sonify data | Sonification only; proprietary dependency |
| 13 | Highcharts sonification module | https://www.highcharts.com/docs/sonification/getting-started ; https://github.com/highcharts/highcharts | NOASSERTION (commercial Highcharts license) | Sonification with "speech tracks" using browser speech synthesis | Proprietary; no pronunciation or structure rules |
| 14 | Apple Audio Graphs (AXChartDescriptor, AXDataSeriesDescriptor) | https://developer.apple.com/documentation/accessibility/audio-graphs | Proprietary Apple SDK (fetch returned only the title; details from model knowledge, unverified) | Native chart title/summary/axes/series for VoiceOver and audio graph | Not open; native apps only; no TTS control |
| 15 | SAS Graphics Accelerator | https://blogs.sas.com/content/sascom/2017/02/22/getting-started-sas-graphics-accelerator/ | Free Chrome extension, proprietary (unverified) | Text description, table view and sonification of SAS graphs | SAS output only; closed |
| 16 | mermaid-js/mermaid | https://github.com/mermaid-js/mermaid | MIT (API-verified), ~91k stars | Parser/renderer; accTitle/accDescr directives | No text-description generator found; you must write narration from parsed nodes/edges |
| 17 | ssmd (markdown-like SSML) | https://github.com/buchwandler/ssmd (formerly holgern/ssmd) ; https://pypi.org/project/ssmd/ | MIT (API-verified), 2 stars | Python: markdown-like syntax to SSML | Syntax only; no content strategy |
| 18 | user3301/ssml_builder | https://github.com/user3301/ssml_builder | NOASSERTION (no clear license) | Fluent SSML builder for Polly/Google/Watson | Unclear license; install-name mismatch per search |
| 19 | ssml-maker | https://pypi.org/project/ssml-maker/ | unknown (unverified) | Context-manager SSML builder (prosody, voice, phoneme, say-as) | v0.1.1, small |
| 20 | num2words | https://github.com/savoirfairelinux/num2words | LGPL-2.1 (API-verified), 970 stars | Numbers to words incl. en, fr, fr_BE, fr_CH, ordinals | No units, percent, ranges or tables; LGPL |
| 21 | Azure SSML pronunciation docs (say-as: cardinal, ordinal, fraction, date, time, currency, unit, telephone; sub; phoneme; lexicon; math) | https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation | Docs, not a repo | Authoritative vendor reference; most say-as values supported for English and French; duration only en/es | Vendor extensions; nothing on tables/charts |
| 22 | ToTTo | https://github.com/google-research-datasets/ToTTo | license null via API (unverified otherwise) | 120k Wikipedia table-to-sentence dataset, English | Dataset of written text, English only |
| 23 | Chart-to-Text (vis-nlp) | https://github.com/vis-nlp/Chart-to-text ; https://arxiv.org/abs/2203.06486 | GPL-3.0 (API-verified), 132 stars | 44,096 charts with summaries (Statista, Pew), BART/T5 baselines; paper reports hallucinations | Written summaries, English, not for ears |
| 24 | EchoTables (IKILeUS, Univ. Stuttgart) | https://b2find.eudat.eu/dataset/47270cb0-d38d-53de-a147-e7a0bb0573ab (DOI 10.18419/DARUS-4774; not on GitHub) | MIT per search snippet (unverified) | LLM table-to-short-summary for blind users; tested with VoiceOver | Summary text only, not speech delivery |

## GAPS (honest)

1. A SKILL.md teaching an LLM/voice agent to narrate tables, charts or diagrams for listening: not found. Existing accessibility skills (#3-#7) target written alt text/ARIA.
2. Structure-first, progressive-disclosure spoken pattern (overview, essentials, drill-down on request): only an analogue in Olli's visual tree (#11); no spoken-dialogue version found.
3. Mermaid/Graphviz/flowchart to spoken description: no tool found (parsers exist, narrators not). Graphviz not searched specifically.
4. SSML generation for tabular/chart content (pauses between cells, say-as for units/percent/ranges): builders (#17-19) are syntax helpers only.
5. Unified en+fr number/unit pronunciation rules (decimal comma vs point, thousands separators, %, currency, ranges, negatives): num2words covers words only; say-as support varies by vendor/locale; none found.
6. MCP servers or TTS skills with SSML pass-through: none found.
7. Evaluation of by-ear comprehension of spoken tables/charts: datasets (#22, #23) are text-only, English; none found.
8. Not covered here: Graphviz/PlantUML parsers, W3C SSML spec, Polly/Google SSML docs, academic audio-graph HCI work, Cursor rules directories, chart-QA models.
