# Deck-HTML → PDF (eine Folie pro Seite) + Vorschau-Bild für ausgewählte Folien.
#
#   uv run --with-requirements requirements/deck.txt python pdf.py <deck.html> [folien,kommagetrennt]
#
# Es entsteht ein Bild-PDF: Chrome macht von jeder Folie einen Screenshot (1,5-fach), daraus wird
# das PDF zusammengesetzt. Grund: Weiche Schatten brechen im normalen Vektor-PDF auf fremden Geräten
# (iPad, Handy). Bilder sehen überall gleich aus. Siehe docs/04-build-anleitung.md.
#
# Das Vorschau-Bild der genannten Folien liegt danach in einem temporären Ordner, der Pfad wird
# ausgegeben. Zum Prüfen vor dem Webinar.
import concurrent.futures as cf
import io
import re
import sys
import tempfile
from pathlib import Path

import fitz
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from chrome import screenshot  # noqa: E402

SCALE = 1.5
SRC = Path(sys.argv[1]).resolve()
PDF = SRC.with_suffix(".pdf")
WORK = Path(tempfile.gettempdir()) / "deck_pdfwork"
WORK.mkdir(exist_ok=True)

h = SRC.read_text(encoding="utf-8")
ms = list(re.finditer(r'<div class="slide[^"]*"><section.*?</section></div>', h, re.S))
if not ms:
    sys.exit("Keine Folien in der Datei gefunden.")
head = h[:ms[0].start()].replace("</head>", (
    "<style>html,body{overflow:hidden!important;background:#0D0D0D!important;margin:0}"
    "#stage{position:static!important;display:block!important}#deck{transform:none!important}"
    ".slide{display:block!important}*{animation:none!important}</style></head>"), 1)


def render(i):
    seite = WORK / f"s{i + 1:02d}.html"
    seite.write_text(head + ms[i].group(0).replace('class="slide active"', 'class="slide"')
                     + "</div></div></body></html>", encoding="utf-8")
    png = screenshot(seite, WORK / f"s{i + 1:02d}.png", 1920, 1080, SCALE)
    img = Image.open(png).convert("RGB")
    puffer = io.BytesIO()
    img.save(puffer, "JPEG", quality=88, optimize=True)
    return puffer.getvalue()


with cf.ThreadPoolExecutor(4) as pool:
    jpgs = list(pool.map(render, range(len(ms))))

doc = fitz.open()
for daten in jpgs:
    seite = doc.new_page(width=1440, height=810)
    seite.insert_image(seite.rect, stream=daten)
doc.save(PDF, deflate=True)
print(PDF, doc.page_count, "Seiten", round(PDF.stat().st_size / 1e6, 1), "MB")

folien = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else []
for n, gruppe in enumerate([folien[k:k + 6] for k in range(0, len(folien), 6)]):
    bogen = Image.new("RGB", (1440, 405 * ((len(gruppe) + 1) // 2)), "white")
    for j, nr in enumerate(gruppe):
        kachel = Image.open(io.BytesIO(jpgs[nr - 1])).resize((720, 405))
        bogen.paste(kachel, ((j % 2) * 720, (j // 2) * 405))
    ziel = WORK / f"vorschau{n + 1}.png"
    bogen.save(ziel)
    print("Vorschau:", ziel, gruppe)
