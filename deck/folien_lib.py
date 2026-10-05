"""Werkzeugkasten zum Umbauen eines fertigen Decks in ein neues Webinar-Deck.

Idee: Man nimmt das letzte fertige Deck (HTML) als Ausgangsstand und ändert gezielt, was sich im neuen
Webinar unterscheidet: Texte, Zahlen, Reihenfolge, neue Folien. Das ist schneller und sicherer, als ein
Deck von Grund auf neu zu bauen, und der Look bleibt automatisch gleich.

    import sys; sys.path.insert(0, "deck")
    from folien_lib import *

    d = Deck("deck/Akquise-Copilot.html")
    d.liste()                                              # zeigt alle Folien mit Nummer
    d.ed("Titel", "Dein Akquise-Copilot:", "Dein Neues Thema:")
    d.notes("Titel", "Das sagen wir hier.")
    d.streichen("Zwei Optionen")
    d.einfuegen_nach("Heute", section("Meine Folie", "Sprechernotiz", "padding:80px;background:#0D0D0D;...", inner))
    d.kuerzel([(1, 10, "A"), (11, 40, "S")])               # Sprecher-Kürzel rechts unten
    d.speichern("webinare/mein-webinar/deck.html")

Jede Textersetzung prüft, ob der alte Text wirklich genau so oft vorkommt wie erwartet. Wenn nicht,
bricht das Programm mit einer verständlichen Meldung ab. So geht nie etwas still schief.
"""
import html as _html
import re
from pathlib import Path

# ---- Farben und Schriften (Design-System, siehe docs/03-design-system.md) -------------------------
MINT, CORAL, GELB = "#7DDBA6", "#E8917A", "#E8C97A"
MONO = "font-family:'Space Mono',monospace;"
BASIS = ("width:100%;height:100%;box-sizing:border-box;color:#F4F2EC;font-family:'Space Grotesk',sans-serif;"
         "position:relative;overflow:hidden;")
CLAUDE_PUNKTE = [(50.0, 3.0), (67.8, 22.2), (89.1, 32.1), (79.7, 54.3), (84.0, 79.5), (59.6, 82.6),
                 (37.6, 92.2), (26.6, 70.3), (4.5, 56.5), (18.2, 35.5), (27.3, 14.7)]

FOLIE = re.compile(r'<div class="slide[^"]*"><section.*?</section></div>', re.S)
KUERZEL = re.compile(r'<div style="position:absolute;right:24px;bottom:16px;z-index:9;[^>]*>[^<]*</div>(?=</section>)')


# ---- kleine HTML-Bausteine -------------------------------------------------------------------------
def csvg(px, strich=6):
    """Claude-Logo als Zeichnung. Große Logos brauchen dünne Striche (z. B. csvg(62, 7))."""
    linien = "".join(f'<line x1="50" y1="50" x2="{x}" y2="{y}"/>' for x, y in CLAUDE_PUNKTE)
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100" fill="none" style="display:block;flex-shrink:0">'
            f'<g stroke="#D97757" stroke-width="{strich}" stroke-linecap="round">{linien}</g></svg>')


def m(t):
    """Text in Mint hervorheben."""
    return f'<span style="color:{MINT}">{t}</span>'


def w(t):
    """Text weiß und halbfett hervorheben."""
    return f'<span style="color:#F4F2EC;font-weight:600">{t}</span>'


def eyebrow(t, farbe=MINT):
    return (f'<div style="{MONO}font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{farbe}">'
            f'{_html.escape(t)}</div>')


def pille(inner, farbe=MINT):
    return (f'<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:16px;background:rgba(125,219,166,.08);'
            f'border:1px solid rgba(125,219,166,.35);border-radius:999px;padding:18px 32px">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{farbe};box-shadow:0 0 12px {farbe}"></span>'
            f'<span style="font-size:26px;font-weight:500">{inner}</span></div>')


def section(label, notiz, stil, inner):
    """Eine komplette neue Folie. `stil` ergänzt das Grundgerüst (Padding, Hintergrund, Layout)."""
    notiz = _html.escape(notiz, quote=True)
    return (f'<div class="slide"><section data-label="{_html.escape(label, quote=True)}" data-speaker-notes="{notiz}" '
            f'style="{BASIS}{stil}">{inner}</section></div>')


# ---- das Deck ---------------------------------------------------------------------------------------
class Deck:
    def __init__(self, datei):
        self.quelle = Path(datei)
        text = self.quelle.read_text(encoding="utf-8")
        treffer = list(FOLIE.finditer(text))
        if not treffer:
            raise SystemExit(f"In {datei} wurden keine Folien gefunden.")
        self.kopf, self.fuss = text[:treffer[0].start()], text[treffer[-1].end():]
        self.folien = [t.group(0) for t in treffer]

    # -- Suchen -----
    @staticmethod
    def _label(x):
        return re.search(r'data-label="([^"]*)"', x).group(1)

    def labels(self):
        return [self._label(x) for x in self.folien]

    def liste(self):
        for n, l in enumerate(self.labels(), 1):
            print(f"{n:3d}  {l}")

    def _index(self, label, k=0):
        treffer = [i for i, l in enumerate(self.labels()) if l == label]
        if not treffer:
            raise SystemExit(f"Folie „{label}“ gibt es nicht. Vorhandene Namen mit d.liste() ansehen.")
        if k >= len(treffer):
            raise SystemExit(f"Folie „{label}“ gibt es nur {len(treffer)}-mal, nicht {k + 1}-mal.")
        return treffer[k]

    # -- Ändern -----
    @staticmethod
    def _muster(text):
        # Zeilenumbrüche und Leerräume zwischen HTML-Tags dürfen abweichen
        return re.escape(text).replace("><", r">\s*<")

    def ed(self, label, alt, neu, k=0, n=1):
        """Text auf einer Folie ersetzen. `n` = wie oft `alt` vorkommen muss (Standard: genau einmal)."""
        i = self._index(label, k)
        ergebnis, anzahl = re.subn(self._muster(alt), lambda _: neu, self.folien[i])
        if anzahl != n:
            raise SystemExit(f"Folie „{label}“: der Text kommt {anzahl}-mal vor, erwartet {n}-mal:\n  {alt[:90]}")
        self.folien[i] = ergebnis

    def notes(self, label, text, k=0):
        i = self._index(label, k)
        text = _html.escape(text, quote=True)
        self.folien[i], anzahl = re.subn(r'data-speaker-notes="[^"]*"', lambda _: f'data-speaker-notes="{text}"',
                                         self.folien[i], count=1)
        if not anzahl:
            raise SystemExit(f"Folie „{label}“ hat keine Sprechernotiz-Stelle.")

    def umbenennen(self, label, neu, k=0):
        i = self._index(label, k)
        self.folien[i] = re.sub(r'data-label="[^"]*"', lambda _: f'data-label="{_html.escape(neu, quote=True)}"',
                                self.folien[i], count=1)

    def streichen(self, label, k=None):
        """Folie entfernen. Ohne `k` werden alle Folien mit diesem Namen entfernt."""
        if k is None:
            idx = [i for i, l in enumerate(self.labels()) if l == label]
            if not idx:
                raise SystemExit(f"Folie „{label}“ gibt es nicht.")
        else:
            idx = [self._index(label, k)]
        for i in reversed(idx):
            del self.folien[i]

    def einfuegen_nach(self, label, folie, k=0):
        self.folien.insert(self._index(label, k) + 1, folie)

    def einfuegen_vor(self, label, folie, k=0):
        self.folien.insert(self._index(label, k), folie)

    def duplizieren(self, label, neues_label=None, k=0):
        """Kopie direkt hinter der Folie. Nützlich für Aufbau in Stufen (jede Kopie zeigt mehr)."""
        kopie = self.folien[self._index(label, k)]
        if neues_label:
            kopie = re.sub(r'data-label="[^"]*"', lambda _: f'data-label="{_html.escape(neues_label, quote=True)}"', kopie, count=1)
        self.folien.insert(self._index(label, k) + 1, kopie)

    def verschieben_nach(self, label, ziel_label, k=0, ziel_k=0):
        folie = self.folien.pop(self._index(label, k))
        self.folien.insert(self._index(ziel_label, ziel_k) + 1, folie)

    def kuerzel(self, bereiche):
        """Sprecher-Kürzel rechts unten auf jede Folie. bereiche = [(von, bis, "A"), (von, bis, "S"), ...]."""
        zuordnung = {}
        for von, bis, wer in bereiche:
            for n in range(von, bis + 1):
                zuordnung[n] = wer
        fehlend = [n for n in range(1, len(self.folien) + 1) if n not in zuordnung]
        if fehlend:
            raise SystemExit(f"Für diese Folien fehlt ein Sprecher-Kürzel: {fehlend[:10]}")
        for n, folie in enumerate(self.folien, 1):
            folie = KUERZEL.sub("", folie)
            marke = (f'<div style="position:absolute;right:24px;bottom:16px;z-index:9;{MONO}font-size:14px;font-weight:700;'
                     f'letter-spacing:.12em;color:rgba(244,242,236,.22)">{zuordnung[n]}</div>')
            ende = folie.rindex("</section>")
            self.folien[n - 1] = folie[:ende] + marke + folie[ende:]

    # -- Speichern -----
    def speichern(self, ziel, titel=None):
        ziel = Path(ziel)
        ziel.parent.mkdir(parents=True, exist_ok=True)
        folien = [re.sub(r'<div class="slide[^"]*">', '<div class="slide">', f, count=1) for f in self.folien]
        folien[0] = folien[0].replace('<div class="slide">', '<div class="slide active">', 1)
        fuss, anzahl = re.subn(r"/ \d+</span>", f"/ {len(folien)}</span>", self.fuss)
        kopf = self.kopf
        if titel:
            kopf = re.sub(r"<title>.*?</title>", lambda _: f"<title>{_html.escape(titel)}</title>", kopf, count=1)
        ziel.write_text(kopf + "\n".join(folien) + fuss, encoding="utf-8")
        print(f"Gespeichert: {ziel}  ({len(folien)} Folien)")
        return ziel
