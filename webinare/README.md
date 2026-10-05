# Webinare

Hier liegt pro Webinar ein eigener Ordner mit allem, was dazugehört. So kommt sich niemand in die Quere.

```
webinare/
  2026-11-12-linkedin-sales/
    build.py        ← Bauskript für das Deck (aus vorlagen/neues-webinar-build.py)
    deck.html       ← fertiges Deck zum Präsentieren
    deck.pdf        ← PDF zum Verschicken
    banner.json     ← Konfiguration fürs Banner
    banner/         ← fertiges Banner (png, jpg)
```

Ordnername: `<Datum>-<Kurzname>`, alles klein, mit Bindestrichen.

Das Webinar vom 22.09.2026 („Dein Akquise-Copilot“) ist das Referenz-Webinar und liegt im Ordner
[`../deck/`](../deck/). Neue Webinare starten von dort aus.

So legt man ein neues Webinar an: in Claude Code **„Wir machen ein neues Webinar zu <Thema>“** sagen. Der
Skill `webinar-deck` führt durch alles, das Banner baut der Skill `webinar-banner`.
