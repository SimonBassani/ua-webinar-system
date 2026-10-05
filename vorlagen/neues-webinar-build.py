"""Vorlage: Deck für ein neues Webinar bauen.

So wird sie benutzt:
  1. Ordner anlegen:  webinare/<datum>-<kurzname>/      (z. B. webinare/2026-11-12-linkedin-sales/)
  2. Diese Datei dorthin kopieren und in  build.py  umbenennen.
  3. Unten die Änderungen eintragen (Titel, Datum, Angebot, Folien streichen/einfügen).
  4. Bauen:   uv run python webinare/<name>/build.py
  5. Prüfen:  uv run --with-requirements requirements/deck.txt python deck/pdf.py webinare/<name>/deck.html 1,5,12

Ohne jede Änderung erzeugt das Skript eine unveränderte Kopie des Ausgangsdecks. Man kann es also
jederzeit zwischendurch laufen lassen.
"""
import sys
from pathlib import Path

# Hauptordner des Repos finden (egal, wo dieses Skript liegt)
WURZEL = next(p for p in Path(__file__).resolve().parents if (p / "deck" / "folien_lib.py").exists())
sys.path.insert(0, str(WURZEL / "deck"))
from folien_lib import *  # noqa: E402,F401,F403

# ---- Ausgangsstand und Ziel -----------------------------------------------------------------------
AUSGANG = WURZEL / "deck" / "Akquise-Copilot.html"   # das letzte fertige Deck
ZIEL = Path(__file__).resolve().parent / "deck.html"

d = Deck(AUSGANG)
# d.liste()   # ← Zeichen „#“ am Anfang entfernen, um alle Folien mit Nummer und Namen zu sehen

# ---- 1. Titel, Datum, Uhrzeit ---------------------------------------------------------------------
# Jede Zeile ersetzt einen Text. Der alte Text muss genau so im Deck stehen (sonst Fehlermeldung).
# d.ed("Titel", "Dein Akquise-Copilot:", "Dein neuer Titel:")
# d.ed("Titel", "22.09.2026", "12.11.2026")
# d.ed("Titel", "11:00 Uhr · Live &amp; Online · keine Aufzeichnung", "11:00 Uhr · Live &amp; Online")

# ---- 2. Angebot -----------------------------------------------------------------------------------
# d.ed("Dein Invest", "5.500 €", "4.900 €")
# d.ed("Marktvergleich", "8.900 €", "9.500 €")

# ---- 3. Folien streichen ---------------------------------------------------------------------------
# d.streichen("Zwei Optionen")          # entfernt alle Folien mit diesem Namen
# d.streichen("Boni", k=2)               # entfernt nur die dritte Folie mit diesem Namen

# ---- 4. Neue Folie einfügen ------------------------------------------------------------------------
# neu = section(
#     "Meine neue Folie",                                   # Name (für die Liste und für Verweise)
#     "Das sagen wir zu dieser Folie.",                     # Sprechernotiz
#     "padding:90px 100px;background:#0D0D0D;display:flex;flex-direction:column;justify-content:center",
#     eyebrow("Das Problem")
#     + f'<h2 style="margin:16px 0 0;font-size:72px;font-weight:700">Genau hier {m("hakt es.")}</h2>',
# )
# d.einfuegen_nach("Kontaktchaos", neu)

# ---- 5. Reihenfolge ändern -------------------------------------------------------------------------
# d.verschieben_nach("Touchpoints", "Schritt 4 · Automation")

# ---- 6. Sprecher-Kürzel (A = Alex, M = Michi, S = Simon) --------------------------------------------
# Jede Folie muss einer Person zugeordnet sein. Nummern siehe d.liste().
# d.kuerzel([(1, 10, "A"), (11, 40, "S"), (41, len(d.folien), "A")])

d.speichern(ZIEL, titel="Webinar-Deck")
