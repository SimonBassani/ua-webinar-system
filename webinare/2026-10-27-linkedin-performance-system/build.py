"""Deck „In 90 Tagen qualifizierte Termine im Kalender“ · LinkedIn Performance System 2027 · 27.10.2026

Rohfassung nach folienplan.md (gleicher Ordner). Ausgangsstand ist das Referenz-Deck; übernommen werden
Titel, „Kalender offen“ und „Live Q&A“ (Logos, Look). Alle anderen Folien sind neu, weil Copilot und
Live-Demo von Simon in diesem Webinar wegfallen.

Gelbe gestrichelte Kästen mit „OFFEN“ = Material fehlt oder ist nicht entschieden. Vor dem Webinar
müssen alle verschwunden sein. Echte Kundennamen und Zahlen stehen nur lokal in deck/referenzen/.

    uv run python webinare/2026-10-27-linkedin-performance-system/build.py
"""
import base64
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

WURZEL = next(p for p in Path(__file__).resolve().parents if (p / "deck" / "folien_lib.py").exists())
sys.path.insert(0, str(WURZEL / "deck"))
from folien_lib import *  # noqa: E402,F401,F403

AUSGANG = WURZEL / "deck" / "Akquise-Copilot.html"
PRIVAT = os.environ.get("LPS_PRIVAT") == "1"
ZIEL = (WURZEL / "deck" / "referenzen" / "lps-2026-10-27" / "deck.html") if PRIVAT else Path(__file__).resolve().parent / "deck.html"

d = Deck(AUSGANG)
alt = {l: d.folien[d._index(l)] for l in ("Titel", "Für wen das ist", "Kalender offen", "Live Q&A")}
alt_deck = d

# ---- Bausteine für dieses Deck ----------------------------------------------------------------------
STIL = "padding:88px 96px;background:#0D0D0D;display:flex;flex-direction:column"
STIL_MITTE = STIL + ";justify-content:center"
GRUEN = "padding:88px 96px;background:linear-gradient(120deg,#0D0D0D 0%,#10241A 100%);display:flex;flex-direction:column;justify-content:center"
FOTOS = WURZEL / "deck" / "fotos"
REFERENZEN = WURZEL / "deck" / "referenzen" / "fotos"


def c(t):
    """Text in Terracotta (Problem, Dringlichkeit)."""
    return f'<span style="color:{CORAL}">{t}</span>'


def h2(t, size=72, top=18):
    return (f'<h2 style="margin:{top}px 0 0;font-weight:700;letter-spacing:-0.025em;line-height:1.05;'
            f'font-size:{size}px">{t}</h2>')


def sub(t, size=30, top=28):
    return f'<p style="margin:{top}px 0 0;font-size:{size}px;line-height:1.45;color:#B4AFA6;max-width:1500px">{t}</p>'


def offen(t, flex="0 0 auto", size=22):
    """Sichtbarer Platzhalter für fehlendes Material."""
    return (f'<div style="flex:{flex};border:2px dashed {GELB};border-radius:22px;padding:22px 28px;'
            f'background:rgba(232,201,122,.06);display:flex;align-items:center;gap:14px;{MONO}font-size:{size}px;'
            f'line-height:1.4;color:{GELB}"><span style="font-weight:700;letter-spacing:.12em">OFFEN</span>'
            f'<span style="color:#E9DDB8">{t}</span></div>')


def karte(titel, text="", art="neutral", label="", sichtbar=True, size=44):
    rahmen = {"neutral": "background:#131312;border:1px solid #34322F",
              "mint": f"background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid {MINT};box-shadow:0 0 80px -30px rgba(125,219,166,.6)",
              "coral": f"background:linear-gradient(160deg,#241512,#2B1915);border:1.5px solid {CORAL}"}[art]
    farbe = {"neutral": "#8C8780", "mint": MINT, "coral": CORAL}[art]
    kopf = f'<div style="{MONO}font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:{farbe}">{label}</div>' if label else ""
    unten = f'<div class="karte-text" style="font-size:31px;line-height:1.45;color:#B4AFA6">{text}</div>' if text else ""
    vis = "" if sichtbar else "visibility:hidden;"
    # Inhalt oben ausgerichtet: Labels, Titel und Texte stehen in jeder Karte einer Reihe auf derselben Linie
    return (f'<div class="karte karte-{art}" style="{vis}flex:1;{rahmen};border-radius:26px;padding:44px 38px;display:flex;flex-direction:column;'
            f'justify-content:flex-start;gap:18px">{kopf}<div style="font-size:{size}px;font-weight:600;line-height:1.25">{titel}</div>{unten}</div>')


BOX_H = 480   # Kartenhöhe wie auf „UA OS“ (Review Michael 25.10.)


def reihe(*karten, gap=32, top=52, hoehe=None):
    groesse = f"height:{hoehe}px;flex:0 0 auto" if hoehe else "flex:1;min-height:0"
    return f'<div style="margin-top:{top}px;display:flex;gap:{gap}px;{groesse}">{"".join(karten)}</div>'


def zitat(t, size=88):
    # Anführungszeichen groß und transparent im Hintergrund, wie das Fragezeichen auf den Frage-Folien
    return (f'<div style="position:relative"><div class="zitat-deko" style="position:absolute;left:-60px;top:-430px;z-index:-1;font-family:Newsreader,serif;font-size:1500px;'
            f'line-height:1;opacity:.11;pointer-events:none;user-select:none;background:linear-gradient(160deg,{MINT} 0%,rgba(125,219,166,0) 70%);'
            f'-webkit-background-clip:text;background-clip:text;color:transparent">“</div>'
            f'<div style="font-size:{size}px;font-weight:700;letter-spacing:-0.025em;line-height:1.08;max-width:1600px">{t}</div></div>')


def kunden_bild(hoehe):
    """Reihe mit Kundenfotos: im privaten Bau echt, im öffentlichen ein Platzhalter."""
    if PRIVAT and KUNDEN_BILD.exists():
        return f'<img src="{bild(KUNDEN_BILD)}" alt="" style="height:{hoehe}px;width:auto;display:block">'
    return (f'<div style="height:{hoehe}px;width:{round(hoehe * 3.3)}px;border:2px dashed {GELB};border-radius:{hoehe // 2}px;display:flex;'
            f'align-items:center;justify-content:center;{MONO}font-size:{max(12, hoehe // 5)}px;color:{GELB}">KUNDENFOTOS</div>')


def tuerkis(t):
    """Hervorhebung, die auch in UA-Überschriften türkis bleibt (statt weiß)."""
    return f'<span class="bleibt-tuerkis" style="color:{MINT}">{t}</span>'


def unsichtbar(bedingung):
    return "" if bedingung else "visibility:hidden;"


def hell(t):
    """Teil einer Überschrift in Weiß statt UA-Grün."""
    return f'<span style="color:#F4F2EC">{t}</span>'


def blasen(liste, k=99):
    """Schräg gestellte Sprechblasen, verteilt über die Folie (Positionen in %)."""
    return ('<div style="position:relative;flex:1;margin-top:20px">'
            + "".join(f'<div class="blase" style="{unsichtbar(j < k)}position:absolute;left:{x}%;top:{y}%;transform:rotate({r}deg);background:#1C1B1A;border:1px solid {CORAL};'
                      f'border-radius:18px;padding:22px 30px;font-size:30px;font-weight:600;color:#F4F2EC;box-shadow:0 20px 40px -20px #000;white-space:nowrap">{txt}</div>'
                      for j, (txt, x, y, r) in enumerate(liste)) + '</div>')


def foto(name, px=190, rand=MINT):
    for ordner in ((FOTOS, REFERENZEN) if PRIVAT else (FOTOS,)):
        for endung in ("jpg", "png"):
            datei = ordner / f"{name}.{endung}"
            if datei.exists():
                b64 = base64.b64encode(datei.read_bytes()).decode()
                return (f'<div style="width:{px}px;height:{px}px;border-radius:50%;flex-shrink:0;'
                        f'background:url(data:image/{endung};base64,{b64}) center/cover;border:3px solid {rand};'
                        f'box-shadow:0 0 60px -18px {rand}"></div>')
    return (f'<div style="width:{px}px;height:{px}px;border-radius:50%;flex-shrink:0;border:3px dashed {GELB};'
            f'display:flex;align-items:center;justify-content:center;{MONO}font-size:18px;color:{GELB}">FOTO</div>')


def live_badge(t="Live-Demo"):
    return (f'<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:10px;padding:13px 26px;border-radius:999px;'
            f'background:{CORAL};color:#3A1B12;{MONO}font-size:15px;font-weight:700;letter-spacing:.16em;text-transform:uppercase">'
            f'<span style="width:9px;height:9px;border-radius:50%;background:#3A1B12;animation:mintPulse 1.4s infinite"></span>{t}</div>')


# ---- Referenzen ---------------------------------------------------------------------------------------
# Echte Namen, Zahlen, Zitate und Fotos liegen nur lokal in deck/referenzen/ (nie im Repo).
# Öffentlicher Bau: Platzhalter. Privater Bau (LPS_PRIVAT=1): echte Referenzen, Ausgabe in deck/referenzen/.
REF_DATEI = WURZEL / "deck" / "referenzen" / "lps-referenzen.json"
REF_REIHE = ["florian", "rebecca", "bettina", "caro_moritz", "barbara", "christine", "thorsten", "sandra_dirk", "chat"]
KUNDEN_BILD = WURZEL / "deck" / "referenzen" / "fotos" / "kunden-avatare.png"   # echte Kunden: nur lokal
if PRIVAT and REF_DATEI.exists():
    REF = json.loads(REF_DATEI.read_text(encoding="utf-8"))
else:
    REF = {k: {"name": f"[Referenz {i}]", "rolle": "[Rolle]", "ergebnis": "[Ergebnis]", "zusatz": "[Zeitraum]",
               "zitat": "[Zitat]", "hebel": "[Der Hebel]", "vorher": "[vorher]", "heute": "[heute]", "nachsatz": "[Nachsatz]"}
           for i, k in enumerate(REF_REIHE, 1)}


def r(key, feld):
    return REF[key].get(feld, "")


def ref_foto(key, px=190, rand=MINT):
    return foto(REF[key].get("foto", "_keins"), px, rand)


def screen(key, hoehe=300):
    name = REF[key].get("screen")
    datei = WURZEL / "deck" / "referenzen" / "screens" / f"{name}.png" if (PRIVAT and name) else None
    if datei and datei.exists():
        b64 = base64.b64encode(datei.read_bytes()).decode()
        return f'<img src="data:image/png;base64,{b64}" style="height:{hoehe}px;width:auto;border-radius:22px;box-shadow:0 30px 60px -25px #000">'
    return (f'<div style="height:{hoehe}px;width:{int(hoehe * 1.7)}px;border:3px dashed {GELB};border-radius:22px;display:flex;align-items:center;'
            f'justify-content:center;{MONO}font-size:20px;color:{GELB}">SCREENSHOT</div>')


def proof(label, wer, notiz, key, eyebrow_text, kopf=""):
    """Referenz-Folie im Stil des Akquise-Copilot: große Zahl, Zitat, Hebel, Foto rechts."""
    neu(label, wer, notiz,
        f'<div style="flex:1;display:flex;align-items:center;gap:90px">'
        f'<div style="flex:1">{eyebrow(eyebrow_text)}{h2(kopf, 64, 24) if kopf else ""}'
        # Peer-Identität: die Referenz stand dort, wo der Zuschauer heute steht
        + (f'<div style="margin-top:18px;font-size:30px;color:#B4AFA6">Stand genau da, wo du heute stehst.</div>' if not kopf else "")
        + f'<div style="margin-top:30px;font-size:150px;font-weight:700;letter-spacing:-0.04em;line-height:.95;color:{MINT}">{r(key, "ergebnis")}</div>'
        f'<div style="margin-top:12px;font-size:40px;font-weight:600">{r(key, "zusatz")}</div>'
        + (f'<div style="margin-top:40px;font-size:36px;line-height:1.4;color:#E4E0D8">„{r(key, "zitat")}“</div>' if r(key, "zitat") else "")
        + (f'<div style="margin-top:34px;padding-top:22px;border-top:1px solid #34322F"><div style="{MONO}font-size:16px;letter-spacing:.14em;color:{MINT}">DER HEBEL</div>'
           f'<div style="margin-top:10px;font-size:28px;color:#B4AFA6">{r(key, "hebel")}</div></div>' if r(key, "hebel") else "")
        + f'</div><div style="display:flex;flex-direction:column;align-items:center;gap:18px">{ref_foto(key, 380)}'
        f'<div style="font-size:44px;font-weight:700">{r(key, "name")}</div><div style="font-size:24px;color:#8C8780">{r(key, "rolle")}</div></div></div>',
        GRUEN)


FOLGE = []   # (html, kürzel)


def neu(label, wer, notiz, inner, stil=STIL):
    FOLGE.append((section(label, notiz, stil, inner), wer))


def stufen(label, wer, notiz, n, bau, stil=STIL):
    """Dieselbe Folie n-mal, jede Stufe zeigt ein Element mehr. bau(k) liefert den Inhalt für Stufe k (1..n)."""
    for k in range(1, n + 1):
        neu(label, wer, notiz, bau(k), stil)


def kapitel(nr, titel, satz, wer, notiz):
    neu(f"Kapitel {nr}", wer, notiz,
        f'<div style="{MONO}font-size:30px;letter-spacing:.2em;color:{MINT}">KAPITEL {nr}</div>'
        f'<div style="margin-top:20px;font-size:190px;font-weight:700;letter-spacing:-0.04em;line-height:.95">{titel}</div>'
        + sub(satz, 38, 36), GRUEN)


def nummern(punkte, k=99, farbe=MINT):
    """Raster 2 × 3 mit nummerierten Karten, Stufe k zeigt die ersten k."""
    art = "coral" if farbe == CORAL else "mint"
    karten = "".join(
        f'<div class="nummer nummer-{art}" style="{"" if k > j else "visibility:hidden;"}display:flex;align-items:center;gap:28px;background:#131312;'
        f'border:1px solid #34322F;border-radius:22px;padding:0 36px">'
        f'<div class="nummer-zahl" style="width:64px;height:64px;border-radius:16px;background:{farbe};color:#10241A;flex-shrink:0;display:flex;'
        f'align-items:center;justify-content:center;font-size:30px;font-weight:700">{j + 1}</div>'
        f'<div style="font-size:34px;font-weight:600;line-height:1.25">{p}</div></div>' for j, p in enumerate(punkte))
    return f'<div style="margin-top:48px;flex:1;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:24px">{karten}</div>'


def gestrichen(punkte):
    return "".join(f'<div style="display:flex;align-items:center;gap:16px;font-size:32px;color:#8C8780">'
                   f'<span style="color:{CORAL};font-weight:700">✕</span><span style="text-decoration:line-through;text-decoration-color:{CORAL}">{p}</span></div>'
                   for p in punkte)


def haken(punkte, farbe=MINT, zeichen="✓"):
    return "".join(f'<div style="display:flex;align-items:flex-start;gap:18px;font-size:34px;line-height:1.3">'
                   f'<span style="color:{farbe};font-weight:700">{zeichen}</span><span>{p}</span></div>' for p in punkte)


# =====================================================================================================
# TEIL 1 · EINSTIEG  (überarbeitet nach Review 21.10.2026)
# =====================================================================================================
def bild(pfad, hoehe=None, spiegeln=False, kante=0):
    """Bild als data-URI (WebP), auf Höhe `hoehe` verkleinert, damit das Deck klein bleibt.
    kante > 0 schneidet den hellen Saum von freigestellten Fotos ab (Pixel am Rand der Maske)."""
    from PIL import Image, ImageFilter, ImageOps
    im = Image.open(pfad)
    if kante and im.mode == "RGBA":
        im.putalpha(im.getchannel("A").filter(ImageFilter.MinFilter(kante)).filter(ImageFilter.GaussianBlur(1.2)))
    if spiegeln:
        im = ImageOps.mirror(im)
    if hoehe and im.height > hoehe:
        im = im.resize((round(im.width * hoehe / im.height), hoehe), Image.LANCZOS)
    puffer = io.BytesIO()
    im.save(puffer, "WEBP", quality=86, method=6)
    return "data:image/webp;base64," + base64.b64encode(puffer.getvalue()).decode()


def sprecher(datei, name, hoehe, rechts, spiegeln=False, kante=0):
    """Freigestellter Sprecher, unten angeschnitten, mit Namens-Pille."""
    return (f'<img src="{bild(WURZEL / "assets" / "hosts" / datei, hoehe * 2, spiegeln, kante)}" alt="{name}" '
            f'style="position:absolute;bottom:0;right:{rechts}px;height:{hoehe}px;width:auto;'
            # Foto läuft unten selbst weich aus, ohne dunkle Fläche davor (Logo steht frei)
            f'-webkit-mask-image:linear-gradient(180deg,#000 58%,transparent 84%);mask-image:linear-gradient(180deg,#000 58%,transparent 84%)">')


def namens_pille(name, rechts):
    return (f'<div style="position:absolute;bottom:250px;right:{rechts}px;z-index:3;display:inline-flex;align-items:center;gap:12px;'
            f'padding:12px 24px;border-radius:999px;background:rgba(13,13,13,.82);border:1.5px solid #34322F">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{MINT}"></span>'
            f'<span style="font-size:30px;font-weight:700">{name}</span></div>')


def countdown(ziel=None, video=False, farbe=MINT):
    """Türkiser Zähler Minuten:Sekunden oben rechts. ziel = Startzeit (Deckblatt) oder video=True (Restlaufzeit des Videos)."""
    if video:
        js = ('var s=document.currentScript,f=s.closest(".slide"),v=f.querySelector("video"),el=f.querySelector(".countdown");'
              'function tick(){var d=isFinite(v.duration)?v.duration:159,r=Math.max(0,Math.ceil(d-v.currentTime));'
              'el.textContent=Math.floor(r/60)+":"+(r%60<10?"0":"")+r%60;}tick();v.addEventListener("timeupdate",tick);'
              'v.addEventListener("loadedmetadata",tick);v.addEventListener("seeked",tick);')
        start = "2:39"
    else:
        js = (f'var s=document.currentScript,el=s.closest(".slide").querySelector(".countdown"),ziel=new Date("{ziel}").getTime();'
              'function tick(){var r=Math.max(0,Math.floor((ziel-Date.now())/1000)),m=Math.floor(r/60),x=r%60;'
              'el.textContent=(m<10?"0":"")+m+":"+(x<10?"0":"")+x;}tick();setInterval(tick,1000);')
        start = "00:00"
    return (f'<div style="position:absolute;top:130px;right:130px;z-index:3;text-align:center">'
            f'<div style="{MONO}font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:{farbe}">Wir starten in</div>'
            f'<div class="countdown" style="margin-top:6px;font-size:84px;font-weight:700;letter-spacing:-0.02em;color:{farbe};'
            f'font-variant-numeric:tabular-nums;text-shadow:0 2px 24px rgba(0,0,0,.6)">{start}</div></div>'
            f'<script>(function(){{{js}}})();</script>')


def ua_logo(**stil):
    return (f'<img src="{bild(WURZEL / "assets" / "logos" / "unternehmensathleten-wortmarke.png", 240)}" alt="unternehmensathleten" '
            f'style="position:absolute;height:80px;width:auto;z-index:3;{";".join(f"{k}:{v}" for k, v in stil.items())}">')


# Titel: Text links, Alex und Michael rechts, UA-Wortmarke unten rechts (doppelte Größe)
neu("Titel", "A", "Willkommen zum LinkedIn Performance System 2027. Heute geht es darum, wie aus LinkedIn in 90 Tagen qualifizierte Termine in deinem Kalender werden. Live, keine Aufzeichnung.",
    '<div style="position:absolute;left:96px;top:0;bottom:0;width:860px;z-index:2;display:flex;flex-direction:column;justify-content:center">'
    f'<div class="badge-live" style="display:inline-flex;align-self:flex-start;align-items:center;gap:14px;padding:15px 28px;border-radius:999px;'
    f'background:{CORAL};color:#3A1B12;{MONO}font-size:18px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;'
    f'box-shadow:0 0 34px -8px rgba(232,145,122,.7)"><span style="width:10px;height:10px;border-radius:50%;background:#3A1B12"></span>Inkl. Live-Q&amp;A</div>'
    '<h1 style="margin:30px 0 0;font-weight:700;letter-spacing:-0.03em;line-height:0.98;font-size:112px">LinkedIn<br>Performance<br>'
    f'<span style="color:{MINT};font-size:84px;letter-spacing:-0.025em;line-height:1.2">System 2027</span></h1>'
    '<p style="margin:34px 0 0;font-size:27px;line-height:1.45;color:#B4AFA6">'
    '<span style="color:#F4F2EC;font-weight:600;font-size:36px;line-height:1.3">Jederzeit qualifizierte Termine im Kalender.</span><br>'
    '<span style="display:inline-block;margin-top:14px">Für Selbstständige, Freelancer und Agenturen,<br>deren Angebot sich schon verkauft.</span></p>'
    '<div style="margin-top:56px;display:flex;align-items:center;gap:22px">'
    f'<div style="display:inline-flex;align-items:center;padding:15px 28px;border-radius:999px;background:{MINT};color:#10241A;font-weight:700;font-size:18px">Di · 27.10.2026</div>'
    '<div style="font-size:19px;color:#B4AFA6">11:00 Uhr · Live &amp; Online · keine Aufzeichnung</div></div>'
    f'<div style="margin-top:34px;display:flex;align-items:center;gap:22px">{kunden_bild(80)}'
    '<span style="font-size:22px;line-height:1.35;color:#B4AFA6">250+ Coaches, Berater und B2B-Dienstleister<br>erfolgreich begleitet</span></div></div>'
    # Michael gespiegelt, damit er zur Mitte schaut
    + sprecher("alex.png", "Alex", 820, 350) + sprecher("michael.png", "Michael", 770, 0, spiegeln=True, kante=7)
    + namens_pille("Alex", 575) + namens_pille("Michael", 200)
    + countdown(ziel="2026-10-27T11:06:00+01:00")
    + ua_logo(right="96px", bottom="64px"),
    "padding:0;position:relative;overflow:hidden;background:radial-gradient(1100px 640px at 18% 78%, rgba(125,219,166,.10), transparent 55%), "
    "radial-gradient(900px 700px at 78% 45%, rgba(125,219,166,.08), transparent 60%), #0D0D0D")

# Video füllt die ganze Folie, ohne Eyebrow. Das Video selbst kommt noch.
neu("Video · Unternehmensathlet", "A", "Unternehmensathlet-Video abspielen. Vermittelt sofort unsere Werte, filtert und unterscheidet uns von anderen.",
    # Das Video liegt neben dem Deck (video/…, nicht im Repo, auf OneDrive). Startet beim Hinblättern, Klick = Pause.
    '<video class="folien-video" src="video/trailer-ein-ua-ist-fuer-mich.mp4" preload="auto" playsinline '
    'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000"></video>'
    f'<div class="video-play" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none">'
    f'<div style="width:150px;height:150px;border-radius:50%;background:{MINT};display:flex;align-items:center;justify-content:center">'
    f'<div style="width:0;height:0;border-left:52px solid #10241A;border-top:32px solid transparent;border-bottom:32px solid transparent;margin-left:12px"></div></div></div>'
    '<script>(function(){var s=document.currentScript,f=s.closest(".slide"),v=f.querySelector("video"),p=f.querySelector(".video-play");'
    'function zeig(){p.style.display=v.paused?"flex":"none";}v.addEventListener("play",zeig);v.addEventListener("pause",zeig);'
    'v.addEventListener("click",function(e){e.stopPropagation();v.paused?v.play():v.pause();});'
    'new MutationObserver(function(){if(f.classList.contains("active")){v.play().catch(function(){});}else{v.pause();}}).observe(f,{attributes:true,attributeFilter:["class"]});})();</script>'
    + countdown(video=True, farbe="#F4F2EC") + ua_logo(left="50%", bottom="56px", transform="translateX(-50%)"),
    "padding:0;position:relative;overflow:hidden;background:#000")


def antworten(opts, farbe="#34322F"):
    """Antwort-Karten für Umfragen: jede mit Nummer, darunter die Anleitung für den Chat."""
    art = "antwort-problem" if farbe == CORAL else "antwort-gut"
    return ('<div style="margin-top:56px;display:flex;gap:20px;height:240px">'
            + "".join(f'<div class="antwort {art}" style="flex:1;border:1.5px solid {farbe};border-radius:20px;background:#131312;display:flex;flex-direction:column;align-items:center;'
                      f'justify-content:center;gap:14px;text-align:center;padding:24px;font-size:{30 if len(o) > 20 else 40}px;font-weight:600;line-height:1.2">'
                      f'<span style="font-size:44px;font-weight:700;line-height:1;opacity:.55">{j}</span>{o}</div>'
                      for j, o in enumerate(opts, 1))
            + "</div>"
            + f'<div style="margin-top:30px;font-size:32px;color:#B4AFA6">Tippe die Zahl {hell(f"1–{len(opts)}")} für deine Antwort in den Chat.</div>')


neu("Wie es den meisten geht", "A", "In den meisten Webinaren werden die Teilnehmer mit Theorie überschüttet. Deshalb bekommst du heute eine klare Reihenfolge, die du ab morgen umsetzen kannst. Fragen bitte notieren, am Ende ist Q&A. Keine Aufzeichnung.",
    f'<div style="flex:1;display:flex;gap:70px;align-items:center">'
    + f'<div style="flex:0 0 620px;height:780px;transform:rotate(-3deg);border:3px dashed {GELB};border-radius:30px;background:rgba(232,201,122,.06);'
      f'display:flex;align-items:center;justify-content:center;text-align:center;padding:50px;{MONO}font-size:24px;line-height:1.5;color:{GELB}">'
      f'OFFEN<br><br>Bild oder GIF: Teilnehmer wird mit Infos überschüttet.<br>Eigenes Motiv, Rechte klären.</div>'
    + '<div style="flex:1;display:flex;flex-direction:column">'
    + eyebrow("Ehrlich gesagt") + h2(f"In den meisten Webinaren geht es den Teilnehmern {c('so.')}", 76)
    + sub("Weil sie mit Theorie und unnötigen Infos überschüttet werden.", 34, 26)
    + f'<div style="margin-top:44px;background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid {MINT};border-radius:26px;padding:40px 44px;font-size:38px;font-weight:600;line-height:1.35">'
      f'Deshalb bekommst du heute eine {m("klare Reihenfolge")}, die du ab morgen umsetzen kannst.</div>'
    + f'<div style="margin-top:28px;background:#131312;border:1px solid #34322F;border-radius:22px;padding:28px 36px;font-size:28px;color:#B4AFA6">'
      f'{w("Wichtig:")} Fragen notieren und am Ende im Q&amp;A stellen. Es gibt keine Aufzeichnung.</div>'
    + "</div></div>")


def stimme(key):
    return (f'<div style="background:#131312;border:1px solid #34322F;border-radius:24px;padding:30px 24px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:20px">'
            f'{ref_foto(key, 190)}<div style="font-size:36px;font-weight:700">{r(key, "name")}</div>'
            f'<div style="font-size:32px;font-weight:600;color:{MINT};line-height:1.25">{r(key, "ergebnis")}</div>'
            f'<div style="font-size:24px;color:#8C8780">{r(key, "zusatz") or r(key, "rolle")}</div></div>')


neu("Social Proof früh", "A", f"Social Proof gleich am Anfang. Über 250 Selbstständige haben mit uns ihre Kundengewinnung aufgebaut. Ein paar davon: {r('florian', 'name')}, {r('rebecca', 'name')}, {r('bettina', 'name')}, {r('caro_moritz', 'name')}, {r('barbara', 'name')}. Sie saßen vor einigen Monaten genau da, wo du heute sitzt.",
    eyebrow("Bevor es losgeht") + h2(f"Über {m('250 Selbstständige')} haben mit uns ihre Kundengewinnung aufgebaut.", 70)
    + sub("Viele von ihnen saßen vor ein paar Monaten genau da, wo du heute sitzt.", 32, 20)
    + f'<div style="margin-top:40px;flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:20px">{"".join(stimme(k) for k in ("florian", "rebecca", "bettina", "caro_moritz", "barbara"))}</div>')

neu("Umfrage 1", "M", "Umfrage im Chat. Antworten vorlesen.",
    eyebrow("Umfrage im Chat")
    + h2(f"Wie sicher bist du, dass LinkedIn für dich die richtige Plattform ist, um Kunden zu gewinnen, {tuerkis('wenn man weiß, wie?')}", 72, 30)
    + antworten(["Sehr sicher", "Eher sicher", "Unsicher", "Gar nicht"]), STIL_MITTE)

neu("Umfrage 2", "M", "Zweite Umfrage. Die Antworten sind unsere Einwand-Landkarte für den Rest des Webinars.",
    eyebrow("Umfrage im Chat")
    + h2(f"Was hält dich bei Kundengewinnung auf LinkedIn {c('aktuell am meisten zurück?')}", 76, 30)
    + antworten(["Zeit", "Wissen", "Technik", "Geld", "Ich weiß nicht, wo ich anfangen soll"], CORAL), STIL_MITTE)

chaos = [("KI-Content überall", 6, 8, -4), ("Reichweite sinkt", 54, 4, 3), ("Vernetzt und sofort gepitcht", 28, 34, -2),
         ("Der Feed langweilt", 64, 40, 5), ("„Lass uns mal telefonieren“", 6, 62, 2), ("Noch ein Carousel", 46, 70, -3)]
neu("LinkedIn ist tot?", "A", "Der Elefant im Raum. Viele haben LinkedIn schon totgesagt. KI flutet den Feed, Reichweiten sinken, bei jeder Vernetzung kommt die nächste Pitch-Nachricht.",
    h2(f'<span style="color:#F4F2EC">LinkedIn ist</span> {c("tot?!")}', 110) + blasen(chaos))

neu("Du hast viel probiert", "M", "Vorerfahrungen ansprechen. Ihr habt schon Workshops, Coachings und Programme gekauft. Und am Ende wollte euch wieder jemand was verkaufen. Das hat einen Grund.",
    eyebrow("Ehrlich gesagt") + h2(f"Du hast schon viel ausprobiert. Und am Ende wollte dir {c('wieder jemand was verkaufen.')}", 76)
    + reihe(karte("Workshops", art="neutral", size=48), karte("Coachings", art="neutral", size=48), karte("Programme", art="neutral", size=48)))

stufen("Vertrauenskrise", "A", "Die Erklärung dafür: Wir leben in einer Vertrauenskrise. Und deshalb ist heute wichtig, was persönlich ist: Outreach von Mensch zu Mensch und Direktnachrichten. Funnels nicht schlechtreden, sie sind nicht falsch, aber Vertrauen entsteht im direkten Kontakt.", 3,
       lambda k: eyebrow("Der Grund dafür", CORAL) + h2(f"Wir leben in einer {c('Vertrauenskrise.')}", 84)
       + reihe(karte("Kalender-Link, Landingpage, Funnel", "Funktioniert, wenn das Vertrauen schon da ist.", "coral", "Wirkt anonym"),
               karte("Persönlicher Outreach und Direktnachricht", "Hier entsteht Vertrauen. Mensch zu Mensch.", "mint", "Wirkt heute", sichtbar=k >= 2))
       + f'<div style="margin-top:36px;{"" if k >= 3 else "visibility:hidden"}">'
       + pille("Deshalb gewinnt, wer persönlich wird. Nicht wer lauter wird.") + "</div>")

neu("Marktlage", "A", "Aufhänger vor den Negativpunkten. Kontrastiv, nicht dramatisch: Fast jeder zweite Selbstständige sagt gerade, er hat zu wenig Aufträge. Ihr habt ein Angebot, das verkauft. Aber wisst ihr, was im März passiert?",
    eyebrow("Die Lage", CORAL)
    + f'<div style="margin-top:30px;font-size:200px;font-weight:700;letter-spacing:-0.04em;line-height:.9;color:{CORAL}">1 von 2</div>'
    + h2("Selbstständigen sagt gerade: zu wenig Aufträge.", 62, 24)
    + sub(f"Dein Angebot verkauft sich. Aber weißt du, {w('was im März passiert?')}", 40, 36)
    + f'<div style="margin-top:36px;display:flex">{offen("Quelle für „fast jeder zweite“ fehlt. Ohne Beleg fliegt die Folie.", "1", 18)}</div>', STIL_MITTE)

stufen("Der Ausfall", "A", "Frage in den Chat, keine Antwort nötig: Was passiert mit deinem Kalender, wenn du im Februar zwei Wochen ausfällst? Pause. Für die meisten: nichts Gutes. Und das, obwohl ihr gute Arbeit macht.", 2,
       lambda k: eyebrow("Frage in den Chat") + h2(f"Was passiert mit deinem Kalender, wenn du im Februar {c('zwei Wochen ausfällst?')}", 92, 30)
       + f'<div style="margin-top:60px;{"" if k >= 2 else "visibility:hidden"}">'
       + pille("Es liegt nicht daran, dass du schlecht bist. Dein Kalender hängt an dir, nicht an einem System.", CORAL) + '</div>', STIL_MITTE)

stufen("Kein System", "A", "Wenn du nicht weißt, welche Schritte heute deinen Kalender nächste Woche füllen, hast du kein System.", 2,
       lambda k: zitat(f"Wenn du nicht weißt, welche Schritte heute deinen Kalender nächste Woche füllen, <span style=\"{unsichtbar(k >= 2)}\">{c('hast du kein System.')}</span>", 80), STIL_MITTE)

neu("Empfehlungen", "M", "In den meisten unserer Gespräche sind Empfehlungen als Quelle schon weggefallen. Frage in den Chat: Was machst du aktuell, um nächste Woche deinen Kalender zu füllen, ohne auf Empfehlungen zu hoffen?",
    eyebrow("Frage in den Chat")
    + h2(f"Was machst du aktuell, um nächste Woche deinen Kalender zu füllen, {c('ohne auf Empfehlungen zu hoffen?')}", 80, 30)
    + sub(f"In {w('80 bis 90 %')} unserer Gespräche sind Empfehlungen als Quelle schon weggefallen.", 36, 48)
    + f'<div style="margin-top:28px;display:flex">{offen("80 bis 90 %: Wortlaut und Basis bestätigen", "1", 18)}</div>', STIL_MITTE)

stufen("Stell dir vor", "M", "Zielbild. Ein System, das dir die richtigen Personen vorschlägt. Vernetzung und Termin in zwei bis drei Nachrichten. Es liegt nicht an dir, es liegt am System.", 3,
       lambda k: eyebrow("Stell dir vor") + h2(f"Jeden Montag weißt du, {m('woher deine Termine kommen.')}", 80)
       + reihe(karte("Die richtigen Menschen", "Das System schlägt sie dir vor.", "mint", "01"),
               karte("2 bis 3 Nachrichten", "Vernetzt und im Gespräch.", "mint", "02", sichtbar=k >= 2),
               karte("Termin im Kalender", "Planbar statt zufällig.", "mint", "03", sichtbar=k >= 3))
       + f'<div style="margin-top:40px;{"" if k >= 3 else "visibility:hidden"}">' + pille("Es liegt nicht an dir. Es liegt am System.") + '</div>')


d.folien = [alt["Für wen das ist"]]
d.ed("Für wen das ist", "Experte, Trainer, Coach oder Berater mit einem funktionierenden Angebot bist",
     "Coach, Berater, Freelancer, Agentur oder Interim-Manager mit einem funktionierenden Angebot bist")
d.ed("Für wen das ist", "bereits Kontakte oder frühere Gespräche hast, aus denen du konsequenter qualifizierte Gespräche entwickeln willst",
     "planbar Anschlussprojekte statt Zufall willst")
d.ed("Für wen das ist", "2026 auf ein persönliches, KI-gestütztes Akquise-System setzen und regelmäßig umsetzen willst",
     "2027 auf ein persönliches LinkedIn-System setzen und regelmäßig umsetzen willst")
d.ed("Für wen das ist", "nicht bereit bist, Kontakte konsequent zu priorisieren, nachzufassen und das System regelmäßig zu nutzen",
     "nicht bereit bist, regelmäßig Gespräche zu führen und nachzufassen")
d.notes("Für wen das ist", "Filtern, wie im letzten Webinar. Wer hier falsch ist, darf gehen. Wer bleibt, ist richtig.")
FOLGE.append((d.folien[0], "A"))

neu("Warum jetzt · Jahresende", "M", "Wer im Januar sicher ins neue Jahr starten will, baut sein System jetzt. Bis Weihnachten steht es. Nicht im Januar, wenn alle Vorsätze fassen.",
    eyebrow("Warum jetzt") + h2(f"Bis Weihnachten bauen. Im Januar {m('sicher starten.')}", 84)
    + reihe(karte("Jetzt", "System aufbauen.", "neutral", "Oktober bis Dezember", size=64),
            karte("Weihnachten", "Das System steht.", "neutral", "Dezember", size=64),
            karte("Januar", "Du startest mit vollem Kalender.", "mint", "2027", size=64)))

aeren = [("1998", "Internet"), ("2010", "Social Media"), ("Jetzt", "KI")]
stufen("Warum jetzt · KI", "M", "1998 das Internet, 2010 Social Media, jetzt KI. Wer jetzt baut, ist vorne. Danach die dritte Umfrage.", 4,
       lambda k: eyebrow("Die Chance im Umbruch") + h2(f"Jedes Fenster geht {m('einmal')} auf.", 84)
       + reihe(*[karte(f'<span style="font-size:96px;letter-spacing:-0.03em;color:{MINT if j == 2 else "#F4F2EC"}">{jahr}</span>', was,
                       "mint" if j == 2 else "neutral", sichtbar=k > j) for j, (jahr, was) in enumerate(aeren)])
       + f'<div style="margin-top:40px;{"" if k >= 4 else "visibility:hidden"}">'
       + pille("Umfrage: Wie groß siehst du die Chance, die LinkedIn mit KI deinem Business bringt?") + '</div>')

neu("Opportunity LinkedIn", "A", "Der Schwenk: Die größte Chance für Selbstständige mit einem Angebot, das verkauft, ist 2027 LinkedIn. Deine Kunden sind schon da. Die meisten nutzen es nur falsch.",
    eyebrow("Die größte Chance 2027") + h2(f"Deine Kunden sind schon da. Auf {m('LinkedIn.')}", 110, 30)
    + sub("Die meisten Selbstständigen nutzen es nur falsch.", 44, 40), GRUEN)

denken = ["Ich muss mehr Content posten.", "Ich muss überall kommentieren.", "Ich brauche mehr Reichweite und Follower."]
wirklich = [("Die Richtigen kennen", "Wer genau kauft bei dir, und wo ist diese Person gerade aktiv?"),
            ("Ins Gespräch kommen", "Persönliche Direktnachricht statt noch ein Beitrag."),
            ("Gespräch in Termin verwandeln", "2 bis 3 Nachrichten, dann ein Termin im Kalender.")]


def denkfehler(k):
    rechts = "".join(f'<div style="{"" if k > j else "visibility:hidden;"}display:flex;gap:20px;align-items:flex-start">'
                     f'<div style="width:52px;height:52px;border-radius:14px;background:{MINT};color:#10241A;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700">{j + 1}</div>'
                     f'<div><div style="font-size:36px;font-weight:600">{t}</div><div style="font-size:26px;color:#B4AFA6;margin-top:6px">{x}</div></div></div>'
                     for j, (t, x) in enumerate(wirklich))
    return (eyebrow("Auf LinkedIn") + h2(f"Der größte {c('Denkfehler')} bei fast allen Selbstständigen.", 72)
            + reihe(f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:26px;padding:44px;display:flex;flex-direction:column;justify-content:center;gap:30px">'
                    f'<div style="{MONO}font-size:18px;letter-spacing:.14em;color:#8C8780">WAS DIE MEISTEN DENKEN</div>{haken(denken, CORAL, "✕")}</div>',
                    f'<div style="flex:1.25;background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid {MINT};border-radius:26px;padding:44px;display:flex;flex-direction:column;justify-content:center;gap:30px">'
                    f'<div style="{MONO}font-size:18px;letter-spacing:.14em;color:{MINT}">WIE ES WIRKLICH IST</div>{rechts}</div>', gap=36, top=40)
            + f'<div style="margin-top:30px;text-align:center;{"" if k >= 4 else "visibility:hidden"}">'
            + f'<div style="font-size:34px;font-weight:600">Du musst nicht mehr posten.</div>'
            + f'<div style="font-size:34px;color:{MINT};margin-top:8px">Du musst wissen, welche einkommensproduzierenden Aktivitäten deinen Kalender füllen.</div></div>')


stufen("Denkfehler", "A", "Was die meisten denken: mehr Content, mehr Kommentare, mehr Reichweite. Wie es wirklich ist: die Richtigen kennen, ins Gespräch kommen, Gespräch in Termin verwandeln. Du musst nur wissen, welche EPAs, also einkommensproduzierende Aktivitäten, deinen Kalender füllen.", 4, denkfehler)

neu("Case-Teaser", "A", f"Nur einer, als Vorgriff. {r('caro_moritz', 'name')} kamen mit {r('caro_moritz', 'vorher')} im Monat zu uns. Heute sind es {r('caro_moritz', 'heute')}. Am Ende zeig ich euch, was sich konkret verändert hat. Nicht Motivation. Steuerung.",
    eyebrow("Ein Vorgriff") + f'<div style="margin-top:30px;display:flex;align-items:center;gap:70px;flex:1">{ref_foto("caro_moritz", 340)}'
    f'<div style="flex:1">{h2(r("caro_moritz", "name"), 64, 0)}'
    f'<div style="margin-top:26px;display:flex;align-items:baseline;gap:30px;font-weight:700"><span style="font-size:80px;color:#8C8780">{r("caro_moritz", "vorher")}</span>'
    f'<span style="font-size:60px;color:{MINT}">→</span><span style="font-size:120px;color:{MINT}">{r("caro_moritz", "heute")}</span></div>'
    f'<div style="margin-top:8px;font-size:30px;color:#B4AFA6">Umsatz im Monat</div>'
    + sub("Am Ende zeig ich dir, was sich konkret verändert hat. Nicht Motivation. Steuerung.", 34, 36) + "</div></div>")

agenda = [("01", "Foundation", "Wo du wirklich stehst und was du verkaufst."),
          ("02", "Voller Kalender", "Qualifizierte Gespräche mit Framework, geplant statt erhofft."),
          ("03", "Deal closen", "Wie aus Gesprächen Kunden werden, ohne Überzeugungsarbeit.")]
stufen("Heute", "M", "Drei Dinge heute. Wörtlich wie im Event-Text.", 3,
       lambda k: eyebrow("Das zeigen wir dir heute") + h2(f"Drei Dinge. {m('Ein System.')}", 84)
       + reihe(*[karte(titel, text, "mint", nr, sichtbar=k > j, size=64) for j, (nr, titel, text) in enumerate(agenda)])
       + f'<div style="margin-top:22px;display:flex">{offen("Kapitelnamen und Überschrift sind Arbeitstitel, Brainstorming läuft", "1", 18)}</div>')


KAPITEL_CASE = {"01": "sandra_dirk", "02": "bettina", "03": "florian"}


def case_einstieg(nr, wer, notiz):
    key = KAPITEL_CASE[nr]
    proof(f"Case · Kapitel {nr}", wer, f"{notiz} {r(key, 'name')}: {r(key, 'ergebnis')} {r(key, 'zusatz')}. {r(key, 'zitat')}", key, "Aus der Praxis")
    if r(key, "ergebnis").startswith("["):
        FOLGE[-1] = (FOLGE[-1][0].replace("</section>", f'<div style="position:absolute;left:96px;bottom:40px;width:900px;display:flex">{offen("Ergebnis in Zahlen und Foto fehlen", "1", 18)}</div></section>'), FOLGE[-1][1])

kapitel("01", "Foundation", "Wo stehst du, was verkaufst du, an wen.", "A", "Kapitel 1. Kurz, als Voraussetzung für alles andere.")
case_einstieg("01", "A", "Jedes Kapitel startet mit einem echten Fall.")

stufen("Alte Welt, neue Welt", "M", "Alte Welt: 150 bis 200 Euro im Monat. Für 20.000 Euro Umsatz brauchst du rund 100 Kunden. Neue Welt: 2.000 Euro einmalig für vier Monate Betreuung. Für dasselbe Ziel 10 Neukunden.", 2,
       lambda k: eyebrow("Alte Welt, neue Welt") + h2(f"Gleiches Ziel. {m('Ein Zehntel der Kunden.')}", 80)
       + reihe(karte(f'<span style="font-size:110px;letter-spacing:-0.04em;color:{CORAL}">100</span><br>Kunden für 20.000 €', "bei 150 bis 200 € im Monat", "coral", "Alte Welt"),
               karte(f'<span style="font-size:110px;letter-spacing:-0.04em;color:{MINT}">10</span><br>Neukunden für 20.000 €', "bei 2.000 € für vier Monate Betreuung", "mint", "Neue Welt", sichtbar=k >= 2), gap=40)
       + f'<div style="margin-top:22px;display:flex">{offen("Zahlen laut Neumann. Quelle auf der Folie nennen?", "1", 18)}</div>')

aufwand = [("Gleiche Einwände", "Bei 200 € und 2.000 € oft identisch. Günstige Kunden sind teils fordernder.", "coral"),
           ("80 % kündigen", "Monatlich kündbare Abos: rund 80 % sind nach einem Monat weg (laut Neumann).", "coral"),
           ("Marge statt Masse", "Weniger Kunden, bessere Betreuung, höhere Bindung. Viele buchen erneut.", "mint")]
stufen("Gleicher Aufwand", "M", "Der Aufwand im Verkauf ist derselbe. Skalierung läuft über Marge, nicht über Masse.", 3,
       lambda k: eyebrow("Warum das so ist") + h2(f"Gleicher Aufwand. {m('Andere Marge.')}", 84)
       + reihe(*[karte(tt, tx, art, sichtbar=k > j, size=40) for j, (tt, tx, art) in enumerate(aufwand)]))

stufen("KI-Moment · Kundensprache", "A", "Live, maximal drei bis vier Minuten. Letzte zehn Kundengespräche oder Testimonials in eine KI, Kundenworte rausziehen, mit dem eigenen Angebotstext vergleichen. Die KI erfindet nichts, sie zeigt dir, was du schon gesagt bekommen hast. Danach: KI ersetzt kein System. Sie macht es leichter zu fahren.", 2,
       lambda k: live_badge() + h2(f"Wie deine Kunden ihr Problem {m('wirklich beschreiben.')}", 76, 28)
       + reihe(karte("Deine letzten 10 Testimonials", label="Schritt 1"), karte("Die KI zieht die Kundenworte raus", label="Schritt 2"),
               karte("Vergleich mit deinem Angebotstext", "Bei den meisten klafft eine Lücke.", "mint", "Schritt 3"), top=44)
       + f'<div style="margin-top:36px;display:flex;gap:24px;align-items:center;{"" if k >= 2 else "visibility:hidden"}">'
       + pille("KI ersetzt kein System. Sie macht es leichter zu fahren.") + "</div>"
       + f'<div style="margin-top:18px;display:flex">{offen("Testimonials für die Demo bereitlegen (nur lokal)", "1", 18)}</div>')

# =====================================================================================================
# TEIL 3 · VOLLER KALENDER
# =====================================================================================================
kapitel("02", "Voller Kalender", "Ihr wisst nicht, woher euer nächstes Gespräch kommt.", "A",
        "Das Problem ist nicht, dass ihr zu wenig verschickt. Das Problem ist, dass ihr nicht wisst, woher euer nächstes Gespräch kommt.")
case_einstieg("02", "A", "Jedes Kapitel startet mit einem echten Fall.")


def balken(monat, wert, hoehe, farbe):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:18px;height:100%">'
            f'<div style="font-size:72px;font-weight:700;color:{farbe}">{wert}</div>'
            f'<div style="width:220px;height:{hoehe}px;border-radius:18px 18px 6px 6px;background:{farbe};opacity:.85"></div>'
            f'<div style="{MONO}font-size:20px;letter-spacing:.14em;color:#B4AFA6">{monat}</div></div>')


neu("Zufall statt System", "A", "Im Oktober hattet ihr vielleicht sechs gute Gespräche. Im November keins. Nicht weil ihr schlechter geworden seid. Weil es Zufall war, kein System.",
    eyebrow("Gute Gespräche, Beispiel") + h2(f"Nicht schlechter geworden. Es war {c('Zufall.')}", 80)
    + f'<div style="flex:1;display:flex;align-items:flex-end;justify-content:center;gap:120px;margin-top:30px">'
    + balken("OKTOBER", "6", 420, MINT) + balken("NOVEMBER", "0", 8, CORAL) + "</div>")

neu("Wie deine Kunden entstehen", "A", "Vergiss das Bild, das du im Kopf hast. Das alles brauchst du nicht. So machen es unsere Kunden. Du schreibst seit Jahren Nachrichten. Genau damit gewinnst du deine Kunden.",
    eyebrow("Wie deine Kunden auf LinkedIn entstehen") + h2(f"Vergiss das Bild, {m('das du im Kopf hast.')}", 72)
    + f'<div style="margin-top:34px;background:#131312;border:1px solid #34322F;border-radius:24px;padding:30px 44px">'
      f'<div style="{MONO}font-size:17px;letter-spacing:.14em;color:#8C8780;margin-bottom:18px">DAS BRAUCHST DU ALLES NICHT</div>'
      f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 60px">{gestrichen(["Jeden Tag posten", "Viral gehen", "Hunderte Kommentare", "Massen-Anfragen verschicken"])}</div></div>'
    + f'<div style="margin-top:22px;text-align:center;{MONO}font-size:18px;letter-spacing:.14em;color:{MINT}">↓ SO MACHEN ES UNSERE KUNDEN</div>'
    + reihe(karte("[Name 1]", "Gewinnt Kunden aus seinem bestehenden Netzwerk.", "mint", "Netzwerk", size=36),
            karte("[Name 2]", "Gewinnt Kunden über Empfehlungen, die er gezielt anstößt.", "mint", "Empfehlung", size=36),
            karte("[Name 3]", "Gewinnt Kunden über gezielte Direktnachrichten.", "mint", "Direktansprache", size=36), top=18)
    + f'<div style="margin-top:22px;display:flex;align-items:center;gap:24px"><div style="flex:1;font-size:30px">Du denkst, du bist nicht der Typ für Direktnachrichten? Du schreibst seit Jahren Nachrichten. {m("Genau damit gewinnst du deine Kunden.")}</div>'
    + offen("3 echte Beispiele, Namen mit Freigabe", "0 0 440px", 16) + "</div>")

zeilen = [("Content", "1 bis 2 Stunden pro Beitrag, allein", "KI im Sparring, Beitrag in deiner Stimme"),
          ("Outreach", "Manuell, nach Gefühl", "KI schlägt dir die Richtigen vor")]


def vergleich(k):
    kopf = (f'<div style="display:grid;grid-template-columns:260px 1fr 1fr;gap:24px;{MONO}font-size:16px;letter-spacing:.14em;color:#8C8780">'
            f'<div></div><div style="color:{CORAL}">ALTE WELT</div><div style="color:{MINT}">NEUE WELT</div></div>')
    rows = "".join(f'<div style="display:grid;grid-template-columns:260px 1fr 1fr;gap:24px;flex:1">'
                   f'<div style="display:flex;align-items:center;font-size:40px;font-weight:700">{n}</div>'
                   f'{karte(a, art="coral", size=32)}{karte(b, art="mint", size=32, sichtbar=k >= 2)}</div>' for n, a, b in zeilen)
    return (eyebrow("Content und Outreach") + h2(f"Zwei Hebel. Allein {c('trägt keiner.')}", 80)
            + f'<div style="margin-top:44px;flex:1;display:flex;flex-direction:column;gap:24px">{kopf}{rows}</div>')


stufen("Content und Outreach", "A", "Zwei Hebel: Content und Outreach. Beide funktionieren isoliert schlecht. Alte Welt gegen neue Welt.", 2, vergleich)

quellen = [("Empfehlungen", "Systematisiert statt dem Zufall überlassen. Gute Kunden kennen andere gute Kunden."),
           ("Dein Netzwerk", "Aktiviert statt ignoriert."),
           ("Direktansprache", "Die Richtigen, nicht die Vielen.")]
stufen("Drei Quellen", "A", "Drei Quellen, jede mit einer eigenen Aufgabe.", 3,
       lambda k: eyebrow("Woher deine Gespräche kommen") + h2(f"Drei Quellen. {m('Jede mit eigener Aufgabe.')}", 80)
       + reihe(*[karte(tt, tx, "mint", f"Quelle 0{j + 1}", sichtbar=k > j, size=46) for j, (tt, tx) in enumerate(quellen)], hoehe=BOX_H), STIL_MITTE)


def trichter(k, label_stufen=4):
    stufen_ = [("100", "Nachrichten", 100), ("[?]", "Antworten", 74), ("[?]", "Gespräche", 52), ("3 bis 4", "Termine", 34)]
    zeilen_ = "".join(
        f'<div style="{"" if k > j else "visibility:hidden;"}width:{b}%;margin:0 auto;display:flex;align-items:center;justify-content:space-between;'
        f'padding:0 44px;flex:1;border-radius:18px;background:{"linear-gradient(90deg,#10241A,#1a4231)" if j == 3 else "#1C1B1A"};'
        f'border:1.5px solid {MINT if j == 3 else "#34322F"}"><span style="font-size:52px;font-weight:700;color:{MINT if j == 3 else "#F4F2EC"}">{z}</span>'
        f'<span style="{MONO}font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:#B4AFA6">{t_}</span></div>'
        for j, (z, t_, b) in enumerate(stufen_))
    return f'<div style="margin-top:40px;flex:1;display:flex;flex-direction:column;gap:16px">{zeilen_}</div>'


stufen("Rechenbeispiel", "A", "Runterrechnen auf Termine. Aus 100 Nachrichten werden 3 bis 4 Termine. Jede Stufe mit Begründung, nicht in die Einzelschritte gehen.", 4,
       lambda k: eyebrow("Rechenbeispiel, konservativ") + h2(f"Aus 100 Nachrichten werden {m('3 bis 4 Termine.')}", 72)
       + trichter(k) + f'<div style="margin-top:18px;display:flex">{offen("Eure Erfahrungswerte für Antworten und Gespräche, jede Zahl begründet", "1", 18)}</div>')

neu("KI-Moment · Kontext", "A", "Bevor du jemanden ansprichst: eine Minute Kontext zur Person von der KI. Eine passende Nachricht an fünf Richtige schlägt zwanzig generische an Beliebige. Die Plattformen bestrafen Volumen.",
    eyebrow("KI im Alltag") + h2(f"Fünf Richtige schlagen {m('zwanzig Beliebige.')}", 84)
    + reihe(karte(f'<span style="white-space:nowrap"><span style="font-size:110px;color:{CORAL}">20</span> generische Nachrichten</span>', "Die Plattform bestraft Volumen.", "coral"),
            karte(f'<span style="white-space:nowrap"><span style="font-size:110px;color:{MINT}">5</span> passende Nachrichten</span>', "Eine Minute KI-Kontext pro Person.", "mint"), gap=40, hoehe=BOX_H), STIL_MITTE)

schritte_dm = ["Qualifizieren", "Nach-<br>Qualifizieren", "Problem-<br>bewusstsein", "Hilfs-<br>bereitschaft", "Termin"]


def dm_kette(k):
    teile = []
    for j, s in enumerate(schritte_dm):
        letzter = j == len(schritte_dm) - 1
        vis = "" if k > j else "visibility:hidden;"
        if j:
            teile.append(f'<div style="{vis}font-size:48px;color:{MINT};flex-shrink:0">→</div>')
        teile.append(f'<div style="{vis}flex:1;min-height:300px;border-radius:26px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;'
                     f'{"background:linear-gradient(160deg,#10241A,#1a4231);border:1.5px solid " + MINT + ";box-shadow:0 0 80px -30px rgba(125,219,166,.7)" if letzter else "background:#131312;border:1px solid #34322F"}">'
                     f'<div style="{MONO}font-size:20px;color:{MINT}">0{j + 1}</div>'
                     f'<div style="font-size:{44 if letzter else 32}px;font-weight:700;text-align:center;line-height:1.2;color:{MINT if letzter else "#F4F2EC"}">{s}</div></div>')
    return f'<div style="margin-top:70px;display:flex;align-items:center;gap:16px">{"".join(teile)}</div>'


stufen("Framework", "A", "Unser DM-Framework: fünf Schritte vom Kontakt zum Termin. Nur die Namen nennen, nicht die Formulierungen. Kein Pitch, nur Fragen, bis klar ist, ob es passt.", 5,
       lambda k: eyebrow("Das Framework") + h2(f"In 5 Schritten vom Kontakt {m('zum Termin.')}", 84) + dm_kette(k)
       + f'<div style="margin-top:60px;{"" if k >= 5 else "visibility:hidden"}">' + pille("Kein Pitch. Nur Fragen, bis klar ist, ob es passt.") + "</div>", STIL_MITTE)

# =====================================================================================================
# TEIL 4 · DEAL CLOSEN
# =====================================================================================================
kapitel("03", "Deal closen", "Keine Überzeugungsarbeit. Eine Passungsfrage.", "M",
        "Wenn deine Gespräche planbar kommen, ist das Verkaufsgespräch keine Überzeugungsarbeit mehr. Es ist eine Passungsfrage.")
case_einstieg("03", "M", "Jedes Kapitel startet mit einem echten Fall.")

neu("Wer fragt, führt", "M", "Derjenige, der fragt, führt. Ihr seid nicht der Bittsteller.",
    eyebrow("Im Gespräch") + h2(f"Wer fragt, {m('führt.')}", 120)
    + sub("Du bist nicht der Bittsteller.", 36, 20)
    + reihe(offen("Schritt 1", "1"), offen("Schritt 2", "1"), offen("Schritt 3", "1"), top=44))

stufen("Kein Geld gerade", "M", "Der häufigste Satz in Verkaufsgesprächen gerade. Und so gehst du damit um.", 3,
       lambda k: h2(f"{hell('Einwand oder')} {c('Ausrede?!')}", 110)
    + blasen([("„Ich hab gerade kein Geld.“", 4, 4, -3), ("„Ich schlafe noch eine Nacht drüber!“", 50, 2, 3),
              ("„Das muss ich noch mit meinem Bruder besprechen.“", 14, 27, -2), ("„Jetzt ist gerade kein guter Zeitpunkt.“", 54, 50, 4),
              ("„Schick mir erst mal Unterlagen.“", 4, 62, 2), ("„Ich melde mich nach den Feiertagen.“", 44, 76, -3)], 0 if k == 1 else 3 if k == 2 else 6),
    "padding:88px 96px;display:flex;flex-direction:column;background:radial-gradient(1100px 700px at 75% 60%, rgba(232,145,122,.16), transparent 60%), "
    "radial-gradient(800px 500px at 15% 20%, rgba(232,145,122,.08), transparent 60%), #0D0D0D")

neu("KI-Moment · Muster", "A", "Nach jedem Gespräch, egal ob es ein Kunde wird: zwei Minuten, Notizen in eine KI, Muster über die letzten zehn Gespräche. Wo hakt es immer an derselben Stelle?",
    eyebrow("KI im Alltag") + h2(f"Zwei Minuten nach jedem Gespräch. {m('Muster statt Bauchgefühl.')}", 72)
    + reihe(karte("Notizen in die KI", label="Nach dem Call"), karte("Muster über 10 Gespräche", "Wo hakt es immer an derselben Stelle?", label="Jede Woche"),
            karte("Kaufsignale erkennen", "In DMs, mit Vorschlag für den nächsten Schritt.", "mint", "Im Programm"), hoehe=BOX_H), STIL_MITTE)

neu("Messung", "A", "Wenn ihr eure Zahlen aus diesen drei Bereichen kennt, wie viele Gespräche aus welcher Quelle, wie viele davon zu Kunden werden, dann wisst ihr im Oktober, wie euer Januar aussieht.",
    eyebrow("Die Brücke") + h2(f"Im Oktober wissen, wie dein {m('Januar')} aussieht.", 84)
    + reihe(karte("Welche Quelle", label="Messen"), karte("Wie viele Gespräche", label="Messen"), karte("Wie viele Kunden", label="Messen"),
            karte("Dein Januar", "Planbar.", "mint", "Ergebnis"), gap=24, hoehe=BOX_H), STIL_MITTE)

fazit = ["Klarheit zuerst. Dein Angebot spricht die Worte deiner Kunden.",
         "Drei Quellen statt Zufall: Empfehlungen, Netzwerk, Direktansprache.",
         "Fünf Richtige schlagen zwanzig Beliebige.",
         "Im Gespräch führst du. Es geht um Passung, nicht um Überzeugung.",
         "Wer seine Zahlen kennt, kennt seinen Januar."]
stufen("Zwischenfazit", "M", "Fünf Punkte, jeder einzeln. Wechselnde Satzanfänge.", 5,
       lambda k: eyebrow("Was du heute mitnimmst") + f'<div style="margin-top:40px;flex:1;display:flex;flex-direction:column;gap:18px">'
       + "".join(f'<div style="{"" if k > j else "visibility:hidden;"}flex:1;display:flex;align-items:center;gap:30px;background:#131312;border:1px solid #34322F;border-radius:22px;padding:0 40px">'
                 f'<span style="{MONO}font-size:22px;color:{MINT}">0{j + 1}</span><span style="font-size:36px;font-weight:600">{p}</span></div>'
                 for j, p in enumerate(fazit)) + "</div>")

stufen("Stell dir mal vor", "A", "Nicht zusammenfassen, Verlangen setzen. Stell dir mal vor, es ist Januar und du weißt, woher deine nächsten Gespräche kommen. Dann die Frage stellen und Pause.", 2,
       lambda k: eyebrow("Stell dir mal vor") + h2(f"Es ist Januar. Du weißt, woher deine {m('nächsten Gespräche')} kommen.", 84, 30)
       + f'<div style="margin-top:70px;{"" if k >= 2 else "visibility:hidden"}">'
       + sub(f"Würdest du dich {w('sicherer fühlen')}, wenn du das schon heute wüsstest?", 46, 0) + "</div>", STIL_MITTE)

# =====================================================================================================
# TEIL 5 · KAPAZITÄT UND VERTRAUEN
# =====================================================================================================
neu("System muss gefahren werden", "A", "Und jetzt der Teil, den die wenigsten Programme zeigen, weil er nicht sexy ist. Ein System muss gefahren werden. Von euch. Wenn Energie, Schlaf und Erholung nicht mitspielen, ist das beste System nur eine Powerpoint.",
    eyebrow("Der Teil, den kaum einer zeigt", CORAL) + h2(f"Ein System muss {c('gefahren werden.')}", 110, 30)
    + sub("Von dir. Wenn Energie, Schlaf und Erholung nicht mitspielen, ist das beste System nur eine Powerpoint.", 38, 40), STIL_MITTE)

neu("Kapazität", "A", "Dein Umsatz hängt an deiner Kapazität. Nicht als Nebensatz. Als Bedingung.",
    zitat(f"Dein Umsatz hängt an deiner {m('Kapazität.')} Nicht als Nebensatz. Als Bedingung."), STIL_MITTE)

neu("Mühelos", "A", "Echte Performance sieht mühelos aus, weil das System dahinter stimmt. Nicht weil ihr weniger arbeitet. Weil ihr klüger arbeitet und euch besser erholt.",
    zitat(f"Echte Performance sieht {m('mühelos')} aus, weil das System dahinter stimmt."), STIL_MITTE)


def gruender(name, rolle, fakten, bild):
    return (f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:28px;padding:48px;display:flex;align-items:center;gap:44px">{bild}'
            f'<div><div style="font-size:54px;font-weight:700">{name}</div><div style="{MONO}font-size:17px;letter-spacing:.14em;color:{MINT};margin-top:8px">{rolle}</div>'
            + "".join(f'<div style="margin-top:18px;font-size:30px;display:flex;gap:14px"><span style="color:{MINT}">●</span>{f}</div>' for f in fakten)
            + "</div></div>")


neu("Wer wir sind", "A/M", "Bevor wir zeigen, wie wir mit Leuten arbeiten: kurz, wer wir sind. Michael: Skalierung, mehrfach gegründet, zuletzt ein Medienhaus auf über 400 Mitarbeiter. Alex: Sportökonom, über 100 Gespräche mit Leistungssportlern, Trainingstherapeut. Zwei Welten, Business und Leistungssport. Genau da liegt der Unterschied zu jedem, der euch nur mehr Vertrieb beibringt.",
    eyebrow("Wer wir sind") + h2(f"Zwei Welten. {m('Ein System.')}", 84)
    + reihe(gruender("Michael", "BUSINESS & SKALIERUNG", ["Mehrfach gegründet", "Medienhaus auf über 400 Mitarbeiter"], foto("michi", 230)),
            gruender("Alex", "LEISTUNGSSPORT & PERFORMANCE", ["Sportökonom, Trainingstherapeut", "Über 100 Gespräche mit Leistungssportlern"], foto("alex", 230)), gap=36, top=44)
    + '<div style="margin-top:32px">' + pille("250+ Kunden aus verschiedenen Branchen · unternehmensathleten") + "</div>")

# =====================================================================================================
# TEIL 6 · PITCH
# =====================================================================================================
jahr = ["Zwölf Monate, in denen dein Kalender vom Zufall abhängt.", "Wieder posten und hoffen, statt die Richtigen anzuschreiben.",
        "Wieder auf Empfehlungen warten.", "Wieder ein Monat voll, der nächste leer.",
        "Wieder zusehen, wie andere über LinkedIn Kunden gewinnen.", "Und im Dezember 2027 stehst du genau da, wo du heute stehst."]
stufen("Ein weiteres Jahr", "A", "Was dich ein weiteres Jahr ohne System kostet. Punkt für Punkt, ruhig vorlesen.", 3,
       lambda k: eyebrow("Ehrlich gerechnet", CORAL) + h2(f"Was dich ein {c('weiteres Jahr')} kostet.", 84) + nummern(jahr, 2 * k, CORAL))

stufen("Zwei Optionen", "A", "Wir könnten dich jetzt allein lassen. Option 1: allein weitermachen. Option 2: die Abkürzung, mit der Reihenfolge, die bei über 250 Selbstständigen funktioniert hat.", 2,
       lambda k: eyebrow("Du hast zwei Optionen") + h2(f"Wer willst du {m('2027')} sein?", 84)
       + reihe(karte("Du bleibst jemand, dessen Kalender vom Zufall abhängt.", "Allein weiter, auf eigene Faust.", "coral" if k >= 2 else "neutral", "Option 1", size=46),
               karte("Du wirst jemand, der im Oktober weiß, wie der Januar aussieht.", "Die Reihenfolge, die bei über 250 Selbstständigen funktioniert hat. In 90 Tagen, gemeinsam.", "mint", "Option 2", sichtbar=k >= 2, size=46), gap=40))

scheitern = ["Wissen sammeln statt Reihenfolge: noch ein Kurs, noch ein Tool.", "Posten statt Gespräche führen.",
             "Keine klare Zielgruppe, kein klares Angebot.", "Alles gleichzeitig probieren und nichts durchziehen.",
             "Die erste Nachricht verschieben: aus nächster Woche wird nie.", "Allein: niemand sagt dir, wo du falsch abbiegst."]
stufen("Woran es scheitert", "A", "Woran es meistens scheitert. Jeder Punkt ist ein Grund für Option 2.", 3,
       lambda k: eyebrow("Aus über 250 Begleitungen", CORAL) + h2(f"{hell('Woran es')} {c('meistens scheitert.')}", 84) + nummern(scheitern, 2 * k, CORAL))

neu("Ergebnis zuerst", "A", "Ergebnis vor Weg. In 90 Tagen qualifizierte Termine im Kalender. Wie viele für dich realistisch sind, rechnen wir im Strategie-Call aus.",
    eyebrow("Das Ergebnis") + h2(f"In 90 Tagen {m('qualifizierte Termine')} im Kalender.", 110, 30)
    + sub("Wie viele für dich realistisch sind, rechnen wir im Strategie-Call aus.", 38, 40), GRUEN)

neu("Was ist das konkret", "A", "Also, was ist das jetzt konkret. Ein Satz, der das Produkt definiert. Hat 2025 gefehlt.",
    eyebrow("Was ist das konkret") + h2(f"{m('Foundation.')} Dein LinkedIn Performance System in 90 Tagen.", 84, 30)
    + f'<div style="margin-top:44px;display:flex">{offen("Produktsatz final formulieren (ein Satz)", "1")}</div>', STIL_MITTE)

bausteine = [("Outreach-System", "Die Richtigen finden und ansprechen."), ("Signature-Framework", "Deine Nachrichten, deine Stimme."),
             ("Onboarding", "Dein Startpunkt, sauber aufgenommen."), ("KI-Onboarding-Sprint", "KI als Werkzeug, nicht als Thema.")]
stufen("Der Weg", "M", "Erst jetzt der Weg. Die Bausteine einzeln, mit Wert dahinter.", 4,
       lambda k: eyebrow("Der Weg in 90 Tagen") + h2(f"Vier Bausteine. {m('Ein Ziel.')}", 80)
       + reihe(*[karte(tt, tx, "mint" if j == 3 else "neutral", f"Baustein 0{j + 1}", sichtbar=k > j, size=36) for j, (tt, tx) in enumerate(bausteine)], gap=24)
       + f'<div style="margin-top:22px;display:flex;gap:20px">{offen("Workshop gemeinsam oder Fragebogen + Voice-Onboarding?", "1", 18)}{offen("Monat 1 bis 3 und Wochenablauf", "1", 18)}</div>')

def stimme_gross(key):
    return (f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:28px;padding:48px;display:flex;flex-direction:column;gap:28px">'
            f'<div style="display:flex;align-items:center;gap:26px">{ref_foto(key, 140)}<div><div style="font-size:40px;font-weight:700">{r(key, "name")}</div>'
            f'<div style="{MONO}font-size:16px;letter-spacing:.14em;color:{MINT};margin-top:6px;text-transform:uppercase">{r(key, "rolle")}</div></div></div>'
            f'<div style="flex:1;display:flex;align-items:center;font-size:40px;font-weight:600;line-height:1.3">„{r(key, "zitat")}“</div>'
            f'<div style="padding-top:20px;border-top:1px solid #34322F;font-size:22px;color:#8C8780">{r(key, "nachsatz")}</div></div>')


neu("Stimmen · Umsetzungsbegleitung", "A", f"Zwei Stimmen aus unserer Umsetzungsbegleitung. {r('barbara', 'name')}: {r('barbara', 'zitat')} {r('christine', 'name')}: {r('christine', 'zitat')} Und die Erkenntnis von beiden: Der Fahrplan ist bei uns allen der gleiche.",
    eyebrow("Stimmen aus der Umsetzungsbegleitung") + h2(f"„Der Fahrplan ist bei uns {m('allen der gleiche.')}“", 76)
    + reihe(stimme_gross("barbara"), stimme_gross("christine"), gap=36, top=44))

neu("Proof · Gruppen-Chat", "A", f"Aus unseren Umsetzungsbegleitungen: {r('chat', 'ergebnis')}. {r('chat', 'zusatz')} Die Zahlen aus dem Trichter sind kein Wunschdenken.",
    f'<div style="flex:1;display:flex;align-items:center;gap:90px"><div style="flex:1">{eyebrow("Aus unseren Umsetzungsbegleitungen")}'
    f'<div style="margin-top:30px;font-size:110px;font-weight:700;letter-spacing:-0.03em;line-height:1">{m(r("chat", "ergebnis"))}</div>'
    + sub(f'{r("chat", "zusatz")} Die Termine aus dem Trichter sind {w("kein Wunschdenken.")}', 38, 36) + f'</div>{screen("chat", 420)}</div>', GRUEN)

neu("Einmal aufbauen", "A", "Das Beste daran: Du baust dieses System einmal auf und nutzt es für den Rest deiner Selbstständigkeit. Etwas, das dir niemand mehr wegnehmen kann.",
    f'<div style="text-align:center">{eyebrow("Das Beste daran")}</div>'
    + f'<div style="margin-top:30px;text-align:center;font-size:96px;font-weight:700;letter-spacing:-0.03em;line-height:1.08">Du baust dieses System {m("einmal")} auf<br>und nutzt es für den Rest deiner Selbstständigkeit.</div>'
    + sub("Etwas, das dir niemand mehr wegnehmen kann. Kein Algorithmus, keine Krise, keine Plattform-Änderung.", 38, 50).replace("max-width:1500px", "max-width:1500px;text-align:center;margin-left:auto;margin-right:auto"),
    GRUEN.replace("justify-content:center", "justify-content:center;align-items:center"))

DREI = ["caro_moritz", "thorsten", "sandra_dirk"]


def case_karte(key):
    return (f'<div style="flex:1;background:#131312;border:1px solid #34322F;border-radius:26px;padding:40px;'
            f'display:flex;flex-direction:column;align-items:center;text-align:center;gap:20px">{ref_foto(key, 180)}'
            f'<div style="font-size:42px;font-weight:700">{r(key, "name")}</div><div style="font-size:24px;color:#8C8780">{r(key, "rolle")}</div>'
            f'<div style="font-size:52px;font-weight:700;color:{MINT}">{r(key, "ergebnis")}</div>'
            f'<div style="font-size:24px;line-height:1.45;color:#B4AFA6">{r(key, "hebel")}</div></div>')


neu("Drei Cases", "A", "Drei völlig unterschiedliche Ausgangslagen. Ein identischer Mechanismus: der Moment, in dem jemand sieht, wo er wirklich steht und was als Nächstes dran ist.",
    eyebrow("Drei Ausgangslagen") + h2(f"Drei Wege. {m('Ein Mechanismus.')}", 76)
    + reihe(*[case_karte(k) for k in DREI], top=40)
    + '<div style="margin-top:28px">' + pille("Der Moment, in dem jemand sieht, wo er steht und was als Nächstes dran ist.") + "</div>"
    + f'<div style="margin-top:14px;display:flex">{offen(f"Fotos {r('thorsten', 'name')} und {r('sandra_dirk', 'name')} · Ergebnis {r('sandra_dirk', 'name')} · Freigaben", "1", 16)}</div>')

neu("Marktanker", "A", "Was vergleichbare Programme kosten. Monatlich ankern, nicht den Gesamtbetrag nennen.",
    eyebrow("Was vergleichbare Programme kosten") + h2(f"Was ist es wert, zu wissen, woher dein {m('nächster Kunde')} kommt?", 72)
    + reihe(offen("Vergleichsprogramm 1, Betrag pro Monat, Quelle", "1"), offen("Vergleichsprogramm 2, Betrag pro Monat, Quelle", "1"), gap=40))

neu("Dein Invest", "A", "Invest, nie Preis. Als Monatsbetrag. Keine 12-Monats-Raten.",
    eyebrow("Dein Invest") + f'<div style="margin-top:30px;display:flex;align-items:baseline;gap:30px">'
    f'<div style="font-size:200px;font-weight:700;letter-spacing:-0.04em;color:{MINT}">[Betrag]</div><div style="font-size:48px;color:#B4AFA6">€ / Monat</div></div>'
    + sub("90 Tage Foundation.", 40, 10)
    + f'<div style="margin-top:44px;display:flex;gap:20px">{offen("Monatsbetrag", "1")}{offen("3 oder 6 Raten? Workshop als erste Rate?", "1.6")}</div>', GRUEN)

neu("Garantie", "A", "Wir lassen niemanden am Anfang stehen. Kein ROI nach 90 Tagen, dann drei weitere Monate kostenlos. In der Runde, mit priorisierten Hot Seats, mit anderen, die dasselbe durchmachen.",
    eyebrow("Unser Versprechen") + h2(f"Wir lassen niemanden {m('am Anfang stehen.')}", 92)
    + reihe(karte("Kein ROI nach 90 Tagen?", "Das kann passieren.", size=44),
            karte("3 weitere Monate kostenlos", "In der Gruppe, mit priorisierten Hot Seats.", "mint", size=44), gap=40)
    + f'<div style="margin-top:22px;display:flex;gap:20px">{offen("Wie messen wir ROI?", "1", 18)}{offen("Rücktrittsrecht nach dem Workshop?", "1", 18)}</div>')

neu("Return", "M", "Der Trichter von vorhin. Gleiche Optik, gleiche Werte.",
    eyebrow("Zur Erinnerung") + h2(f"Aus 100 Nachrichten werden {m('3 bis 4 Termine.')}", 72) + trichter(4))

proof("Referenz nach Invest", "A", f"Erinnerst du dich an {r('florian', 'name')}? {r('florian', 'ergebnis')} {r('florian', 'zusatz')}. Denkst du, für ihn hat es sich gelohnt? Danach Kalender öffnen.",
      "florian", f"Erinnerst du dich an {r('florian', 'name')}?", f"Denkst du, für ihn {m('hat es sich gelohnt?')}")

nicht = ["… du nur mal gucken willst, was es kostet.", "… du keine [X] Stunden pro Woche investieren kannst.",
         "… du keine Ratschläge annehmen willst.", "… du nicht bereit bist, in dich selbst zu investieren.",
         "… du erst perfekt sein willst, bevor du loslegst.", "… du dir sicher bist, dass du es allein besser kannst."]
neu("Buch dir keinen Call, wenn", "A", "Ganz klare Qualifizierung. Wir nehmen nicht jeden.",
    eyebrow("Ehrlich gesagt") + h2(f'<span style="white-space:nowrap">{hell("Buch dir bitte")} {c("keinen Call")}{hell(", wenn …")}</span>', 84) + nummern(nicht, 99, CORAL)
    + f'<div style="margin-top:20px;display:flex">{offen("Stunden pro Woche festlegen", "1", 18)}</div>')

schritte = [("01", "Termin wählen", "Du suchst dir einen passenden Termin aus."),
            ("02", "Fragen beantworten", "Ein paar kurze Fragen, damit wir vorbereitet ins Gespräch gehen."),
            ("03", "Engpass-Analyse", "Alex und Michael machen den Call persönlich und schauen sich an, wo du stehst, wo du konkret hin willst, und wenn es passt, laden sie dich ein.")]


neu("So läuft dein Call ab", "A/M", "Auch wenn es selbsterklärend wirkt: einmal klar benennen, wie der Strategie-Call abläuft.",
    eyebrow("Der nächste Schritt") + h2(f"So geht es weiter {m('für dich.')}", 84)
    + f'<div style="margin-top:44px;flex:1;display:flex;gap:56px">'
    + '<div style="flex:1.1;display:flex;flex-direction:column;gap:22px">'
    + "".join(f'<div style="flex:1;display:flex;gap:30px;align-items:center;padding:0 34px;border-radius:24px;{"background:#131312;border:1.5px solid " + MINT if nr == "03" else "border:1px solid #34322F"}">'
              f'<div style="font-family:Newsreader,serif;font-style:italic;font-size:72px;color:{MINT if nr == "03" else "#2C4A3A"}">{nr}</div>'
              f'<div><div style="font-size:36px;font-weight:700">{t}</div><div style="font-size:24px;color:#B4AFA6;margin-top:6px;line-height:1.4">{x}</div></div></div>'
              for nr, t, x in schritte)
    # Terminauswahl: KI-generiert über Higgsfield (GPT Image 2.5), Di 27.10. und Mi 28.10.
    + "</div>" + f'<img src="{bild(Path(__file__).resolve().parent / "bilder" / "terminauswahl.png", 1100)}" alt="Terminauswahl" '
      'style="flex:0 0 auto;align-self:center;height:640px;width:auto;border-radius:28px;border:1.5px solid #34322F;box-shadow:0 34px 80px -18px rgba(0,0,0,.7)">' + "</div>")

neu("Kalender offen", "A", "QR-Code zum ersten Mal, vor den Boni. Ab sofort ist unser Kalender offen. Nur 5 Plätze. Kein Verkaufsgespräch, kein Risiko. Du kennst den Deal. Jetzt geht es nur darum, ob es für dich passt.",
    '<div style="flex:0 1 760px">'
    f'<div style="display:inline-flex;align-items:center;gap:16px;background:rgba(125,219,166,.1);border:1px solid rgba(125,219,166,.35);border-radius:999px;padding:8px 26px 8px 8px;margin-bottom:28px">'
    f'{kunden_bild(48)}<span style="font-size:20px;font-weight:600;color:#A9E8C5">250+ Kunden erfolgreich begleitet</span></div>'
    f'<h2 style="margin:0;font-weight:700;letter-spacing:-0.03em;line-height:0.98;font-size:92px">Unser Kalender<br>ist ab {m("jetzt offen.")}</h2>'
    f'<div style="margin-top:40px;display:inline-flex;align-items:center;gap:10px;padding:15px 28px;border-radius:999px;background:{CORAL};color:#3A1B12;font-weight:700;font-size:18px">'
    '<span style="width:8px;height:8px;border-radius:50%;background:#3A1B12;animation:mintPulse 1.4s infinite"></span>Nur 5 Plätze</div>'
    f'<div style="margin-top:38px;{MONO}font-size:22px;line-height:1.5;color:#B4AFA6">Kein Verkaufsgespräch. Kein Risiko. Du kennst den Deal. Jetzt geht’s nur darum, {m("ob es für dich passt.")}</div></div>'
    '<div style="flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:22px">'
    f'<div style="width:560px;height:560px;border:3px dashed {GELB};border-radius:36px;display:flex;align-items:center;justify-content:center;'
    f'{MONO}font-size:26px;color:{GELB};text-align:center;line-height:1.5">QR-CODE<br>STRATEGIE-CALL</div>'
    f'<div style="{MONO}font-size:17px;letter-spacing:.08em;color:#A9E8C5">Scan &amp; sichere dir deinen Platz</div></div>',
    "padding:100px 80px;background:linear-gradient(120deg, #0D0D0D 0%, #10241A 100%);display:flex;align-items:center;justify-content:center;gap:100px;position:relative;overflow:hidden")

def bonus_karte(nr, titel, text):
    return (f'<div style="flex:1;background:#F0EEE6;color:#141413;border-radius:24px;padding:34px 28px;display:flex;flex-direction:column;gap:16px;'
            f'transform:rotate({(-3, 2, -1, 3, -2)[nr - 1]}deg);box-shadow:0 30px 60px -25px #000">'
            f'<div style="align-self:flex-end;{MONO}font-size:14px;letter-spacing:.12em;background:#141413;color:#F0EEE6;border-radius:8px;padding:6px 12px">BONUS {nr}</div>'
            f'<div style="font-size:34px;font-weight:700;line-height:1.15">{titel}</div><div style="font-size:22px;line-height:1.4;color:#5A564F">{text}</div></div>')


neu("Bonus erste [N]", "M", "Boni einzeln, ausführlich, mit Geschichte. Nur für die ersten [N], die heute buchen. Danach der Gesamtvorteil.",
    '<div style="text-align:center">' + h2(f"Bonus nur für die {m('ersten [N].')}", 92, 0) + "</div>"
    + f'<div style="margin-top:56px;flex:1;display:flex;gap:26px;padding:0 20px">'
    + bonus_karte(1, "Strategie-Call", "Analyse deiner Situation mit Alex oder Michi.")
    + bonus_karte(2, "[Masterclass?]", "Kandidat. Gibt es noch nicht.")
    + bonus_karte(3, "[Bonus 3]", "Kandidat: Athleten-Call für Kopf und Körper.")
    + bonus_karte(4, "[Bonus 4]", "Kandidat: Geschenk mit Proof-of-Concept.")
    + "</div>"
    + f'<div style="margin-top:40px;display:flex;justify-content:center"><div style="background:{CORAL};color:#3A1B12;border-radius:20px;padding:22px 60px;text-align:center">'
      f'<div style="{MONO}font-size:16px;letter-spacing:.16em">DEIN GESAMTVORTEIL</div><div style="font-size:64px;font-weight:700">[Betrag] €</div></div></div>'
    + f'<div style="margin-top:18px;display:flex">{offen("Boni, Werte, Zahl [N] und Gesamtvorteil festlegen", "1", 18)}</div>',
    "padding:70px 96px;background:radial-gradient(1200px 700px at 50% 40%, #152C20, #0D0D0D);display:flex;flex-direction:column")

neu("Webinar-Code", "A", "Exklusiv für die Teilnehmer heute: euer Webinar-Code. Nennt ihn im Strategie-Call.",
    f'<div style="text-align:center">{eyebrow("Nur für dich als Teilnehmer")}</div>'
    + f'<div style="margin:40px auto 0;background:#131312;border:1.5px solid #2C4A3A;border-radius:30px;padding:60px 140px;text-align:center">'
      f'<span style="font-family:Newsreader,serif;font-size:140px;color:{MINT}">“</span>'
      f'<span style="font-size:120px;font-weight:700;letter-spacing:.02em">PERFORMANCE27</span>'
      f'<span style="font-family:Newsreader,serif;font-size:140px;color:{MINT}">”</span></div>'
    + sub("Nenn ihn im Strategie-Call. Dein Vorteil als Webinar-Teilnehmer.", 38, 44).replace("max-width:1500px", "max-width:1500px;text-align:center;margin-left:auto;margin-right:auto")
    + f'<div style="margin-top:30px;display:flex;justify-content:center">{offen("Was der Code bringt", "0 0 auto", 18)}</div>',
    GRUEN.replace("justify-content:center", "justify-content:center;align-items:center"))

neu("Knappheit", "A", "Die Crew startet am [Datum] mit der Foundation. Wir nehmen [N] Leute auf. Nicht wegen Marketing, sondern weil Hot Seats nur funktionieren, wenn jeder in jedem Call wirklich drankommt. Wer bis [Datum] startet, hat den Roadmap-Call noch vor Weihnachten.",
    eyebrow("Warum die Plätze begrenzt sind", CORAL) + h2(f"Hot Seats funktionieren nur, wenn {c('jeder drankommt.')}", 80)
    + reihe(karte(f'<span style="font-size:96px;color:{CORAL}">[N]</span> Plätze', "Die Zusammensetzung der Runde ist Teil dessen, wofür du investierst.", "coral"),
            karte("Crew-Start am [Datum]", "Foundation-Phase.", size=44),
            karte("Roadmap-Call vor Weihnachten", "Für alle, die bis [Datum] starten.", "mint", size=44))
    + f'<div style="margin-top:22px;display:flex">{offen("Startdatum, Platzzahl, Stichtag", "1", 18)}</div>')

neu("Einwände", "A/M", "Bevor ihr fragt, drei Sachen, die uns oft gefragt werden. Wir stellen sie uns selbst.",
    eyebrow("Das werden wir oft gefragt") + h2(f"Drei Fragen, {m('bevor ihr fragt.')}", 84)
    + reihe(offen("Einwand 1 aus euren Sales-Calls", "1"), offen("Einwand 2", "1"), offen("Einwand 3", "1"), top=44))

d.folien = [alt["Live Q&A"]]
d.ed("Live Q&A", "Stell deine Fragen — wir gehen sie gemeinsam durch, bevor die Plätze weg sind.", "Stell deine Fragen. Wir gehen sie gemeinsam durch.")
FOLGE.append((d.folien[0], "A/M"))

neu("Finaler CTA", "A", "Der Link steht im Chat. Nehmt euch zwei Minuten, wir warten. Wer heute bucht, ist noch vor Weihnachten startklar. Dann bewusst Pause, nicht weiterreden.",
    eyebrow("Jetzt") + h2(f"Der Link steht im Chat. {m('Wir warten.')}", 120, 30)
    + sub("Nimm dir zwei Minuten. Wer heute bucht, ist vor Weihnachten startklar.", 40, 40), GRUEN)

# =====================================================================================================
# SKRIPT 23.10.2026 · Einleitung, Teil 1 Vertrauen, Pipeline-Umbau, iPhone-Effekt, Boni nach Einwand
# Quelle: Notion „Webinar-Aufbau LinkedIn Performance System 2027 – Script“ und Skript-Review vom 23.10.
# =====================================================================================================
stufen("Hook", "A", "Bevor wir loslegen: Heute geht es um eine Sache. Wir schauen uns gemeinsam an, warum deine Kundengewinnung auf LinkedIn 2026 nicht mehr funktioniert und wieso 2027 noch herausfordernder wird, wenn du eine Sache nicht für dich meisterst.", 2,
       lambda k: eyebrow("Heute geht es um eine Sache")
       + h2(f"Warum deine Kundengewinnung auf LinkedIn 2026 {c('nicht mehr funktioniert.')}", 84, 30)
       + f'<div style="{"" if k >= 2 else "visibility:hidden"}">' + sub(f"Und wieso 2027 noch herausfordernder wird, {w('wenn du eine Sache nicht meisterst.')}", 42, 40) + "</div>", STIL_MITTE)

neu("Gib uns eine Chance", "M", "Doch bevor wir starten: Gib uns eine Chance. Wir wissen, du warst schon bei vielen Webinaren. Du hörst oft das Gleiche und gehst mit mehr Fragezeichen raus als rein. Und gefühlt jeder hat schon mal bei einem Coach gekauft und war enttäuscht. Deshalb zeigen wir dir heute vor allem die Menschen, die mit uns in den letzten 5 Jahren ihr Business aufgebaut haben. Und es lohnt sich, bis zum Schluss dabei zu sein: Am Ende gibt es ein Geschenk.",
    f'<div style="flex:1;display:flex;gap:90px;align-items:center">'
    # Bild: KI-generiert über Higgsfield (Nano Banana 2.1), Teilnehmer wird mit Infos überschüttet
    + f'<img src="{bild(Path(__file__).resolve().parent / "bilder" / "ueberschuettet.jpg", 1100)}" alt="" '
      'style="flex:0 0 auto;height:820px;width:auto;transform:rotate(-3deg);border-radius:30px;border:1.5px solid #34322F;'
      'box-shadow:0 40px 90px -30px #000,0 0 90px -40px rgba(125,219,166,.5)">'
    + '<div style="flex:1;display:flex;flex-direction:column">'
    + eyebrow("Bevor wir starten") + h2(f"Gib uns {m('eine Chance.')}", 112)
    + sub("Du warst schon bei vielen Webinaren. Du hörst oft das Gleiche und gehst mit mehr Fragezeichen raus als rein.", 42, 34)
    + "</div></div>")


def code_box(px=100):
    return (f'<div style="margin:40px auto 0;background:#131312;border:1.5px solid #2C4A3A;border-radius:30px;padding:50px 90px;text-align:center;white-space:nowrap">'
            f'<span style="font-size:{px}px;font-weight:700;letter-spacing:.02em">PERFORMANCE27</span></div>')


ZENTRIERT = GRUEN.replace("justify-content:center", "justify-content:center;align-items:center")
neu("Code merken", "A", "Diesen Code wirst du heute noch brauchen. Schreib ihn dir jetzt auf oder mach einen Screenshot. Am Ende sagen wir dir, wofür.",
    f'<div style="text-align:center">{eyebrow("Mit diesem Code bekommst du ein Geschenk.")}</div>' + code_box()
    + sub(f"Mach einen Screenshot.<br>{w('Du brauchst den Code am Ende.')}", 40, 44).replace("max-width:1500px", "max-width:1500px;text-align:center;margin-left:auto;margin-right:auto"), ZENTRIERT)

neu("Zustand · Kalender", "M", "Erste Frage in den Chat, ganz ohne LinkedIn: Was machst du aktuell, um nächste Woche deinen Kalender zu füllen, ohne auf Empfehlungen zu hoffen?",
    eyebrow("Frage in den Chat")
    + h2(f"Was machst du aktuell, um nächste Woche deinen Kalender zu füllen, {c('ohne auf Empfehlungen zu hoffen?')}", 86, 30), STIL_MITTE)

neu("Zustand · LinkedIn", "M", "Zweite Frage, jetzt mit LinkedIn. Die Antworten sind unsere Einwand-Landkarte für den Rest des Webinars.",
    eyebrow("Umfrage im Chat")
    + h2(f"Was hält dich auf LinkedIn aktuell am meisten zurück, {c('Termine zu vereinbaren?')}", 76, 30)
    + antworten(["Zeit", "Wissen", "Technik", "Geld", "Ich weiß nicht, wo ich anfangen soll"], CORAL), STIL_MITTE)

stufen("Marktlage · 1 von 2", "A", "1 von 2 Selbstständigen sagt gerade: Ich habe zu wenig Aufträge. Und: Ich kann nicht sagen, wie es in 3 bis 4 Monaten aussieht.", 4,
       lambda k: eyebrow("Die Lage", CORAL)
       + f'<div style="margin-top:30px;font-size:200px;font-weight:700;letter-spacing:-0.04em;line-height:.9;color:{CORAL}">1 von 2</div>'
       + h2(f'<span style="{unsichtbar(k >= 2)}">{hell("Selbstständigen sagt gerade:")}</span> <span style="{unsichtbar(k >= 3)}">{c("Ich habe zu wenig Aufträge.")}</span>', 62, 24)
       + f'<div style="{"" if k >= 4 else "visibility:hidden"}">' + sub(f"Und: {w('Ich kann nicht sagen, wie es in 3 bis 4 Monaten aussieht.')}", 42, 36) + "</div>", STIL_MITTE)


def stat(zahl, text, sichtbar=True):
    return (f'<div class="karte karte-coral" style="{unsichtbar(sichtbar)}flex:1;background:linear-gradient(160deg,#241512,#2B1915);border:1.5px solid {CORAL};border-radius:26px;padding:48px 38px;'
            f'display:flex;flex-direction:column;justify-content:flex-start;gap:20px">'
            f'<div style="font-size:104px;font-weight:700;letter-spacing:-0.04em;line-height:.9;color:{CORAL};white-space:nowrap">{zahl}</div>'
            f'<div style="font-size:34px;font-weight:600;line-height:1.3">{text}</div></div>')


stufen("Marktlage · Zahlen", "A", "Kurz gesagt: Die Stimmung im deutschsprachigen Raum ist schlecht. 48,4 Prozent der Solo-Selbstständigen haben Auftragsmangel. 80,6 Prozent haben Schwierigkeiten, die Geschäftsentwicklung vorherzusagen. Und 85 Prozent der Selbstständigen in unseren Gesprächen sagen: Empfehlungen sind als Lead-Quelle weggebrochen. Es fehlt Planbarkeit. Es fehlen Signale. Es fehlt ein klares System.", 4,
       lambda k: reihe(stat("48,4 %", "der Solo-Selbstständigen haben Auftragsmangel."),
                       stat("80,6 %", "können ihre Geschäftsentwicklung kaum vorhersagen.", k >= 2),
                       stat("85 %", "sagen: Empfehlungen sind als Lead-Quelle weggebrochen.", k >= 3), gap=28, top=0, hoehe=BOX_H)
       + f'<div style="{"" if k >= 4 else "visibility:hidden"}">' + h2(f'<span style="color:#F4F2EC">Es fehlt</span> {c("Planbarkeit.")}', 96, 56) + "</div>",
       STIL_MITTE)

stufen("Alte Welt · Covid", "M", "Alte Welt: Covid hat einen regelrechten Boom ausgelöst. Es war einfach. Die meisten lebten von Empfehlungen, weil der Aufholbedarf riesig war. Und deshalb werden wir immer öfter gefragt, und vielleicht fragst du dich das gerade selbst: Ist LinkedIn tot?", 4,
       lambda k: h2(f"Covid hat einen {m('Boom')} ausgelöst. Es war einfach.", 84)
       + reihe(karte("Aufholbedarf", "Alle wollten nachholen, alle wollten online.", size=48, sichtbar=k >= 2),
               karte("Empfehlungen", "Die meisten lebten davon. Der Kalender füllte sich von selbst.", size=48, sichtbar=k >= 3),
               karte("Vorbei", "Und jetzt fragen sich viele: Ist LinkedIn tot?", "coral", size=48, sichtbar=k >= 4), top=48, hoehe=BOX_H), STIL_MITTE)

stufen("Vertrauenskrise 2027", "A", "Neue Welt: LinkedIn funktioniert. Das Thema ist ein ganz anderes. Wir haben kein LinkedIn-Problem. Wir leben in einer Vertrauenskrise: politische Unsicherheit, Anbieter am Markt, die enttäuscht haben, und KI-Content, der alles überschwemmt.", 5,
       lambda k: reihe(karte("Politische Unsicherheit", "Menschen sind verunsichert und halten Geld zurück.", "coral", size=40),
                       karte("Enttäuschende Anbieter", "Fast jeder hat schon gekauft und wurde enttäuscht.", "coral", size=40, sichtbar=k >= 2),
                       karte("KI-Content überall", "Der Feed ist voll. Niemand weiß mehr, wem er glauben kann.", "coral", size=40, sichtbar=k >= 3),
                       top=0, hoehe=BOX_H)
       + f'<div style="{"" if k >= 4 else "visibility:hidden"}">'
       + h2(f'{hell("Kein LinkedIn-Problem.")}<br><span style="color:{CORAL};{"" if k >= 5 else "visibility:hidden"}">Eine Vertrauenskrise.</span>', 84, 56)
       + "</div>", STIL_MITTE)

stufen("Wendepunkt", "M", "Doch in jeder Krise liegt eine Chance. Krise bedeutet eigentlich nur Wendepunkt. Wer jetzt seine Hausaufgaben macht, geht gestärkt aus der Krise. Doch jede Chance hat nur ein kurzes Fenster.", 3,
       lambda k: zitat(f"Krise heißt Wendepunkt. <span style=\"{'' if k >= 2 else 'visibility:hidden'}\">Wer jetzt seine Hausaufgaben macht, {m('geht gestärkt raus.')}</span>", 84)
       + f'<div style="{"" if k >= 3 else "visibility:hidden"}">' + sub("Doch jede Chance hat nur ein kurzes Fenster.", 40, 50) + "</div>", STIL_MITTE)

fenster = [("1998", "Internet"), ("2010", "Facebook und Instagram"), ("2020", "LinkedIn-Reichweite, kostenfrei"), ("Jetzt", "KI")]
stufen("Chance · Fenster", "M", "1998 war das Internet eine große Chance. 2010 Facebook und Instagram. 2020 schenkte dir LinkedIn enorme Reichweite, völlig kostenfrei. Jetzt erleben wir dank KI die größte Chance. Wenn du sie nutzt. Frage: Wie oft hast du dir bei einer vertanen Chance ein paar Jahre später gesagt: Hätte ich doch …", 5,
       lambda k: eyebrow("Jede Chance hat ein Fenster")
       + f'<div style="{"" if k >= 5 else "visibility:hidden"}">' + h2(f"Jetzt ist {m('KI')} die größte Chance. Wenn du sie nutzt.", 76) + "</div>"
       + reihe(*[karte(f'<span style="font-size:84px;letter-spacing:-0.03em;color:{MINT if j == 3 else "#F4F2EC"}">{jahr}</span>', was,
                       "mint" if j == 3 else "neutral", size=40, sichtbar=k > j) for j, (jahr, was) in enumerate(fenster)], gap=24, top=44, hoehe=BOX_H)
       + f'<div style="margin-top:36px;{"" if k >= 5 else "visibility:hidden"}">' + pille("Frage in den Chat: Wie oft hast du dir schon gesagt: Hätte ich doch …?") + "</div>", STIL_MITTE)

stufen("Chance · Umfrage", "M", "Deshalb noch eine Frage: Wie groß siehst du aktuell die Chance, mit KI dein Business voranzubringen? Und wirst du sie nutzen? Egal, wie du sie siehst: Dein Mitbewerb nutzt sie. Wer KI heute als festen Bestandteil integriert, hat einen Vorsprung, den andere nicht mehr aufholen.", 2,
       lambda k: eyebrow("Umfrage im Chat")
       + h2(f"Wie groß siehst du aktuell die Chance, mit KI dein Business {m('voranzubringen?')}", 76, 30)
       + antworten(["Riesig", "Groß", "Eher klein", "Weiß ich nicht"])
       + f'<div style="margin-top:50px;{"" if k >= 2 else "visibility:hidden"}">' + pille("Egal, wie du sie siehst: Dein Mitbewerb nutzt sie.", CORAL) + "</div>", STIL_MITTE)

stufen("KI ersetzt nichts", "A", "Und damit meinen wir nicht, dass du alles an die KI auslagern sollst. Du kannst mit KI auf Knopfdruck LinkedIn mit Content überschwemmen. Dann hast du enorm viel Müll ohne Resonanz. Du kannst deinen Online-Kurs an einem Wochenende mit KI bauen. Gekauft hat ihn trotzdem keiner. Dann hast du nur schneller nichts verdient. KI kann nicht ersetzen, was nicht vorhanden ist.", 4,
       lambda k: eyebrow("Aber Vorsicht", CORAL)
       + f'<div style="{"" if k >= 4 else "visibility:hidden"}">' + h2(f"{hell('KI kann nicht ersetzen,')} {c('was nicht vorhanden ist.')}", 84) + "</div>"
       + reihe(karte('<span style="display:block;min-height:2.5em">Content auf Knopfdruck</span>', "Enorm viel Müll, der keine Resonanz erzeugt." if k >= 3 else "", "coral", size=42),
               karte('<span style="display:block;min-height:2.5em">Online-Kurs an einem Wochenende</span>', "Gekauft hat ihn trotzdem keiner. Nur schneller nichts verdient." if k >= 3 else "", "coral", size=42, sichtbar=k >= 2),
               gap=36, top=44, hoehe=BOX_H), STIL_MITTE)

stufen("Heute 2027", "M", "Drei Dinge heute. Wörtlich wie im Event-Text.", 4,
       lambda k: eyebrow("Das zeigen wir dir heute") + h2(f"Drei Dinge. {m('Ein System.')}", 84)
       + reihe(*[karte(f'<span style="white-space:nowrap">{tt}</span>', tx, "mint", f"0{j + 1}", sichtbar=k > j + 1, size=50)
                 for j, (tt, tx) in enumerate([("Vertrauen", "Wie du in der Vertrauenskrise Vertrauen aufbaust."),
                                               ("Volle Pipeline", "Woher deine Gespräche kommen, wenn du sie planst statt hoffst."),
                                               ("Abschluss", "Der iPhone-Effekt: verkaufen ohne Einwandbehandlung.")])], hoehe=BOX_H), STIL_MITTE)

# ---- Teil 1 · Vertrauen --------------------------------------------------------------------------------
kapitel("1", "Vertrauen", "Wie gewinnst du Vertrauen zurück?", "M", "Teil 1. Wie gewinnen wir das Vertrauen zurück?")

stufen("Vertrauen braucht Zeit?", "M", "Jetzt wirst du vielleicht sagen: Vertrauen braucht Zeit. Dabei funktionieren wir Menschen ganz anders. Sonst würden wir alle nichts mehr kaufen. Und Menschen kaufen. Nach wie vor.", 2,
       lambda k: zitat(f"„Vertrauen braucht Zeit.“ <span style=\"{'' if k >= 2 else 'visibility:hidden'}\">Dabei kaufen Menschen {m('nach wie vor.')}</span>", 96), STIL_MITTE)

IPHONE = bild(Path(__file__).resolve().parent / "bilder" / "iphone-duo.jpg", 1300)   # Higgsfield (Nano Banana 2.1), fiktives „iPhone Duo“
stufen("iPhone", "M", "Das iPhone hat es vor ein paar Wochen wieder gezeigt: alle Preise um 100 bis 200 Euro erhöht. Ein neues Modell für 2.500 Euro. Und LinkedIn ist voll von Leuten, die schreiben: Hab ich mir schon geholt. Keiner weiß, ob es funktioniert. Warum? Vertrauen ist immer ein Vorschuss.", 3,
       lambda k: (eyebrow("Ein Beispiel")
                  + h2(f"Apple hat gerade alle Preise um {m('200 €')} angehoben. Und das neue iPhone Duo um {m('<span style=\"white-space:nowrap\">2.500 €</span>')} vorgestellt.", 84, 30))
       if k == 1 else
       (eyebrow("Ein Beispiel") + '<div style="margin-top:30px;display:flex;align-items:center;gap:80px"><div style="flex:1">'
        + h2(f"Vorbestellungen, noch bevor du es überhaupt {m('in der Hand halten kannst.')}", 76, 0)
        + sub("Lieferzeit mittlerweile Januar 2027.", 40, 34)
        + f'<div style="margin-top:44px;{unsichtbar(k >= 3)}">' + pille("Vertrauen ist immer ein Vorschuss.") + "</div></div>"
        + f'<img src="{IPHONE}" alt="" style="flex:0 0 auto;height:820px;width:auto;border-radius:30px"></div>'), STIL_MITTE)

fails = ["Akkus, die viel zu schnell leer waren.", "iPhone 4: Antenne an der falschen Stelle. Apple verschenkt Hüllen, statt das Gerät zurückzurufen.",
         "Ein Modell verbiegt sich in der Hosentasche.", "Und trotzdem: Lieferzeiten über mehrere Monate, ohne es je gesehen zu haben."]
stufen("Apple Fails", "M", "Ich nehme ganz bewusst Apple. Die haben schon so oft etwas falsch gemacht. Akkus. Die Antenne beim iPhone 4, Apple hat Hüllen verschenkt statt das Gerät vom Markt zu nehmen. Ein iPhone, das sich in der Hosentasche verbiegt. Fails über Fails. Und trotzdem wird das neue Modell für 2.500 Euro vorbestellt.", 5,
       lambda k: eyebrow("Fails über Fails", CORAL) + h2(f"{hell('Apple hat')} {c('oft danebengelegen.')} {hell('Und trotzdem kaufen alle.')}", 76)
       + nummern(fails, k - 1, CORAL)
       + f'<div style="margin-top:20px;display:flex">{offen("Beispiele prüfen: Das Verbiegen betraf das iPhone 6 Plus, nicht das 7", "1", 18)}</div>')

stufen("Was Apple richtig macht", "M", "Weil Apple eines richtig macht: Sie kennen ihre Zielgruppe. Sie kennen deren Bedürfnisse. Und sie verpacken ihre Produkte in die passende Story. Und du hast dieselben Voraussetzungen: Du hast in der Vergangenheit großartige Ergebnisse bei deinen Kunden erzeugt. Du hast großartige Angebote.", 5,
       lambda k: eyebrow("Was Apple richtig macht")
       + reihe(karte("Apple kennt seine Zielgruppe.", label="01", size=44), karte("Apple kennt deren Bedürfnisse.", label="02", size=44, sichtbar=k >= 2),
               karte("Apple verpackt jedes Produkt in die passende Story.", label="03", size=44, sichtbar=k >= 3), top=36, hoehe=400)
       + f'<div style="margin-top:40px;display:flex;flex-direction:column">'
       + f'<div style="{unsichtbar(k >= 4)}">' + pille("Du hast großartige Ergebnisse bei deinen Kunden erzeugt. Du hast ein großartiges Angebot.") + "</div>"
       + f'<div style="{unsichtbar(k >= 5)}">' + h2(f"Du hast also {m('dieselben Voraussetzungen.')}", 84, 30) + "</div></div>", STIL_MITTE)


def spalte(titel, punkte, art):
    # Inhalt oben ausgerichtet, damit „Weniger davon“ und „Mehr davon“ auf einer Linie stehen
    farbe = MINT if art == "mint" else CORAL
    zeichen = "✓" if art == "mint" else "✕"
    return (f'<div style="flex:1;{"background:linear-gradient(160deg,#10241A,#152C20);border:1.5px solid " + MINT if art == "mint" else "background:#131312;border:1px solid #34322F"};'
            f'border-radius:26px;padding:44px;display:flex;flex-direction:column;justify-content:flex-start;gap:28px">'
            f'<div style="{MONO}font-size:18px;letter-spacing:.14em;color:{farbe}">{titel}</div>{haken(punkte, farbe, zeichen)}</div>')


neu("Kommunikation 2027", "M", "Vor ein paar Jahren hat es gereicht zu sagen: Ich mache X, und ich mache das so und so. Heute hat jeder schon Erfahrungen damit. Um 2027 Vertrauen zu bekommen, brauchst du weniger Tipps, Expertise und Methode. Und mehr Zielgruppenverständnis, ihre Focus Pain Situations, eine Positionierung, die auf ihr Motiv einzahlt, und eine Brücke: dein transformatives Angebot.",
    h2(f"Was 2027 {m('Vertrauen')} schafft.", 84)
    + reihe(spalte("WENIGER DAVON", ["Fach-Content: Tipps und Tricks", "Expertise", "Deine Methode", "Belehrend wirken"], "coral"),
            spalte("MEHR DAVON", ["Zielgruppenverständnis", "Bedürfnisse und Focus Pain Situations",
                                  f"Positionierung auf das {m('verkaufspsychologische')} Motiv deiner Zielgruppe",
                                  "Eine Brücke bauen: dein transformatives Angebot"], "mint"), gap=36, top=44))

stufen("UA OS", "M", "Stell dir vor, du hast ein System: unser UA OS. Live, maximal drei bis vier Minuten: Deine letzten zehn Testimonials in die KI, sie zieht die Kundenworte raus, du vergleichst mit deinem Angebotstext. Die KI erfindet nichts, sie zeigt dir, was du schon gesagt bekommen hast. KI ersetzt kein System. Sie macht es leichter zu fahren.", 2,
       lambda k: live_badge() + h2(f"Stell dir vor, du hast ein System: {m('UA OS.')}", 80, 28)
       + reihe(karte("Deine letzten 10 Testimonials", label="Schritt 1"), karte("Die KI zieht die Kundenworte raus", label="Schritt 2"),
               karte("Vergleich mit deinem Angebotstext", "Bei den meisten klafft eine Lücke.", "mint", "Schritt 3"), top=44)
       + f'<div style="margin-top:36px;display:flex;gap:24px;align-items:center;{"" if k >= 2 else "visibility:hidden"}">'
       + pille("KI ersetzt kein System. Sie macht es leichter zu fahren.") + "</div>"
       + f'<div style="margin-top:18px;display:flex">{offen("Name UA OS final? Testimonials für die Demo bereitlegen (nur lokal)", "1", 18)}</div>')

# ---- Teil 2 · Volle Pipeline ---------------------------------------------------------------------------
kapitel("2", "Volle Pipeline", "Du brauchst Menschen, die mit dir sprechen.", "A", "Teil 2. Du brauchst eine volle Pipeline.")

weg = [("40", "Nachrichten an die Richtigen", False), ("[?]", "Antworten", False), ("[?]", "Gespräche", False),
       ("3 bis 4", "Termine im Kalender", True), ("1 bis 2", "neue Kunden, je nach Abschlussquote", True)]


def rechenweg(k=99, zeilen=None):
    html = "".join(
        f'<div style="{"" if k > j else "visibility:hidden;"}width:1100px;margin:0 auto;flex:1;display:flex;align-items:center;gap:40px;padding:0 50px;border-radius:20px;'
        f'{"background:linear-gradient(90deg,#10241A,#1a4231);border:1.5px solid " + MINT if gut else "background:#1C1B1A;border:1px solid #34322F"}">'
        f'<div style="width:260px;font-size:60px;font-weight:700;color:{MINT if gut else "#F4F2EC"}">{z}</div>'
        f'<div style="font-size:34px;color:{"#F4F2EC" if gut else "#B4AFA6"}">{t_}</div></div>'
        for j, (z, t_, gut) in enumerate(zeilen or weg))
    return f'<div style="margin-top:40px;flex:1;display:flex;flex-direction:column;gap:14px">{html}</div>'


weg_100 = [("100", "Massennachrichten", False), ("[?]", "Antworten", False), ("[?]", "Gespräche", False),
           ("3 bis 4", "Termine im Kalender", True), ("1 bis 2", "neue Kunden, je nach Abschlussquote", True)]
weg_100_40 = [(f'<span style="color:#6B665F;text-decoration:line-through;text-decoration-color:{CORAL};text-decoration-thickness:6px">100</span>'
               f' <span style="color:{MINT}">40</span>', "Nachrichten an die Richtigen", False)] + weg_100[1:]

stufen("Nachrichten · 100", "A", "So lief Outreach bisher: 100 Massennachrichten. Daraus wurden 3 bis 4 Termine, je nach Abschlussquote 1 bis 2 neue Kunden. Heute brauchst du nicht mehr 100, sondern nur noch 40, die richtigen, für dasselbe Ergebnis. Die KI zeigt dir mit Signalen, wen du ansprechen solltest und warum gerade jetzt.", 7,
       lambda k: (eyebrow("Der Unterschied") + h2(f"Nicht mehr 100. {m('Nur noch 40, die richtigen.')}", 72) if k >= 7 else
                  eyebrow("Rechenbeispiel, so wie bisher") + h2(f"Aus 100 Nachrichten werden {m('1 bis 2 Kunden.')}", 72))
       + rechenweg(k, weg_100_40 if k >= 6 else weg_100)
       + f'<div style="margin-top:24px;{"" if k >= 7 else "visibility:hidden"}">' + pille("Gleiches Ergebnis. Weniger als die Hälfte der Nachrichten.") + "</div>")


neu("Das meinen wir nicht", "A", "Und damit meinen wir nicht solche Nachrichten. Ich habe diese Woche wieder zwei, drei davon bekommen. Kurz vorlesen. Das meinen wir nicht. Wir meinen persönliche Nachrichten an die Richtigen.",
    eyebrow("Das meinen wir nicht", CORAL) + h2(f"{hell('Solche Nachrichten')} {c('meinen wir nicht.')}", 84)
    + reihe(offen("Screenshot generische Pitch-Nachricht 1 (Absender unkenntlich)", "1"), offen("Screenshot generische Pitch-Nachricht 2 (Absender unkenntlich)", "1"), gap=36, top=44))

stufen("Rechenweg", "A", "Das macht das Ergebnis messbar. Aus 40 Nachrichten an die Richtigen werden 3 bis 4 Termine. Je nach Abschlussquote sind das 1 bis 2 neue Kunden. Und im persönlichen Gespräch kommt dein größter USP voll zur Geltung: deine Persönlichkeit.", 5,
       lambda k: eyebrow("Rechenbeispiel, konservativ") + h2(f"Aus 40 Nachrichten werden {m('1 bis 2 Kunden.')}", 72) + rechenweg(k)
       + f'<div style="margin-top:16px;display:flex">{offen("Erfahrungswerte für Antworten und Gespräche, jede Zahl begründet", "1", 18)}</div>')

# ---- Teil 3 · Abschluss --------------------------------------------------------------------------------
kapitel("3", "Abschluss", "Der iPhone-Effekt.", "M", "Teil 3. Nicht über Closing-Skripte reden. Zeigen, dass bei richtigem System kein harter Abschluss nötig ist.")

stufen("iPhone-Effekt", "M", "Beim iPhone macht keiner eine Einwandbehandlung. Wenn dein Angebot und deine Pipeline zusammenspielen, wird dein Abschluss zum Selbstläufer. Das ist der iPhone-Effekt.", 4,
       lambda k: eyebrow("Der iPhone-Effekt")
       + h2(f"Beim iPhone macht {m('keiner eine Einwandbehandlung.')}", 96, 30)
       + reihe(karte("Vertrauen", "Dein Angebot trifft die Zielgruppe.", size=48, sichtbar=k >= 2), karte("Volle Pipeline", "Die Richtigen sprechen mit dir.", size=48, sichtbar=k >= 3),
               karte("Selbstläufer", "Der Abschluss passiert fast von allein.", "mint", size=48, sichtbar=k >= 4), top=50, hoehe=BOX_H), STIL_MITTE)

# ---- Pitch -----------------------------------------------------------------------------------------------
neu("Garantie 2027", "A", "Unser Versprechen: Kein Return on Invest nach 90 Tagen? Dann arbeiten wir so lange mit dir weiter, wie es notwendig ist. In der Gruppe, mit priorisierten Hot Seats. Wir lassen niemanden am Anfang stehen.",
    eyebrow("Unser Versprechen") + h2(f"Wir lassen niemanden {m('am Anfang stehen.')}", 92)
    + reihe(karte("Kein ROI nach 90 Tagen?", "Das kann passieren.", size=44),
            karte("Wir arbeiten weiter mit dir, so lange es nötig ist.", "In der Gruppe, mit priorisierten Hot Seats.", "mint", size=44), gap=40)
    + f'<div style="margin-top:22px;display:flex;gap:20px">{offen("Wie messen wir ROI?", "1", 18)}{offen("Alternative im Call genannt: 3 Monate 1:1. Was gilt?", "1", 18)}</div>')

neu("Return 2027", "A", "Erinnerst du dich? Aus 40 Nachrichten an die Richtigen werden 3 bis 4 Termine, je nach Abschlussquote 1 bis 2 neue Kunden.",
    eyebrow("Zur Erinnerung") + h2(f"Aus 40 Nachrichten werden {m('1 bis 2 Kunden.')}", 72) + rechenweg())


def bonus_einwand(nr, einwand, titel, text):
    return (f'<div style="flex:1;min-height:380px;background:#F0EEE6;color:#141413;border-radius:24px;padding:34px 28px;display:flex;flex-direction:column;gap:16px;'
            f'transform:rotate({(-2, 2, -1, 3)[nr - 1]}deg);box-shadow:0 30px 60px -25px #000">'
            f'<div style="display:flex;justify-content:flex-end;align-items:center">'
            f'<span style="{MONO}font-size:14px;letter-spacing:.12em;background:#141413;color:#F0EEE6;border-radius:8px;padding:6px 12px">BONUS {nr}</span></div>'
            f'<div style="font-size:34px;font-weight:700;line-height:1.15">{titel}</div><div style="font-size:22px;line-height:1.4;color:#5A564F">{text}</div></div>')


neu("Boni nach Einwand", "M", "Jeder Bonus beantwortet einen Einwand. Bonus 1, Thema Zeit: Was auch immer in den nächsten drei Monaten dazwischenkommt, Ferien, Weihnachten und Co., hängen wir hinten dran. Du kannst die drei Monate komplett nochmal mit uns durchgehen, als würdest du neu starten. Damit gibt es keine Ausrede.",
    '<div style="text-align:center">' + h2(f"Dein exklusiver {m('Webinar-Bonus.')}", 84, 0) + "</div>"
    + f'<div style="margin-top:80px;display:flex;gap:26px;padding:0 20px;align-items:center">'
    + bonus_einwand(1, "ZEIT", "+3 Monate", "Ferien, Weihnachten, was auch immer dazwischenkommt: hängen wir hinten dran. Alle 3 Monate komplett nutzbar.")
    + bonus_einwand(2, "GELD", "[Bonus 2]", "Kandidat. Muss den Geld-Einwand entkräften.")
    + bonus_einwand(3, "[EINWAND]", "[Bonus 3]", "Kandidat.")
    + bonus_einwand(4, "[EINWAND]", "[Bonus 4]", "Kandidat.")
    + "</div>",
    "padding:70px 96px;background:radial-gradient(1200px 700px at 50% 40%, #152C20, #0D0D0D);display:flex;flex-direction:column;justify-content:center")

neu("Code einlösen", "A", "Erinnerst du dich an den Code vom Anfang? Nenn ihn im Strategie-Call. Dann bekommst du dein Geschenk: einen KI-Skill, der dir zeigt, was dir auf LinkedIn noch fehlt.",
    f'<div style="text-align:center">{eyebrow("Erinnerst du dich an deinen Code?")}</div>' + code_box()
    + sub(f"Nenn ihn im Strategie-Call. {w('Dann bekommst du dein Geschenk:')} einen KI-Skill, der dir zeigt, was dir auf LinkedIn noch fehlt.", 36, 40).replace("max-width:1500px", "max-width:1400px;text-align:center;margin-left:auto;margin-right:auto")
    + f'<div style="margin-top:28px;display:flex;justify-content:center">{offen("Skill bauen: LinkedIn-Profil-Roaster oder Focus-Pain-Diagnose", "0 0 auto", 18)}</div>', ZENTRIERT)

neu("iPhone-Effekt · Schluss", "A", "Zum Schluss: Wenn dein Angebot und deine Pipeline zusammenspielen, verkaufst du wie Apple. Ohne Einwandbehandlung. Das ist der iPhone-Effekt. Und genau den bauen wir in 90 Tagen mit dir.",
    f'<div style="text-align:center">{eyebrow("Zum Schluss")}</div>'
    + f'<div style="margin-top:30px;text-align:center;font-size:104px;font-weight:700;letter-spacing:-0.03em;line-height:1.05">Vertrauen plus volle Pipeline<br>ist dein {m("iPhone-Effekt.")}</div>'
    + sub("Kein Überzeugen. Keine Einwandbehandlung. Menschen, die längst wissen, dass du das Richtige für sie bist.", 38, 44).replace("max-width:1500px", "max-width:1400px;text-align:center;margin-left:auto;margin-right:auto"),
    ZENTRIERT)


# ---- Ablauf: verkaufspsychologisch gestrafft, Stand Skript 23.10.2026 (22.10.2026) -------------------------------------------
# Jede Zeile: Folienname und welche Stufen gezeigt werden. "alle" = jede Aufbaustufe, "letzte" = nur die fertige Folie,
# Liste = genau diese Stufen (1-basiert). Folien, die hier fehlen, werden gebaut, aber nicht gezeigt.
ABLAUF = [
    # 1. Hook und Vertrauen
    ("Titel", "alle"), ("Video · Unternehmensathlet", "alle"), ("Hook", "alle"), ("Gib uns eine Chance", "alle"),
    ("Social Proof früh", "alle"), ("Code merken", "alle"),
    # 2. Zustand abholen
    ("Zustand · Kalender", "alle"), ("Zustand · LinkedIn", "alle"), ("Umfrage 1", "alle"),
    # 3. Marktlage
    ("Marktlage · 1 von 2", "alle"), ("Marktlage · Zahlen", "alle"), ("Kein System", "alle"),
    # 4. Alte Welt, neue Welt, Vertrauenskrise
    ("Alte Welt · Covid", "alle"), ("LinkedIn ist tot?", "alle"), ("Vertrauenskrise 2027", "alle"),
    # 5. Chance, Fenster, KI-Warnung
    ("Wendepunkt", "alle"), ("Chance · Fenster", "alle"), ("Chance · Umfrage", "alle"), ("KI ersetzt nichts", "alle"),
    # 6. Case, Agenda, Filter
    ("Case-Teaser", "alle"), ("Heute 2027", "alle"), ("Für wen das ist", "alle"),
    # 7. Teil 1 · Vertrauen
    ("Kapitel 1", "alle"), ("Case · Kapitel 01", "alle"), ("Vertrauen braucht Zeit?", "alle"), ("iPhone", "alle"), ("Apple Fails", "alle"),
    ("Was Apple richtig macht", "alle"), ("Kommunikation 2027", "alle"), ("UA OS", "alle"),
    # 8. Teil 2 · Volle Pipeline (Alex)
    ("Kapitel 2", "alle"), ("Case · Kapitel 02", "alle"), ("Opportunity LinkedIn", "alle"), ("Denkfehler", [1, 4]),
    ("Wie deine Kunden entstehen", "alle"), ("Drei Quellen", "letzte"), ("Nachrichten · 100", "alle"),
    ("Das meinen wir nicht", "alle"), ("KI-Moment · Kontext", "alle"),
    # 9. Teil 3 · Abschluss
    ("Kapitel 3", "alle"), ("Case · Kapitel 03", "alle"), ("iPhone-Effekt", "alle"), ("Kein Geld gerade", "alle"),
    ("KI-Moment · Muster", "alle"), ("Messung", "alle"), ("Zwischenfazit", "alle"), ("Stell dir mal vor", "alle"),
    # 10. Kapazität und Vertrauensbrücke
    ("System muss gefahren werden", "alle"), ("Kapazität", "alle"), ("Wer wir sind", "alle"),
    # 11. Pitch
    ("Ein weiteres Jahr", "letzte"), ("Zwei Optionen", "alle"), ("Woran es scheitert", "letzte"), ("Ergebnis zuerst", "alle"),
    ("Was ist das konkret", "alle"), ("Der Weg", "letzte"), ("Stimmen · Umsetzungsbegleitung", "alle"), ("Einmal aufbauen", "alle"),
    ("Drei Cases", "alle"), ("Marktanker", "alle"), ("Dein Invest", "alle"), ("Garantie 2027", "alle"), ("Return 2027", "alle"),
    ("Proof · Gruppen-Chat", "alle"), ("Referenz nach Invest", "alle"),
    # 12. Qualifizieren, Kalender, Boni, Code, Schluss
    ("Buch dir keinen Call, wenn", "alle"), ("So läuft dein Call ab", "alle"), ("Kalender offen", "alle"), ("Boni nach Einwand", "alle"),
    ("Code einlösen", "alle"), ("Knappheit", "alle"), ("Einwände", "alle"), ("Live Q&A", "alle"), ("iPhone-Effekt · Schluss", "alle"),
    ("Finaler CTA", "alle"),
]

alle_stufen = {}
for html, wer in FOLGE:
    alle_stufen.setdefault(Deck._label(html), []).append((html, wer))
auswahl = []
for label, modus in ABLAUF:
    if label not in alle_stufen:
        raise SystemExit(f"Folie „{label}“ steht im Ablauf, wird aber nicht gebaut.")
    s = alle_stufen[label]
    auswahl += s if modus == "alle" else [s[-1]] if modus == "letzte" else [s[k - 1] for k in modus]

# Frage-Folien (Eyebrow „Frage in den Chat“ / „Umfrage im Chat“): großes Fragezeichen hinter dem Inhalt
FRAGEZEICHEN = (f'<div class="frage-deko" style="position:absolute;right:-20px;top:50%;transform:translateY(-52%);z-index:-1;'
                f'font-size:1250px;font-weight:700;line-height:1;pointer-events:none;user-select:none;opacity:.2;'
                f'background:linear-gradient(160deg,{MINT} 0%,rgba(125,219,166,0) 78%);-webkit-background-clip:text;'
                f'background-clip:text;color:transparent">?</div>')


def mit_fragezeichen(html):
    frage = re.search(r">(Frage in den Chat|Umfrage im Chat)</div>", html)
    if not (frage or 'class="zitat-deko"' in html):
        return html
    html = re.sub(r'(<section[^>]*?style=")', r"\1position:relative;z-index:0;overflow:hidden;", html, count=1)
    return html.replace("</section>", FRAGEZEICHEN + "</section>", 1) if frage else html


auswahl = [(mit_fragezeichen(f), wer) for f, wer in auswahl]
d.folien = [f for f, _ in auswahl]
d.kuerzel([(n, n, wer) for n, (_, wer) in enumerate(auswahl, 1)])
d.speichern(ZIEL, titel="LinkedIn Performance System 2027")


# ---- UA-Design ---------------------------------------------------------------------------------------------------
# Dieses Webinar läuft im UA-Design (Farben und Schriften aus dem Skill ua-design, ua_slides.js). Gebaut wird zuerst
# im Grundgerüst der Kooperation, danach werden Farben und Schriften umgesetzt. Es gibt nur diese eine Fassung.
# Die Farbbedeutung bleibt: Mint „gelöst“ → Türkis, Terracotta „Problem“ → Signalrot, Grautöne → UA-Grün.
# Gelb für OFFEN-Kästen, die Temperatur-Skala und das Claude-Logo bleiben unverändert.
UA_FARBEN = {
    # gelöst, gut, Gewinn → Türkis 2CD99C
    "#7DDBA6": "#2CD99C", "#57C98C": "#1FB585", "#A9E8C5": "#8CEBC9", "#2E8B5A": "#1E9C70", "#2C4A3A": "#1F4A3D",
    # Problem, Dringlichkeit → Signalrot D60748
    "#E8917A": "#D60748", "#B4513A": "#9E0535", "#3A1B12": "#2A0610", "#241512": "#1C050C", "#2B1915": "#22060E",
    "#5A3A30": "#4A0A1E", "#1A1613": "#140508",
    # Bühne und Karten → Schwarz und UA-Karte 141414
    "#0D0D0D": "#000000", "#131312": "#141414", "#1C1B1A": "#1A1A1A", "#34322F": "#24302E",
    # Tiefgrün für Verläufe → in Richtung UA-Grün
    "#10241A": "#0B1F1B", "#152C20": "#102A24", "#1A4231": "#17443A", "#132A1F": "#0F2722", "#3C4A45": "#33504A",
    # Text: Weiß statt Creme, Sekundärtext UA-Grün statt Grau
    "#F4F2EC": "#FFFFFF", "#EDEBE5": "#FFFFFF", "#E4E0D8": "#FFFFFF", "#F0EEE6": "#FFFFFF", "#141413": "#000000",
    "#B4AFA6": "#78A49C", "#8C8780": "#78A49C", "#6B665F": "#4E6E68", "#5A564F": "#3F5A55",
}
UA_RGB = {"125,219,166": "44,217,156", "232,145,122": "214,7,72", "244,242,236": "255,255,255", "13,13,13": "0,0,0"}
UA_SCHRIFTEN = ('<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@700;800'
                '&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
                "<style>h1,h2{font-family:'League Spartan',sans-serif!important;text-transform:uppercase;"
                "color:#78A49C;letter-spacing:-0.01em!important}"
                ".frage-deko{font-family:'League Spartan',sans-serif!important}"
                ".bleibt-tuerkis{color:#2CD99C!important}"
                # Sprechblasen komplett pink mit weißer Schrift
                ".blase{background:linear-gradient(160deg,#2A0610,#22060E)!important;border:1.5px solid #D60748!important;color:#FFFFFF!important;"
                "box-shadow:0 0 50px -22px rgba(214,7,72,.75),0 20px 40px -20px #000!important}"
                # Leichter Glanz auf farbigen Karten und Nummern-Kacheln
                ".karte,.nummer,.antwort{position:relative}"
                ".karte-coral::before,.karte-mint::before,.nummer::before,.antwort::before{content:'';position:absolute;inset:0;border-radius:inherit;"
                "background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,0) 45%);pointer-events:none}"
                # In pinken Karten keine grüne Schrift
                ".karte-coral .karte-text{color:#FF8DB4!important}"
                ".nummer-coral{background:linear-gradient(160deg,#2A0610,#22060E)!important;border:1.5px solid #D60748!important}"
                ".nummer-coral .nummer-zahl{background:#D60748!important;color:#FFFFFF!important}"
                ".nummer-mint{background:linear-gradient(160deg,#0B1F1B,#102A24)!important;border:1.5px solid #2CD99C!important}"
                ".nummer-mint .nummer-zahl{background:#2CD99C!important;color:#000000!important}"
                # Live-Pille auf dem Titel: weiße Schrift auf Signalrot
                ".badge-live{color:#FFFFFF!important}.badge-live span{background:#FFFFFF!important}"
                # Antwort-Karten: schwarz, Verlaufsrahmen mit leichtem Glanz, Schrift in der Rahmenfarbe
                ".antwort-problem{background:linear-gradient(160deg,#2A0610,#22060E)!important;border:1.5px solid #D60748!important;"
                "color:#FFFFFF;box-shadow:0 0 50px -22px rgba(214,7,72,.75)}"
                ".antwort-gut{background:linear-gradient(160deg,#0B1F1B,#102A24)!important;border:1.5px solid #2CD99C!important;"
                "color:#FFFFFF;box-shadow:0 0 50px -22px rgba(44,217,156,.7)}"
                "</style>\n")


def ua_fassung(quelle):
    """Setzt die gebaute Datei in die UA-Brandfarben und -Schriften um (überschreibt sie)."""
    t = quelle.read_text(encoding="utf-8")
    t = re.sub(r"#[0-9A-Fa-f]{6}\b", lambda m: UA_FARBEN.get(m.group(0).upper(), m.group(0)), t)
    t = re.sub(r"rgba?\(\s*(\d+\s*,\s*\d+\s*,\s*\d+)",
               lambda m: m.group(0).replace(m.group(1), UA_RGB.get(re.sub(r"\s", "", m.group(1)), m.group(1))), t)
    # Kicker und Labels: Montserrat fett statt Space Mono, Fließtext Montserrat, Überschriften League Spartan
    t = re.sub(r"'Space Mono',\s*monospace;?", "'Montserrat',sans-serif;font-weight:700;", t)
    t = t.replace("'Space Grotesk'", "'Montserrat'")
    t = re.sub(r"'?Newsreader'?,\s*serif", "'League Spartan',sans-serif", t)
    # In Überschriften nie UA-Grün und Türkis im selben Satz: Hervorhebungen werden dort weiß
    t = re.sub(r"<h2\b.*?</h2>", lambda m: m.group(0).replace("color:#2CD99C", "color:#FFFFFF"), t, flags=re.S)
    t = t.replace("</head>", UA_SCHRIFTEN + "</head>", 1)
    quelle.write_text(t, encoding="utf-8")
    print(f"UA-Design angewendet: {quelle}")


ua_fassung(ZIEL)

# Privater Bau mit echten Referenzen, nur wenn die lokale Datei existiert
if not PRIVAT and (REF_DATEI.exists() or KUNDEN_BILD.exists()):
    subprocess.run([sys.executable, __file__], env={**os.environ, "LPS_PRIVAT": "1"}, check=True)
