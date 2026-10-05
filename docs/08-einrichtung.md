# 08 · Einrichtung: von null bis zum ersten Banner

Für Alex und Michi. Danach könnt ihr selbst Webinar-Banner und Präsentationen bauen. Dauer etwa
30 Minuten. Das meiste erledigt Claude Code für euch, ihr müsst nur ein paar Mal bestätigen.

## Was ihr braucht

- Ein Mac oder Windows-Rechner (Windows ist noch nicht ausführlich getestet, meldet Probleme an Simon)
- Ein Claude-Konto, mit dem ihr Claude Code nutzen könnt (Pro, Max oder Team)
- Später, zum Speichern und Teilen eurer Arbeit: ein kostenloses GitHub-Konto (Schritt D)

Das Repo ist öffentlich. Zum **Ausprobieren** braucht ihr weder Einladung noch GitHub-Konto.

## Schritt A: Claude Code installieren (5 Minuten)

Claude Code ist der Assistent, mit dem ihr arbeitet. Er läuft im Terminal.

- **Mac:** Programm „Terminal“ öffnen (Spotlight: Cmd + Leertaste, „Terminal“ tippen) und eingeben:
  ```
  curl -fsSL https://claude.ai/install.sh | bash
  ```
- **Windows:** „PowerShell“ öffnen und eingeben:
  ```
  irm https://claude.ai/install.ps1 | iex
  ```

Falls sich der Installationsweg geändert hat, steht die aktuelle Anleitung auf
https://claude.com/product/claude-code. Danach im Terminal `claude` eingeben und mit dem Claude-Konto
anmelden, dann mit `exit` wieder beenden.

## Schritt B: Webinar-System herunterladen (2 Minuten)

Im Terminal (Windows: PowerShell) diese Zeilen eingeben. Wenn git fehlt, fragt der Mac, ob er es installieren soll:
bestätigen. Unter Windows git vorher von https://git-scm.com/download/win installieren.

```
git clone https://github.com/SimonBassani/ua-webinar-system.git Webinar-System
cd Webinar-System
claude
```

Claude fragt beim ersten Mal, ob ihr dem Ordner vertraut. Mit „Ja“ bestätigen.

## Schritt C: Der Einrichtungsassistent (15 Minuten)

Er startet **von selbst**, sobald `claude` im Ordner läuft. Er erklärt jeden Schritt, prüft selbst, ob es geklappt
hat, und führt euch durch:

1. Welche Programme fehlen noch (uv, Chrome)
2. Euren Namen für gespeicherte Änderungen setzen und den Schutz vor versehentlich hochgeladenen Schlüsseln aktivieren
3. Optional: euren eigenen Schlüssel für KI-Hintergründe (Gemini)
4. Optional: euer Foto für die Banner freistellen
5. Optional: eure echten Referenzen (Teilnehmerfotos, Screenshots) in den privaten Ordner `deck/referenzen/` legen
6. Ein Probelauf: Beispiel-Banner bauen und das Deck öffnen
7. Optional: GitHub-Konto verbinden, um eure Arbeit zu speichern und mit Simon zu teilen

## Schritt D: GitHub-Konto, um Arbeit zu speichern und zu teilen (optional)

Nur nötig, wenn eure Arbeit (zum Beispiel ein neues Webinar im Ordner `webinare/`) bei Simon und beim anderen
ankommen soll.

1. https://github.com/signup öffnen, kostenloses Konto anlegen, E-Mail bestätigen.
2. **Benutzernamen an Simon schicken.** Simon lädt euch als Mitarbeiter ein, die Einladung per E-Mail annehmen.
3. Im Assistenten `/einrichten` sagen, dass ihr GitHub verbinden wollt. Er führt euch durch die Anmeldung.

Ohne Einladung geht auch etwas: Claude kann einen eigenen Fork anlegen und einen Vorschlag (Pull Request) schicken.

## Schritt E: Ab jetzt

Ordner öffnen, `claude` starten, sagen was ihr wollt. Zum Beispiel:

- „Baue mir ein Banner für mein nächstes Webinar.“
- „Wir machen ein neues Webinar zu <Thema>. Hilf mir, das Deck zu planen und zu bauen.“
- „Was haben wir in den letzten Webinaren gelernt?“
- „Ändere auf Folie ‚Dein Invest‘ den Betrag auf [euer Betrag].“

Claude kennt die gesamte Dokumentation in diesem Ordner und die zwei Skills `webinar-banner` und
`webinar-deck`. Vor jeder Arbeit holt es sich automatisch den neuesten Stand.

## Eure Schlüssel gehören euch

- Der **Gemini-Schlüssel** ist persönlich. Er steht nur in der Datei `.env` auf eurem Rechner. Diese Datei
  wird nie hochgeladen. Gebt ihn niemandem weiter und fügt ihn nie in einen Chat ein.
- Falls er doch irgendwo gelandet ist: auf https://aistudio.google.com/apikey löschen und einen neuen
  erstellen.
- Gemini ist **optional**. Banner und Präsentationen funktionieren auch ohne.

## Wenn etwas nicht klappt

1. `python3 tools/pruefen.py` zeigt, was fehlt (Windows: `py tools/pruefen.py`).
2. In Claude Code **„/einrichten“** eingeben, der Assistent repariert, was fehlt.
3. Simon fragen.
