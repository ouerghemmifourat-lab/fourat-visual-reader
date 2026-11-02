# SSML: what to use, and what each engine does with it

Checked against official documentation on 2026-11-02 (URLs below). Re-check before relying on a detail: engines change.

## Rule

Produce **plain spoken text first**, with numbers, units and dates already in words. Add SSML only for rhythm. Then an
engine that strips or rejects tags still speaks correctly.

## Safe subset (works, or degrades harmlessly, almost everywhere)

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <p><s>A table with four columns and twelve rows.</s></p>
  <p><s>Row one of twelve, Tokyo:<break time="300ms"/> population thirty-seven million;<break time="300ms"/>
  area two thousand square kilometres.</s></p>
  <break time="600ms"/>
  <p><s>Shall I continue?</s></p>
</speak>
```

- `speak`, `p`, `s`, `break time="…ms"` (≤ 3 s), `sub alias="…"`, and `say-as` only for `characters` (spelled IDs),
  `date` and `time`; numbers are already words, so no `cardinal`/`unit`/`currency` is needed for correctness.
- Pauses used by this skill: 300 ms between cells, 600 ms between rows and groups, 1 s before a question.
- `prosody`, `emphasis`, `phoneme`: optional, engine-specific; never required for correctness.

## Engine matrix

| Engine | SSML | Notes (official docs) |
|---|---|---|
| Amazon Polly | yes | Neural/long-form/generative voices: `break`, `p`, `s`, `sub`, `w`, `lang` full; `say-as` partial on neural; no `emphasis`. **Unsupported tags cause an error.** `say-as`: cardinal, ordinal, digits, fraction, unit, date (with `format`), time, telephone (en, fr-FR, fr-CA…). https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html |
| Google Cloud TTS | yes | Full set incl. `say-as` cardinal, ordinal, characters, date, time, currency, unit, fraction, telephone; `prosody`/`emphasis` should wrap whole sentences. **Chirp 3 HD voices accept only `phoneme`, `p`, `s`, `sub`, `say-as`** (no `break`). https://docs.cloud.google.com/text-to-speech/docs/ssml ; https://docs.cloud.google.com/text-to-speech/docs/release-notes |
| Azure Speech | yes, richest | `say-as`: cardinal, ordinal, number_digit, fraction, date, time, currency, unit, telephone, address, name, alphanumeric; French supported. Math domain or MathML for formulas. Lexicons (PLS). https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation |
| Amazon Alexa | yes | `break` ≤ 10 s, `say-as`, `prosody`, `emphasis`, `phoneme`, `sub`, `lang`, `voice`, `audio`. **Unsupported tags are silently removed.** https://developer.amazon.com/en-US/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html |
| ElevenLabs | partial | `<break time="1.0s"/>` ≤ 3 s, **not on v3/v4** (use punctuation); `<phoneme>` only on flash v2; pronunciation dictionaries otherwise. Docs recommend expanding abbreviations and writing numbers as words. https://elevenlabs.io/docs/best-practices/prompting/controls |
| OpenAI TTS / Realtime | no SSML documented | Style through the `instructions` parameter (gpt-4o-mini-tts). Send plain normalised text. Docs state tts-1 and gpt-4o-mini-tts shut down 2027-01-06; Realtime recommended. https://developers.openai.com/api/docs/guides/text-to-speech |
| Apple AVSpeechSynthesizer | yes (iOS 16+, macOS 13+) | `AVSpeechUtterance(ssmlRepresentation:)` **returns nil on invalid SSML**; rate/pitch properties ignored for SSML utterances; supported tag list not documented. https://developer.apple.com/documentation/avfaudio/avspeechutterance/init(ssmlrepresentation:)-8zam9 |
| Windows System.Speech (SAPI) | SSML 1.0 | `SpeakSsml` needs `<speak>`; official sample uses legacy `say-as type="…"`. Tested here: `break` and plain text fine; `interpret-as` support varies by voice. https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis.speechsynthesizer.speakssml |
| Windows OneCore (WinRT) | SSML 1.1 | `SynthesizeSsmlToStreamAsync`; per-tag support undocumented. https://learn.microsoft.com/en-us/uwp/api/windows.media.speechsynthesis.speechsynthesizer.synthesizessmltostreamasync |
| espeak-ng | subset | `speak`, `voice`, `prosody`, `say-as`, `s`, `p`, `sub`, `emphasis`, `break`, `audio`. GPL. https://github.com/espeak-ng/espeak-ng/blob/master/docs/markup.md |
| Piper | unconfirmed | No SSML in the repo docs; issue #275 mentions work in progress. GPL-3.0. https://github.com/rhasspy/piper/issues/275 |
| Coqui TTS | no | Feature request only. https://github.com/coqui-ai/TTS/issues/752 |
| Cartesia | no SSML; normaliser | Auto-normalises numbers, dates, currency by locale; ranges and fractions unreliable: write "10 to 15", "two thirds". `normalization: off` for full control. https://docs.cartesia.ai/build-with-cartesia/capability-guides/text-normalization.md |

## Plain-text fallback (no SSML)

- Numbers, units, dates, symbols already in words (this skill's default).
- Pauses: full stop for a sentence pause, semicolon between cells, a blank line between groups, an ellipsis or em dash is
  **not** reliable.
- One idea per sentence; a question at the end of the turn.
- No Markdown or table characters in the spoken stream.
- Where the engine supports a style prompt (OpenAI `instructions`), ask for "slow, clear, pause at semicolons and
  between paragraphs".

## Validation

Check well-formed XML before sending; keep `xml:lang` consistent with the text language (`en-US`, `en-GB`, `fr-FR`,
`fr-CA`); on an engine that errors (Polly) or returns nil (Apple), fall back to the plain text.
