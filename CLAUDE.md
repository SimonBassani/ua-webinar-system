# Arbeitsanweisungen für Claude Code in diesem Repo

Dieses Repo ist das Webinar-System von unternehmensathleten × DigiUp: Doku, Design-System, Skills,
Werkzeuge und ein fertiges 80-Folien-Deck. Hier arbeiten Alex, Michi und Simon. **Das Repo ist öffentlich:** nie echte Teilnehmerfotos, Umsatzzahlen, Zitate, Kundendaten oder Schlüssel committen. Alex und Michi sind
Vertriebs- und Positionierungsprofis ohne Technik-Hintergrund. Sprich mit ihnen einfach und ohne Fachjargon.

## Beim Start jeder Sitzung

1. **Gibt es die Datei `.einrichtung-fertig`?** Wenn nicht, ist das hier die erste Sitzung auf diesem
   Rechner: Begrüße freundlich und starte sofort den Einrichtungsassistenten (Skill `einrichten`,
   `.claude/skills/einrichten/SKILL.md`). Warte nicht auf eine Aufforderung.
2. **Stand holen:** `git pull` (bei Fehlern nicht raten, sondern erklären und Hilfe anbieten).
3. Dann erst auf die Aufgabe der Person eingehen.

## Skills in diesem Repo

| Skill | Wofür |
|---|---|
| `einrichten` | Einrichtungsassistent (Programme, Schlüssel, Foto, Referenzen, Probelauf, GitHub) |
| `webinar-banner` | Banner / Thumbnail / Event-Bild fürs Webinar |
| `webinar-deck` | Präsentation für ein neues Webinar bauen oder ändern |

Passt eine Aufgabe zu einem Skill, benutze ihn, statt etwas Eigenes zu bauen.

## Was in welchem Ordner liegt

| Ordner | Inhalt |
|---|---|
| `docs/` | Anleitung und Wissen: Playbook, Dramaturgie, Design-System, Build, Lehren, Historie, Checklisten, Einrichtung |
| `deck/` | Das Referenz-Deck (22.09.2026, mit Platzhaltern statt Referenzen), Bauskripte, `folien_lib.py` zum Umbauen, Sprecherfotos, privater Ordner `referenzen/` |
| `banner/` | Banner-Werkzeuge: freistellen, bauen, optional KI-Hintergrund |
| `vorlagen/` | Folien-Bausteine, Event-Text, Vorlage für ein neues Deck-Bauskript |
| `webinare/` | Pro Webinar ein Ordner mit Deck, Banner und Skript |
| `assets/` | Logos, Fotos der Sprecher, Banner-Beispiele |
| `tools/` | Hilfsprogramme: Umgebungs-Check, Chrome-Steuerung |

## Bevor du am Deck etwas änderst

1. `docs/02-deck-dramaturgie.md`, `docs/03-design-system.md` und `docs/05-lehren.md` lesen. Sie sind verbindlich.
2. **Nie die fertige HTML-Datei von Hand ändern.** Sie wird beim Bauen neu erzeugt. Änderungen gehören in ein
   Bauskript: das Referenz-Deck wird über `deck/build3.py` gebaut, neue Webinare über
   `webinare/<name>/build.py` (Vorlage: `vorlagen/neues-webinar-build.py`, Werkzeuge: `deck/folien_lib.py`).
3. Nach jedem Bau die geänderten Folien als Bild ansehen, bevor du „fertig“ sagst:
   `uv run --with-requirements requirements/deck.txt python deck/pdf.py <deck.html> 1,5,12` erzeugt Vorschaubilder.
   Den Pfad der Vorschau liest du mit dem Read-Werkzeug.

## Regeln für Folien

- Format 1920 × 1080, dunkler Hintergrund, eine `<section>` pro Folie.
- Aufbau: Eyebrow (klein, Großbuchstaben, Mint) → große Überschrift mit **einem** farbigen Teil → Inhalt.
  Keine nackten Aufzählungen, lieber Karten, Grafiken, echte Zahlen. Wenig Leerraum.
- **Mint `#7DDBA6` = „gelöst, gut, Gewinn“. Terracotta `#E8917A` = „Problem, Dringlichkeit, live“.** Nicht mischen.
- Lange Inhalte stufenweise aufbauen (dieselbe Folie mehrfach, jeweils ein Element mehr sichtbar). Nie alles
  auf einmal zeigen. Überladene Folien teilen.
- Sprecher-Kürzel rechts unten (`A`, `M`, `S`, `A/S`) bleibt auf jeder Folie.
- DigiUp-Logo auf dunklem Grund: Datei `assets/logos/wortmarke-digiup-dunkel.png` („dunkel“ = für dunklen Hintergrund).

## Sprache und Inhalt

- Deutsch, Du-Form, echte Umlaute.
- **Copilot, nicht Autopilot:** Er bereitet vor, der Mensch entscheidet und schickt ab.
- **„Invest“ statt „Preis“** bei Selbstständigen.
- **Nichts erfinden:** keine Zahlen, Namen, Referenzen, Zitate oder Versprechen. Fehlt Material, nachfragen.
  Keine Platzhalter im fertigen Deck. Offene Punkte am Ende klar auflisten.
- Fotos und Zitate von Teilnehmern nur mit Freigabe, und nur lokal in `deck/referenzen/{fotos,screens}/` (nicht im
  Repo, vom Schutz-Hook blockiert). Im öffentlichen Deck stehen Platzhalter („[Name 1]“, „FOTO“, „PLATZHALTER“).
  Vor einem echten Webinar ersetzt die Person sie mit ihren eigenen Referenzen.

## Git: so arbeitet ihr zu dritt, ohne euch in die Quere zu kommen

- Vor der Arbeit immer `git pull`.
- **Neue Webinar-Ordner unter `webinare/`** dürfen direkt auf `main` (vorher `git pull --rebase`, dann
  `git add webinare/<name>`, committen, `git push`). Commit-Meldungen kurz auf Deutsch.
- **`main` ist geschützt.** Ohne Schreibrecht (kein Mitarbeiter) legt die Person einen Fork an und schickt einen
  Pull Request (`gh repo fork --clone`, `gh pr create`).
- **Gemeinsame Dateien** (`docs/`, `tools/`, `deck/`, `banner/`, `.claude/`, `.githooks/`, `requirements/`,
  `assets/logos/`, `vorlagen/`, `CLAUDE.md`, `README.md`) **nie direkt auf `main`:** eigenen Branch anlegen (`<vorname>/<thema>`), pushen,
  Pull Request mit `gh pr create` öffnen und der Person sagen, dass Simon Bescheid bekommen soll.
- **Nie** `git push --force`, nie die Historie umschreiben, nie fremde Änderungen verwerfen.
- Hat die Person Änderungen, die nicht gespeichert sind, vor einem `git pull` erst nachfragen.

## Schlüssel und Passwörter

- Persönliche Schlüssel (Gemini) stehen nur in `.env`. Diese Datei wird nie hochgeladen (`.gitignore` und
  Schutz-Hook in `.githooks/`).
- Lies `.env` nie vor, gib sie nie aus, kopiere sie nie in andere Dateien. Fragt jemand, ob ein Schlüssel
  eingetragen ist, prüfe das mit `python3 tools/pruefen.py` (zeigt nur „vorhanden“).
- Bitte niemanden, einen Schlüssel in den Chat einzufügen. Passiert es trotzdem, sage sofort, dass der
  Schlüssel ungültig gemacht und neu erstellt werden muss.
- Aktiviere den Schutz-Hook mit `git config core.hooksPath .githooks`, falls er fehlt.

## Technik in Kürze

- Programme laufen mit `uv run …` (Python wird automatisch bereitgestellt).
- PDF und Banner entstehen über Google Chrome (oder Edge), gesteuert von `tools/chrome.py`. Das PDF ist ein
  Bild-PDF, damit weiche Schatten auf jedem Gerät gleich aussehen. Details: `docs/04-build-anleitung.md`.
- Der Umgebungs-Check: `python3 tools/pruefen.py` (Windows: `py tools/pruefen.py`).
