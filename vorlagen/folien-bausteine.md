# Folien-Bausteine

Fertige Code-Stücke im Deck-Look. Farben und Schriften wie im Design-System.
In `build3.py` stehen diese Bausteine als Funktionen bereit (`eyebrow()`, `pill()`, `photo()`,
`csvg()`, `section()`), hier die Bausteine zum Nachschlagen.

## Grundgerüst einer Folie

```html
<div class="slide"><section data-label="Kurzname" data-speaker-notes="Was gesagt wird."
  style="width:100%;height:100%;box-sizing:border-box;color:#F4F2EC;font-family:'Space Grotesk',sans-serif;
         position:relative;overflow:hidden;padding:80px;background:#0D0D0D;display:flex;flex-direction:column">
  <!-- Inhalt -->
</section></div>
```

## Eyebrow und Überschrift

```html
<div style="font-family:'Space Mono',monospace;font-size:15px;letter-spacing:.16em;
            text-transform:uppercase;color:#7DDBA6">Das Problem heute</div>
<h2 style="margin:14px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:62px">
  Deine Kontakte liegen nicht brach — <span style="color:#7DDBA6">du siehst sie nur nicht.</span>
</h2>
```

Regel: genau **ein** farbiger Satzteil pro Überschrift.

## Karte

```html
<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:26px;
            padding:40px 38px;display:flex;flex-direction:column;gap:20px">
  <div style="font-family:'Space Mono',monospace;font-size:14px;letter-spacing:.14em;color:#8C8780">GRUND 01</div>
  <div style="font-size:30px;font-weight:600;line-height:1.3">Dein Netzwerk kennt dich schon.</div>
</div>
```

Hervorgehobene Karte (Lösung, Gewinn):

```html
style="background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid #7DDBA6;
       box-shadow:0 0 80px -26px rgba(125,219,166,.6)"
```

Problem-Karte (Einwand, Dringlichkeit): dieselbe Struktur mit `#241512` / `#E8917A`.

## Merksatz-Pille

```html
<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:16px;
            background:rgba(125,219,166,.08);border:1px solid rgba(125,219,166,.35);
            border-radius:999px;padding:18px 32px">
  <span style="width:10px;height:10px;border-radius:50%;background:#7DDBA6;box-shadow:0 0 12px #7DDBA6"></span>
  <span style="font-size:26px;font-weight:500">Du entscheidest und schickst ab — der Copilot bereitet vor.</span>
</div>
```

## Live-Badge

```html
<div style="display:inline-flex;align-items:center;gap:10px;padding:13px 26px;border-radius:999px;
            background:#E8917A;color:#3A1B12;font-family:'Space Mono',monospace;font-size:15px;
            font-weight:700;letter-spacing:.16em;text-transform:uppercase">
  <span style="width:9px;height:9px;border-radius:50%;background:#3A1B12;animation:mintPulse 1.4s infinite"></span>Live-Demo
</div>
```

## Große Zahl

```html
<div style="font-size:150px;font-weight:700;letter-spacing:-0.04em;line-height:0.9;color:#7DDBA6">200</div>
<div style="margin-top:18px;font-size:27px;color:#B4AFA6">erreichte Menschen — statt 30.</div>
```

## Porträt mit Rand

```html
<div style="width:150px;height:150px;border-radius:50%;flex-shrink:0;
            background:url(DATEI) center/cover;border:3px solid #7DDBA6;
            box-shadow:0 0 60px -18px #7DDBA6"></div>
```

In `build3.py`: `photo('maria', 150)` nimmt die Datei `deck/referenzen/fotos/maria.jpg`. Fehlt sie, erscheint ein
sichtbarer Platzhalter statt eines Fotos. Der Ordner `deck/referenzen/` ist privat und wird nie hochgeladen.

## Sprecher-Kürzel (gehört auf jede Folie)

```html
<div style="position:absolute;right:24px;bottom:16px;z-index:9;font-family:'Space Mono',monospace;
            font-size:14px;font-weight:700;letter-spacing:.12em;color:rgba(244,242,236,.22)">A</div>
```

## Stufenweiser Aufbau

Dieselbe Folie mehrfach in die Reihenfolge aufnehmen und die noch nicht gezeigten Teile
unsichtbar schalten — die Elemente behalten ihren Platz, es springt nichts:

```html
<div style="visibility:hidden;display:flex;...">…</div>
```

In `build3.py` machen das die Funktionen `stufen()`, `methode_stufen()`, `zwischenfazit()`.

## Claude-Logo

Nie als Bild einfügen, sondern zeichnen lassen: `csvg(px, strichstaerke)`.
Faustregel: großes Logo braucht dünne Striche (`csvg(62, 7)`), kleines darf kräftiger sein
(`csvg(24)`).
