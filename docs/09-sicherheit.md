# 09 · Sicherheit: was geschützt ist und worauf ihr achtet

Kurz und ohne Technik-Chinesisch. **Dieses Repo ist öffentlich.** Jeder kann es lesen und herunterladen. Darum
liegen hier weder Teilnehmerfotos noch Umsatz-Screenshots noch Schlüssel, und es gibt ein paar feste Regeln.

## Was automatisch geschützt ist

| Schutz | Wirkung |
|---|---|
| **Schlüssel nur in `.env`** | Diese Datei steht auf der Ignorierliste und wird nie hochgeladen. Auch `.env.local` und Ähnliches nicht. |
| **Eigene Referenzen nur in `deck/referenzen/`** | Fotos von Teilnehmern und Umsatz-Screenshots legt ihr dort ab. Der Ordner steht auf der Ignorierliste und bleibt auf eurem Rechner. |
| **Schutz-Hook** | Beim Speichern von Änderungen prüft git, ob eine Schlüsseldatei, etwas wie ein Schlüssel (Google, GitHub, OpenAI) oder eine Datei aus `deck/referenzen/` mit hochgeladen würde, und stoppt. Der Einrichtungsassistent schaltet ihn ein. |
| **Feste Paketversionen** | Alle Python-Pakete (Banner, PDF, Freistellen, Gemini) sind in `requirements/` mit exakter Version und Prüfsumme festgelegt. Es wird nie „irgendeine neueste Version“ aus dem Internet geladen. |
| **Fehlermeldungen ohne Schlüssel** | Das Gemini-Programm gibt den Schlüssel nie aus, auch nicht in Fehlermeldungen. |
| **Kein Schlüssel im Chat** | Der Einrichtungsassistent lässt euch den Schlüssel selbst in die Datei eintragen. Nichts davon geht durch den Chat. |
| **Änderungen nur mit Freigabe** | Auf `main` kommt nur, was per Pull Request von Simon freigegeben wurde (Branch-Schutz plus Code-Besitzer, siehe unten). |

## Eure Regeln

1. **Den Gemini-Schlüssel niemandem geben**, nicht in den Chat einfügen, nicht in Dateien außer `.env` schreiben.
   Ist er doch irgendwo gelandet: auf https://aistudio.google.com/apikey löschen und einen neuen erstellen.
2. **Nie etwas Echtes von Teilnehmern ins Repo.** Fotos, Namen, Umsatzzahlen, Zitate und Screenshots gehören nur
   mit Freigabe der Person und nur nach `deck/referenzen/`. Im öffentlichen Deck stehen Platzhalter
   („[Name 1]“, „FOTO“, „PLATZHALTER“). Vor einem Webinar ersetzt ihr sie lokal durch eure echten Referenzen.
3. **Keine Kundendaten, Preislisten oder Verträge ins Repo.** Alles in diesem Repo ist weltweit lesbar. Ein Banner
   oder PDF zum Verschicken ist etwas anderes: das darf natürlich raus.
4. **Gemeinsame Dateien nur per Pull Request ändern.** Änderungen an `docs/`, `tools/`, `deck/`, `banner/`,
   `.claude/`, `.githooks/`, `requirements/` und `vorlagen/` laufen über einen Pull Request (Claude macht das für
   euch). Simon gibt frei.
5. **Neue Programme nur bewusst installieren.** Die Einrichtung nutzt die Installer von uv, Claude Code und GitHub
   direkt von deren offiziellen Seiten. Sonst nichts blind aus dem Internet laufen lassen.

## Gut zu wissen

- **Gemini ist optional und kostet Geld** (ein paar Cent pro Bild, über das eigene Google-Konto). Wer ein Bild als
  Vorlage mitgibt (`--ref`), lädt dieses Bild zu Google hoch.
- **Freistellen läuft nur auf dem eigenen Rechner.** Das Modell wird einmal heruntergeladen, die Fotos verlassen
  den Rechner dabei nicht.
- **Alle Befehle laufen auf eurem Rechner.** Banner und PDF entstehen lokal über Chrome.
- **Wer das Repo nur herunterlädt, kann nichts ändern.** Schreiben darf nur, wer als Mitarbeiter eingeladen ist;
  alle anderen können höchstens einen Vorschlag (Pull Request) machen, den Simon freigeben müsste.

## Warum der Freigabe-Schritt wichtig ist

Wer Schreibrechte hat, kann Dateien ändern, die auf den Rechnern der anderen automatisch ausgeführt werden
(`.claude/settings.json`, `.githooks/`, die Programme in `tools/`, `banner/`, `deck/`). Das ist bei jedem
Repo so, das andere klonen. Deshalb ist `main` geschützt: Änderungen nur per Pull Request, für die genannten
Ordner mit Freigabe von Simon (Datei `.github/CODEOWNERS`).

Zusätzlich: die GitHub-Konten mit **Zwei-Faktor-Anmeldung** schützen (GitHub → Settings → Password and
authentication). Das ist der wirksamste Einzelschritt gegen übernommene Konten.

## Wenn etwas schiefgeht

- Schlüssel versehentlich hochgeladen? Sofort Schlüssel löschen und neu erstellen, dann Simon Bescheid geben.
  Ein einmal veröffentlichter Schlüssel gilt als bekannt, das Löschen aus der Historie ist nachrangig.
- Versehentlich etwas Echtes von Teilnehmern hochgeladen? Sofort Simon Bescheid geben, bevor ihr weitermacht.
  Öffentliche Inhalte werden schnell kopiert, deshalb zählt jede Minute.
- Verdacht, dass jemand Fremdes Zugriff hat? Simon informieren, GitHub-Passwort ändern, Sitzungen beenden.
