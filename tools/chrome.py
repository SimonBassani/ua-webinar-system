"""Chrome (oder Edge) im Hintergrund starten und von einer HTML-Datei einen Screenshot machen.

Läuft auf Mac, Windows und Linux. Wird von deck/pdf.py und banner/banner.py benutzt.

Warum so umständlich: Chrome beendet sich nach --screenshot nicht von selbst. Wir warten deshalb,
bis die Bilddatei fertig geschrieben ist, und beenden den Browser dann selbst. Gelegentlich bricht
Chrome ab, deshalb gibt es mehrere Versuche.
"""
import os
import platform
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def finde_browser():
    """Gibt den Pfad zu Chrome (oder ersatzweise Edge) zurück, sonst None."""
    system = platform.system()
    kandidaten = []
    if system == "Darwin":
        kandidaten += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                       "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    elif system == "Windows":
        for basis in filter(None, [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"),
                                   os.environ.get("LOCALAPPDATA")]):
            kandidaten += [rf"{basis}\Google\Chrome\Application\chrome.exe",
                           rf"{basis}\Microsoft\Edge\Application\msedge.exe"]
    else:
        for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
            pfad = shutil.which(name)
            if pfad:
                kandidaten.append(pfad)
    for k in kandidaten:
        if Path(k).exists():
            return k
    return None


def screenshot(html, ziel, breite=1920, hoehe=1080, scale=1.5, versuche=4, warte_sekunden=120):
    """Rendert `html` (Pfad) als PNG nach `ziel`. Gibt den Zielpfad zurück."""
    browser = finde_browser()
    if not browser:
        raise RuntimeError("Weder Chrome noch Edge gefunden. Bitte Google Chrome installieren: "
                           "https://www.google.com/chrome/")
    html = Path(html).resolve()
    ziel = Path(ziel).resolve()
    ziel.parent.mkdir(parents=True, exist_ok=True)

    for versuch in range(1, versuche + 1):
        ziel.unlink(missing_ok=True)
        profil = tempfile.mkdtemp(prefix="webinar-chrome-")
        prozess = subprocess.Popen(
            [browser, "--headless=new", "--hide-scrollbars", "--disable-gpu", "--no-first-run",
             f"--force-device-scale-factor={scale}", f"--window-size={breite},{hoehe}",
             f"--user-data-dir={profil}", "--virtual-time-budget=6000",
             f"--screenshot={ziel}", html.as_uri()],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        letzte_groesse, stabil = -1, 0
        try:
            for _ in range(warte_sekunden * 2):
                time.sleep(0.5)
                groesse = ziel.stat().st_size if ziel.exists() else 0
                if prozess.poll() is not None and groesse:
                    break
                stabil = stabil + 1 if groesse and groesse == letzte_groesse else 0
                letzte_groesse = groesse
                if stabil >= 4:
                    break
        finally:
            if prozess.poll() is None:
                prozess.kill()
            shutil.rmtree(profil, ignore_errors=True)
        if ziel.exists() and ziel.stat().st_size:
            return ziel
    raise RuntimeError(f"Screenshot fehlgeschlagen nach {versuche} Versuchen: {html.name}")
