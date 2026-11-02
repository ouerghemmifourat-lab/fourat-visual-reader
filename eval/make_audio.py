#!/usr/bin/env python3
"""Synthesise a few 'skill' outputs to WAV with the local Windows voices (System.Speech), WITHOUT playing anything.
Reports duration and words per minute. Files go to eval/audio/ (git-ignored).
  python make_audio.py [--arm skill] [--ids en_table_small,fr_table_small,...]
Voices used: Microsoft Zira Desktop (en-US), Microsoft Hortense Desktop (fr-FR). No install, no network.
"""
import argparse, json, re, subprocess, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_IDS = "en_table_small,en_bars_simple,en_flowchart_loop,fr_table_small,fr_courbe,fr_flux_boucle"
VOICE = {"en": "Microsoft Zira Desktop", "fr": "Microsoft Hortense Desktop"}


def synth(text, lang, out):
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SelectVoice('{VOICE[lang]}'); "
        f"$s.SetOutputToWaveFile('{out}'); "
        "$t = [IO.File]::ReadAllText($env:VVR_TXT, [Text.Encoding]::UTF8); "
        "$s.Speak($t); $s.Dispose()"
    )
    tmp = out.with_suffix(".txt")
    tmp.write_text(text, encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, env={**__import__("os").environ, "VVR_TXT": str(tmp)})
    tmp.unlink()
    with wave.open(str(out)) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="skill")
    ap.add_argument("--ids", default=DEFAULT_IDS)
    a = ap.parse_args()
    cases = {c["id"]: c for c in json.loads((HERE / "cases.json").read_text(encoding="utf-8"))}
    (HERE / "audio").mkdir(exist_ok=True)
    rows = []
    for cid in a.ids.split(","):
        text = (HERE / "outputs" / a.arm / f"{cid}.txt").read_text(encoding="utf-8")
        out = HERE / "audio" / f"{a.arm}_{cid}.wav"
        dur = synth(text, cases[cid]["lang"], out)
        words = len(re.findall(r"\w+(?:[-']\w+)*", text))
        rows.append({"id": cid, "arm": a.arm, "seconds": round(dur, 1), "words": words, "wpm": round(60 * words / dur) if dur else None,
                     "file": out.name})
        print(rows[-1])
    (HERE / "audio" / f"durations_{a.arm}.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
