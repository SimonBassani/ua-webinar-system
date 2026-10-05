---
name: webinar-banner
description: Baut das Banner (LinkedIn-Event-Bild, Webinar-Thumbnail) für ein Webinar im Look von unternehmensathleten × DigiUp. Zwei Personen links und rechts mit Namen und Pfeilen, Titel in der Mitte, Datum, Live-Demo-Badge, Logos und optional eine kleine Produktkarte. Verwenden bei "Banner", "Thumbnail", "Event-Bild", "Titelbild fürs Webinar", "LinkedIn-Event".
---

# Webinar-Banner

Erzeugt aus einer kleinen Konfigurationsdatei ein fertiges Banner (1920 × 1080, auch 3840 × 2160).
Läuft komplett ohne KI-Bildgenerierung. Gemini ist nur für einen optionalen Hintergrund da.

So sieht das Ergebnis aus: `banner/beispiel/ergebnis.jpg`.
Alle Felder der Konfiguration: `banner/README.md`.

## Wann benutzen

Die Person will ein Banner, Thumbnail, Event-Bild oder Titelbild für ein Webinar. Für YouTube-Thumbnails
oder andere Formate ist dieser Skill nicht gedacht (nur 16:9).

## Vorab prüfen

1. Ist die Einrichtung fertig? Datei `.einrichtung-fertig` vorhanden? Wenn nicht: erst `/einrichten`.
2. Stand holen: `git pull`.

## Ablauf

### 1. Angaben einsammeln (fehlendes nachfragen, nichts erfinden)

| Angabe | Hinweis |
|---|---|
| Titel groß | Das Produkt in 1 bis 2 Wörtern, z. B. „Akquise-Copilot“. Titelregeln: `docs/01-webinar-playbook.md`, `docs/05-lehren.md` |
| Titel klein (optional) | Ein kleines Wort davor, z. B. „Dein“ |
| Untertitel | Ergebnis in einem Satz. Mit `[[doppelten Klammern]]` wird ein Teil in Terracotta hervorgehoben |
| Datum-Pille | Format `LIVE · DI 22.09. · 11:00 UHR` |
| Badge oben | Zum Beispiel `INKL. LIVE-DEMO` |
| Personen | Zwei Personen mit Name, Firma, freigestelltem Foto |
| Produktkarte (optional) | Ein kleiner Blick ins System: Titel, Status, zwei bis drei Beispiel-Chips, ein Ergebnis |

Faustregeln aus unseren Banner-Runden:
- **Wenig Text.** Das Thema und das Ergebnis, nicht die ganze Agenda.
- **Das System steht im Vordergrund**, nicht die Textblöcke. Darum gibt es die kleine Produktkarte.
- **Beide Personen mit Name** und Pfeil zu sich, damit man sieht, wer dabei ist.
- **Datum und Uhrzeit müssen auf dem Handy lesbar sein.**
- Die Posen sollen zur Mitte zeigen. Bei Bedarf Foto spiegeln (`"spiegeln": true`).

### 2. Fotos vorbereiten

Liegen die Fotos schon freigestellt in `assets/hosts/<vorname>.png`? Dann direkt weiter.
Sonst freistellen (beim allerersten Mal lädt das Programm ein Modell von rund 170 MB):

```bash
uv run --with-requirements requirements/freistellen.txt python banner/freistellen.py "<Foto.jpg>" -o assets/hosts/<vorname>.png
```

Das Ergebnis mit dem Read-Werkzeug ansehen und ehrlich prüfen: saubere Ränder, keine abgeschnittenen
Hände, keine Reste vom Hintergrund. Bei schlechtem Ergebnis ein besseres Foto anfordern.

### 3. Konfiguration anlegen

Ordner `webinare/<datum>-<kurzname>/` anlegen und dort `banner.json` aus `banner/beispiel/config.json`
ableiten. Pfade in der Datei gelten ab dem Hauptordner des Repos. `ausgabe` auf
`webinare/<datum>-<kurzname>/banner` setzen.

Logos: Für dunkle Hintergründe `assets/logos/wortmarke-digiup-dunkel.png` verwenden. Der Name ist
verwirrend, aber so gemeint: „dunkel“ heißt „für dunklen Hintergrund“ (weißes „Digi“). Die Datei „hell“ ist
für helle Flächen und auf dem Banner kaum lesbar.

### 4. Bauen und prüfen

```bash
uv run --with-requirements requirements/banner.txt python banner/banner.py webinare/<name>/banner.json
```

Dauert etwa 20 Sekunden. Das PNG mit dem Read-Werkzeug ansehen und **selbst kritisch prüfen**, bevor es
der Person gezeigt wird:

- Ragt jemand in den Titel? → `hoehe` verkleinern oder `x` verschieben
- Ist der Titel zu lang und wird klein? → kürzer formulieren
- Ist ein Foto abgeschnitten oder zu groß? → `beschnitt`, `hoehe`
- Passt die Pose? → `spiegeln`
- Sind Text und Pillen scharf und lesbar?

Anpassen, neu bauen, erneut ansehen, bis es stimmt. Dann der Person zeigen und Feedback einholen.

### 5. Optional: KI-Hintergrund

Nur nach Rückfrage, weil es ein paar Cent kostet und einen eigenen Schlüssel (`.env`) braucht.

```bash
uv run --with-requirements requirements/gemini.txt python banner/gemini_bild.py \
  --prompt "Abstrakter dunkler Hintergrund für ein Business-Webinar-Banner, 16:9. Tiefschwarz mit weichem mintgrünem Lichtschein links und korallenrotem Lichtschein rechts, feine Bokeh-Lichtpunkte. Keine Personen, kein Text, keine Logos." \
  --ausgabe webinare/<name>/hintergrund.png
```

Dann in der Konfiguration `"hintergrund": "webinare/<name>/hintergrund.png"` eintragen und neu bauen.
Wichtig: Keine Personen und keinen Text vom Modell erzeugen lassen. Gesichter werden verfälscht und
deutsche Wörter fehlerhaft. Personen und Text setzt immer das Banner-Skript.

### 6. Abliefern

- Dateien: `<name>.png` (volle Qualität) und `<name>.jpg` (klein, zum Verschicken).
- Datei öffnen (Mac: `open -R <Pfad>`, Windows: `explorer /select,<Pfad>`).
- Banner und Konfiguration in `webinare/<name>/` speichern, `git pull`, dann committen und pushen
  (`git add webinare/<name>`, Meldung auf Deutsch, z. B. „Banner für Webinar Linkedin-Sales“).
  Das Verzeichnis `banner/ausgabe/` wird nicht hochgeladen.

## Farben und ihre Bedeutung

Mint `#7DDBA6` steht für „gelöst, gut, Gewinn“. Terracotta `#E8917A` steht für „Problem, Dringlichkeit,
live“. Auf dem Banner: Titel in Mint, „Live“-Badge in Terracotta, Ergebnis-Zahl in Terracotta. Nicht
umfärben, die Farben sind mit der Kooperation abgestimmt.
