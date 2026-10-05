"""Bild mit Google Gemini („Nano Banana Pro“) erzeugen. Optional, das Banner geht auch ohne.

    uv run --with-requirements requirements/gemini.txt python banner/gemini_bild.py \
        --prompt "Dunkler Hintergrund, mintgrünes Licht links, korallenrotes Licht rechts, kein Text" \
        --ausgabe banner/ausgabe/hintergrund.png

Optional mit Referenzbildern (--ref, mehrfach möglich), zum Beispiel ein Logo oder ein Foto,
dessen Stil übernommen werden soll.

Der persönliche Schlüssel steht in der Datei .env im Hauptordner (GEMINI_API_KEY=…). Er wird hier
nur gelesen und nie ausgegeben. Jede Bildgenerierung kostet ein paar Cent, abgerechnet über das
Google-Konto, mit dem der Schlüssel erstellt wurde.
"""
import argparse
import os
import sys
from pathlib import Path

MODELL = "gemini-3-pro-image-preview"
WURZEL = Path(__file__).resolve().parents[1]


def lade_env():
    """Liest .env aus dem Hauptordner (nur einfache KEY=WERT-Zeilen)."""
    datei = WURZEL / ".env"
    if not datei.exists():
        return
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#") or "=" not in zeile:
            continue
        schluessel, wert = zeile.split("=", 1)
        os.environ.setdefault(schluessel.strip(), wert.strip().strip('"').strip("'"))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prompt", required=True, help="Beschreibung des gewünschten Bildes")
    p.add_argument("--ausgabe", required=True, help="Zieldatei (PNG)")
    p.add_argument("--ref", action="append", default=[], help="Referenzbild (mehrfach möglich)")
    p.add_argument("--format", default="16:9", help="Seitenverhältnis, z. B. 16:9, 1:1, 4:5")
    a = p.parse_args()

    lade_env()
    schluessel = os.environ.get("GEMINI_API_KEY", "").strip()
    if not schluessel:
        sys.exit("Kein GEMINI_API_KEY gefunden. Einrichtung starten: in Claude Code /einrichten eingeben. "
                 "Das Banner funktioniert auch ganz ohne Gemini.")

    from google import genai
    from google.genai import types
    from PIL import Image

    inhalt = [a.prompt]
    for r in a.ref:
        if not Path(r).exists():
            sys.exit(f"Referenzbild nicht gefunden: {r}")
        inhalt.append(Image.open(r))

    client = genai.Client(api_key=schluessel)
    try:
        antwort = client.models.generate_content(
            model=MODELL, contents=inhalt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=a.format)))
    except Exception as fehler:  # noqa: BLE001
        text = str(fehler).replace(schluessel, "***")   # den Schlüssel nie in Fehlermeldungen ausgeben
        if "API key" in text or "API_KEY" in text or "401" in text or "403" in text:
            sys.exit("Der Schlüssel wird nicht akzeptiert. In der .env prüfen, ob er vollständig und ohne "
                     "Leerzeichen eingetragen ist, und ob im Google-Konto die Abrechnung aktiv ist.")
        sys.exit(f"Gemini hat einen Fehler gemeldet: {text[:400]}")

    ziel = Path(a.ausgabe)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    gespeichert, notiz = False, ""
    kandidaten = getattr(antwort, "candidates", None) or []
    teile = kandidaten[0].content.parts if kandidaten and kandidaten[0].content and kandidaten[0].content.parts else []
    for teil in teile:
        if getattr(teil, "inline_data", None) is not None:
            teil.as_image().save(str(ziel))
            gespeichert = True
        elif getattr(teil, "text", None):
            notiz += teil.text
    if not gespeichert:
        sys.exit("Es wurde kein Bild erzeugt. Mögliche Ursache: Der Prompt wurde abgelehnt. "
                 "Beschreibung ändern und neu versuchen. " + (f"Hinweis des Modells: {notiz[:300]}" if notiz else ""))
    print(f"Gespeichert: {ziel}")


if __name__ == "__main__":
    main()
