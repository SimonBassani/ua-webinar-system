# 04 · Deck bauen und exportieren

## Einmal einrichten

1. **Google Chrome** installieren (wird für PDF und Banner gebraucht; unter Windows geht notfalls auch
   Edge). Brave funktioniert nicht.
2. **uv** installieren, das startet Python samt Paketen ohne weitere Einrichtung:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Repo klonen und im Terminal in den Hauptordner wechseln.

## Deck ansehen

`deck/Akquise-Copilot.html` doppelklicken. Steuerung:

| Taste | Wirkung |
|---|---|
| `←` `→`, Leertaste | blättern |
| `F` | Vollbild — so wird präsentiert |
| Zahlen `1`–`9` | direkt zur Folie springen |
| `Home` / `End` | Anfang / Ende |

Die Datei läuft offline und braucht kein PowerPoint.

## Ein neues Webinar bauen

Das Referenz-Deck wird über `build3.py` gebaut. Für ein **neues** Webinar nimmt man dagegen das fertige Deck
als Ausgangsstand und ändert nur, was neu ist. Das geht mit `deck/folien_lib.py`:

1. Ordner `webinare/<datum>-<kurzname>/` anlegen.
2. `vorlagen/neues-webinar-build.py` dorthin kopieren und in `build.py` umbenennen.
3. In `build.py` die gewünschten Änderungen eintragen (Titel, Datum, Angebot, Folien streichen oder einfügen,
   Reihenfolge, Sprecher-Kürzel). Alle Möglichkeiten sind in der Datei als Beispiele vorbereitet.
4. Bauen: `uv run python webinare/<name>/build.py`
5. PDF und Vorschau: `uv run --with-requirements requirements/deck.txt python deck/pdf.py webinare/<name>/deck.html 1,5,12`

In Claude Code übernimmt das der Skill `webinar-deck`. Banner baut der Skill `webinar-banner`
(Anleitung: [../banner/README.md](../banner/README.md)).

## Folien ändern (Referenz-Deck)

Alle Änderungen gehen in **`build3.py`**, nie in die fertige HTML. Der Ablauf:

```bash
uv run python deck/build3.py
uv run --with-requirements requirements/deck.txt python deck/pdf.py deck/Akquise-Copilot.html 12,41,59
```

Alle Befehle werden im Hauptordner des Repos ausgeführt (nicht im Unterordner).

Der erste Befehl baut die HTML neu und gibt die Folienliste aus. Der zweite erzeugt das PDF und
zusätzlich Vorschau-Bilder der genannten Folien, damit man das Ergebnis prüfen kann, bevor es
ins Webinar geht.

### Wie build3.py arbeitet

Das Skript liest `base_v2.html` (den alten Stand), zerlegt sie in Folien und verändert sie gezielt:

```python
ed('Warum jetzt', 'Alter Text', 'Neuer Text')      # Text auf einer Folie ersetzen
notes('Warum jetzt', 'Neue Sprechernotiz')          # Sprechernotiz setzen
order = [T('Titel'), T('Kontaktchaos'), ...]        # Reihenfolge der Folien
```

Wichtig: Jede Ersetzung prüft, ob der alte Text genau einmal vorkommt. Passt er nicht mehr,
bricht der Build mit einer Fehlermeldung ab. Das ist gewollt — so bleibt nichts unbemerkt.

Neue Folien werden als Funktion geschrieben (`def zielgruppe(): ...`) und in der Liste `order`
einsortiert.

### Sprechernotizen

Jede Folie trägt `data-speaker-notes="..."`. Die Notiz steht im HTML und lässt sich später
auslesen, sie wird im Deck selbst nicht angezeigt.

## PDF-Export

`pdf.py` macht von jeder Folie einen Chrome-Screenshot in 1,5-facher Auflösung und setzt daraus
ein PDF zusammen.

**Warum kein normales PDF:** Chrome speichert weiche Schatten in einer Form, die manche
PDF-Betrachter (iPad, Handy, Vorschau-Apps) als harte grüne oder rote Flächen zeichnen. Auf dem
eigenen Rechner sieht alles gut aus, beim Empfänger nicht. Bilder sehen überall gleich aus.
Nachteil: Der Text im PDF ist nicht markierbar und die Datei ist größer (~15 MB).

**Chrome beendet sich nach dem Screenshot nicht von selbst.** Das Skript wartet deshalb, bis die
Bilddatei fertig geschrieben ist, und beendet Chrome dann. Wenn doch einmal Prozesse hängen
bleiben:

```bash
pkill -f -- "--headless=new"
```

## Typische Fehler

| Symptom | Ursache und Lösung |
|---|---|
| Build bricht mit `AssertionError` ab | Der zu ersetzende Text steht nicht mehr so in der Datei. Text im Skript an den aktuellen Stand anpassen. |
| Änderung ist im Deck nicht zu sehen | In der HTML statt in `build3.py` geändert. Der nächste Build überschreibt das. |
| PDF-Seite fehlt | Chrome hatte einen Aussetzer. Das Skript versucht es viermal, danach kommt eine Fehlermeldung. Einfach neu starten. |
| Folien sehen im PDF anders aus als im Browser | Animationen sind im Export abgeschaltet, das ist Absicht. |
| Schriften sehen falsch aus | Beim Bauen muss Internet verfügbar sein, die Schriften kommen von Google Fonts. |

## Dateien im Ordner `deck/`

| Datei | Zweck |
|---|---|
| `Akquise-Copilot.html` | fertiges Deck zum Präsentieren |
| `Akquise-Copilot.pdf` | fertiges PDF zum Verschicken |
| `build3.py` | hier wird geändert |
| `base_v2.html` | Ausgangsstand, auf dem das Skript aufsetzt |
| `pdf.py` | Export (läuft auf Mac und Windows) |
| `folien_lib.py` | Werkzeugkasten für neue Webinar-Decks (`Deck`-Klasse) |
| `fotos/` | Porträts (Alex, Simon, Referenzen) |
| `screens/` | Screenshots und die Masterclass-Box |
