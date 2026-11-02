# 04 - TTS / SSML / voice-design survey

Method: WebSearch + WebFetch, 2026-11-02. Every claim carries a URL fetched or seen in results. "UNVERIFIED" = not confirmed in a fetched page. Quotes < 15 words. The fetch tool summarises pages with a small model, so verbatim wording should be re-checked before citing in the skill.

## 1. SSML

### 1.1 W3C SSML 1.1
- URL: https://www.w3.org/TR/speech-synthesis11/ (W3C Recommendation; first 100k of 181k chars read).
- say-as: the spec does NOT enumerate interpret-as values; it says it "does not enumerate the possible values" and defers to a separate WG note. So cardinal/ordinal/digits/telephone etc. are engine conventions, not normative -> the skill must treat them as per-engine.
- `sub`: `alias` required; processor "SHOULD apply text normalization to the alias value."
- `phoneme`: `ph` required, `alphabet="ipa"` SHOULD be supported; phonemic string is not text-normalized.
- `lang`: `xml:lang` required. break/prosody sections not read (truncated) - UNVERIFIED here; see engine docs.

### 1.2 Per-engine support
| Engine | Source | Findings |
|---|---|---|
| Amazon Polly | https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html ; https://docs.aws.amazon.com/polly/latest/dg/say-as-tag.html | break/lang/p/s/sub/w/speak full on neural, long-form, generative; `say-as` partial on neural, full on long-form and generative; `phoneme` partial on generative; `prosody` partial everywhere; `emphasis`, auto-breaths, whisper, soft: not available on neural/long-form/generative. "If you use unsupported SSML tags ... you will get an error." say-as values: characters/spell-out, cardinal/number, ordinal, digits, fraction (mixed form needs "+", e.g. 3+1/2), unit (`1/2inch`, no space), date (format mdy,dmy,ymd,md,dm,ym,my,d,m,y,yyyymmdd with `?`), time (= minutes/seconds duration, e.g. 1'21"), address, expletive, telephone (en, es, fr-FR/fr-CA, pt, de, it, ja, ru). `characters` on a neural voice falls back to the standard voice for that sentence (still billed neural). |
| Google Cloud TTS | https://docs.cloud.google.com/text-to-speech/docs/ssml | speak, break, say-as, audio, p, s, sub, mark, prosody, emphasis, par/seq/media, phoneme (IPA, X-SAMPA...), voice, lang, google:style. say-as: currency, telephone, verbatim/spell-out, date, characters, cardinal, ordinal, fraction, expletive/bleep, unit, time, duration. Advice: prosody/emphasis "should wrap only full sentences"; `lang` is best effort. |
| Google Chirp 3 HD | https://docs.cloud.google.com/text-to-speech/docs/release-notes (17 Oct 2025) | SSML subset only: phoneme, p, s, sub, say-as (no break/prosody listed). Forum thread (https://discuss.google.dev/t/chirp3-hd-voices-dont-support-markup-field-in-long-audio-synthesis/185977) says markup not available in long-audio synthesis - community report. |
| Azure Speech | https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation (updated 2026-02) | say-as interpret-as: characters/spell-out, alphanumeric, cardinal/number, ordinal, number_digit, fraction, date (dmy,mdy,ymd...), time (hms12/24), duration (en, es only), telephone, currency, unit, address, name. Non-characters values supported for Arabic, Catalan, Chinese, Danish, Dutch, English, French, Finnish, German, Hindi, Italian, Japanese, Korean, Norwegian, Polish, Portuguese, Russian, Spanish, Swedish. Also phoneme (ipa/sapi/ups/x-sampa), sub, lexicon (PLS), `mstts:markdown`, and Math: `<mstts:prompt domain="Math"/>` or MathML (fr-FR, fr-CA included). Parentheses unread by default; `mathspeechverbosity level="verbose"`. |
| ElevenLabs | https://elevenlabs.io/docs/best-practices/prompting/controls | `<break time="x.xs">` up to 3 s, NOT on Eleven v3/v4; `<phoneme>` only on `eleven_flash_v2`; alias/lexeme dictionaries elsewhere. Normalization on by default; "Expand all abbreviations to their full spoken forms." Flash v2.5 may misread "$1,000,000". Examples: "100%" -> "one hundred percent". |
| OpenAI TTS | https://developers.openai.com/api/docs/guides/text-to-speech | Page does not mention SSML (UNVERIFIED whether tags are ignored or spoken literally; test needed). Style via `instructions` on gpt-4o-mini-tts. tts-1, tts-1-hd and gpt-4o-mini-tts: page says shutdown January 6, 2027; Realtime API recommended. Requires AI-voice disclosure. |
| Alexa | https://developer.amazon.com/en-US/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html | Tags: domain, effect, emotion, audio, break, emphasis, lang, p, phoneme, prosody, s, say-as, speak, sub, voice, w. "Alexa removes unsupported tags." break max 10 s. say-as values not read (truncated). |
| espeak-ng | https://github.com/espeak-ng/espeak-ng/blob/master/docs/markup.md | Lists speak, voice, prosody, say-as, mark, s, p, sub, tts:style, audio, emphasis, break. No `phoneme` element listed (espeak has its own [[...]] mechanism - UNVERIFIED here). Licence GPL (not fetched). |
| Piper | https://github.com/OHF-Voice/piper1-gpl (GPL-3.0; uses espeak-ng for phonemization) ; https://github.com/rhasspy/piper/issues/275 | No SSML documented on the repo page. Issue #275 (~Aug 2024): maintainer said SSML in progress (breaks, substitutions, some say-as). Shipped status UNVERIFIED. |
| Coqui TTS | https://github.com/coqui-ai/TTS/issues/752 | SSML only a feature request/prototype; no official support found. Maintenance status UNVERIFIED. |
| Windows System.Speech (SAPI) | https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis.speechsynthesizer.speakssml | `SpeakSsml` requires `<speak>`, conforms to SSML 1.0; the official sample uses legacy `<say-as type="date:mdy">` (not `interpret-as`). Expect SSML 1.0 + `type=` syntax; test `interpret-as`. |
| Windows OneCore/WinRT | https://learn.microsoft.com/en-us/uwp/api/windows.media.speechsynthesis.speechsynthesizer.synthesizessmltostreamasync | Takes SSML 1.1; element-by-element support not documented in results (UNVERIFIED). Only Microsoft-signed installed voices usable (class page). |
| Apple AVSpeechSynthesizer | https://developer.apple.com/documentation/avfaudio/avspeechutterance/init(ssmlrepresentation:)-8zam9.md | `init?(ssmlRepresentation:)` iOS 16+/macOS 13+; returns nil on invalid SSML; `rate`/`pitchMultiplier` ignored for SSML utterances. Tag list not documented in results (UNVERIFIED). |

Takeaway for the skill: ship an SSML path (Polly/Google/Azure/Alexa), a degrade-to-plain-text path, and a per-engine capability table; always validate and fall back (Polly errors on unsupported tags; Apple returns nil; Alexa silently strips).

## 2. Number / unit / date / symbol verbalization

### French (OQLF)
- https://vitrinelinguistique.oqlf.gouv.qc.ca/25100/la-prononciation/prononciation-des-nombres/regles-generales-de-lecture-des-nombres (OQLF, Quebec; undated):
  - "zero" and "virgule" are in principle not pronounced; when dictating or at risk of misunderstanding, spell elements in written order (1,6 km -> "un kilomètre six").
  - Radio frequency exception: 104,2 FM -> "cent quatre virgule deux".
  - Decimal part read as integer: 3,25 $ -> "trois dollars vingt-cinq". 0,5 % -> "cinq dixièmes pour cent"; 7/10 -> "sept dixièmes".
  - "de" is spoken between magnitude and unit: 10 000 000 km -> "dix millions de kilomètres". 1 555 M$ -> "mille cinq cent cinquante-cinq millions de dollars".
  - CAUTION: Quebec guidance. Metropolitan school sources say "trente-huit virgule cinquante-quatre" (search result only, not fetched: https://eduscol.education.fr/document/64936/download). For data readout, saying "virgule" is the safe default; decide per locale (practice).
- Written form: French uses a comma decimal and a non-breaking space between 3-digit groups and between number and unit/$ (OQLF and Académie, from search results: https://vitrinelinguistique.oqlf.gouv.qc.ca/la-typographie/nombres ; https://dictionnaire-academie.fr/article/QDL057). The normalizer must parse "1 234,5" as 1234.5 and "1,234.5" as English.
- Billion/milliard false friend: https://en.wikipedia.org/wiki/Long_and_short_scales - EN billion = 10^9; FR milliard = 10^9, FR billion = 10^12 (long scale); Canadian government advises avoiding FR billion/trillion. Rule: say "milliard" in FR and "billion" in EN for 10^9; never translate word for word.
- Not found: Académie française rule on dates (premier vs. cardinal), 70/80/90 variants (Belgium/Switzerland septante/nonante; num2words has fr_BE/fr_CH locales).

### English / general
- Azure date: format attribute controls order ("October twelfth two thousand sixteen" vs dmy) - Azure page above. ElevenLabs: 01/02/2023 is ambiguous, state the format (https://elevenlabs.io/docs/best-practices/prompting/controls).
- Cartesia (https://docs.cartesia.ai/build-with-cartesia/capability-guides/text-normalization.md): numbers, dates, times, phones, currency auto-normalized by locale; ranges and fractions not reliable -> write "10 to 15 dollars", "two thirds"; equations/chemistry/uncommon units: write as spoken ("volts" for V); full control via `normalization: off`.
- Polly telephone: US vs UK grouping ("double five") - Polly say-as page.
- Rules to adopt (practice, derived, to be tested): percentages "12 percent"/"12 pour cent"; ranges "from 10 to 15"/"de 10 à 15"; negatives "minus 3"/"moins 3"; round decimals to speech precision and say "about"; years as years, quantities as cardinals; spell acronyms only if not pronounceable (`characters`, or Azure `alphanumeric`); symbols: >= "at least", ≈ "about", ± "plus or minus", → "leads to".
- Currency: Azure `currency` reads "99.9 USD" as "ninety-nine US dollars and ninety cents". FR word order for euros: no source fetched (UNVERIFIED); OQLF says $ goes after the number in FR typography.

### Libraries
- num2words: https://github.com/savoirfairelinux/num2words - locales en, fr, fr_BE, fr_CH; converters cardinal, ordinal, ordinal_num, year, currency. Licence LGPL-2.1+ (Debian copyright, https://metadata.ftp-master.debian.org/changelogs/main/p/python-num2words/stable_copyright). WARNING: one aggregator (mcp.depscope.dev/pkg/pypi/num2words) claims advisory MAL-2025-6794 flags the PyPI package as malicious; UNVERIFIED - check OSV/PyPI and pin hashes before depending on it.
- Unicode CLDR RBNF: https://unicode.org/reports/tr35/tr35-numbers.html - SpelloutRules (numbering, numbering-year, cardinal, ordinal). Data licence not confirmed in the fetch (UNVERIFIED).
- NVIDIA NeMo-text-processing: https://github.com/NVIDIA/NeMo-text-processing - TN + ITN, Apache-2.0, pynini dependency, pip install not supported on Windows/macOS. Language list not confirmed (FR/EN UNVERIFIED).

### Math / chemistry
- MathCAT: https://github.com/daisy/MathCAT - MIT; speech languages include English and French; outputs speech strings "with embedded speech engine commands" (SSML not named). Rule files ClearSpeak/SimpleSpeak (https://docs.rs/crate/mathcat/0.7.5/source/tests/Languages/en/shared.rs). An NVDA commit note says ClearSpeak is not available for all languages, e.g. French (https://app.semanticdiff.com/gh/nvaccess/nvda/commit/90ee3cd85df1985f9ec772dc23c343637c2666dc), so use SimpleSpeak for FR (inference). Benetech link: not found.
- ClearSpeak vs MathSpeak: Texthelp help (https://support.texthelp.com/help/clearspeak-and-mathspeak-speech-engines-in-equatio): ClearSpeak natural, MathSpeak precise ("start fraction ... end fraction"). ClearSpeak origin: ETS report https://www.ets.org/research/policy_research_reports/publications/report/2016/jwog.html.
- Azure Math domain / MathML: see table.
- Chemical formulas: no authoritative source found. Practice (unverified): read element symbols and subscripts ("H two O") or give the name.

## 3. Voice-UI information density
- Google Design, "Rule of three": https://design.google/library/rule-of-three (Google Assistant conversation designer; no date/byline). Adopt: speak 3 items, show the rest on screen; split long menus into groups of <=3; argues Miller's 7 does not apply. It is an essay: a target, not a hard cap.
- Google Conversation Design "write your dialog" page returned 404 (https://developers.google.com/assistant/conversation-design/write-your-dialog) - not verified.
- Amazon: https://developer.amazon.com/en-US/blogs/alexa/alexa-skills-kit/2019/08/how-to-reduce-cognitive-load-for-voice-design (19 Aug 2019, guest post by Eckoh): put focal info at the end of the prompt; use "first/second/third" markers; offer options just in time. Alexa Voice Design Guide "one-breath test", be brief (https://developer.amazon.com/fr/designing-for-voice/what-alexa-says/, search summary); Alexa Haus: one to a few options at a time (https://developer.amazon.com/alexa/alexa-haus/design-principles/be-brief, search summary).
- W3C COGA draft "Voice Systems and Conversational Interfaces": https://w3c.github.io/coga/research-modules/Conversational-Voice-Systems.html (draft; comments by 15 Apr 2026): "Each list item should be a single idea."; option label before key; pauses between phrases; allow repeat; confirm receipt; task overview; some users hold only 2-3 items.
- Counterpoint: IVR research found broad menus beat deep ones and that the "5 items" rule misreads Miller (search summary, https://stars.library.ucf.edu/facultybib2000/233). So 3 per chunk is a default, not a law; use "want more?" patterns.
- Nielsen Norman Group: no NN/g voice article found (UNVERIFIED). Apple Siri/HIG speech guidance and earcons: not retrieved.
- Skill defaults (practice): structure first ("a table with 4 columns and 12 rows"), then headline, then <=3 items, then "Want the details?"; short sentences; one number per sentence where possible.

## 4. Tooling
- Text normalization: NeMo-text-processing (Apache-2.0), num2words (LGPL), CLDR/ICU spellout, vendor normalizers (Cartesia, ElevenLabs).
- Azure custom lexicon validator: https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomLexiconValidation (linked from the Azure doc; licence not checked).
- Open-source SSML builders/validators: searched, none confirmed (UNVERIFIED). Practical route: XML well-formedness check + engine dry run.
- Free local Windows engines: System.Speech/SAPI (SSML 1.0, `type=` say-as sample), WinRT SpeechSynthesizer (SSML 1.1), Piper (GPL-3.0, SSML unclear), espeak-ng (SSML subset, GPL). French voice availability on a given PC: untested.

## RISKS - when SSML is unavailable
- Engines differ: Polly errors on unsupported tags; Apple returns nil; Alexa strips; Chirp 3 HD supports 5 tags; ElevenLabs v3/v4 ignore `break`; OpenAI docs mention no SSML. Literal reading of tags by engines that do not parse them is possible (UNVERIFIED).
- Plain-text fallbacks:
  - Pre-normalize to spoken words yourself (ElevenLabs and Cartesia both recommend it; Cartesia has `normalization: off`) - documented.
  - "to" for ranges, spell fractions and units - Cartesia, documented.
  - Punctuation for pauses: ElevenLabs v3/v4 "relies on audio tags and punctuation" (ElevenLabs page) - documented; the ordering period > comma > dash and use of line breaks is practice, unverified.
  - Short sentences, one idea each; no markdown/table symbols in the spoken stream (only Azure offers `mstts:markdown`); spoken structure sentence first; closing offer for more.
- Locale pitfalls: "1,234" misread in FR; billion/milliard; date order; phoneme/IPA only on some models.
- Re-verify before release: num2words advisory, OpenAI deprecation date (2027-01-06), Piper SSML status.
