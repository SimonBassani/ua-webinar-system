"""Prüft, ob dieser Rechner für das Webinar-System eingerichtet ist. Ändert nichts.

    python3 tools/pruefen.py          (Windows: py tools/pruefen.py)

Zeigt für jeden Punkt ✓ (in Ordnung) oder ✗ (fehlt) mit einem Hinweis, was zu tun ist.
Der Gemini-Schlüssel wird nur auf Vorhandensein geprüft und nie angezeigt.
"""
import platform
import shutil
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from chrome import finde_browser  # noqa: E402

PFLICHT_FEHLT = []


def lauf(befehl, timeout=25):
    try:
        r = subprocess.run(befehl, capture_output=True, text=True, timeout=timeout, cwd=WURZEL)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, "", ""


def zeile(ok, titel, detail="", hinweis="", pflicht=True):
    zeichen = "✓" if ok else ("✗" if pflicht else "–")
    print(f"  {zeichen}  {titel}" + (f"   {detail}" if detail else ""))
    if not ok and hinweis:
        print(f"       → {hinweis}")
    if not ok and pflicht:
        PFLICHT_FEHLT.append(titel)


def main():
    print(f"\nWebinar-System · Einrichtungs-Check  ({platform.system()} {platform.release()})\n")

    git = shutil.which("git")
    zeile(bool(git), "git", lauf(["git", "--version"])[1] if git else "",
          "git installieren: Mac: im Terminal „xcode-select --install“; Windows: https://git-scm.com/download/win")

    gh = shutil.which("gh")
    zeile(bool(gh), "GitHub-Programm (gh)", lauf(["gh", "--version"])[1].splitlines()[0] if gh else "",
          "nur zum Teilen deiner Arbeit nötig: https://cli.github.com/", pflicht=False)

    angemeldet = False
    if gh:
        rc, _, _ = lauf(["gh", "auth", "status"])
        angemeldet = rc == 0
        konto = lauf(["gh", "api", "user", "-q", ".login"])[1] if angemeldet else ""
        zeile(angemeldet, "bei GitHub angemeldet", f"als {konto}" if konto else "", "nur zum Teilen deiner Arbeit nötig: gh auth login", pflicht=False)

    if git and (WURZEL / ".git").exists():
        rc, _, _ = lauf(["git", "ls-remote", "--exit-code", "origin", "HEAD"], timeout=30)
        zeile(rc == 0, "Verbindung zum Webinar-Repo (zum Aktualisieren)", "",
              "Internet prüfen. Zum Lesen und Arbeiten ist keine Einladung nötig", pflicht=False)
        name = lauf(["git", "config", "user.name"])[1]
        mail = lauf(["git", "config", "user.email"])[1]
        zeile(bool(name and mail), "Name für gespeicherte Änderungen", f"{name} <{mail}>" if name else "",
              "wird vom Einrichtungsassistenten gesetzt (/einrichten)")
        hooks = lauf(["git", "config", "core.hooksPath"])[1]
        zeile(hooks == ".githooks", "Schutz vor versehentlich hochgeladenen Schlüsseln", "",
              "wird vom Einrichtungsassistenten aktiviert (/einrichten)")

    uv = shutil.which("uv")
    zeile(bool(uv), "uv (startet Python-Programme)", lauf(["uv", "--version"])[1] if uv else "",
          "Mac/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh   ·   Windows (PowerShell): "
          "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")

    browser = finde_browser()
    zeile(bool(browser), "Chrome (oder Edge) für PDF und Banner", Path(browser).name if browser else "",
          "Google Chrome installieren: https://www.google.com/chrome/")

    env = WURZEL / ".env"
    schluessel_da = False
    if env.exists():
        for z in env.read_text(encoding="utf-8").splitlines():
            if z.strip().startswith("GEMINI_API_KEY="):
                wert = z.split("=", 1)[1].strip().strip('"').strip("'")
                schluessel_da = bool(wert) and "hier" not in wert.lower()
    zeile(schluessel_da, "eigener Gemini-Schlüssel (optional, nur für KI-Hintergründe)", "vorhanden" if schluessel_da else "",
          "Schlüssel erstellen: https://aistudio.google.com/apikey und in die Datei .env eintragen. Das Banner "
          "funktioniert auch ohne.", pflicht=False)

    fotos = sorted((WURZEL / "assets" / "hosts").glob("*.png"))
    zeile(len(fotos) >= 2, "freigestellte Fotos der Sprecher", ", ".join(f.stem for f in fotos),
          "eigenes Foto freistellen: siehe Skill webinar-banner", pflicht=False)

    fertig = (WURZEL / ".einrichtung-fertig").exists()
    zeile(fertig, "Einrichtungsassistent abgeschlossen", "", "in Claude Code „/einrichten“ eingeben", pflicht=False)

    print()
    if PFLICHT_FEHLT:
        print("Noch zu tun:  " + " · ".join(PFLICHT_FEHLT))
    else:
        print("Alles Wichtige ist bereit.")
    print()


if __name__ == "__main__":
    main()
