# Banner-Werkzeuge

Baut das Webinar-Banner (LinkedIn-Event-Bild, Thumbnail) im Look von unternehmensathleten × DigiUp.
So sieht das Ergebnis aus: [`beispiel/ergebnis.jpg`](beispiel/ergebnis.jpg)

In Claude Code reicht: **„Baue mir ein Banner für mein nächstes Webinar.“** Der Skill `webinar-banner`
führt dann durch alles. Hier steht, was dahinter passiert.

## Die drei Programme

| Programm | Aufgabe | Aufruf |
|---|---|---|
| `freistellen.py` | Person aus einem Foto freistellen (Hintergrund entfernen) | `uv run --with-requirements requirements/freistellen.txt python banner/freistellen.py foto.jpg -o assets/hosts/vorname.png` |
| `banner.py` | Banner aus einer Konfigurationsdatei bauen | `uv run --with-requirements requirements/banner.txt python banner/banner.py banner/beispiel/config.json` |
| `gemini_bild.py` | Optional: KI-Hintergrundbild mit Google Gemini erzeugen (kostet ein paar Cent, eigener Schlüssel nötig) | `uv run --with-requirements requirements/gemini.txt python banner/gemini_bild.py --prompt "…" --ausgabe bild.png` |

Beim ersten Freistellen lädt das Programm einmalig ein Modell von rund 170 MB. Das dauert einige Minuten.

## Die Konfigurationsdatei

Eine JSON-Datei, Vorlage: [`beispiel/config.json`](beispiel/config.json). Pfade gelten ab dem Hauptordner
des Repos. Mit `[[doppelten Klammern]]` wird ein Textteil in Terracotta hervorgehoben.

| Feld | Bedeutung | Pflicht |
|---|---|---|
| `name` | Dateiname des Ergebnisses | nein (Standard: `banner`) |
| `titel_gross` | Produktname groß in Mint, z. B. `Akquise-Copilot` | **ja** |
| `titel_klein` | kleines Wort davor, z. B. `Dein` | nein |
| `untertitel` | Ergebnis in einem Satz | nein |
| `datum_pille` | grüne Pille, z. B. `LIVE · DI 22.09. · 11:00 UHR` | nein |
| `badge_oben` | Terracotta-Badge oben mittig, z. B. `INKL. LIVE-DEMO` | nein |
| `logos` | Liste von Logo-Dateien oben links, durch „×“ getrennt | nein |
| `hosts` | **genau zwei** Personen, siehe unten | **ja** |
| `karte` | kleine Produktkarte unter dem Titel, siehe unten | nein |
| `hintergrund` | eigenes Hintergrundbild (z. B. von `gemini_bild.py`) | nein |
| `text_oben` | Abstand des Textblocks von oben in Pixel (Standard 250) | nein |
| `ausgabe` | Zielordner (Standard `banner/ausgabe`) | nein |

### Person (`hosts`)

| Feld | Bedeutung |
|---|---|
| `name`, `firma` | erscheinen in der Namenspille unten |
| `foto` | freigestelltes PNG, z. B. `assets/hosts/alex.png` |
| `seite` | `links` oder `rechts` (Standard: erste Person links, zweite rechts) |
| `farbe` | `mint`, `coral` oder `gelb`: Farbe von Schein, Pfeil und Pille |
| `spiegeln` | `true` dreht das Foto, damit die Pose zur Mitte zeigt |
| `hoehe` | Höhe der Person in Pixel (Standard 1000; wird automatisch begrenzt, damit sie nicht in den Titel ragt) |
| `x` | Verschiebung in Pixel, positiv = zur Mitte hin |
| `beschnitt` | Anteil von unten abschneiden, z. B. `0.2` schneidet das untere Fünftel ab |

### Produktkarte (`karte`)

```json
"karte": {
  "titel": "Akquise-Copilot",
  "status": "aktiv",
  "chips": [{"text": "Sarah", "tag": "SUPER HEISS", "farbe": "mint"},
            {"text": "Thomas", "tag": "HEISS", "farbe": "coral"}],
  "ergebnis": "20.000 €"
}
```

Sie gibt einen Blick ins System, damit das Banner nach „Das muss ich sehen“ aussieht und nicht nach reinem
Text. Für ein anderes Thema passt man Titel, Chips und Ergebnis an. Ohne `karte` bleibt der Bereich leer.

## Ergebnis

Im Ordner `ausgabe` entstehen `<name>.png` (3840 × 2160) und `<name>.jpg` (1920 × 1080, klein genug zum
Verschicken). Der Ordner `banner/ausgabe/` wird nicht hochgeladen. Fertige Banner gehören in den Ordner des
jeweiligen Webinars unter `webinare/`.

## Wenn etwas nicht passt

| Problem | Lösung |
|---|---|
| Person ragt in den Titel | `hoehe` verkleinern oder `x` verkleinern |
| Titel wird zu klein | kürzer formulieren (die Schrift passt sich der Länge an) |
| Foto wirkt abgeschnitten | `beschnitt` ändern oder anderes Foto |
| Pose zeigt nach außen | `spiegeln: true` |
| Ränder der Person sind unsauber | besseres Foto (ruhiger Hintergrund, gutes Licht) und neu freistellen |
| DigiUp-Logo kaum lesbar | Datei `wortmarke-digiup-dunkel.png` benutzen („dunkel“ = für dunklen Hintergrund) |
