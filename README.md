# Webinar-System · unternehmensathleten × DigiUp

Alles, was wir in drei gemeinsamen Webinaren gelernt und gebaut haben: Aufbau, Dramaturgie,
Design, fertige Folien und die Skripte, mit denen aus Text ein Deck wird.

Ziel: Alex und Michi können damit **ohne Simon** das nächste Webinar-Deck bauen — im selben Look,
mit derselben Dramaturgie.

## Schnellstart für Alex und Michi

Ihr wollt selbst Banner und Präsentationen für Webinare bauen, im selben Look wie wir? Drei Schritte, kein
Konto und keine Einladung zum Ausprobieren nötig:

1. **Claude Code installieren.** Mac (Terminal): `curl -fsSL https://claude.ai/install.sh | bash`
   Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`. Danach einmal `claude` starten, anmelden, `exit`.
2. **Herunterladen:**
   ```
   git clone https://github.com/SimonBassani/ua-webinar-system.git Webinar-System
   cd Webinar-System
   claude
   ```
3. **Der Einrichtungsassistent startet von selbst** und führt euch in etwa 15 bis 30 Minuten durch alles Weitere
   (Programme, optional Gemini-Schlüssel, euer Foto, eure Referenzen, Probelauf, GitHub).
   Danach sagt ihr einfach: **„Baue mir ein Banner für mein nächstes Webinar“** oder
   **„Wir machen ein neues Webinar zu …“**.

Ein GitHub-Konto braucht ihr erst, wenn ihr eure Arbeit speichern und mit Simon teilen wollt. Alle Details:
[docs/08-einrichtung.md](docs/08-einrichtung.md).

**Wichtig:** Dieses Repo ist öffentlich. Echte Teilnehmerfotos, Umsatz-Screenshots und Zitate liegen nicht hier.
Das Deck zeigt Platzhalter. Eure echten Referenzen legt ihr nur lokal in `deck/referenzen/` ab, siehe
[docs/09-sicherheit.md](docs/09-sicherheit.md).

## Womit du anfängst

| Du willst … | Dann lies |
|---|---|
| verstehen, wie wir ein Webinar von der Idee bis zum Termin aufziehen | [docs/01-webinar-playbook.md](docs/01-webinar-playbook.md) |
| wissen, **warum** welche Folie an welcher Stelle steht | [docs/02-deck-dramaturgie.md](docs/02-deck-dramaturgie.md) |
| Farben, Schriften, Bausteine nachschlagen | [docs/03-design-system.md](docs/03-design-system.md) |
| Folien ändern und ein neues PDF bauen | [docs/04-build-anleitung.md](docs/04-build-anleitung.md) |
| die Fehler nicht wiederholen, die uns Geld gekostet haben | [docs/05-lehren.md](docs/05-lehren.md) |
| nachsehen, was in den drei Webinaren passiert ist | [docs/06-historie.md](docs/06-historie.md) |
| kurz vor dem Webinar nichts vergessen | [docs/07-checklisten.md](docs/07-checklisten.md) |
| alles einrichten (Claude Code, Schlüssel, GitHub) | [docs/08-einrichtung.md](docs/08-einrichtung.md) |
| wissen, was geschützt ist und worauf ihr achten müsst | [docs/09-sicherheit.md](docs/09-sicherheit.md) |
| ein Banner bauen | [banner/README.md](banner/README.md) |
| ein neues Webinar anlegen | [webinare/README.md](webinare/README.md) |

## Das fertige Deck

Im Ordner [`deck/`](deck/) liegt das komplette Webinar vom 22.09.2026 („Dein Akquise-Copilot“, 80 Folien):

- **`Akquise-Copilot.html`** — das Präsentations-Deck. Doppelklick, dann `F` für Vollbild, mit `←` `→` blättern. Läuft offline, ohne Internet, ohne PowerPoint.
- **`Akquise-Copilot.pdf`** — dieselben Folien als PDF, zum Verschicken.
- **`build3.py`** — das Skript, das aus dem alten Deck das neue baut. Hier wird geändert, nicht in der HTML.
- **`base_v2.html`** — der Stand, auf dem `build3.py` aufsetzt.
- **`pdf.py`** — macht aus der HTML das PDF.
- **`folien_lib.py`** — Werkzeugkasten, um aus diesem Deck ein neues Webinar-Deck zu machen.
- **`fotos/`, `screens/`** — Fotos der Sprecher und Produktbilder. Echte Referenzen (Teilnehmer, Umsätze) kommen nur lokal nach `referenzen/`.

## Skills für Claude Code

In diesem Ordner kennt Claude Code drei Skills, die ihr einfach beim Namen oder per Beschreibung ruft:

- **`/einrichten`** — Einrichtungsassistent (startet beim ersten Mal automatisch)
- **`webinar-banner`** — Banner, Thumbnail, Event-Bild für ein Webinar
- **`webinar-deck`** — Präsentation für ein neues Webinar bauen oder ändern

## Wichtigste Regel beim Ändern

Änderungen gehören in **`deck/build3.py`**, nicht direkt in die HTML-Datei.
Die HTML wird bei jedem Build neu erzeugt und überschreibt alles, was du von Hand hineinschreibst.

## Wer macht was

- **Alex (Unternehmensathleten)** — Positionierung, Angebot, Vertriebslogik, Publikum, Skript, Referenzen.
- **Michi (Unternehmensathleten)** — Verkaufspsychologie, Pitch-Aufbau, Dramaturgie.
- **Simon (DigiUp)** — KI-System, Live-Demo, Deck-Bau.

Farben, Schriften und das Co-Branding sind abgestimmt. Bitte nicht eigenmächtig ändern —
warum, steht in [docs/03-design-system.md](docs/03-design-system.md).

## Stand

Letztes Webinar: 22.09.2026, „Dein Akquise-Copilot: doppelter Umsatz aus alten Kontakten!“, 80 Folien.
Dieses Repo ist öffentlich, ohne Teilnehmerdaten (Platzhalter statt Referenzen).
