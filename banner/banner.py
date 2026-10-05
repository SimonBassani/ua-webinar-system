"""Webinar-Banner (LinkedIn-Event, Thumbnail) aus einer Konfigurationsdatei bauen.

    uv run --with-requirements requirements/banner.txt python banner/banner.py banner/beispiel/config.json

Es entstehen zwei Dateien im Ordner `ausgabe` (Standard: banner/ausgabe/):
    <name>.png   3840 × 2160, volle Qualität
    <name>.jpg   1920 × 1080, klein genug zum Verschicken

Alle Pfade in der Konfiguration gelten ab dem Hauptordner des Repos. Das Banner läuft komplett ohne
KI-Bildgenerierung. Wer einen eigenen Hintergrund möchte, erzeugt ihn mit gemini_bild.py und trägt
ihn unter "hintergrund" ein.
"""
import argparse
import base64
import html
import io
import json
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL / "tools"))
from chrome import screenshot  # noqa: E402

FARBEN = {"mint": "#7DDBA6", "coral": "#E8917A", "terracotta": "#E8917A", "gelb": "#E8C97A"}
MINT, CORAL = FARBEN["mint"], FARBEN["coral"]
MONO = "font-family:'Space Mono',monospace;"
CLAUDE_PUNKTE = [(50.0, 3.0), (67.8, 22.2), (89.1, 32.1), (79.7, 54.3), (84.0, 79.5), (59.6, 82.6),
                 (37.6, 92.2), (26.6, 70.3), (4.5, 56.5), (18.2, 35.5), (27.3, 14.7)]


def pfad(p):
    q = Path(p)
    return q if q.is_absolute() else WURZEL / q


def daten_uri(p, max_hoehe=1800):
    """Bild verkleinern und als eingebetteten Text zurückgeben (das HTML bleibt eine einzelne Datei)."""
    bild = Image.open(pfad(p))
    if bild.height > max_hoehe:
        bild = bild.resize((round(bild.width * max_hoehe / bild.height), max_hoehe), Image.LANCZOS)
    puffer = io.BytesIO()
    if bild.mode == "RGBA":
        bild.save(puffer, "PNG")
        mime = "png"
    else:
        bild.convert("RGB").save(puffer, "JPEG", quality=92)
        mime = "jpeg"
    return f"data:image/{mime};base64," + base64.b64encode(puffer.getvalue()).decode(), bild.size


def text(t, farbe=CORAL):
    """HTML-sicher machen; [[so]] markierte Teile werden in `farbe` hervorgehoben."""
    sauber = html.escape(str(t))
    return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span style="color:{farbe}">{m.group(1)}</span>', sauber)


def claude_logo(px, strich=7):
    linien = "".join(f'<line x1="50" y1="50" x2="{x}" y2="{y}"/>' for x, y in CLAUDE_PUNKTE)
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100" fill="none" style="display:block">'
            f'<g stroke="#D97757" stroke-width="{strich}" stroke-linecap="round">{linien}</g></svg>')


def host_html(h, index):
    seite = h.get("seite", "links" if index == 0 else "rechts")
    farbe = FARBEN.get(h.get("farbe", "mint" if seite == "links" else "coral"), MINT)
    uri, (b, hoehe_px) = daten_uri(h["foto"])
    seitenverhaeltnis = b / hoehe_px
    beschnitt = float(h.get("beschnitt", 0.0))
    # Höhe so wählen, dass die Person nicht in den Text in der Mitte ragt (max. ~600 px breit)
    hoehe = min(float(h.get("hoehe", 1000)), 600 / seitenverhaeltnis)
    sichtbar = hoehe * (1 - beschnitt)
    x = int(h.get("x", 0))
    rand = f"left:{x - 20}px" if seite == "links" else f"right:{x - 20}px"   # positiv = zur Mitte hin
    spiegeln = "transform:scaleX(-1);" if h.get("spiegeln") else ""
    pille_x = 150 if seite == "links" else 150
    pille_seite = f"left:{pille_x}px" if seite == "links" else f"right:{pille_x}px"
    pfeil_seite = f"left:{pille_x + 70}px" if seite == "links" else f"right:{pille_x + 70}px"
    pfeil_spiegel = "" if seite == "links" else "transform:scaleX(-1);"
    name = html.escape(h["name"])
    firma = html.escape(h.get("firma", ""))
    return (
        # Der Schein (drop-shadow) liegt auf dem äußeren Rahmen, damit er nicht eckig abgeschnitten wird
        f'<div style="position:absolute;{rand};bottom:0;width:{hoehe * seitenverhaeltnis:.0f}px;height:{sichtbar:.0f}px;overflow:hidden;'
        f'filter:drop-shadow(0 0 46px {farbe}59) drop-shadow(0 24px 40px rgba(0,0,0,.6))">'
        f'<img src="{uri}" alt="{name}" style="position:absolute;left:0;top:0;height:{hoehe:.0f}px;{spiegeln}"></div>'
        f'<svg style="position:absolute;{pfeil_seite};bottom:104px;{pfeil_spiegel}" width="62" height="120" viewBox="0 0 62 120" fill="none">'
        f'<path d="M14 116 C 4 84, 4 46, 36 14" stroke="{farbe}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M20 10 L38 12 L42 30" stroke="{farbe}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        f'<div style="position:absolute;{pille_seite};bottom:34px;display:inline-flex;align-items:baseline;gap:14px;padding:14px 30px;'
        f'border-radius:999px;border:2px solid {farbe}88;background:rgba(13,13,13,.78)">'
        f'<span style="width:11px;height:11px;border-radius:50%;background:{farbe};align-self:center"></span>'
        f'<span style="font-size:38px;font-weight:700">{name}</span>'
        f'<span style="{MONO}font-size:17px;color:#B4AFA6">{firma}</span></div>')


def karte_html(k):
    chips = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:10px;padding:10px 20px;border-radius:999px;'
        f'border:1.5px solid {FARBEN.get(c.get("farbe", "mint"), MINT)}88;background:{FARBEN.get(c.get("farbe", "mint"), MINT)}1F">'
        f'<span style="width:10px;height:10px;border-radius:50%;background:{FARBEN.get(c.get("farbe", "mint"), MINT)}"></span>'
        f'<span style="font-size:24px;font-weight:600">{html.escape(c["text"])}</span>'
        f'<span style="{MONO}font-size:15px;font-weight:700;color:{FARBEN.get(c.get("farbe", "mint"), MINT)}">{html.escape(c.get("tag", ""))}</span></span>'
        for c in k.get("chips", []))
    ergebnis = (f'<span style="{MONO}font-size:30px;font-weight:700;color:{CORAL}">→ {html.escape(k["ergebnis"])}</span>'
                if k.get("ergebnis") else "")
    status = (f'<span style="{MONO}font-size:19px;color:{MINT}">● {html.escape(k["status"])}</span>' if k.get("status") else "")
    return (
        f'<div style="margin-top:34px;width:760px;box-sizing:border-box;background:rgba(19,19,18,.92);border:1.5px solid #34322F;'
        f'border-radius:24px;padding:22px 28px;box-shadow:0 30px 70px -30px rgba(0,0,0,.9)">'
        f'<div style="display:flex;align-items:center;gap:16px"><div style="width:54px;height:54px;border-radius:14px;background:#F0EEE6;'
        f'display:flex;align-items:center;justify-content:center">{claude_logo(36)}</div>'
        f'<span style="font-size:32px;font-weight:700">{html.escape(k.get("titel", ""))}</span>'
        f'<span style="margin-left:auto">{status}</span></div>'
        f'<div style="margin-top:18px;display:flex;align-items:center;gap:16px;flex-wrap:wrap">{chips}{ergebnis}</div></div>')


def baue_html(c):
    hosts = c["hosts"]
    if len(hosts) != 2:
        sys.exit("In der Konfiguration müssen genau zwei Personen unter \"hosts\" stehen.")
    for h in hosts:
        if not pfad(h["foto"]).exists():
            sys.exit(f"Foto nicht gefunden: {h['foto']}  (zuerst freistellen: banner/freistellen.py)")

    gross = str(c["titel_gross"])
    groesse = int(min(140, 1700 / max(len(gross), 1)))
    klein = (f'<div style="font-size:54px;font-weight:700;margin-top:26px;line-height:1">{text(c["titel_klein"])}</div>'
             if c.get("titel_klein") else "")
    untertitel = (f'<div style="margin-top:14px;font-size:44px;font-weight:700;letter-spacing:-0.01em">{text(c["untertitel"])}</div>'
                  if c.get("untertitel") else "")
    datum = (f'<div style="display:inline-flex;align-items:center;gap:12px;padding:14px 32px;border-radius:999px;background:{MINT};'
             f'color:#10241A;{MONO}font-size:25px;font-weight:700;letter-spacing:.1em;box-shadow:0 0 40px -10px {MINT}">'
             f'<span style="width:11px;height:11px;border-radius:50%;background:#10241A"></span>{html.escape(c["datum_pille"])}</div>'
             if c.get("datum_pille") else "")
    badge = (f'<div style="position:absolute;top:42px;left:50%;transform:translateX(-50%);display:inline-flex;align-items:center;gap:12px;'
             f'padding:14px 32px;border-radius:999px;background:{CORAL};color:#3A1B12;{MONO}font-size:24px;font-weight:700;'
             f'letter-spacing:.14em;box-shadow:0 0 36px -8px {CORAL}"><span style="width:11px;height:11px;border-radius:50%;background:#3A1B12"></span>'
             f'{html.escape(c["badge_oben"])}</div>' if c.get("badge_oben") else "")
    logos = ""
    for i, l in enumerate(c.get("logos", [])):
        uri, _ = daten_uri(l, 300)
        if i:
            logos += f'<span style="{MONO}font-size:22px;color:#8C8780">×</span>'
        logos += f'<img src="{uri}" style="height:46px;width:auto" alt="Logo">'
    logos_html = f'<div style="position:absolute;top:44px;left:70px;display:flex;align-items:center;gap:22px">{logos}</div>' if logos else ""

    if c.get("hintergrund"):
        uri, _ = daten_uri(c["hintergrund"], 1200)
        grund = f"background:linear-gradient(rgba(13,13,13,.55),rgba(13,13,13,.55)),url({uri}) center/cover,#0D0D0D;"
    else:
        grund = (f"background:radial-gradient(1000px 900px at 4% 62%, {MINT}4D, transparent 62%),"
                 f"radial-gradient(1000px 900px at 98% 58%, {CORAL}52, transparent 62%),"
                 "radial-gradient(900px 500px at 50% 0%, rgba(255,255,255,.04), transparent 70%),#0D0D0D;")
    karte = karte_html(c["karte"]) if c.get("karte") else ""
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Banner</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:#0D0D0D}}</style></head><body>
<div style="position:relative;width:1920px;height:1080px;overflow:hidden;color:#F4F2EC;font-family:'Space Grotesk',sans-serif;{grund}">
{logos_html}{badge}{host_html(hosts[0], 0)}{host_html(hosts[1], 1)}
<div style="position:absolute;left:50%;top:{int(c.get("text_oben", 250))}px;transform:translateX(-50%);width:1040px;display:flex;flex-direction:column;align-items:center;text-align:center">
{datum}{klein}
<div style="font-size:{groesse}px;font-weight:700;letter-spacing:-0.03em;line-height:1.02;color:{MINT};text-shadow:0 0 60px {MINT}40">{html.escape(gross)}</div>
{untertitel}{karte}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:10px;background:linear-gradient(90deg,{MINT},{CORAL})"></div>
</div></body></html>"""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("config", help="Konfigurationsdatei (JSON), Beispiel: banner/beispiel/config.json")
    a = p.parse_args()
    konfig = pfad(a.config)
    if not konfig.exists():
        sys.exit(f"Konfiguration nicht gefunden: {konfig}")
    c = json.loads(konfig.read_text(encoding="utf-8"))
    for pflicht in ("titel_gross", "hosts"):
        if pflicht not in c:
            sys.exit(f"In der Konfiguration fehlt: {pflicht}")

    ordner = pfad(c.get("ausgabe", "banner/ausgabe"))
    ordner.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]", "-", str(c.get("name", "banner"))).strip(".-") or "banner"   # nur harmlose Zeichen im Dateinamen
    seite = Path(tempfile.gettempdir()) / f"{name}-banner.html"
    seite.write_text(baue_html(c), encoding="utf-8")
    png = screenshot(seite, ordner / f"{name}.png", 1920, 1080, 2)
    Image.open(png).convert("RGB").resize((1920, 1080), Image.LANCZOS).save(ordner / f"{name}.jpg", quality=90)
    print(f"Fertig:\n  {png}\n  {ordner / (name + '.jpg')}")


if __name__ == "__main__":
    main()
