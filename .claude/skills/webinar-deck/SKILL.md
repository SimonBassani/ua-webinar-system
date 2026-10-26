---
name: webinar-deck
description: Baut oder überarbeitet die Präsentation (Deck) für ein Webinar von unternehmensathleten × DigiUp im gemeinsamen Look und mit der bewährten Dramaturgie. Ausgangspunkt ist das letzte fertige Deck, geändert werden Titel, Zahlen, Angebot, Folien und Reihenfolge. Verwenden bei "neues Webinar", "Präsentation", "Deck", "Folien ändern", "Folie einfügen", "PDF bauen".
---

# Webinar-Deck bauen

Das Deck wird nie von Grund auf neu gebaut. Man nimmt das letzte fertige Deck (`deck/Akquise-Copilot.html`)
und ändert gezielt, was im neuen Webinar anders ist. So bleibt der Look gleich und die erprobte
Dramaturgie bleibt erhalten.

## Vorab

1. Einrichtung fertig? (Datei `.einrichtung-fertig`). Sonst `/einrichten`.
2. `git pull`, damit der neueste Stand da ist.
3. **Lies diese drei Dokumente, bevor du etwas baust:**
   - `docs/02-deck-dramaturgie.md` (warum welche Folie wo steht)
   - `docs/03-design-system.md` (Farben, Schriften, Bausteine)
   - `docs/05-lehren.md` (was uns Anmeldungen gekostet hat)
   Für Zahlen aus früheren Webinaren: `docs/06-historie.md`.

## Ablauf

### 1. Briefing

Frage nach, was fehlt. **Erfinde nie Zahlen, Namen, Referenzen oder Versprechen.**

- Titel (Ergebnis + Mechanismus, mit Filter) und Termin
- Zielgruppe
- Was bleibt gleich, was ist neu gegenüber dem letzten Webinar?
- Angebot: Invest, Plätze, Dauer, Boni, Marktanker
- Wer spricht welche Folien? (Kürzel A, M, S)
- Neue Referenzen: Foto, Zitat, Screenshot, Freigabe
- Was wird live gezeigt?

### 2. Ordner und Skript anlegen

```
webinare/<datum>-<kurzname>/
    build.py      ← Kopie von vorlagen/neues-webinar-build.py
```

### 3. Änderungen eintragen

In `build.py` die vorbereiteten Zeilen aktivieren und anpassen. Die Funktionen stehen in
`deck/folien_lib.py` und sind in der Vorlage erklärt:

| Aufgabe | Befehl |
|---|---|
| alle Folien mit Nummer anzeigen | `d.liste()` |
| Text ersetzen | `d.ed("Folienname", "alter Text", "neuer Text")` |
| Sprechernotiz ändern | `d.notes("Folienname", "Text")` |
| Folie streichen | `d.streichen("Folienname")` |
| Folie einfügen | `d.einfuegen_nach("Folienname", section(...))` |
| Folie in Stufen aufbauen | `d.duplizieren(...)` und in jeder Kopie Teile mit `visibility:hidden` verstecken |
| Reihenfolge ändern | `d.verschieben_nach("Folie", "Zielfolie")` |
| Sprecher-Kürzel | `d.kuerzel([(1, 10, "A"), (11, 40, "S"), ...])` |

Wenn eine Ersetzung abbricht („Text kommt 0-mal vor“), steht der alte Text nicht mehr genau so im Deck.
Dann mit `grep` oder `d.liste()` den aktuellen Wortlaut suchen und anpassen. Niemals die fertige HTML
von Hand ändern, sie wird beim nächsten Bauen überschrieben.

### 4. Bauen und prüfen

```bash
uv run python webinare/<name>/build.py
uv run --with-requirements requirements/deck.txt python deck/pdf.py webinare/<name>/deck.html 1,5,12
```

Der zweite Befehl baut das PDF (etwa 3 bis 5 Minuten bei 80 Folien) und erzeugt Vorschaubilder der
genannten Folien. **Sieh dir die geänderten Folien selbst an**, bevor du „fertig“ sagst: das Vorschaubild
mit dem Read-Werkzeug öffnen und kritisch prüfen (Lesbarkeit, Überlappung, Leerräume, Farben).

Zwischendurch reicht es, nur die HTML zu bauen und im Browser zu öffnen (`F` = Vollbild).

### 5. Regeln für neue Folien

- Aufbau: Eyebrow (klein, Mint) → große Überschrift mit einem farbigen Teil → Inhalt.
- Keine nackten Aufzählungen. Karten, Zahlen, Grafiken. Wenig Leerraum.
- Mint = gelöst, Terracotta = Problem. Nicht mischen.
- Überladene Folien teilen oder in Stufen aufbauen.
- Jede Referenz mit Foto. Keine Platzhalter ins fertige Deck. Fehlt Material, am Ende klar auflisten.
- Sprecher-Kürzel auf jeder Folie.
- Code-Bausteine zum Kopieren: `vorlagen/folien-bausteine.md`.
- **Webinar im UA-Design:** Muster in `vorlagen/ua-webinar-muster.md` lesen und befolgen (fester Kopf bei
  88/124 px, Antwortkarten auf fester Höhe, Preisfolien, QR-Code, Live Q&A mit Mitteilungen). Ausgangspunkt ist
  `webinare/2026-10-27-linkedin-performance-system/build.py`, nicht das Alex-Simon-Deck.

### 6. Abliefern

- Dateien in `webinare/<name>/`: `deck.html`, `deck.pdf`, `build.py`.
- Datei im Dateimanager zeigen (Mac: `open -R`, Windows: `explorer /select,`).
- Offene Punkte nennen (fehlende Fotos, ungeklärte Zahlen, Freigaben).
- `git pull`, dann `git add webinare/<name>`, committen (deutsche Kurzmeldung), pushen.
  Änderungen an gemeinsamen Dateien (`docs/`, `tools/`, `deck/`, `.claude/`, `assets/logos`) nie direkt
  auf `main`: eigenen Branch anlegen, pushen, Pull Request öffnen (`gh pr create`) und Simon Bescheid geben.
- Nach dem Webinar: `docs/06-historie.md` um das neue Webinar ergänzen.
