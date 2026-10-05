# 03 · Design-System

Gilt für alle Decks der Kooperation. Die Farben sind abgestimmt, bitte nicht eigenmächtig ändern.

## Format

1920 × 1080 (16:9), dunkles Theme. Jede Folie ist ein `<section>` innerhalb von
`<div class="slide">`.

## Farben

| Rolle | Hex |
|---|---|
| Hintergrund | `#0D0D0D` |
| Karten dunkel | `#1C1B1A` / `#131312`, Rahmen `#34322F` |
| **Mint** (gut, gelöst, Gewinn, CTA) | `#7DDBA6`, dunkler `#57C98C` |
| Tiefgrün (Verläufe, Glow) | `#10241A` / `#152C20` / `#1a4231` |
| Creme-Karte (hell) | `#F0EEE6`, Text `#141413` |
| Text gedämpft | `#B4AFA6` / `#8C8780` / `#6B665F` |
| **Terracotta** (Problem, Dringlichkeit, live) | `#E8917A` |
| Claude-Logo | `#D97757` |

**Die wichtigste Farbregel:** Mint heißt „gelöst“, Terracotta heißt „Problem“. Deshalb stehen die
Einwände in Terracotta und die Lösung in Mint. Und deshalb ist die 97-%-Folie terracotta, die
20-%-Folie aber grün.

**Temperatur-Skala** (durchgängig für Lead-Status):
KALT `#6E8BA6` → LAUWARM `#E8C97A` → WARM `#E8A46E` → HEISS `#E8917A` → SUPER HEISS `#7DDBA6`.

## Schriften

- **Space Grotesk** — Überschriften und Fließtext (700 für Headlines, 400–600 im Text).
- **Space Mono** — Eyebrows, Labels, Zeitangaben, Preise. Großbuchstaben, Laufweite `.16em`.
- **Newsreader** — nur dekorativ für große Anführungszeichen.

Alle drei über Google Fonts eingebunden. Beim ersten Öffnen ohne Internet greift die
Systemschrift — für die Präsentation vorher einmal mit Internet öffnen.

## Logos

- **unternehmensathleten-Wortmarke** ([assets/logos](../assets/logos/)) — oben links auf Titel- und
  CTA-Folie, bündig zur Überschrift. Kleinschreibung gehört zur Marke.
- **× DigiUp** als Sekundärmarke oben rechts.
- **DigiUp-Wortmarke:** Auf dunklem Hintergrund die Datei `wortmarke-digiup-dunkel.png` verwenden. Der Name ist
  irreführend, gemeint ist „für dunklen Hintergrund“ (weißes „Digi“, grünes „Up“). Die Datei
  `wortmarke-digiup-hell.png` ist für helle Flächen: Auf dem dunklen Deck oder Banner ist „Digi“ darin kaum
  zu erkennen.
- **Claude-Logo** wird als SVG im Code erzeugt, nie als PNG eingefügt. Die Funktion `csvg()` in
  `build3.py` zeichnet die elf Strahlen. Dünne Striche bei großen Logos, sonst wird es ein Klecks.
- Trust-Zeile: „250+ Kunden Erfahrung · unternehmensathleten × DigiUp“.

## Aufbau einer Folie

1. **Eyebrow** — Space Mono, klein, Großbuchstaben, Mint.
2. **Überschrift** — groß, fett, **ein** Wort oder Satzteil farbig hervorgehoben.
3. **Inhalt** — Karten, Grafiken, Zahlen. Keine nackten Aufzählungen.
4. Optional eine **Pille** unten als Merksatz.
5. Rechts unten das **Sprecher-Kürzel**.

Fertige Code-Bausteine dafür: [../vorlagen/folien-bausteine.md](../vorlagen/folien-bausteine.md).

## Gestaltungsregeln (hart gelernt)

- **Wenig Leerraum.** Karten füllen ihre Höhe, Inhalt wird zentriert oder verteilt. Große Löcher
  unter dem Text wirken unfertig.
- **Grafiken statt Listen.** Ein Trichter, ein Diagramm, echte Oberflächen. Keine vier Kästchen
  mit 1, 2, 3, 4.
- **Ein Durchlauf, eine Leserichtung.** Von links (Problem) nach rechts (Ergebnis). Nicht zwei
  konkurrierende Endpunkte auf einer Folie.
- **Text auf Folien ist kurz.** Wenn eine Folie nach Textwüste aussieht, wird sie geteilt:
  oben die Aussage, darunter die Aufzählung als Karten — oder zwei Folien.
- **Zahlen groß.** 30 gegen 200, 10.000 € gegen 20.000 €. Die Zahl ist das Argument.
- **Fotos sind Pflicht** bei jeder Referenz. Rund, mit farbigem Rand.
- **Stufenweiser Aufbau** statt voller Folie: dieselbe Folie mehrfach, jeweils ein Element mehr.

## Was nicht funktioniert hat

- Helle Hintergründe oder Farbwechsel „zur Abwechslung“.
- Metaphern statt echter Systemdarstellung.
- Schatten mit weichem Verlauf im Vektor-PDF (siehe [04-build-anleitung.md](04-build-anleitung.md)).
- Das Claude-Logo als dicker Strich-Klecks in großen Kreisen.
