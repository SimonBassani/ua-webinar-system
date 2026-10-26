# Muster für Webinare im UA-Design

Festgelegt beim Webinar „LinkedIn Performance System 2027“ (27.10.2026) im Review mit Michael.
Neue Webinare im UA-Design übernehmen diesen Aufbau. Die fertigen Bausteine stehen im Bauskript
`webinare/2026-10-27-linkedin-performance-system/build.py`. Ein neues UA-Webinar startet am besten
mit einer Kopie dieses Skripts statt mit `vorlagen/neues-webinar-build.py`.

Jedes Webinar läuft in genau einem Design (UA oder Alex-Simon), nie in beiden.

## 1. Einheitlicher Kopf: zwei feste Höhen

Inhaltsfolien werden **nie senkrecht zentriert**. Sonst springt der Kopf von Folie zu Folie, je nachdem wie viel
Inhalt darunter steht. Stattdessen gibt es genau zwei Folientypen mit fester Höhe:

| Typ | Kopfzeile (Eyebrow) | Überschrift | Wofür |
|---|---|---|---|
| **Inhalt** | 88 px | 124 px | Folien mit viel Inhalt: Karten, Listen, Tabellen, Schritte |
| **Aussage** | 219 px | 256 px | Fragen, Umfragen, große Aussagen und Folien mit wenig Inhalt. Maß ist „Unser Versprechen“ (Garantie) |

- Aussage-Folien nie oben ankleben lassen. Das sieht leer und gequetscht aus.
- Folien ohne Kopfzeile: die Überschrift steht trotzdem auf der Höhe ihres Typs.
- Im Skript erledigt das `einheitlicher_kopf()` automatisch. Aussage-Folien stehen in `AUSSAGE_FOLIEN`,
  Folien mit eigenem, freigegebenem Aufbau in `KOPF_AUSNAHMEN` (Deckblatt, Video, Kapitel, Zitate, Referenzen,
  Preisfolien, Kalender offen, Live Q&A). Freigegebene Folien nie nachträglich umstellen.
- Folien mit Bild daneben: Text und Bild oben bündig (`align-items:flex-start`), nicht mittig.
- Lange Überschriften früher umbrechen (`max-width` auf der Überschrift), statt sie über die ganze Breite laufen zu lassen.

## 2. Frage- und Umfragefolien

- Kopfzeile „Frage in den Chat“ oder „Umfrage im Chat“, großes Fragezeichen im Hintergrund.
- Frage- und Umfragefolien sind vom Typ **Aussage** (Kopfzeile bei 219 px).
- Die **Antwortkarten** stehen immer auf derselben Höhe (**600 px** von oben), egal ob die Frage
  zwei oder drei Zeilen hat (`antworten()`, `ANTWORT_OBEN`). Jede Karte mit Nummer, darunter
  „Tippe die Zahl 1–n für deine Antwort in den Chat.“

## 3. Preisfolien (freigegeben)

1. **Marktanker**: Frage in den Chat, was es kostet, keinen Kunden zu gewinnen.
2. **Dein Invest**, zwei Stufen mit identischem Gerüst:
   - Stufe 1: Kopfzeile „Dein Invest bisher“, bisheriger Invest (90 px).
   - Stufe 2: Kopfzeile „Webinar-Special am <Datum>:“, derselbe Betrag an **derselben Stelle** durchgestrichen,
     darunter der neue Invest groß in Türkis, „einmalig“ und die Ratenzahlung.
   - Auf beiden Stufen unten die Kundenfotos mit „250+ Coaches, Berater und B2B-Dienstleister erfolgreich begleitet“.
   - Inhalt 250 px vom linken Rand, wie bei „Kalender offen“.
   - Die Zahl darf beim Weiterklicken nicht springen. Der neue Teil wird nur sichtbar geschaltet.
3. **Garantie** in drei Stufen.
4. **Kalender offen**: Text links, QR-Code rechts (560 px) mit Link darunter, beides als Gruppe mittig.
   „Nur 5 Plätze“ als rote Pille mit weißer Schrift.

## 4. QR-Code

- Ein QR-Code führt auf den Calendly-Link des Strategie-Calls, darunter steht der kurze Webinar-Link.
- Vor dem Einbauen mit einem Lesegerät prüfen, wohin er führt (z. B. `zxing-cpp`).
- Helfer `qr_code(groesse, link=True)`. Oben rechts auf Folien mit Überschrift: `qr_oben()`
  (150 px, rechtsbündig, auf Höhe der Kopfzeile), auf aufeinanderfolgenden Folien an derselben Stelle.
- QR-Code zusätzlich auf: Ergebnis-Folie aus dem Gruppen-Chat, „So geht es weiter für dich“,
  „Buch dir bitte keinen Call, wenn …“, „Code einlösen“ und Live Q&A.

## 5. Live Q&A (freigegeben)

- Pille „Jetzt seid ihr dran“, große Überschrift „Live Q&A“, darunter
  „Stelle deine Fragen jetzt direkt in den Chat oder nutze den Q&A-Button.“
- Rechts der QR-Code (400 px) mit Link. Ränder links und rechts 250 px, wie bei „Kalender offen“.
- Buchungs-Mitteilungen im Apple-Stil ganz rechts oben (310 px breit):
  erste nach 3 s, zweite nach 6 s darunter; die erste geht bei 12 s, die zweite rutscht an ihren Platz
  und geht bei 14 s; eine dritte kommt 5 s später und geht nach gut 2 s.
- Die Mitteilungen sind ein vorbereiteter Effekt, keine echte Buchung. Keine Namen oder Uhrzeiten hineinschreiben.
- Helfer: `mitteilung()`, `kurze_mitteilung()` (eine Mitteilung, steht 2 s). Die Animation startet jedes Mal neu,
  wenn die Folie aufgerufen wird. Im PDF sind Mitteilungen nicht zu sehen.

## 6. Hintergrund und Technik

- Alle Inhaltsfolien haben den dunkelgrünen Verlauf `linear-gradient(120deg,#000000 0%,#0B1F1B 100%)`,
  keine rein schwarzen Folien. Eigene Hintergründe nur für Deckblatt und Video.
- Die Folie darf im Browser nie gestaucht werden (`#deck{flex-shrink:0}`), sonst bricht der Text im Browser
  anders um als im PDF. Immer auch im Browser in einem kleinen Fenster prüfen, nicht nur im PDF.
- Lange Inhalte stufenweise aufbauen: erst die Überschrift, dann Element für Element.
