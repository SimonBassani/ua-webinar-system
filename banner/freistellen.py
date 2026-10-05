"""Person aus einem Foto freistellen (Hintergrund entfernen) → PNG mit Transparenz.

    uv run --with-requirements requirements/freistellen.txt python banner/freistellen.py foto.jpg
    uv run --with-requirements requirements/freistellen.txt python banner/freistellen.py foto.jpg -o assets/hosts/alex.png

Beim allerersten Lauf lädt das Programm ein KI-Modell (ca. 170 MB) herunter. Das dauert einige
Minuten, danach ist es gespeichert und jeder weitere Lauf geht schnell.

Tipps für gute Ergebnisse:
- Foto mit klarem Hintergrund (Wand, Studio), Person gut ausgeleuchtet, Hände sichtbar.
- Halbnah (bis zur Hüfte) funktioniert am besten für Banner. Die Pose sollte zur Mitte zeigen.
"""
import argparse
from pathlib import Path

from PIL import Image


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("foto", help="Eingabefoto (JPG oder PNG)")
    p.add_argument("-o", "--ausgabe", help="Zieldatei (PNG). Standard: <foto>-frei.png")
    p.add_argument("--modell", default="u2net_human_seg", help="rembg-Modell (Standard für Personen)")
    a = p.parse_args()

    quelle = Path(a.foto)
    if not quelle.exists():
        raise SystemExit(f"Foto nicht gefunden: {quelle}")
    ziel = Path(a.ausgabe) if a.ausgabe else quelle.with_name(quelle.stem + "-frei.png")
    ziel.parent.mkdir(parents=True, exist_ok=True)

    from rembg import new_session, remove  # erst hier importieren: der Import ist langsam

    print("Modell wird geladen (beim ersten Mal ein größerer Download) …")
    sitzung = new_session(a.modell)
    bild = Image.open(quelle).convert("RGB")
    frei = remove(bild, session=sitzung)
    box = frei.getbbox()  # überflüssigen transparenten Rand abschneiden
    if box:
        frei = frei.crop(box)
    frei.save(ziel)
    print(f"Fertig: {ziel}  ({frei.width}×{frei.height} px)")


if __name__ == "__main__":
    main()
