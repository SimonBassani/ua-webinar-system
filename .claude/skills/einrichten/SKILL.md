---
name: einrichten
description: Einrichtungsassistent für das Webinar-System. Führt Schritt für Schritt durch benötigte Programme, Schutz vor Schlüssel-Pannen, persönlichen Gemini-Schlüssel, eigene Fotos und Referenzen, einen Probelauf und zum Schluss die optionale GitHub-Anmeldung. Immer verwenden beim allerersten Start in diesem Ordner, wenn die Datei .einrichtung-fertig fehlt, oder wenn jemand "einrichten", "Setup", "Installation" oder "es funktioniert nicht" sagt.
---

# Einrichtungsassistent

Du führst eine Person (meist Alex oder Michi von den Unternehmensathleten, ohne Technik-Hintergrund)
durch die Einrichtung. Ziel: Danach kann sie selbst Webinar-Banner und Präsentationen bauen.
Dauer: etwa 15 Minuten, ohne Gemini-Schlüssel und Foto-Freistellen weniger. Das Repo ist öffentlich und der Start braucht weder Einladung noch GitHub-Konto.

## Regeln für dich

- **Einfache Sprache, Du-Form, Deutsch.** Kein Fachjargon. Wenn ein Fachwort nötig ist, ein Satz Erklärung.
- **Ein Schritt nach dem anderen.** Sag zu Beginn jedes Schritts in einem Satz, was passiert und warum.
- **Prüfe selbst, frag nicht „hat es geklappt?“.** Nach jedem Schritt mit einem Befehl kontrollieren
  (`python3 tools/pruefen.py`) und das Ergebnis in einem Satz zurückmelden.
- **Erkläre jeden Befehl vorher**, bevor Claude Code um Erlaubnis fragt. Die Person soll wissen, wofür
  sie „Ja“ sagt.
- **Schlüssel und Passwörter:** Bitte die Person NIE, einen Schlüssel in den Chat einzufügen. Sie trägt
  ihn selbst in die Datei `.env` ein. Lies die Datei `.env` nie vor und gib ihren Inhalt nie aus. Falls
  doch einmal ein Schlüssel im Chat auftaucht: sofort sagen, dass er ungültig gemacht und neu erstellt
  werden muss (https://aistudio.google.com/apikey).
- **Nichts Zerstörerisches:** kein `rm -rf`, kein `git push --force`, nichts außerhalb des Repo-Ordners
  löschen oder verändern.
- **Betriebssystem erkennen** (Mac, Windows) und nur die passenden Befehle zeigen. Unter Windows heißt
  das Python-Programm oft `py` statt `python3`.
- **Bleib freundlich bei Fehlern.** Fehler sind normal. Erst die Ursache erklären, dann beheben.

## Ablauf

Zeige am Anfang diese Liste und hake sie im Gespräch ab:

1. Kennenlernen
2. Bestandsaufnahme
3. Programme installieren
4. Name für gespeicherte Änderungen und Schutz vor Schlüssel-Pannen
5. Eigener Gemini-Schlüssel (optional)
6. Eigenes Foto für Banner (optional)
7. Eigene Referenzen (optional)
8. Probelauf
9. GitHub-Konto verbinden (optional)
10. Abschluss

### 1. Kennenlernen

Prüfe, ob die Datei `.einrichtung-fertig` existiert. Falls ja: Frage, ob alles neu durchgegangen oder
nur etwas repariert werden soll, und starte dann mit Schritt 2.

Frage nach dem Vornamen. Erkläre in zwei Sätzen, was in diesem Ordner steckt: fertiges Webinar-Deck,
Anleitung, wie Webinare aufgebaut werden, und Werkzeuge für Präsentationen und Banner.

### 2. Bestandsaufnahme

Führe `python3 tools/pruefen.py` aus (Windows: `py tools/pruefen.py`; falls gar kein Python da ist: erst
uv installieren, siehe Schritt 3, und dann `uv run python tools/pruefen.py`). Erkläre das Ergebnis in
einfachen Worten: was ist schon da, was fehlt.

### 3. Programme installieren

Nur das installieren, was laut Prüfung fehlt.

- **uv** (startet die Python-Programme, ohne dass man Python selbst einrichten muss):
  - Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - Wenn `uv` danach nicht gefunden wird: auf dem Mac `export PATH="$HOME/.local/bin:$PATH"` setzen
    oder Claude Code schließen und neu öffnen.
- **Google Chrome** (macht aus den Folien PDF und Banner): Wenn es fehlt, Download-Seite nennen
  (https://www.google.com/chrome/), die Person installieren lassen, danach erneut prüfen. Edge geht
  unter Windows notfalls auch.
- **git:** Mac: `xcode-select --install` (öffnet ein Fenster, bestätigen). Windows:
  https://git-scm.com/download/win
- Das GitHub-Programm (`gh`) wird erst in Schritt 9 gebraucht, und nur, wenn die Person ihre Arbeit teilen will.

### 4. Name für gespeicherte Änderungen und Schutz vor Schlüssel-Pannen

- Name: nach dem vollen Namen fragen (ist `gh` schon angemeldet, kann `gh api user -q .name` ihn vorschlagen). Dann
  `git config user.name "<Name>"`. Den Namen immer in Anführungszeichen setzen und Sonderzeichen wie `"`, `$`, `` ` `` und `;`
  entfernen oder entschärfen, bevor er in einen Befehl eingesetzt wird.
- E-Mail: **nicht** die private Adresse verwenden, denn jede gespeicherte Änderung trägt sie, und dieses Repo ist
  öffentlich. Vorläufig `git config user.email "<vorname>@users.noreply.github.com"` setzen und erklären, warum.
  Wird in Schritt 9 GitHub verbunden, ersetzt du sie durch die echte noreply-Adresse
  `<id>+<login>@users.noreply.github.com` (`gh api user -q '.id'` und `gh api user -q '.login'`).
- Schutz aktivieren: `git config core.hooksPath .githooks`. Erkläre: Ab jetzt blockiert git automatisch,
  wenn jemand versehentlich einen Schlüssel, eine `.env`-Datei oder etwas aus dem privaten Ordner `deck/referenzen/` hochladen will.

### 5. Eigener Gemini-Schlüssel (optional)

Frage, ob die Person KI-Hintergründe für Banner möchte. Erkläre ehrlich: Das Banner funktioniert auch
**ohne**. Gemini ist nur für zusätzliche, KI-erzeugte Hintergrundbilder. Jedes Bild kostet ein paar Cent,
abgerechnet über das Google-Konto der Person. Für die Bildfunktion braucht der Schlüssel ein
Google-Projekt mit hinterlegter Zahlungsart; kostenlose Schlüssel funktionieren dafür oft nicht.

Wenn ja:
1. `https://aistudio.google.com/apikey` öffnen, mit dem Google-Konto anmelden, „Create API key“.
2. `cp .env.example .env` (Windows: `copy .env.example .env`).
3. Die Datei `.env` öffnen (Mac: `open -e .env`, Windows: `notepad .env`), den Schlüssel direkt hinter
   `GEMINI_API_KEY=` einfügen, speichern. **Nicht in den Chat einfügen.**
4. `python3 tools/pruefen.py` zeigt „vorhanden“, aber nie den Schlüssel selbst.
5. Mit Zustimmung (wegen der Cent-Kosten) einen Testlauf:
   `uv run --with-requirements requirements/gemini.txt python banner/gemini_bild.py --prompt "Dunkler Hintergrund mit mintgrünem Licht links, korallenrotem Licht rechts, kein Text" --ausgabe banner/ausgabe/test.png`
   und das Bild zeigen.

### 6. Eigenes Foto für Banner (optional)

Die Person braucht ein Foto, auf dem sie halbnah (bis zur Hüfte) vor einem ruhigen Hintergrund steht,
gut beleuchtet, mit offener Pose, die zur Mitte des Banners zeigen kann.

1. Die Person nennt den Dateipfad (oder zieht die Datei ins Terminal).
2. Freistellen:
   `uv run --with-requirements requirements/freistellen.txt python banner/freistellen.py "<Foto>" -o assets/hosts/<vorname>.png`
   Warnung vorab: Beim allerersten Mal wird ein Modell von rund 170 MB geladen, das dauert einige Minuten.
3. Das Ergebnis mit dem Read-Werkzeug ansehen, ehrlich beurteilen (Ränder, abgeschnittene Hände) und
   der Person zeigen. Bei schlechtem Ergebnis ein besseres Foto empfehlen.

### 7. Eigene Referenzen (optional)

Erkläre: Das Deck zeigt Platzhalter statt echter Teilnehmer („[Name 1]“, „FOTO“, „PLATZHALTER“), weil dieses Repo
öffentlich ist. Eigene Referenzen (Teilnehmerfoto, Umsatz-Screenshot) gehören nur auf den eigenen Rechner, in die
Ordner `deck/referenzen/fotos/` und `deck/referenzen/screens/`. Diese Ordner werden nie hochgeladen, der Schutz-Hook
blockiert sie. Wichtig: nur Material verwenden, für das die Person die Freigabe der abgebildeten Personen hat.
Frage, ob sie jetzt etwas ablegen möchte, und zeige, wie die Dateinamen zu den Schlüsseln im Deck passen
(`vorlagen/folien-bausteine.md`). Muss nicht jetzt sein.

### 8. Probelauf

1. Beispiel-Banner bauen: `uv run --with-requirements requirements/banner.txt python banner/banner.py banner/beispiel/config.json`
   und die Datei `banner/ausgabe/beispiel-akquise-copilot.jpg` öffnen (Mac: `open`, Windows: `start`).
2. Das fertige Deck im Browser öffnen: `deck/Akquise-Copilot.html`. Erkläre: Taste `F` = Vollbild,
   Pfeiltasten = blättern.
3. Erkläre in drei Sätzen, wie es weitergeht: Banner bauen (Skill `webinar-banner`), neues Deck bauen
   (Skill `webinar-deck`), und dass Claude die Doku in `docs/` kennt.

### 9. GitHub-Konto verbinden (optional)

Frage, ob die Person ihre Arbeit speichern und mit Simon teilen will. Wenn sie nur ausprobieren möchte: überspringen,
sie kann `/einrichten` später erneut aufrufen.

- **Kein Konto?** Kostenlos anlegen unter https://github.com/signup (E-Mail bestätigen). Den Benutzernamen an Simon
  schicken, damit er sie als Mitarbeiter einlädt. Die Einladung per E-Mail annehmen.
- **GitHub-Programm (`gh`) fehlt?** Mac: `brew install gh` (falls Homebrew vorhanden), sonst https://cli.github.com/
- **Anmelden:** `gh auth status`; wenn nicht angemeldet `gh auth login`: GitHub.com, HTTPS, „Login with a web
  browser“, Code im Browser eingeben.
- **Schreibrecht prüfen:** `gh api repos/SimonBassani/ua-webinar-system -q .permissions.push`. Bei `true` kann die
  Person direkt Zweige und Pull Requests anlegen. Bei `false` (noch keine Einladung): einen Fork anlegen
  (`gh repo fork --remote`), damit Vorschläge trotzdem möglich sind.
- Dann die noreply-E-Mail aus Schritt 4 setzen.

### 10. Abschluss

- Schreibe die Datei `.einrichtung-fertig` mit Datum und Vornamen (sie wird nicht hochgeladen).
- Führe `python3 tools/pruefen.py` ein letztes Mal aus und fasse zusammen, was bereit ist.
- Gib der Person drei Sätze zum Starten mit:
  - „Baue mir ein Banner für mein nächstes Webinar.“
  - „Wir machen ein neues Webinar zu <Thema>. Hilf mir, das Deck zu planen und zu bauen.“
  - „Was haben wir in den letzten Webinaren gelernt?“
- Erinnere an die zwei wichtigsten Regeln: (1) vor der Arbeit holt Claude immer den neuesten Stand
  (`git pull`), (2) Schlüssel gehören nur in die `.env`, (3) das Repo ist öffentlich: nichts Echtes von
  Teilnehmern hochladen, das bleibt in `deck/referenzen/`.
- Bei Problemen: Simon fragen.

## Häufige Probleme

| Meldung / Situation | Ursache und Lösung |
|---|---|
| `command not found: uv` direkt nach der Installation | Neues Terminalfenster öffnen oder `export PATH="$HOME/.local/bin:$PATH"` |
| `gh: command not found` | GitHub-Programm installieren (Schritt 9) |
| `Permission denied` beim Hochladen | Noch kein Schreibrecht (Einladung nicht angenommen) oder falsches GitHub-Konto angemeldet (`gh auth status` prüfen). Zum Lesen und Arbeiten braucht es das nicht |
| Freistellen bricht beim Modell-Download ab | Internet prüfen, erneut starten. Der Download läuft dann weiter |
| Gemini: „Schlüssel wird nicht akzeptiert“ | Schlüssel in `.env` unvollständig oder Leerzeichen dabei; Zahlungsart im Google-Projekt fehlt |
| PDF oder Banner bleibt hängen | `pkill -f -- "--headless=new"` (Mac), Windows: Chrome im Task-Manager beenden, neu starten |
