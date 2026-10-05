# Stufe 3 (Call 17.09.2026 + Simons Feedback 17.09.): Einstieg mit Problem, Proof verteilt, Pitch umgebaut.
# Basis: base_v2.html (= Deck-Stand 15.09.). Schreibt _output/Akquise-Copilot.html.
import re, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / 'Akquise-Copilot.html'
h = (HERE / 'base_v2.html').read_text(encoding='utf-8')
ms = list(re.finditer(r'<div class="slide[^"]*"><section.*?</section></div>', h, re.S))
head, tail = h[:ms[0].start()], h[ms[-1].end():]
S = [x.group(0) for x in ms]
LAB = [re.search(r'data-label="([^"]*)"', s).group(1) for s in S]
assert len(S) == 57, len(S)
used = set()

def I(label, k=0):
    return [i for i, l in enumerate(LAB) if l == label][k]

def T(label, k=0):
    i = I(label, k)
    used.add(i)
    return S[i]

def rx(s):
    return re.escape(s).replace('><', r'>\s*<')

def sub(s, old, new, n=1, where=''):
    s, c = re.subn(rx(old), lambda _: new, s)
    assert c == n, f'{where}: {c}× „{old[:70]}"'
    return s

def ed(label, old, new, k=0, n=1):
    i = I(label, k)
    S[i] = sub(S[i], old, new, n, f'{label}[{k}]')

def setnote(s, text):
    s, c = re.subn(r'data-speaker-notes="[^"]*"', lambda _: f'data-speaker-notes="{text}"', s, count=1)
    assert c == 1
    return s

def notes(label, text, k=0):
    i = I(label, k)
    S[i] = setnote(S[i], text)

def relabel(s, new):
    return re.sub(r'data-label="[^"]*"', f'data-label="{new}"', s, count=1)

PTS = [(50.0, 3.0), (67.8, 22.2), (89.1, 32.1), (79.7, 54.3), (84.0, 79.5), (59.6, 82.6),
       (37.6, 92.2), (26.6, 70.3), (4.5, 56.5), (18.2, 35.5), (27.3, 14.7)]
def csvg(px, sw=6):
    lines = ''.join(f'<line x1="50" y1="50" x2="{x}" y2="{y}"/>' for x, y in PTS)
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100" fill="none" style="display:block;flex-shrink:0">'
            f'<g stroke="#D97757" stroke-width="{sw}" stroke-linecap="round">{lines}</g></svg>')

MINT, CORAL = '#7DDBA6', '#E8917A'
BASE = "width:100%;height:100%;box-sizing:border-box;color:#F4F2EC;font-family:'Space Grotesk',sans-serif;position:relative;overflow:hidden;"
MONO = "font-family:'Space Mono',monospace;"
def m(t): return f'<span style="color:{MINT}">{t}</span>'
def w(t): return f'<span style="color:#F4F2EC;font-weight:600">{t}</span>'
def eyebrow(t, color=MINT):
    return f'<div style="{MONO}font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{color}">{t}</div>'
def section(label, note, style, inner):
    return f'<div class="slide"><section data-label="{label}" data-speaker-notes="{note}" style="{BASE}{style}">{inner}</section></div>'
def pill(inner, color=MINT):
    return (f'<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:16px;background:rgba(125,219,166,.08);border:1px solid rgba(125,219,166,.35);border-radius:999px;padding:18px 32px">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{color};box-shadow:0 0 12px {color}"></span><span style="font-size:26px;font-weight:500">{inner}</span></div>')
import base64
def lade_bilder(*ordner):
    """Lädt alle JPGs aus den Ordnern. Spätere Ordner überschreiben frühere."""
    out = {}
    for o in ordner:
        for k in sorted(o.glob('*.jpg')):
            out[k.stem] = 'data:image/jpeg;base64,' + base64.b64encode(k.read_bytes()).decode()
    return out
# fotos/ und screens/ liegen im Repo (nur Sprecher). referenzen/ ist PRIVAT (gitignored): hier kommen die echten
# Fotos und Screenshots von Teilnehmern hinein. Fehlt ein Bild, erscheint auf der Folie ein sichtbarer Platzhalter.
FOTOS = lade_bilder(HERE / 'fotos', HERE / 'referenzen' / 'fotos')
SHOTS = lade_bilder(HERE / 'screens', HERE / 'referenzen' / 'screens')
BOX = 'data:image/png;base64,' + base64.b64encode((HERE / 'screens' / 'masterclass-box.png').read_bytes()).decode()
def platzhalter_kreis(text, size):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;border:2px dashed #57C98C;background:#10241A;display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;text-align:center;color:{MINT};{MONO}font-size:{max(12, size // 11)}px;letter-spacing:.12em;line-height:1.5">{text}</div>')
def photo(key, size, border=MINT):
    if key not in FOTOS:
        return platzhalter_kreis('FOTO', size)
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;background:url({FOTOS[key]}) center/cover;'
            f'border:3px solid {border};box-shadow:0 0 60px -18px {border}"></div>')
def shot(key, alt, stil, breite, hoehe):
    """Screenshot einbinden. Ohne Datei in referenzen/screens/ erscheint ein sichtbarer Platzhalter."""
    if key in SHOTS:
        return f'<img src="{SHOTS[key]}" alt="{alt}" style="{stil}">'
    return (f'<div style="width:{breite}px;height:{hoehe}px;flex-shrink:0;box-sizing:border-box;border:2px dashed {CORAL};border-radius:28px;background:#1C1B1A;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px;color:{CORAL};{MONO}font-size:20px;letter-spacing:.14em">'
            f'<span style="font-weight:700">PLATZHALTER</span><span style="color:#B4AFA6">Screenshot hier einsetzen</span></div>')
def foto(name, size):
    key = re.sub(r'[^a-z0-9-]', '', name.lower().replace(' & ', '-'))   # "[Name 2]" → name2, "Maria" → maria
    if key in FOTOS:
        return photo(key, size)
    return platzhalter_kreis(f'FOTO<br>{name.upper()}', size)
def initial(letter, size):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;background:linear-gradient(160deg,#1a4231,#10241A);border:1.5px solid #2A4438;'
            f'display:flex;align-items:center;justify-content:center;font-size:{size // 2}px;font-weight:700;color:{MINT};box-shadow:0 0 90px -20px rgba(125,219,166,.6)">{letter}</div>')
def hebel(t, size=23):
    return (f'<div style="border-top:1px solid #2A2926;padding-top:20px"><div style="{MONO}font-size:13px;letter-spacing:.12em;color:{MINT}">DER HEBEL</div>'
            f'<div style="font-size:{size}px;line-height:1.42;color:#D9D6CF;margin-top:8px">{t}</div></div>')

ZITAT_2 = f'{m("<b>5 neue Kunden in einem Monat</b>")} — weil aus Outreach ein echtes Sales-System wurde.'
ZITAT_3 = f'Du brauchst keinen perfekten Kalender — du brauchst eine Sales-Routine, die auch mit {m("<b>30–60 Minuten am Tag</b>")} funktioniert.'

# ============================================================ NEUE FOLIEN
def warum_jetzt():
    return section('Warum jetzt',
                   'Warum jetzt: KI ist schnelllebig. Wer KI jetzt nicht in seine Akquise holt, bleibt zurück – dein Mitbewerb macht es schon, der Zug rollt. Stillstand heißt: Andere überholen dich. Und im B2B: Jetzt werden die Aufträge für 2027 vergeben. Ein Trainer, der in ein Unternehmen mit 500 Mitarbeitern will, wird jetzt für das ganze nächste Jahr gebucht.',
                   'padding:100px;background:radial-gradient(1000px 620px at 80% 25%, rgba(232,145,122,.09), transparent 55%), #0D0D0D;display:flex;flex-direction:column;justify-content:center',
                   f'{eyebrow("Warum jetzt")}'
                   f'<h2 style="margin:26px 0 0;font-weight:700;letter-spacing:-0.03em;line-height:1;font-size:110px">Der Zug rollt.</h2>'
                   f'<p style="margin:36px 0 0;max-width:1400px;font-size:34px;line-height:1.45;color:#B4AFA6">KI verändert Akquise gerade in Monaten, nicht in Jahren. {w("Dein Mitbewerb baut sich das schon auf.")}</p>'
                   f'<div style="margin:30px 0 0;font-weight:700;letter-spacing:-0.02em;line-height:1.1;font-size:62px;color:{MINT}">Stillstand heißt: Andere überholen dich.</div>'
                   f'<div style="margin-top:52px;display:flex">{pill(f'Und im B2B werden <span style="color:{CORAL};font-weight:700">jetzt die Aufträge für 2027</span> vergeben.', CORAL)}</div>')

def stimmen():
    cards = ''
    for name, tag, quote, heb in [
        ('[Name 2]', 'Neukunden', ZITAT_2, 'Klare Prioritäten und passende nächste Schritte — jede Woche statt nach Gefühl.'),
        ('[Name 3]', 'Alltagstauglich', ZITAT_3, 'Jeden Tag klar, wer dran ist. Deshalb reichen 30–60 Minuten.')]:
        cards += (f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:30px">'
                  f'<div style="display:flex;align-items:center;gap:28px">{foto(name, 150)}<div>'
                  f'<div style="font-size:38px;font-weight:700">{name}</div>'
                  f'<div style="display:inline-block;margin-top:10px;background:rgba(125,219,166,.1);border:1px solid #2A4438;border-radius:999px;padding:6px 14px;{MONO}font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#A9E8C5">{tag}</div></div></div>'
                  f'<div style="flex:1;display:flex;align-items:center;font-size:42px;font-weight:500;letter-spacing:-0.01em;line-height:1.3;color:#EDEBE5"><div>„{quote}“</div></div>{hebel(heb)}</div>')
    return section('Stimmen',
                   'Social Proof nach der Agenda, mit Gesicht: [Name 2] – 5 neue Kunden in einem Monat. [Name 3] – eine Sales-Routine, die mit 30 bis 60 Minuten am Tag funktioniert. [Name 1] kommt später vor der Live-Demo, [Name 2] nochmal nach dem Invest.',
                   'padding:64px 80px;background:#0D0D0D;display:flex;flex-direction:column',
                   f'<div style="display:inline-flex;align-self:flex-start;align-items:center;gap:12px;background:rgba(125,219,166,.1);border:1px solid rgba(125,219,166,.35);border-radius:999px;padding:11px 22px">'
                   f'<span style="width:9px;height:9px;border-radius:50%;background:{MINT}"></span><span style="font-size:17px;font-weight:600;color:#A9E8C5">Über 250 begleitete Kunden · unternehmensathleten × DigiUp</span></div>'
                   f'<h2 style="margin:22px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:54px">Was passiert, wenn Akquise {m("Priorität")} bekommt.</h2>'
                   f'<div style="margin-top:38px;flex:1;display:flex;gap:28px">{cards}</div>')

def case(label, note, eb, question, big, big_sub, quote, name, who, heb, avatar):
    q = f'<h2 style="margin:18px 0 0;font-weight:700;letter-spacing:-0.02em;line-height:1.1;font-size:58px">{question}</h2>' if question else ''
    return section(label, note,
                   'padding:90px 110px;background:radial-gradient(1000px 640px at 80% 50%, rgba(125,219,166,.10), transparent 58%), #0D0D0D;display:flex;align-items:center;gap:90px',
                   f'<div style="flex:1">{eyebrow(eb)}{q}'
                   f'<div style="margin-top:34px;font-size:120px;font-weight:700;letter-spacing:-0.04em;line-height:0.95;color:{MINT}">{big}</div>'
                   f'<div style="margin-top:14px;font-size:34px;font-weight:600">{big_sub}</div>'
                   f'<div style="margin-top:36px;font-size:30px;line-height:1.42;color:#D9D6CF;max-width:1000px">„{quote}“</div>'
                   f'<div style="margin-top:34px;max-width:1000px">{hebel(heb, 24)}</div></div>'
                   f'<div style="flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:22px">{avatar}'
                   f'<div style="text-align:center"><div style="font-size:36px;font-weight:700">{name}</div><div style="font-size:19px;color:#8C8780;margin-top:4px">{who}</div></div></div>')

def proof_name1():
    return case('Proof · [Name 1]',
                'Proof vor der Live-Demo: Jedes gute Follow-up folgt derselben Formel. Wenn du sie anwendest, passiert so etwas wie bei [Name 1]: 7 Termine in 7 Tagen – aus Kontakten, die schon da waren. Der Hebel: nicht mehr alle Kontakte gleich behandelt, Signale priorisiert, konkrete nächste Aktionen.',
                'Wenn du diese Formel anwendest', '', '7 Termine', 'in 7 Tagen',
                'Weil die richtigen Kontakte schon da waren. Wir mussten sie nur sauber aktivieren.',
                '[Name 1]', 'aus vorhandenen Kontakten',
                'Nicht mehr alle Kontakte gleich behandelt: Signale priorisiert, Gesprächskontext sichtbar, konkrete nächste Aktionen.',
                photo('name1', 320))

def proof_name2():
    return case('Proof · [Name 2]',
                'Nach dem Invest: Erinnerst du dich an [Name 2]? 5 neue Kunden in einem Monat. Denkst du, für ihn hat es sich gelohnt? Damit ist klar: Die 4 Projekte aus dem Trichter sind nicht erfunden, sondern praktisch drin. Danach Kalender öffnen.',
                'Erinnerst du dich an [Name 2]?', f'Denkst du, für ihn {m("hat es sich gelohnt?")}',
                '5 neue Kunden', 'in einem Monat',
                'Weil aus Outreach ein echtes Sales-System wurde.',
                '[Name 2]', 'Outreach → Sales-System',
                'Klare Prioritäten und passende nächste Schritte — jede Woche statt nach Gefühl.',
                foto('[Name 2]', 320))

def gruppenchat():
    return section('Proof · Gruppen-Chat',
                   'Und dass 4 Projekte kein Wunschdenken sind, sieht man jede Woche in unseren Umsetzungsbegleitungen: [Zahl] Neukunden im [Monat] – und das schon am [Tag] des Monats.',
                   'padding:90px 110px;background:radial-gradient(1000px 640px at 78% 50%, rgba(125,219,166,.10), transparent 58%), #0D0D0D;display:flex;align-items:center;gap:90px',
                   f'<div style="flex:1">{eyebrow("Aus unseren Umsetzungsbegleitungen")}'
                   f'<h2 style="margin:20px 0 0;font-weight:700;letter-spacing:-0.03em;line-height:1.02;font-size:92px">[Zahl] Neukunden<br>{m("im [Monat].")}</h2>'
                   f'<p style="margin:30px 0 0;font-size:36px;line-height:1.4;color:#B4AFA6">Und das {w("schon am [Tag] des Monats.")} Die 4 Projekte aus dem Trichter sind kein Wunschdenken.</p></div>'
                   f'{shot("gruppe-neukunden", "WhatsApp-Gruppe: Neukunden", "width:720px;flex-shrink:0;border-radius:30px;border:1px solid #34322F;box-shadow:0 40px 90px -30px rgba(0,0,0,.9), 0 0 100px -40px rgba(125,219,166,.5)", 720, 420)}')

def wow_a():
    items = ['Welche Kontakte gerade relevant sind.', 'Warum sie jetzt relevant sind.', 'Was dein nächster sinnvoller Schritt ist.']
    cards = ''.join(
        f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:26px;padding:40px 38px;display:flex;flex-direction:column;gap:22px">'
        f'<div style="{MONO}font-size:54px;font-weight:700;color:{MINT};line-height:1">0{k + 1}</div>'
        f'<div style="font-size:44px;font-weight:700;letter-spacing:-0.02em;line-height:1.15">{t}</div></div>' for k, t in enumerate(items))
    return section('Wow · Stell dir vor',
                   'Stell dir mal vor, du öffnest morgens deinen Akquise-Copiloten und siehst sofort: welche Kontakte gerade relevant sind, warum sie jetzt relevant sind und was dein nächster sinnvoller Schritt ist.',
                   'padding:100px;background:radial-gradient(1100px 680px at 50% 12%, rgba(125,219,166,.12), transparent 58%), #0D0D0D;display:flex;flex-direction:column;justify-content:center',
                   f'{eyebrow("Stell dir mal vor")}'
                   f'<h2 style="margin:18px 0 0;font-weight:700;letter-spacing:-0.02em;line-height:1.1;font-size:66px">Du öffnest morgens deinen Akquise-Copiloten<br>und siehst {m("sofort:")}</h2>'
                   f'<div style="margin-top:56px;display:flex;gap:28px">{cards}</div>')

def wow_b():
    used.add(I('Wow-Moment'))
    return section('Wow · Frage',
                   'Würdest du dich sicherer fühlen, weil deine Pipeline nicht mehr vom Zufall oder deiner Tagesform abhängt? Kurz wirken lassen. Und das war erst der Anfang: Ab hier arbeitet dein Copilot jede Woche mit.',
                   'padding:120px;background:radial-gradient(1100px 680px at 50% 40%, rgba(125,219,166,.13), transparent 60%), #0D0D0D;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center',
                   f'<h2 style="margin:0;font-weight:700;letter-spacing:-0.03em;line-height:1.12;font-size:78px;max-width:1500px">Würdest du dich {m("sicherer")} fühlen, weil deine Pipeline nicht mehr vom Zufall oder deiner Tagesform abhängt?</h2>'
                   f'<div style="margin-top:60px;display:inline-flex;align-items:center;gap:14px;background:rgba(125,219,166,.08);border:1px solid #2A4438;border-radius:999px;padding:16px 32px">'
                   f'<span style="font-size:22px;color:#B4AFA6">Und das war erst der Anfang.</span><span style="font-size:22px;color:{MINT};font-weight:700">Ab hier arbeitet dein Copilot jede Woche mit →</span></div>')

PCOL = {1: MINT, 2: CORAL, 3: '#E8C97A', 4: '#E8A46E', 5: '#8FB3D9'}
PICKS = [
    dict(n='Sandra Huber', r='GF · Huber Consulting', p=1, temp='HEISS', short='antwortet nach 5 Monaten',
         trig='Antwortet auf deine Nachricht von vor 5 Monaten', ctx='März: Teamentwicklung besprochen, Budget erst im Q4',
         nxt='Call-Termin vorschlagen', nshort='Call vorschlagen',
         msg='Hey Sandra, schön von dir zu hören! Im März war Q4 euer Zeitpunkt fürs Team-Thema — passt ein kurzer Call diese Woche?'),
    dict(n='Thomas Weiß', r='HR-Leiter · Weiß Logistik', p=2, temp='HEISS', short='Angebot 2× geöffnet',
         trig='Hat dein Angebot 2× geöffnet, aber nie entschieden', ctx='Führungskräfte-Training, seit 3 Wochen offen',
         nxt='Offene Frage klären — nicht drängen', nshort='Frage klären',
         msg='Hey Thomas, das Angebot liegt noch bei euch — gibt’s eine Frage, die ich dir vorab beantworten kann?'),
    dict(n='Markus Hofer', r='Vertrieb · Hofer Maschinenbau', p=3, temp='WARM', short='kommentiert zum 3. Mal',
         trig='Kommentiert zum 3. Mal deine Beiträge', ctx='Noch kein direktes Gespräch, Thema Führung',
         nxt='Persönliche Nachricht, kein Pitch', nshort='Nachricht, kein Pitch',
         msg='Hey Markus, danke für deine Kommentare — Führung im Vertrieb scheint dich zu beschäftigen. Wie geht ihr das gerade an?'),
    dict(n='Lena Voss', r='Trainerin · Voss Akademie', p=4, temp='WARM', short='Newsletter 3× geöffnet',
         trig='Hat deinen Newsletter 3× geöffnet', ctx='Projekt im Frühjahr im Sand verlaufen',
         nxt='Mehrwert senden', nshort='Mehrwert senden',
         msg='Hey Lena, ich musste an unser Gespräch im Frühjahr denken — hier ein Artikel, der genau euer Thema trifft. Wie steht’s bei euch?'),
    dict(n='Jan Feld', r='HR-Leiter · Feld Logistik', p=5, temp='NEU', short='neu vernetzt',
         trig='Hat deine Vernetzung angenommen', ctx='Post zur Führungskräfte-Entwicklung',
         nxt='Erste Nachricht, kein Pitch', nshort='erste Nachricht',
         msg='Hey Jan, danke fürs Vernetzen! Dein Post zur Führungskräfte-Entwicklung hat mich abgeholt — wie geht ihr das Thema gerade an?'),
]
CONTACTS = [('Sandra Huber', 'GF · Huber Consulting', 'LinkedIn-Chat', 1), ('Petra Lang', 'Beraterin · Lang Consulting', 'E-Mail', 0),
            ('Thomas Weiß', 'HR-Leiter · Weiß Logistik', 'Angebot', 2), ('Markus Hofer', 'Vertrieb · Hofer Maschinenbau', 'Beiträge', 3),
            ('Stefan Brunner', 'GF · Brunner Bau', 'Kalender', 0), ('Lena Voss', 'Trainerin · Voss Akademie', 'Newsletter', 4),
            ('Jan Feld', 'HR-Leiter · Feld Logistik', 'LinkedIn', 5)]

def morgen5():
    used.add(I('Morgen'))
    lines = [f'Du öffnest morgens deinen Akquise-Copiloten und siehst {m("fünf Namen.")}',
             f'Du weißt, {m("warum")} diese Personen gerade relevant sind.',
             f'Du weißt, was der {m("nächste sinnvolle Schritt")} ist.',
             f'Und du hast bereits einen {m("Nachrichtenvorschlag")} in deiner Sprache.']
    L = ''.join(f'<div style="font-size:{62 if k == 0 else 26}px;font-weight:{700 if k == 0 else 500};letter-spacing:{"-0.02em" if k == 0 else "0"};line-height:{1.15 if k == 0 else 1.4};'
                f'color:{"#F4F2EC" if k == 0 else "#B4AFA6"};margin-top:{0 if k == 0 else (40 if k == 1 else 10)}px">{t}</div>' for k, t in enumerate(lines))
    rows = ''.join(
        f'<div style="background:#1C1B1A;border:1px solid #34322F;border-left:4px solid {PCOL[c["p"]]};border-radius:14px;padding:13px 18px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:22px;font-weight:700">{c["n"]}</span>'
        f'<span style="{MONO}font-size:12px;font-weight:700;letter-spacing:.1em;color:{PCOL[c["p"]]}">PRIO {c["p"]}</span></div>'
        f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:8px">'
        f'<span style="background:#262420;border-radius:8px;padding:5px 11px;font-size:15px;color:#D9D6CF">Signal: {c["short"]}</span>'
        f'<span style="background:rgba(125,219,166,.12);border:1px solid #2A4438;border-radius:8px;padding:5px 11px;font-size:15px;color:{MINT}">→ {c["nshort"]}</span></div></div>'
        for c in PICKS)
    card = (f'<div style="width:620px;flex-shrink:0;background:#131312;border:1px solid #2A4438;border-radius:28px;padding:26px;box-shadow:0 0 110px -30px rgba(125,219,166,.6)">'
            f'<div style="display:flex;align-items:center;gap:14px">{csvg(32)}<div><div style="font-size:24px;font-weight:700">Dein Akquise-Copilot</div>'
            f'<div style="{MONO}font-size:13px;color:{MINT};margin-top:2px">DIENSTAG · 08:00 · 5 NAMEN FÜR HEUTE · NACHRICHTEN BEREIT</div></div></div>'
            f'<div style="margin-top:18px;display:flex;flex-direction:column;gap:10px">{rows}</div></div>')
    return section('Morgen', 'Denn stell dir mal vor, du wüsstest ganz genau, wer heute dran ist. Du öffnest morgens deinen Akquise-Copiloten und siehst fünf Namen. Du weißt, warum diese Personen gerade relevant sind, was der nächste sinnvolle Schritt ist, und hast schon einen Nachrichtenvorschlag in deiner Sprache.',
                   'padding:90px 100px;background:radial-gradient(1000px 700px at 82% 50%, rgba(125,219,166,.10), transparent 60%), #0D0D0D;display:flex;align-items:center;gap:80px',
                   f'<div style="flex:1">{eyebrow("Stell dir vor")}<div style="margin-top:30px">{L}</div></div>{card}')

def contact_list(marked):
    rows = ''
    for n, r, src, p in CONTACTS:
        if marked and p:
            c = PCOL[p]
            box = f'background:rgba(125,219,166,.05);border:1px solid {c}55;border-left:4px solid {c}'
            badge = (f'<span style="margin-left:auto;width:32px;height:32px;border-radius:50%;background:{c};color:#141312;{MONO}font-size:15px;font-weight:700;'
                     f'display:flex;align-items:center;justify-content:center;flex-shrink:0">{p}</span>')
            op = ''
        elif marked:
            box, op = 'background:#100F0E;border:1px dashed #2A2926', 'opacity:.45;'
            badge = f'<span style="margin-left:auto;{MONO}font-size:11px;letter-spacing:.08em;color:#8C8780;white-space:nowrap">HEUTE NICHT</span>'
        else:
            box, op = 'background:#131312;border:1px solid #34322F', ''
            badge = f'<span style="margin-left:auto;{MONO}font-size:12px;color:#6B665F;white-space:nowrap">{src}</span>'
        rows += (f'<div style="{op}{box};border-radius:14px;padding:13px 18px;display:flex;align-items:center;gap:12px">'
                 f'<div style="min-width:0"><div style="font-size:20px;font-weight:700">{n}</div>'
                 f'<div style="font-size:14px;color:#8C8780;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{r}</div></div>{badge}</div>')
    rows += (f'<div style="border:1px dashed #34322F;border-radius:14px;padding:13px 18px;text-align:center;{MONO}font-size:13px;letter-spacing:.08em;color:#8C8780">+ 120 WEITERE KONTAKTE</div>')
    return (f'<div style="width:380px;flex-shrink:0;display:flex;flex-direction:column;gap:10px">'
            f'<div style="{MONO}font-size:14px;letter-spacing:.12em;color:#8C8780">DEINE KONTAKTE · 127</div>{rows}</div>')

def pick_row(c):
    col = PCOL[c['p']]
    lab = lambda t: f'<div style="{MONO}font-size:11px;letter-spacing:.12em;color:#8C8780">{t}</div>'
    return (f'<div style="display:grid;grid-template-columns:270px 1fr 230px 1.3fr;gap:22px;align-items:center;background:#131312;border:1px solid #34322F;border-left:5px solid {col};border-radius:18px;padding:16px 22px">'
            f'<div><div style="{MONO}font-size:12px;font-weight:700;letter-spacing:.1em;color:{col}">PRIO {c["p"]} · {c["temp"]}</div>'
            f'<div style="font-size:24px;font-weight:700;margin-top:4px">{c["n"]}</div><div style="font-size:14px;color:#8C8780">{c["r"]}</div></div>'
            f'<div>{lab("AUSLÖSER · KONTEXT")}<div style="font-size:18px;line-height:1.3;margin-top:4px">{c["trig"]}</div>'
            f'<div style="font-size:14px;line-height:1.3;margin-top:3px;color:#8C8780">{c["ctx"]}</div></div>'
            f'<div>{lab("NÄCHSTER SCHRITT")}<div style="font-size:18px;line-height:1.3;margin-top:4px;color:{MINT};font-weight:600">{c["nxt"]}</div></div>'
            f'<div style="background:#10241A;border:1px solid #2A4438;border-radius:12px;padding:10px 14px;font-size:15px;line-height:1.4">„{c["msg"]}“</div></div>')

def mini_demo5(marked):
    used.add(I('Mini-Demo', 1 if marked else 0))
    if marked:
        h2 = f'Über 100 Kontakte. {m("Fünf sind heute dran.")}'
        right = f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:12px">{"".join(pick_row(c) for c in PICKS)}</div>'
        note = 'Aus über 100 Kontakten markiert der Copilot fünf – aus ganz unterschiedlichen Signalen: Sandra antwortet auf eine alte Nachricht, Thomas hat ein Angebot gesehen, aber nie entschieden, Markus kommentiert wiederholt, Lena öffnet deinen Newsletter, Jan ist neu vernetzt. Für jede Person: Auslöser, Kontext, nächster Schritt und ein Nachrichtenvorschlag.'
    else:
        h2 = f'Über 100 Kontakte. <span style="color:#8C8780">Wer ist heute dran?</span>'
        right = (f'<div style="flex:1;border:1.5px dashed #34322F;border-radius:24px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;text-align:center;padding:40px">'
                 f'<div style="width:150px;height:150px;border-radius:50%;background:linear-gradient(160deg,#1a4231,#10241A);border:1.5px solid {MINT};display:flex;align-items:center;justify-content:center;box-shadow:0 0 90px -16px rgba(125,219,166,.7)">{csvg(64, 19)}</div>'
                 f'<div style="font-size:44px;font-weight:700;letter-spacing:-0.02em">Welche fünf sind heute dran — {m("und warum?")}</div>'
                 f'<div style="font-size:24px;color:#8C8780;max-width:820px;line-height:1.45">Der Copilot prüft Signale, Gesprächskontext und offene Angebote aus allen Kanälen.</div></div>')
        note = 'Mini-Demo: Du hast über 100 Kontakte. Für dich sehen alle gleich aus. Wer ist heute dran – und warum? Nächste Folie: was der Copilot daraus macht.'
    return section('Mini-Demo', note, 'padding:56px 64px;background:#0D0D0D;display:flex;flex-direction:column',
                   f'<div style="display:flex;align-items:center;gap:12px">{csvg(24)}<span style="{MONO}font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{MINT}">Mini-Demo · Dein Akquise-Copilot · Dienstag, 08:00</span></div>'
                   f'<h2 style="margin:12px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:54px">{h2}</h2>'
                   f'<div style="margin-top:26px;flex:1;display:flex;gap:28px;align-items:stretch">{contact_list(marked)}{right}</div>')

def stufen(s, markers, n):
    """n Stufen; markers = Liste von (html_start, ab_stufe). Element wird unsichtbar, solange stufe < ab_stufe."""
    out = []
    for k in range(1, n + 1):
        x = s
        for mk, ab in markers:
            if k < ab:
                assert x.count(mk) >= 1, mk[:60]
                x = x.replace(mk, mk.replace('<div style="', '<div style="visibility:hidden;', 1), 1)
        out.append(x)
    return out

def div_start(x, text):
    i = x.index(text); j = x.rfind('<div style="', 0, i)
    return x[j:j + 200]

def stimmen_stufen():
    s = stimmen()
    card = '<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:30px">'
    i = s.index(card, s.index(card) + 1)
    first, second = s[:i], s[i:]
    return [first + second.replace(card, card.replace('<div style="', '<div style="visibility:hidden;', 1), 1), s]

def methode_stufen():
    s = T('Follow-up statt Content')
    card = '<div style="background:#1C1B1A;border:1px solid #34322F;border-radius:24px;padding:36px 34px;display:flex;flex-direction:column;gap:22px">'
    pill_ = '<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:16px;background:rgba(125,219,166,.08)'
    assert s.count(card) == 3 and s.count(pill_) == 1, (s.count(card), s.count(pill_))
    parts = s.split(card)
    out = []
    for k in range(1, 4):
        x = parts[0] + ''.join((card if j <= k else card.replace('<div style="', '<div style="visibility:hidden;', 1)) + parts[j] for j in range(1, 4))
        if k < 3:
            x = x.replace(pill_, pill_.replace('<div style="', '<div style="visibility:hidden;', 1))
        out.append(x)
    return out

def arten_stufen():
    s = T('Arten von Follow-ups')
    aktiv = '<div style="background:linear-gradient(150deg,#10241A,#152C20);border:1.5px solid #7DDBA6;border-radius:26px'
    return stufen(s, [(aktiv, 2), (div_start(s, 'Die Wahl triffst du'), 2), (div_start(s, 'Praxis-Tipp'), 2)], 2)

def optionen_stufen():
    s = optionen()
    return stufen(s, [('<div style="background:linear-gradient(160deg,#10241A,#152C20)', 2), ('<div style="margin-top:40px;font-size:42px', 2)], 2)

def stimmen_umsetzung():
    def card(key, name, tag, big, small):
        return (f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:26px">'
                f'<div style="display:flex;align-items:center;gap:26px">{photo(key, 150)}<div><div style="font-size:38px;font-weight:700">{name}</div>'
                f'<div style="display:inline-block;margin-top:10px;background:rgba(125,219,166,.1);border:1px solid #2A4438;border-radius:999px;padding:6px 14px;{MONO}font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#A9E8C5">{tag}</div></div></div>'
                f'<div style="flex:1;display:flex;align-items:center;font-size:36px;font-weight:500;letter-spacing:-0.01em;line-height:1.3;color:#EDEBE5"><div>„{big}“</div></div>'
                f'<div style="border-top:1px solid #2A2926;padding-top:18px;font-size:21px;line-height:1.45;color:#B4AFA6">{small}</div></div>')
    return section('Stimmen · [Name 4] & [Name 5]',
                   'Zwei Stimmen aus unserer Umsetzungsbegleitung: [Name 5] dachte, für Technik bräuchte sie jemanden für locker 10.000 Euro im Monat – heute kann sie, was sie braucht, selbst. Und die Erkenntnis von beiden: Das Produkt ist egal, der Fahrplan ist bei uns allen der gleiche. [Name 4]: Ihr seid für uns der Fokusgeber.',
                   'padding:64px 80px;background:#0D0D0D;display:flex;flex-direction:column',
                   f'{eyebrow("Stimmen aus der Umsetzungsbegleitung")}'
                   f'<h2 style="margin:14px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:56px">„Der Fahrplan ist bei uns {m("allen der gleiche.")}“</h2>'
                   f'<div style="margin-top:36px;flex:1;display:flex;gap:28px">'
                   + card('name5', '[Name 5]', 'Coachin', f'Ich kann das jetzt alles selbst. {m("Ich bin kein Profi, aber das, was ich brauche, das kann ich.")}',
                          'Vorher: „Für alles mit Technik brauche ich jemanden, der mir das abnimmt. Für locker 10.000 Euro im Monat.“')
                   + card('name4', '[Name 4]', 'Umsetzungsbegleitung', f'Ihr seid für uns {m("der Fokusgeber.")} Und das ist genau das, was ich auch brauche.',
                          '„Am Ende ist das Produkt völlig egal. Der Fahrplan ist bei uns allen der gleiche.“')
                   + '</div>')

def masterclass():
    return section('Bonus 2 · Masterclass',
                   'Bonus 2 ausführlich: die LinkedIn-Masterclass „30 Tage zum LinkedIn-Athleten“ – die komplette Akquise-Bibliothek mit Videos und Workbooks, sofort freigeschaltet.',
                   'padding:80px 120px;background:radial-gradient(1000px 700px at 28% 50%, rgba(232,145,122,.13), transparent 60%), #0D0D0D;display:flex;align-items:center;gap:110px',
                   f'<img src="{BOX}" alt="Box: 30 Tage zum LinkedIn-Athleten" style="height:820px;flex-shrink:0;filter:drop-shadow(0 50px 70px rgba(0,0,0,.75))">'
                   f'<div style="flex:1">{eyebrow("Bonus 2 · LinkedIn-Masterclass", CORAL)}'
                   f'<h2 style="margin:20px 0 0;font-weight:700;letter-spacing:-0.03em;line-height:1.02;font-size:92px">30 Tage zum<br><span style="color:{CORAL}">LinkedIn-Athleten.</span></h2>'
                   f'<p style="margin:34px 0 0;font-size:36px;line-height:1.4;color:#B4AFA6">Die komplette Akquise-Bibliothek: {w("Videos + Workbooks")}, sofort freigeschaltet.</p></div>')

def zielgruppe():
    ok = ['Experte, Trainer, Coach oder Berater mit einem funktionierenden Angebot bist',
          'bereits selbstständig bist, aber noch keine stabilen 15.000 Euro Monatsumsatz erreichst',
          'bereits Kontakte oder frühere Gespräche hast, aus denen du konsequenter qualifizierte Gespräche entwickeln willst',
          'Selbstbestimmung, Impact und Wachstum wichtiger findest als Status',
          '2026 auf ein persönliches, KI-gestütztes Akquise-System setzen und regelmäßig umsetzen willst']
    no = ['noch kein klares Angebot und keine definierte Zielgruppe hast',
          'auf automatische Kunden ohne eigene Gespräche hoffst',
          'den nächsten Copy-Paste- oder Schnell-reich-Knopf suchst',
          'wahllos Massen-Nachrichten verschicken willst',
          'nicht bereit bist, Kontakte konsequent zu priorisieren, nachzufassen und das System regelmäßig zu nutzen']
    def col(title, items, good):
        c = MINT if good else CORAL
        box = (f'background:linear-gradient(160deg,#10241A,#132A1F);border:1.5px solid {MINT}' if good
               else 'background:linear-gradient(160deg,#241512,#1A1613);border:1.5px solid #5A3A30')
        lis = ''.join(f'<div style="display:flex;gap:18px;align-items:flex-start">'
                      f'<span style="flex-shrink:0;width:38px;height:38px;border-radius:50%;background:{"rgba(125,219,166,.16)" if good else "rgba(232,145,122,.16)"};color:{c};'
                      f'display:flex;align-items:center;justify-content:center;font-size:21px;font-weight:700;margin-top:1px">{"✓" if good else "✕"}</span>'
                      f'<span style="font-size:29px;line-height:1.34;color:#EDEBE5">{t}</span></div>' for t in items)
        return (f'<div style="flex:1;{box};border-radius:28px;padding:40px 44px;display:flex;flex-direction:column;justify-content:space-between;gap:18px">'
                f'<div style="{MONO}font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:{c};font-weight:700">{title}</div>{lis}</div>')
    return section('Für wen das ist',
                   'Alex: Für wen das ist und für wen nicht. Für Experten, Trainer, Coaches und Berater mit funktionierendem Angebot, die noch nicht stabil bei 15.000 Euro Monatsumsatz sind und aus bestehenden Kontakten konsequent Gespräche machen wollen. Nicht für alle, die auf automatische Kunden, Copy-Paste oder Massen-Nachrichten hoffen.',
                   'padding:60px 76px;background:#0D0D0D;display:flex;flex-direction:column',
                   f'{eyebrow("Bevor wir starten")}'
                   f'<h2 style="margin:12px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:58px">Für wen das ist — {m("und für wen nicht.")}</h2>'
                   f'<div style="margin-top:34px;flex:1;display:flex;gap:28px">'
                   + col('Das ist für dich, wenn du', ok, True) + col('Das ist nichts für dich, wenn du', no, False) + '</div>')

def live_gast():
    return section('Live-Stimme · [Name 4]',
                   'Direkt vor dem Pitch: [Name 4] live dazuholen (hat zugesagt). Sie erzählt in 2–3 Minuten, was sich bei ihr verändert hat.',
                   'padding:90px;background:radial-gradient(900px 640px at 50% 40%, rgba(125,219,166,.12), transparent 60%), #0D0D0D;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center',
                   f'<div style="display:inline-flex;align-items:center;gap:12px;padding:13px 26px;border-radius:999px;background:{CORAL};color:#3A1B12;{MONO}font-size:15px;font-weight:700;letter-spacing:.16em;text-transform:uppercase">'
                   f'<span style="width:9px;height:9px;border-radius:50%;background:#3A1B12;animation:mintPulse 1.4s infinite"></span>Live zugeschaltet</div>'
                   f'<div style="margin-top:44px">{foto("[Name 4]", 320)}</div>'
                   f'<h2 style="margin:36px 0 0;font-weight:700;letter-spacing:-0.03em;font-size:96px;line-height:1">[Name 4]</h2>'
                   f'<p style="margin:18px 0 0;font-size:32px;color:#B4AFA6">Teilnehmerin — erzählt live, {w("was sich bei ihr verändert hat.")}</p>')

def optionen():
    def card(tag, title, items, good):
        c = MINT if good else CORAL
        box = (f'background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid {MINT};box-shadow:0 0 80px -26px rgba(125,219,166,.6)'
               if good else 'background:#1C1B1A;border:1px solid #34322F')
        lis = ''.join(f'<div style="display:flex;gap:16px;align-items:flex-start"><span style="color:{c};font-weight:700;font-size:28px;line-height:1.2">{"✓" if good else "✕"}</span>'
                      f'<span style="font-size:34px;line-height:1.35;color:{"#F4F2EC" if good else "#B4AFA6"}">{t}</span></div>' for t in items)
        return (f'<div style="{box};border-radius:28px;padding:50px 52px;display:flex;flex-direction:column;justify-content:center;gap:30px">'
                f'<div style="{MONO}font-size:16px;letter-spacing:.16em;color:{c};font-weight:700">{tag}</div>'
                f'<div style="font-size:48px;font-weight:700;letter-spacing:-0.02em;margin-bottom:8px">{title}</div>{lis}</div>')
    return section('Zwei Optionen',
                   'Pitch-Einstieg: Wir könnten dich jetzt allein lassen – du hast gesehen, was der Copilot kann und welche Schritte es braucht. Du hast zwei Optionen. Option 1: Du setzt weiterhin alles auf eigene Faust um. Den Copiloten baust du nebenbei, Stück für Stück – realistisch brauchst du dafür mehrere Monate. Option 2: Wir setzen es gemeinsam um – mit jahrelanger Akquise-Erfahrung, in 90 Tagen. Die Frage ist nur: allein ausprobieren oder auf dieser Erfahrung aufbauen?',
                   'padding:80px 90px;background:#0D0D0D;display:flex;flex-direction:column',
                   f'{eyebrow("Du hast jetzt zwei Optionen")}'
                   f'<h2 style="margin:14px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:66px">Wir könnten dich jetzt {m("allein lassen.")}</h2>'
                   f'<div style="margin-top:44px;flex:1;display:grid;grid-template-columns:1fr 1fr;gap:30px">'
                   + card('OPTION 1', 'Du machst es allein.', ['Du setzt weiterhin alles auf eigene Faust um.', 'Den Copiloten baust du nebenbei — Stück für Stück.', 'Realistisch brauchst du dafür mehrere Monate.'], False)
                   + card('OPTION 2', 'Wir setzen es gemeinsam um.', ['Jahrelange Erfahrung in der Akquise gebündelt.', 'Wir bauen deinen Copiloten mit dir.', 'Jede Woche ein Call, bis er läuft.', 'In 90 Tagen ist er im Einsatz.'], True)
                   + f'</div><div style="margin-top:40px;font-size:42px;font-weight:700;letter-spacing:-0.02em">Die Frage ist nur: Allein ausprobieren — oder auf {m("jahrelange Akquise-Erfahrung")} aufbauen?</div>')

def plus20():
    s = relabel(NETZ_ORIG, 'Mehrwert · 20 %')
    s = setnote(s, 'Gleiche Folie wie eben, jetzt mit dem Mehrwert des Systems: Statt 3 Prozent hast du mit dem Copiloten 20 Prozent deiner Kontakte im Blick. Bei 1.000 Kontakten sind das 200 Menschen, die du erreichst, statt 30 – mit Signal und nächstem Schritt.')
    s = sub(s, 'Die Signale sind da. <span style="color:#7DDBA6">Du siehst sie nur nicht.</span>',
            'Mit deinem Copiloten: <span style="color:#7DDBA6">20 % im Blick.</span>', where='plus20')
    s = sub(s, '>3 %</div>', '><span style="font-size:46px;color:#6B665F;text-decoration:line-through;margin-right:16px">3 %</span>20 %</div>', where='plus20')
    s = sub(s, '>97 %</div>', '>200</div>', where='plus20')
    s = sub(s, 'der Signale gehen unter.', 'erreichte Menschen — statt 30.', where='plus20')
    return s

def hub():
    wishes = [('Dein Kalender füllt sich', 'statt Leerlauf zwischen den Projekten'),
              ('Neukunden aus Kontakten, die du schon hast', 'statt ständig neue Leads zu jagen'),
              ('Planbarer Umsatz', 'statt Monaten, die ungefähr gleich bleiben'),
              ('Jeden Tag klar, wer dran ist', 'statt alles im Kopf zu behalten'),
              ('Akquise läuft weiter, auch im Projektstress', 'statt Funkstille, wenn du ausgebucht bist'),
              ('Nachrichten, die nach dir klingen', 'statt Rätselraten, was du schreibst')]
    CX, CY, YS = 960, 630, [390, 630, 870]
    pos = [(80, y) for y in YS] + [(1360, y) for y in YS]
    lines = ''.join(f'<line x1="{CX}" y1="{CY}" x2="{x + (480 if x < CX else 0)}" y2="{y}" stroke="#2A4438" stroke-width="3" stroke-dasharray="8 10"/>' for x, y in pos)
    cards = ''.join(
        f'<div style="position:absolute;left:{x}px;top:{y - 70}px;width:480px;height:140px;box-sizing:border-box;background:#131312;border:1px solid #2A4438;border-radius:22px;padding:22px 28px;display:flex;align-items:center;gap:18px">'
        f'<span style="width:44px;height:44px;border-radius:50%;background:rgba(125,219,166,.14);color:{MINT};display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;flex-shrink:0">✓</span>'
        f'<div><div style="font-size:27px;font-weight:700;line-height:1.2">{t}</div><div style="font-size:18px;color:#8C8780;margin-top:5px">{d}</div></div></div>'
        for (t, d), (x, y) in zip(wishes, pos))
    rings = ''.join(
        f'<div style="position:absolute;left:{CX - r}px;top:{CY - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;border:{bw}px {st} {col}"></div>'
        for r, bw, st, col in [(330, 1, 'dashed', '#2A4438'), (282, 2, 'solid', 'rgba(125,219,166,.22)')])
    import math
    dots = ''
    for ang, r, c, sz in [(-58, 330, MINT, 16), (22, 330, CORAL, 14), (128, 330, '#E8C97A', 14), (200, 330, MINT, 12),
                          (-128, 282, CORAL, 12), (70, 282, MINT, 14), (160, 282, '#E8C97A', 10), (-12, 282, MINT, 10)]:
        x, y = CX + r * math.cos(math.radians(ang)), CY + r * math.sin(math.radians(ang))
        dots += (f'<div style="position:absolute;left:{x - sz / 2:.0f}px;top:{y - sz / 2:.0f}px;width:{sz}px;height:{sz}px;border-radius:50%;'
                 f'background:{c};box-shadow:0 0 14px {c}"></div>')
    circle = (f'{rings}{dots}'
              f'<div style="position:absolute;left:{CX - 230}px;top:{CY - 230}px;width:460px;height:460px;border-radius:50%;'
              f'background:radial-gradient(circle at 50% 30%,#23543D 0%,#123022 45%,#0B1A13 100%);border:2px solid {MINT};'
              f'box-shadow:0 0 0 14px rgba(125,219,166,.06), 0 0 150px -20px rgba(125,219,166,.75);'
              f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
              f'<div style="width:96px;height:96px;border-radius:26px;background:#F0EEE6;display:flex;align-items:center;justify-content:center;'
              f'box-shadow:0 12px 30px -10px rgba(0,0,0,.6)">{csvg(62, 7)}</div>'
              f'<div style="margin-top:26px;{MONO}font-size:15px;letter-spacing:.2em;color:{MINT}">DEIN</div>'
              f'<div style="margin-top:4px;font-size:52px;font-weight:700;letter-spacing:-0.03em;line-height:1">Akquise-<br>Copilot</div>'
              f'<div style="margin-top:22px;display:inline-flex;align-items:center;gap:8px;background:rgba(13,13,13,.55);border:1px solid #2A4438;border-radius:999px;padding:8px 16px;'
              f'{MONO}font-size:13px;letter-spacing:.12em;color:#A9E8C5"><span style="width:8px;height:8px;border-radius:50%;background:{MINT}"></span>90 TAGE · LÄUFT AUF CLAUDE</div></div>')
    return section('Ergebnis · Copilot',
                   'Was du wirklich kaufst, sind Ergebnisse: In 90 Tagen 4 zusätzliche Projekte aus Kontakten, die du schon hast – im B2C 10.000, im B2B 20.000 Euro. Dafür bauen wir mit dir deinen Akquise-Copiloten – damit dein Kalender sich füllt, du Neukunden aus Kontakten gewinnst, die du schon hast, und dein Umsatz planbar wird. Jeden Tag klar, wer dran ist, auch im Projektstress, mit Nachrichten, die nach dir klingen. Wie wir dorthin kommen: Monat für Monat.',
                   'padding:60px 80px;background:radial-gradient(900px 700px at 50% 56%, rgba(125,219,166,.10), transparent 60%), #0D0D0D',
                   f'<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">{lines}</svg>'
                   f'<div style="position:relative;text-align:center">{eyebrow("Dein Ergebnis")}'
                   f'<h2 style="margin:12px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:58px">In 90 Tagen: {m("4 zusätzliche Projekte")} aus deinen Kontakten.</h2>'
                   f'<div style="margin-top:12px;font-size:26px;color:#B4AFA6">= {w("10.000 € im B2C")} · {w("20.000 € im B2B")} — dafür bauen wir mit dir deinen Akquise-Copiloten.</div></div>'
                   f'{circle}{cards}')

def erinnerung(label, k, eb_old, eb_new, note):
    i = I(label, k)
    s = relabel(S[i], f'{label} · Erinnerung')
    s = setnote(s, note)
    s = sub(s, 'Konservativ gerechnet — Erfahrungswerte, keine Bestwerte.</div>',
            'Konservativ gerechnet — Erfahrungswerte, keine Bestwerte.</div>'
            f'<div style="margin-top:18px;white-space:nowrap;font-size:26px;font-weight:600;color:#F4F2EC">Im B2B sogar {m("20.000 €")} '
            '<span style="font-size:19px;font-weight:400;color:#8C8780">· 4 × 5.000 €</span></div>', where='Erinnerung B2B')
    return sub(s, eb_old, eb_new, where=f'{label} Erinnerung')

def kalender():
    s = relabel(T('Buch deinen Platz'), 'Kalender offen')
    used.discard(I('Buch deinen Platz'))
    s = setnote(s, 'Erstes Mal QR-Code, direkt nach Invest, Trichter-Erinnerung und [Name 2] – noch vor den Boni: Ab sofort ist unser Kalender offen. Wir nehmen nicht jeden. Du kennst den Deal, das ist kein Verkaufsgespräch mehr – wir klären nur, ob es wirklich für dich passt. Danach kommen die Boni.')
    s = sub(s, 'font-size:104px">Buch dir<br>deinen <span style="color:#7DDBA6">Platz.</span>',
            'font-size:92px">Unser Kalender<br>ist ab <span style="color:#7DDBA6">jetzt offen.</span>', where='Kalender')
    s = sub(s, '>Start im Oktober</div>', '>Wir nehmen nicht jeden.</div>', where='Kalender')
    s = sub(s, 'Dein <span style="color:#7DDBA6">Akquise-Copilot</span> · 90 Tage',
            'Du kennst den Deal — im Gespräch klären wir nur, <span style="color:#7DDBA6">ob es für dich passt.</span>', where='Kalender')
    s = sub(s, 'font-size:22px;color:#B4AFA6">Du kennst', 'font-size:22px;line-height:1.5;color:#B4AFA6">Du kennst', where='Kalender')
    return s

def extras():
    items = [('Onboarding-Videokurs', 'Claude-Basics zum Selbst-Durcharbeiten, in deinem Tempo.', False),
             ('5 Copilot-Skills', 'Fertig eingerichtet in Claude — zum Sofort-Nutzen.', False),
]
    cards = ''.join(
        f'<div style="background:#1C1B1A;border:1px solid #34322F;border-radius:22px;padding:30px 32px;display:flex;flex-direction:column;justify-content:center;gap:10px">'
        f'<div style="display:flex;align-items:center;justify-content:space-between"><span style="font-size:38px;font-weight:700;color:{CORAL};line-height:1">+</span>'
        + (f'<span style="{MONO}font-size:12px;letter-spacing:.14em;color:#3A1B12;background:{CORAL};border-radius:6px;padding:4px 10px">PLATZHALTER</span>' if ph else '')
        + f'</div><div style="font-size:42px;font-weight:700;letter-spacing:-0.01em">{t}</div><div style="font-size:26px;color:#B4AFA6;line-height:1.4">{d}</div></div>'
        for t, d, ph in items)
    box = (f'<div style="width:560px;flex-shrink:0;height:560px;transform:rotate(-4deg);background:linear-gradient(150deg,#2A1814,#141312 70%);border:2px solid {CORAL};border-radius:30px;'
           f'box-shadow:24px 30px 0 -6px #1F1512, 0 0 110px -30px rgba(232,145,122,.8);padding:40px;display:flex;flex-direction:column;justify-content:space-between">'
           f'<div style="{MONO}font-size:15px;letter-spacing:.16em;color:{CORAL}">NEUE MASTERCLASS · LAUNCH IM HERBST</div>'
           f'<div style="align-self:center;transform:rotate(-8deg);border:6px solid {CORAL};border-radius:14px;padding:14px 28px;white-space:nowrap;font-size:58px;font-weight:700;letter-spacing:.08em;color:{CORAL}">TOP SECRET</div>'
           f'<div style="font-size:26px;line-height:1.4;color:#EDEBE5">Du bekommst sie schon jetzt — {w("vor allen anderen.")}</div></div>')
    return section('Boni · Noch nicht alles',
                   'Und das ist noch nicht alles: Wir arbeiten gerade an einer neuen Masterclass, die erst im Herbst gelauncht wird – Top Secret, aber du bekommst sie jetzt schon dazu. Dazu Onboarding-Videokurs und die 5 Copilot-Skills.',
                   'padding:70px 90px;background:radial-gradient(1000px 640px at 20% 60%, rgba(232,145,122,.10), transparent 58%), #0D0D0D;display:flex;flex-direction:column',
                   f'{eyebrow("Und das ist noch nicht alles", CORAL)}'
                   f'<h2 style="margin:14px 0 0;font-weight:700;letter-spacing:-0.02em;font-size:62px">Das kommt noch <span style="color:{CORAL}">obendrauf.</span></h2>'
                   f'<div style="margin-top:36px;flex:1;display:flex;align-items:center;gap:70px">{box}'
                   f'<div style="flex:1;display:grid;grid-template-columns:1fr;grid-auto-rows:230px;gap:26px">{cards}</div></div>')

def zwischenfazit():
    s = T('Zwischenfazit')
    marker = '<div style="display:flex;align-items:center;gap:16px">'
    hidden = marker.replace('gap:16px">', 'gap:16px;visibility:hidden">')
    parts = s.split(marker)
    assert len(parts) == 4, len(parts)
    row = parts[1][:parts[1].index('</div>') + 6]
    rest = parts[3][parts[3].index('</div>') + 6:]
    hl = lambda t: f'<span style="color:{MINT};font-weight:600">{t}</span>'
    texts = [f'Du hast {hl("gesehen")}, wer gerade relevant ist — erkannt aus Signalen in allen Kanälen.',
             f'Zu jedem Namen stand {hl("warum")}: Auslöser und Gesprächskontext auf einen Blick.',
             f'Der {hl("nächste sinnvolle Schritt")} war schon vorbereitet — samt Nachricht in deiner Sprache.',
             f'Auch für {hl("neue Kontakte")} liegt die erste Nachricht bereit — mit echtem Anlass statt Pitch.',
             f'Und jeden Montag {hl("aktualisiert")} sich deine Liste von selbst.']
    rows = []
    for t in texts:
        r, c = re.subn(r'(<span style="font-size:25px[^"]*">).*(</span></div>)$', lambda mm: mm.group(1) + t + mm.group(2), row, flags=re.S)
        assert c == 1
        rows.append(r)
    out = []
    for k in range(7):
        x = parts[0] + ''.join((marker if j <= k else hidden) + r for j, r in enumerate(rows, 1)) + rest
        if k < 6:
            x = sub(x, 'margin-top:46px;align-self:flex-start', 'margin-top:46px;visibility:hidden;align-self:flex-start', where='Zwischenfazit')
        out.append(x)
    return out

def drei_fragen_stufen():
    s = T('Drei Fragen')
    card = '<div style="background:#131312;border:1px solid #34322F;border-radius:26px;padding:40px 38px;display:flex;flex-direction:column">'
    line = '<div style="margin-top:36px;font-size:28px;color:#8C8780">'
    assert s.count(card) == 3 and s.count(line) == 1
    parts = s.split(card)
    out = []
    for k in range(3):
        x = parts[0] + ''.join((card if j <= k + 1 else card.replace('flex-direction:column">', 'flex-direction:column;visibility:hidden">')) + parts[j] for j in range(1, 4))
        if k < 2:
            x = x.replace(line, line.replace('color:#8C8780">', 'color:#8C8780;visibility:hidden">'))
        out.append(x)
    return out

# ============================================================ BESTEHENDE FOLIEN
notes('Dein Netzwerk', 'Direkt nach dem Problem: Frage in den Chat – wie viele Kontakte habt ihr auf LinkedIn? Die meisten haben 600 bis 1.500. Im Schnitt 1.000 – aber nur rund 3 Prozent davon hast du im Blick. 97 Prozent der Signale gehen unter.')

ed('Kontaktchaos', 'Heute liegen diese Informationen verteilt — in LinkedIn, alten Chats, E-Mails und deinem Kopf. ',
   'Die Infos liegen verteilt — in LinkedIn, alten Chats, E-Mails und deinem Kopf. Du weißt nicht, wer heute dran ist. Also tust du nichts. ')
notes('Kontaktchaos', 'Direkt nach dem Intro das Problem, damit sich die Leute wiederfinden: Du hast viele Kontakte, aber wer davon ist heute dran? Wem schreibst du? Das weißt du nicht – die Infos liegen verteilt in LinkedIn, alten Chats, E-Mails und deinem Kopf. Und weil du es nicht weißt, tust du nichts. Genau deshalb bleibt enorm viel Potenzial liegen.')
notes('Morgen', 'Denn stell dir mal vor, du wüsstest ganz genau: Sandra, Thomas, Markus – das sind die drei, die heute dran sind. Du öffnest morgens deinen Akquise-Copiloten und siehst genau diese drei Namen. Du weißt, warum, was der nächste Schritt ist, und hast schon einen Nachrichtenvorschlag.')

EXTRA_ROW = (f'<div style="border:1px dashed #34322F;border-radius:14px;padding:16px 20px;text-align:center;{MONO}font-size:14px;letter-spacing:.08em;color:#8C8780">+ 122 WEITERE KONTAKTE</div>')
for k in (0, 1):
    ed('Mini-Demo', 'Fünf Kontakte.', 'Über 100 Kontakte.', k)
    ed('Mini-Demo', 'DEINE KONTAKTE · 5', 'DEINE KONTAKTE · 127', k)
    ed('Mini-Demo', '</div><div style="flex:1;', f'{EXTRA_ROW}</div><div style="flex:1;', k)
notes('Mini-Demo', 'Mini-Demo: Du hast über 100 Kontakte. Für dich sehen alle gleich aus. Wer ist heute dran – und warum? Nächste Folie: was der Copilot daraus macht.', 0)
notes('Mini-Demo', 'Aus über 100 Kontakten markiert der Copilot drei – aus drei ganz unterschiedlichen Signalen: Sandra antwortet auf eine alte Nachricht, Thomas hat ein Angebot gesehen, aber nie entschieden, Markus interagiert wiederholt mit deinen Inhalten. Für jede Person: Auslöser, Priorität, Gesprächskontext, nächster Touchpoint und ein Nachrichtenvorschlag.', 1)

i = I('Ergebnisse')
ed('Ergebnisse', 'color:#7DDBA6;margin-top:8px">17.000 €</div>',
   f'color:#7DDBA6;margin-top:8px"><span style="display:block;font-size:34px;letter-spacing:0;color:#B4AFA6;margin-bottom:6px">über</span>XX.000 €</div>')
ed('Ergebnisse', '>Umsatz über den Funnel</div>', '>Umsatz in einem Monat</div>')
ed('Ergebnisse', 'font-size:54px">Kein einzelner Hack.', 'font-size:54px">Kein einzelner Hack.')
S[i] = S[i].replace('</section>', (
    f'<div style="margin-top:34px;align-self:flex-start;display:flex;align-items:center;gap:32px">'
    f'{shot("umsatz-push", "Push-Nachricht: Umsatz letzter Monat", "height:170px;border-radius:85px;box-shadow:0 24px 60px -24px rgba(0,0,0,.9)", 560, 170)}'
    f'<span style="font-size:26px;line-height:1.4;color:#B4AFA6;max-width:520px">Direkt vom Handy: {w("[Betrag] Umsatz im letzten Monat.")}</span></div></section>'))
notes('Ergebnisse', 'Proof am Ende von Kapitel 1: [Name 6] – aus Webinar, Follow-up und klarer Angebotslogik wurde eine echte Sales-Strecke. [Betrag] Umsatz in einem Monat – dazu den Screenshot zeigen. Kein einzelner Hack, ein System.')

notes('Follow-up-Framework', 'Die Methode: Jede gute Nachricht folgt derselben Formel – anknüpfen, echten Mehrwert bringen, mit einem weichen CTA schließen. Und wenn du diese Formel anwendest, passiert so etwas wie bei [Name 1] – das zeigen wir nach Schritt 4.')

for k in range(3):
    ed('Das System', 'In 90 Tagen — gemeinsam gebaut', 'So kommst du dorthin', k)
    notes('Das System', f'So kommst du dorthin – Monat für Monat. Monat {k + 1} wird eingeblendet. Monat 1: Fundament und Konfiguration. Monat 2: Signale und Priorisierung. Monat 3: Routine und Skalieren.', k)

ed('Dein Preis', 'data-label="Dein Preis"', 'data-label="Dein Invest"')
ed('Dein Preis', '>Dein Preis</div>', '>Dein Invest</div>')
notes('Dein Preis', 'Dein Invest – nie vom Preis sprechen: 5.500 Euro statt 8.900 am Markt. Schon 2 bis 3 zusätzliche Projekte tragen die kompletten 90 Tage. Voraussetzung: ein bestehendes Angebot. Nur 5 Plätze.')
notes('Dein Ablauf', 'Simon übernimmt: So laufen deine 90 Tage Woche für Woche ab. Zum Start Onboarding-Call 1:1 und Videokurs. Alle 2 Wochen baust du mit Simon am Copiloten weiter – 6 Bau-Calls. Jede Woche Outreach- und Follow-up-Call mit Alex oder Michi. Einmal im Monat ein Technik-Q&amp;A.')
ed('So arbeitet der Copilot', 'padding:11px 24px"><svg width="26" height="26"', 'padding:18px 40px;gap:20px"><svg width="46" height="46"')
ed('So arbeitet der Copilot', '<span style="font-weight:700;font-size:21px">Dein Akquise-Copilot</span>', '<span style="font-weight:700;font-size:36px">Dein Akquise-Copilot</span>')
ed('So arbeitet der Copilot', "font-size:13px;color:#7DDBA6\">läuft auf Claude", "font-size:22px;color:#7DDBA6\">läuft auf Claude")
ed('So arbeitet der Copilot', 'margin-bottom:34px', 'margin-bottom:46px')

for k in range(5):
    S[I('Boni', k)] = S[I('Boni', k)].replace('Boni nach dem Preis', 'Boni nach Invest, Trichter-Erinnerung, [Name 2] und geöffnetem Kalender – jeden Bonus ausführlich erzählen')

# ============================================================ REIHENFOLGE
CMAP = [('#7DDBA6', '#E8917A'), ('#57C98C', '#D97757'), ('#A9E8C5', '#F2C3B4'), ('#EAF7F0', '#F7E7E1'), ('#10241A', '#2A1814'),
        ('#152C20', '#33201A'), ('#163024', '#3A2019'), ('#1a4231', '#3E241D'), ('#2A4438', '#5A3A30'), ('#3C6B52', '#7A4A3C'),
        ('#4E9670', '#C97A62'), ('#2E5A45', '#6B3E31'), ('#3E6B54', '#8A5343'), ('rgba(125,219,166,', 'rgba(232,145,122,')]
def terra(x, protect=()):
    for n, p in enumerate(protect):
        x = x.replace(p, f'@@SCHUTZ{n}@@')
    for a, b in CMAP:
        x = x.replace(a, b)
    for n, p in enumerate(protect):
        x = x.replace(f'@@SCHUTZ{n}@@', p)
    return x
def segment(x, start, end):
    i = x.index(start); j = x.index(end, i)
    return x[:i], x[i:j], x[j:]

# 1) Live-Demo-Teil (Copilot-Schritte 01–04) in Terracotta; Status-Skala „SUPER HEISS" bleibt, wie sie ist
for lab in ('Schritt 1 · Liste', 'Schritt 2 · Scoring', 'Schritt 4 · Automation'):
    i = I(lab)
    x, prot = S[i], []
    for mm in re.finditer('SUPER HEISS', x):
        if lab.startswith('Schritt 4'):
            a = x.rfind('<div style="height:98px', 0, mm.start()); b = x.find('<div style="height:98px', mm.start())
        else:
            a = x.rfind('<div', 0, mm.start()); b = x.find('</div>', mm.start()) + 6
        prot.append(x[a:b])
    S[i] = terra(x, prot)

# 2) 97 % auf der Netzwerk-Folie in Terracotta (die 20-%-Folie bleibt grün)
NETZ_ORIG = S[I('Dein Netzwerk')]
a_, mid, b_ = segment(NETZ_ORIG, 'background:linear-gradient(150deg, #10241A, #163024)', 'der Signale gehen unter.')
S[I('Dein Netzwerk')] = a_ + terra(mid) + b_
netzwerk_reprise = setnote(relabel(S[I('Dein Netzwerk')], 'Dein Netzwerk · Heute 30'),
                           'Erinnere dich an die Folie vom Anfang: 1.000 Kontakte, davon hast du 3 Prozent im Blick. Das sind 30 Menschen, die du wirklich erreichst – 97 Prozent gehen unter. Nächste Folie: mit dem Copiloten schrauben wir das auf 200 hoch.')
netzwerk_reprise = sub(netzwerk_reprise, 'Die Signale sind da. <span style="color:#7DDBA6">Du siehst sie nur nicht.</span>',
                       'Heute: <span style="color:#E8917A">3 % im Blick.</span>', where='Reprise')
netzwerk_reprise = sub(netzwerk_reprise, '>97 %</div>', '>30</div>', where='Reprise')
netzwerk_reprise = sub(netzwerk_reprise, 'color:#7DDBA6">3 %</div>', 'color:#E8917A">3 %</div>', where='Reprise')
netzwerk_reprise = sub(netzwerk_reprise, 'der Signale gehen unter.', 'erreichte Menschen — 97 % gehen unter.', where='Reprise')

# 4) Fotos: Über uns + [Name 6]
i = I('Vorstellung')
hdr = '<div style="display:flex;align-items:center;gap:28px">'
assert S[i].count(hdr) == 2
S[i] = S[i].replace(hdr, hdr + photo('alex', 170, '#57C98C'), 1)
k = S[i].rfind(hdr); S[i] = S[i][:k] + hdr + photo('simon', 170, '#57C98C') + S[i][k + len(hdr):]
i = I('Ergebnisse')
S[i], c = re.subn(r'<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient\(160deg,#1a4231,#10241A\);border:1px solid #2A4438;display:flex;align-items:center;justify-content:center;flex-shrink:0"><svg.*?</svg></div>',
                  lambda _: photo('name6', 120), S[i], count=1, flags=re.S)
assert c == 1

# 5) Wow-Folie: neuer Haupttext, Schlusssatz bleibt
i = I('Wow-Moment')
S[i], c1 = re.subn(r'<div style="font-size:104px[^"]*">Ist das nicht<br>unglaublich\?</div>', lambda _: (
    '<div style="font-size:48px;font-weight:600;letter-spacing:-0.02em;line-height:1.32;color:#F4F2EC;max-width:1500px">Stell dir mal vor, du öffnest morgens deinen Akquise-Copiloten '
    'und siehst sofort, welche Kontakte gerade relevant sind, warum sie jetzt relevant sind und was dein nächster sinnvoller Schritt ist.</div>'), S[i])
S[i], c2 = re.subn(r'<div style="margin-top:30px;font-size:32px[^"]*">Das läuft.*?</div>', lambda _: (
    '<div style="margin-top:48px;font-size:54px;font-weight:700;letter-spacing:-0.02em;line-height:1.2;color:#7DDBA6;max-width:1500px">Würdest du dich sicherer fühlen, weil deine Pipeline nicht mehr vom Zufall oder deiner Tagesform abhängt?</div>'), S[i], flags=re.S)
assert c1 == 1 and c2 == 1
S[i] = setnote(S[i], 'Stell dir mal vor, du öffnest morgens deinen Akquise-Copiloten und siehst sofort, welche Kontakte gerade relevant sind, warum sie jetzt relevant sind und was dein nächster sinnvoller Schritt ist. Würdest du dich sicherer fühlen, weil deine Pipeline nicht mehr vom Zufall oder deiner Tagesform abhängt? Und das war erst der Anfang: Ab hier arbeitet dein Copilot jede Woche mit.')

# Titel: Live-Demo-Pille in Akzentfarbe
i = I('Titel')
S[i], c = re.subn(r'<div style="display:inline-flex;align-self:flex-start;align-items:center;gap:16px;padding:15px 26px;border-radius:999px;border:1px solid rgba\(125,219,166,\.35\);background:rgba\(125,219,166,\.06\);color:#A9E8C5;font-size:22px;font-weight:600;letter-spacing:\.02em">\s*<span style="width:4px;height:26px;border-radius:2px;background:#7DDBA6"></span>Inkl\. Live-Demo in Claude\s*</div>',
                  lambda _: f'<div style="display:inline-flex;align-self:flex-start;align-items:center;gap:14px;padding:15px 28px;border-radius:999px;background:{CORAL};color:#3A1B12;{MONO}font-size:18px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;box-shadow:0 0 34px -8px rgba(232,145,122,.7)"><span style="width:10px;height:10px;border-radius:50%;background:#3A1B12"></span>Inkl. Live-Demo in Claude</div>', S[i])
assert c == 1

# Kontaktchaos: erdrückend statt übersichtlich
CHIPS = [('LINKEDIN-CHAT', '„Melde mich im Q4 wieder.“', 10, 0, -4, 1), ('E-MAIL', 'Angebot Führungskräfte-Training · 2× geöffnet', 400, 30, 3, 1),
         ('LINKEDIN', '14 neue Profilbesuche', 190, 110, -2, .55), ('NOTIZ-APP', '„Sandra anrufen!!!“', 520, 160, 5, 1),
         ('LINKEDIN', 'Markus hat deinen Beitrag kommentiert', 0, 215, 2, 1), ('CRM', 'Follow-up überfällig · seit 23 Tagen', 300, 285, -3, .8),
         ('KALENDER', 'Kennenlern-Call mit Lena · März', 540, 330, -6, 1), ('DEIN KOPF', '„Wem wollte ich nochmal schreiben?“', 40, 380, 4, .85),
         ('LINKEDIN', '38 ungelesene Nachrichten', 390, 435, 2, 1), ('WHATSAPP', '„Schick mir gern mal Infos!“', 0, 500, -3, 1),
         ('E-MAIL', '„Re: Re: Angebot – kurze Rückfrage“', 250, 550, 6, .7), ('DEIN KOPF', '„Thomas wollte doch noch …?“', 520, 600, -2, 1),
         ('VISITENKARTEN', 'Messe Linz · 17 Karten, nie abgetippt', 70, 650, 3, 1), ('WHATSAPP', 'Sprachnachricht · 2:14 · ungehört', 380, 700, -4, .9),
         ('EXCEL-LISTE', '342 Zeilen · zuletzt gepflegt im Juni', 10, 770, -1, .75), ('E-MAIL', 'Newsletter · 3× geöffnet von Jan', 430, 790, 2, .8)]
chips = ''.join(
    f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg);opacity:{op};max-width:390px;background:#1C1B1A;border:1px solid {"#5A3A30" if "KOPF" in src or "CRM" in src else "#34322F"};'
    f'border-radius:14px;padding:13px 19px;box-shadow:0 18px 40px -16px rgba(0,0,0,.9)">'
    f'<div style="{MONO}font-size:12px;letter-spacing:.12em;color:{CORAL if "KOPF" in src or "CRM" in src else "#8C8780"}">{src}</div>'
    f'<div style="font-size:19px;margin-top:4px;line-height:1.3;color:#D9D6CF">{t}</div></div>' for src, t, x, y, rot, op in CHIPS)
i = I('Kontaktchaos')
S[i], c = re.subn(r'<div style="position:relative;width:780px;height:740px;flex-shrink:0">.*(?=</section>)',
                  lambda _: f'<div style="position:relative;width:840px;height:870px;flex-shrink:0">{chips}</div>', S[i], flags=re.S)
assert c == 1
S[i] = S[i].replace('padding:80px 90px;background:radial-gradient(900px 700px at 78% 50%, rgba(232,145,122,.07)', 'padding:60px 80px;background:radial-gradient(900px 800px at 76% 50%, rgba(232,145,122,.12)')

# Drei Fragen: Schlüsselwörter in Akzentfarbe
i = I('Drei Fragen')
for kw, rest in [('Wer', ' ist gerade relevant?'), ('Warum', ' ist diese Person relevant?'), ('Was', ' ist mein nächster sinnvoller Schritt?')]:
    S[i] = sub(S[i], f'>{kw}{rest}</div>', f'><div><span style="color:{CORAL}">{kw}</span>{rest}</div></div>', where='Drei Fragen')

# Einwände in Terracotta (Lösung kommt erst danach)
S[I('Warum nicht')] = terra(S[I('Warum nicht')])

# Trichter größer (alle Rechenbeispiel-Stufen)
for k in range(7):
    i = I('Rechenbeispiel', k)
    S[i] = sub(S[i], 'flex:1.1;max-width:660px;display:flex;flex-direction:column;align-items:center;justify-content:center',
               'flex:1.1;max-width:900px;zoom:1.32;display:flex;flex-direction:column;align-items:center;justify-content:center', where='Trichter')

# So kommst du dorthin: Monatskarten größer
for k in range(3):
    i = I('Das System', k)
    S[i] = sub(S[i], 'gap:19px;font-size:22px;color:#C7C3BA;line-height:1.35', 'gap:30px;font-size:31px;color:#C7C3BA;line-height:1.3', n=None or S[i].count('gap:19px;font-size:22px;color:#C7C3BA;line-height:1.35'), where='Monate')
    S[i] = S[i].replace('<div style="font-size:34px;font-weight:700;letter-spacing:-0.015em">', '<div style="font-size:46px;font-weight:700;letter-spacing:-0.02em">')
    S[i] = S[i].replace('font-size:34px;font-weight:700;color:#6B665F', 'font-size:46px;font-weight:700;color:#6B665F')
    S[i] = S[i].replace("letter-spacing:.1em;color:#7DDBA6\">MONAT", "letter-spacing:.1em;color:#7DDBA6;font-size:20px\">MONAT").replace("letter-spacing:.1em;color:#57C98C\">MONAT", "letter-spacing:.1em;color:#57C98C;font-size:20px\">MONAT")

# Boni: Masterclass-Box im Bonus-2-Kärtchen
for k in range(1, 5):
    i = I('Boni', k)
    S[i], c = re.subn(r'<div style="width:46px;height:46px;border-radius:12px;background:rgba\(232,145,122,\.14\);display:flex;align-items:center;justify-content:center"><svg(?:(?!</svg>).)*</svg></div>(\s*<div[^>]*>Bonus 2</div>)',
                      lambda mm: f'<img src="{BOX}" alt="Masterclass-Box" style="height:120px;align-self:flex-start;filter:drop-shadow(0 12px 18px rgba(0,0,0,.6))">' + mm.group(1), S[i], flags=re.S)
    assert c == 1, (k, c)

DF = drei_fragen_stufen()
ZF = zwischenfazit()
order = [
    T('Titel'), T('Kontaktchaos'), T('Dein Netzwerk'), morgen5(),
    mini_demo5(False), mini_demo5(True), *DF, T('Der Unterschied'),
    T('Vorstellung'), T('Heute'), warum_jetzt(), *stimmen_stufen(),
    T('An dir'), T('Warum nicht'), T('Der Copilot'),
    *[T('Rechenbeispiel', k) for k in range(7)], T('Rechenbeispiel B2B'),
    *methode_stufen(), *arten_stufen(), T('Ergebnisse'),
    T('So arbeitet der Copilot'), T('Schritt 1 · Liste'), T('Schritt 2 · Scoring'),
    T('Schritt 3 · Live-Demo'), T('Schritt 3 · Outreach'), T('Brand Voice'), T('Follow-up-Framework'),
    T('Schritt 4 · Automation'), proof_name1(), T('Live-Demo · Copilot'),
    *ZF, wow_a(), wow_b(), T('Touchpoints'), T('Zusammenspiel'),
    live_gast(), netzwerk_reprise, plus20(),
    *optionen_stufen(), hub(),
    *[T('Das System', k) for k in range(3)], T('Dein Ablauf'),
    T('Marktvergleich'), T('Dein Preis'),
    erinnerung('Rechenbeispiel', 6, 'Das Rechenbeispiel · B2C', 'Erinnere dich · B2C',
               'Erinnere dich an den Trichter vom Anfang: 1.000 Kontakte, 4 Projekte à 2.500 Euro – im B2C sind das 10.000 Euro. Und im B2B mit denselben 4 Projekten sogar 20.000 Euro, fast das Vierfache deines Invests von 5.500 Euro.'),
    proof_name2(), stimmen_umsetzung(), gruppenchat(), kalender(),
    T('Boni', 0), T('Boni', 1), masterclass(), *[T('Boni', k) for k in range(2, 5)], extras(),
    T('Buch deinen Platz'), T('Live Q&A'),
]
# Sprecher-Kürzel (Call 21.09.): Nummern = Deck-Stand ohne die neue Zielgruppen-Folie
assert len(order) == 79, len(order)
SPRECHER = {}
for a_, b_, who in [(1, 3, 'A'), (4, 6, 'S'), (7, 10, 'A'), (11, 11, 'A/S'), (12, 17, 'A'), (18, 26, 'S'), (27, 32, 'A'),
                    (33, 40, 'S'), (41, 41, 'A'), (42, 42, 'S'), (43, 51, 'A'), (52, 53, 'S'), (54, 54, 'S/A'), (55, 59, 'A'),
                    (60, 63, 'S'), (64, 70, 'A'), (71, 72, 'S'), (73, 73, 'A'), (74, 77, 'S'), (78, 78, 'A'), (79, 79, 'A/S')]:
    for n_ in range(a_, b_ + 1):
        SPRECHER[n_] = who
assert sorted(SPRECHER) == list(range(1, 80))
def kuerzel(x, who):
    tag = (f'<div style="position:absolute;right:24px;bottom:16px;z-index:9;{MONO}font-size:14px;font-weight:700;letter-spacing:.12em;'
           f'color:rgba(244,242,236,.22)">{who}</div></section>')
    i = x.rindex('</section>')
    return x[:i] + tag + x[i + len('</section>'):]
order = [kuerzel(x, SPRECHER[n_]) for n_, x in enumerate(order, 1)]
order.insert(11, kuerzel(zielgruppe(), 'A'))

dropped = sorted(LAB[i] for i in set(range(len(S))) - used - {I('Warum jetzt'), I('Stimmen')})
print('gestrichen:', dropped)

tail, c = re.subn(r'/ \d+</span>', f'/ {len(order)}</span>', tail)
assert c == 1
html = head + '\n'.join(order) + tail
OUT.write_text(html, encoding='utf-8')
for n, l in enumerate(re.findall(r'<section data-label="([^"]*)"', html), 1):
    print(n, l)
