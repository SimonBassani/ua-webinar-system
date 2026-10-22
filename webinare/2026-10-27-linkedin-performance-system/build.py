"""Deck „In 90 Tagen qualifizierte Termine im Kalender“ · LinkedIn Performance System 2027 · 27.10.2026

Rohfassung nach folienplan.md (gleicher Ordner). Ausgangsstand ist das Referenz-Deck; übernommen werden
Titel, „Kalender offen“ und „Live Q&A“ (Logos, Look). Alle anderen Folien sind neu, weil Copilot und
Live-Demo von Simon in diesem Webinar wegfallen.

Gelbe gestrichelte Kästen mit „OFFEN“ = Material fehlt oder ist nicht entschieden. Vor dem Webinar
müssen alle verschwunden sein. Echte Kundennamen und Zahlen stehen nur lokal in deck/referenzen/.

    uv run python webinare/2026-10-27-linkedin-performance-system/build.py
"""
import base64
import sys
from pathlib import Path

WURZEL = next(p for p in Path(__file__).resolve().parents if (p / "deck" / "folien_lib.py").exists())
sys.path.insert(0, str(WURZEL / "deck"))
from folien_lib import *  # noqa: E402,F401,F403

AUSGANG = WURZEL / "deck" / "Akquise-Copilot.html"
ZIEL = Path(__file__).resolve().parent / "deck.html"

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
    unten = f'<div style="font-size:31px;line-height:1.45;color:#B4AFA6">{text}</div>' if text else ""
    vis = "" if sichtbar else "visibility:hidden;"
    return (f'<div style="{vis}flex:1;{rahmen};border-radius:26px;padding:40px 38px;display:flex;flex-direction:column;'
            f'justify-content:center;gap:18px">{kopf}<div style="font-size:{size}px;font-weight:600;line-height:1.25">{titel}</div>{unten}</div>')


def reihe(*karten, gap=32, top=52):
    return f'<div style="margin-top:{top}px;display:flex;gap:{gap}px;flex:1;min-height:0">{"".join(karten)}</div>'


def zitat(t, size=88):
    return (f'<div style="font-family:Newsreader,serif;font-size:220px;line-height:.6;color:{MINT};opacity:.5">„</div>'
            f'<div style="font-size:{size}px;font-weight:700;letter-spacing:-0.025em;line-height:1.08;max-width:1600px">{t}</div>')


def foto(name, px=190, rand=MINT):
    for ordner in (FOTOS, REFERENZEN):
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
    karten = "".join(
        f'<div style="{"" if k > j else "visibility:hidden;"}display:flex;align-items:center;gap:28px;background:#131312;'
        f'border:1px solid #34322F;border-radius:22px;padding:0 36px">'
        f'<div style="width:64px;height:64px;border-radius:16px;background:{farbe};color:#10241A;flex-shrink:0;display:flex;'
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
t = alt["Titel"]
d.folien = [t]
d.ed("Titel", "Inkl. Live-Demo in Claude", "Inkl. Live-Demo")
d.ed("Titel", "Dein Akquise-Copilot:<br>", "LinkedIn Performance<br>")
d.ed("Titel", "doppelter Umsatz aus alten Kontakten!", "System 2027")
d.ed("Titel", "Der Akquise-Copilot zeigt dir, wer heute in deiner Pipeline dran ist.", "In 90 Tagen qualifizierte Termine im Kalender.")
d.ed("Titel", "Für Trainer, Coaches &amp; Berater mit einem Angebot, das sich bereits verkauft.",
     "Für Selbstständige, Freelancer und Agenturen, deren Angebot sich schon verkauft.")
d.ed("Titel", "22.09.2026", "Di · 27.10.2026")
# Webinar läuft unter unternehmensathleten: kein DigiUp, kein Claude-Logo
d.ed("Titel", "× DigiUp", "")
d.ed("Titel", '<div style="position:absolute;right:-80px;bottom:-110px;opacity:.12;pointer-events:none">', '<div style="display:none">')
d.notes("Titel", "Willkommen zum LinkedIn Performance System 2027. Heute geht es darum, wie aus LinkedIn in 90 Tagen qualifizierte Termine in deinem Kalender werden. Live, keine Aufzeichnung.")
FOLGE.append((d.folien[0], "A"))

neu("Video · Unternehmensathlet", "A", "Unternehmensathlet-Video abspielen. Vermittelt sofort unsere Werte, filtert und unterscheidet uns von anderen.",
    eyebrow("Bevor wir starten")
    + f'<div style="margin-top:36px;flex:1;border-radius:32px;background:#131312;border:1px solid #34322F;display:flex;'
      f'align-items:center;justify-content:center;flex-direction:column;gap:28px">'
      f'<div style="width:150px;height:150px;border-radius:50%;background:{MINT};display:flex;align-items:center;justify-content:center">'
      f'<div style="width:0;height:0;border-left:52px solid #10241A;border-top:32px solid transparent;border-bottom:32px solid transparent;margin-left:12px"></div></div>'
      f'<div style="font-size:48px;font-weight:700">Unternehmens{m("athlet")}</div></div>')


def antworten(opts, farbe="#34322F"):
    return ('<div style="margin-top:56px;display:flex;gap:20px;height:240px">'
            + "".join(f'<div style="flex:1;border:1.5px solid {farbe};border-radius:20px;background:#131312;display:flex;align-items:center;'
                      f'justify-content:center;text-align:center;padding:24px;font-size:40px;font-weight:600;line-height:1.2">{o}</div>' for o in opts)
            + "</div>")


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


def stimme(j):
    return (f'<div style="background:#131312;border:1px solid #34322F;border-radius:22px;padding:26px;display:flex;flex-direction:column;gap:14px">'
            f'<div style="height:150px;border-radius:14px;border:2px dashed {GELB};display:flex;align-items:center;justify-content:center;{MONO}font-size:16px;color:{GELB}">VIDEO / FOTO</div>'
            f'<div style="font-size:26px;font-weight:700">[Name {j}]</div><div style="font-size:20px;color:{MINT}">[Ergebnis in einem Satz]</div></div>')


neu("Social Proof früh", "A", "Social Proof gleich am Anfang. Diese Menschen saßen vor einigen Monaten genau da, wo du heute sitzt. Über 250 Selbstständige haben mit uns ihre Kundengewinnung aufgebaut.",
    eyebrow("Bevor es losgeht") + h2(f"Über {m('250 Selbstständige')} haben mit uns ihre Kundengewinnung aufgebaut.", 70)
    + sub("Viele von ihnen saßen vor ein paar Monaten genau da, wo du heute sitzt.", 32, 20)
    + f'<div style="margin-top:36px;flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:20px">{"".join(stimme(j) for j in range(1, 6))}</div>'
    + f'<div style="margin-top:22px;display:flex">{offen("5 Stimmen mit Foto oder Video-Screenshot und Freigabe · Formulierung zu 250+ bestätigen", "1", 18)}</div>')

neu("Umfrage 1", "M", "Umfrage im Chat. Antworten vorlesen.",
    eyebrow("Umfrage im Chat")
    + h2(f"Wie sicher bist du, dass LinkedIn für dich die richtige Plattform ist, um Kunden zu gewinnen, {m('wenn man weiß, wie?')}", 72, 30)
    + antworten(["Sehr sicher", "Eher sicher", "Unsicher", "Gar nicht"]), STIL_MITTE)

neu("Umfrage 2", "M", "Zweite Umfrage. Die Antworten sind unsere Einwand-Landkarte für den Rest des Webinars.",
    eyebrow("Umfrage im Chat")
    + h2(f"Was hält dich bei Kundengewinnung auf LinkedIn {c('aktuell am meisten zurück?')}", 76, 30)
    + antworten(["Zeit", "Wissen", "Technik", "Geld", "Ich weiß nicht, wo ich anfangen soll"], CORAL), STIL_MITTE)

chaos = [("KI-Content überall", 6, 8, -4), ("Reichweite sinkt", 54, 4, 3), ("Vernetzt und sofort gepitcht", 28, 34, -2),
         ("Der Feed langweilt", 64, 40, 5), ("„Lass uns mal telefonieren“", 6, 62, 2), ("Noch ein Carousel", 46, 70, -3)]
neu("LinkedIn ist tot?", "A", "Der Elefant im Raum. Viele haben LinkedIn schon totgesagt. KI flutet den Feed, Reichweiten sinken, bei jeder Vernetzung kommt die nächste Pitch-Nachricht.",
    eyebrow("Der Elefant im Raum", CORAL) + h2(f"LinkedIn ist {c('tot?')}", 110)
    + '<div style="position:relative;flex:1;margin-top:20px">'
    + "".join(f'<div style="position:absolute;left:{x}%;top:{y}%;transform:rotate({r}deg);background:#1C1B1A;border:1px solid {CORAL};'
              f'border-radius:18px;padding:22px 30px;font-size:30px;font-weight:600;color:#F4F2EC;box-shadow:0 20px 40px -20px #000">{txt}</div>'
              for txt, x, y, r in chaos) + '</div>')

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

neu("Kein System", "A", "Wenn du nicht weißt, welche Schritte heute deinen Kalender nächste Woche füllen, hast du kein System.",
    zitat(f"Wenn du nicht weißt, welche Schritte heute deinen Kalender nächste Woche füllen, {c('hast du kein System.')}", 80), STIL_MITTE)

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

neu("Case-Teaser · [Case 1]", "A", "Nur einer, als Vorgriff. Die volle Auflösung kommt vor dem Pitch: Am Ende zeig ich euch, was sich bei denen konkret verändert hat. Nicht Motivation. Steuerung.",
    eyebrow("Ein Vorgriff") + f'<div style="margin-top:40px;display:flex;align-items:center;gap:60px;flex:1">{foto("case1", 300)}'
    f'<div style="flex:1">{h2(f"[Case 1]: von [vorher] auf {m("[heute]")} im Monat.", 76, 0)}'
    + sub("Am Ende zeig ich euch, was sich konkret verändert hat. Nicht Motivation. Steuerung.", 34)
    + f'<div style="margin-top:36px;display:flex">{offen("Freigabe, Foto, Zahlen (nur lokal einsetzen)", "1", 18)}</div></div></div>')

agenda = [("01", "Foundation", "Wo du wirklich stehst und was du verkaufst."),
          ("02", "Voller Kalender", "Qualifizierte Gespräche mit Framework, geplant statt erhofft."),
          ("03", "Deal closen", "Wie aus Gesprächen Kunden werden, ohne Überzeugungsarbeit.")]
stufen("Heute", "M", "Drei Dinge heute. Wörtlich wie im Event-Text.", 3,
       lambda k: eyebrow("Das zeigen wir dir heute") + h2(f"Drei Dinge. {m('Ein System.')}", 84)
       + reihe(*[karte(titel, text, "mint", nr, sichtbar=k > j, size=64) for j, (nr, titel, text) in enumerate(agenda)])
       + f'<div style="margin-top:22px;display:flex">{offen("Kapitelnamen und Überschrift sind Arbeitstitel, Brainstorming läuft", "1", 18)}</div>')


def case_einstieg(nr, wer, notiz):
    neu(f"Case · Kapitel {nr}", wer, notiz,
        eyebrow("Aus der Praxis") + f'<div style="margin-top:36px;flex:1;display:flex;gap:48px">'
        + f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">{foto(f"case-kapitel{nr}", 200)}{h2("[Name]", 64, 0)}'
        + sub("[vorher] → [ein Hebel] → [Ergebnis]", 32, 0) + "</div>"
        + offen("Welcher Case leitet dieses Kapitel ein? Screenshot statt Zitat", "1.4") + "</div>")
# =====================================================================================================
# TEIL 2 · FOUNDATION
# =====================================================================================================
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
    + f'<div style="margin-top:22px;display:flex;align-items:center;gap:24px"><div style="font-size:30px">Du schreibst seit Jahren Nachrichten. {m("Genau damit gewinnst du deine Kunden.")}</div>'
    + offen("3 echte Beispiele, Namen mit Freigabe", "1", 16) + "</div>")

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
       + reihe(*[karte(tt, tx, "mint", f"Quelle 0{j + 1}", sichtbar=k > j, size=46) for j, (tt, tx) in enumerate(quellen)]))


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
    + reihe(karte(f'<span style="font-size:110px;color:{CORAL}">20</span> generische Nachrichten', "Die Plattform bestraft Volumen.", "coral"),
            karte(f'<span style="font-size:110px;color:{MINT}">5</span> passende Nachrichten', "Eine Minute KI-Kontext pro Person.", "mint"), gap=40))

saeulen = [("Zielgruppe", "Positionierung", "Wem hilfst du, womit, warum du?"),
           ("Signale", "Recherche", "Wer ist gerade relevant? KI-Recherche aus Event- und Profildaten."),
           ("Nachricht", "Signature-Framework", "2 bis 3 persönliche Nachrichten in deiner Stimme."),
           ("Termin", "Kaufsignal", "Kaufsignale erkennen, nächster Schritt, Termin im Kalender.")]
stufen("Framework", "A", "Unser Framework für einen vollen Kalender, Säule für Säule. Nicht jedes Detail, aber die Reihenfolge.", 4,
       lambda k: eyebrow("Das Framework") + h2(f"Vier Säulen für einen {m('vollen Kalender.')}", 80)
       + reihe(*[f'<div style="{"" if k > j else "visibility:hidden;"}flex:1;background:linear-gradient(170deg,#10241A,#131312);border:1.5px solid {MINT if j == 3 else "#2C4A3A"};'
                 f'border-radius:26px;padding:40px 32px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:22px">'
                 f'<div style="{MONO}font-size:16px;letter-spacing:.14em;color:{MINT};border:1px solid #2C4A3A;border-radius:999px;padding:8px 18px">{tag}</div>'
                 f'<div style="font-family:Newsreader,serif;font-style:italic;font-size:54px">{name}</div>'
                 f'<div style="margin-top:auto;font-size:26px;line-height:1.4;color:#B4AFA6">{txt}</div></div>' for j, (name, tag, txt) in enumerate(saeulen)], gap=24, top=44)
       + f'<div style="margin-top:22px;display:flex">{offen("Säulen-Namen mit eurem echten DM-Framework abgleichen", "1", 18)}</div>')

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

neu("Kein Geld gerade", "M", "Der häufigste Satz in Verkaufsgesprächen gerade. Und so gehst du damit um.",
    eyebrow("Der häufigste Einwand gerade", CORAL)
    + f'<div style="margin-top:30px;font-size:120px;font-weight:700;letter-spacing:-0.03em;line-height:1;color:{CORAL}">„Ich hab gerade kein Geld.“</div>'
    + sub("So gehst du damit um:", 36, 44) + f'<div style="margin-top:24px;display:flex">{offen("Eure Antwort auf den Einwand", "1")}</div>', STIL_MITTE)

neu("KI-Moment · Muster", "A", "Nach jedem Gespräch, egal ob es ein Kunde wird: zwei Minuten, Notizen in eine KI, Muster über die letzten zehn Gespräche. Wo hakt es immer an derselben Stelle?",
    eyebrow("KI im Alltag") + h2(f"Zwei Minuten nach jedem Gespräch. {m('Muster statt Bauchgefühl.')}", 72)
    + reihe(karte("Notizen in die KI", label="Nach dem Call"), karte("Muster über 10 Gespräche", "Wo hakt es immer an derselben Stelle?", label="Jede Woche"),
            karte("Kaufsignale erkennen", "In DMs, mit Vorschlag für den nächsten Schritt.", "mint", "Im Programm")))

neu("Messung", "A", "Wenn ihr eure Zahlen aus diesen drei Bereichen kennt, wie viele Gespräche aus welcher Quelle, wie viele davon zu Kunden werden, dann wisst ihr im Oktober, wie euer Januar aussieht.",
    eyebrow("Die Brücke") + h2(f"Im Oktober wissen, wie dein {m('Januar')} aussieht.", 84)
    + reihe(karte("Welche Quelle", label="Messen"), karte("Wie viele Gespräche", label="Messen"), karte("Wie viele Kunden", label="Messen"),
            karte("Dein Januar", "Planbar.", "mint", "Ergebnis"), gap=24))

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


def founder(name, satz, fakten, bild, eb):
    return (eyebrow(eb) + f'<div style="margin-top:40px;flex:1;display:flex;align-items:center;gap:80px">{bild}'
            f'<div style="flex:1">{h2(name, 130, 0)}{sub(satz, 46, 24)}'
            + "".join(f'<div style="margin-top:26px;font-size:40px;display:flex;gap:18px"><span style="color:{MINT}">●</span>{f}</div>' for f in fakten)
            + "</div></div>")


neu("Founder · Michi", "M", "Michael, kurz: Skalierung, mehrfach gegründet, zuletzt ein Medienhaus auf über 400 Mitarbeiter.",
    founder("Michael", "Business und Skalierung.", ["Mehrfach gegründet", "Zuletzt ein Medienhaus auf über 400 Mitarbeiter"], foto("michi", 460), "Wer wir sind"))

neu("Founder · Alex", "A", "Alex, kurz: Sportökonom, über 100 Gespräche mit Leistungssportlern, Trainingstherapeut.",
    founder("Alex", "Leistungssport und Performance.", ["Sportökonom und Trainingstherapeut", "Über 100 Gespräche mit Leistungssportlern"], foto("alex", 460), "Wer wir sind"))

neu("Zwei Welten", "A/M", "Wir kommen aus zwei Welten. Business und Leistungssport. Und genau da liegt der Unterschied zu jedem, der euch nur mehr Vertrieb beibringt.",
    eyebrow("Warum wir") + h2(f"Zwei Welten. {m('Ein System.')}", 96)
    + reihe(karte("Business", "Skalierung, Vertrieb, Gründung.", size=80), karte("Leistungssport", "Energie, Steuerung, Regeneration.", size=80), gap=40)
    + '<div style="margin-top:36px">' + pille("250+ Kunden aus verschiedenen Branchen · unternehmensathleten") + "</div>")

# =====================================================================================================
# TEIL 6 · PITCH
# =====================================================================================================
jahr = ["Zwölf Monate, in denen dein Kalender vom Zufall abhängt.", "Wieder posten und hoffen, statt die Richtigen anzuschreiben.",
        "Wieder auf Empfehlungen warten.", "Wieder ein Monat voll, der nächste leer.",
        "Wieder zusehen, wie andere über LinkedIn Kunden gewinnen.", "Und im Dezember 2027 stehst du genau da, wo du heute stehst."]
stufen("Ein weiteres Jahr", "A", "Was dich ein weiteres Jahr ohne System kostet. Punkt für Punkt, ruhig vorlesen.", 3,
       lambda k: eyebrow("Ehrlich gerechnet", CORAL) + h2(f"Was dich ein {c('weiteres Jahr')} kostet.", 84) + nummern(jahr, 2 * k, CORAL))

stufen("Zwei Optionen", "A", "Wir könnten dich jetzt allein lassen. Option 1: allein weitermachen. Option 2: die Abkürzung, mit der Reihenfolge, die bei über 250 Selbstständigen funktioniert hat.", 2,
       lambda k: eyebrow("Du hast zwei Optionen") + h2(f"Allein weiter. Oder {m('gemeinsam in 90 Tagen.')}", 80)
       + reihe(karte("Allein weitermachen", "Mit allem, was du heute gesehen hast. Auf eigene Faust.", "neutral", "Option 1", size=48),
               karte("Die Abkürzung", "Die Reihenfolge, die bei über 250 Selbstständigen funktioniert hat. In 90 Tagen, gemeinsam.", "mint", "Option 2", sichtbar=k >= 2, size=48), gap=40))

scheitern = ["Wissen sammeln statt Reihenfolge: noch ein Kurs, noch ein Tool.", "Posten statt Gespräche führen.",
             "Keine klare Zielgruppe, kein klares Angebot.", "Alles gleichzeitig probieren und nichts durchziehen.",
             "Die erste Nachricht verschieben: aus nächster Woche wird nie.", "Allein: niemand sagt dir, wo du falsch abbiegst."]
stufen("Woran es scheitert", "A", "Woran es meistens scheitert. Jeder Punkt ist ein Grund für Option 2.", 3,
       lambda k: eyebrow("Aus über 250 Begleitungen", CORAL) + h2(f"Woran es {c('meistens scheitert.')}", 84) + nummern(scheitern, 2 * k, CORAL))

neu("Ergebnis zuerst", "A", "Ergebnis vor Weg. In 90 Tagen qualifizierte Termine im Kalender. Wie viele für dich realistisch sind, rechnen wir im Strategie-Call aus.",
    eyebrow("Das Ergebnis") + h2(f"In 90 Tagen {m('qualifizierte Termine')} im Kalender.", 110, 30)
    + sub("Wie viele für dich realistisch sind, rechnen wir im Strategie-Call aus.", 38, 40)
    + f'<div style="margin-top:36px;display:flex">{offen("Was heißt „qualifiziert“? Gleiches Kriterium wie bei der Garantie", "1", 18)}</div>', GRUEN)

neu("Was ist das konkret", "A", "Also, was ist das jetzt konkret. Ein Satz, der das Produkt definiert. Hat 2025 gefehlt.",
    eyebrow("Was ist das konkret") + h2(f"{m('Foundation.')} Dein LinkedIn Performance System in 90 Tagen.", 84, 30)
    + f'<div style="margin-top:44px;display:flex">{offen("Produktsatz final formulieren (ein Satz)", "1")}</div>', STIL_MITTE)

bausteine = [("Outreach-System", "Die Richtigen finden und ansprechen."), ("Signature-Framework", "Deine Nachrichten, deine Stimme."),
             ("Onboarding", "Dein Startpunkt, sauber aufgenommen."), ("KI-Onboarding-Sprint", "KI als Werkzeug, nicht als Thema.")]
stufen("Der Weg", "M", "Erst jetzt der Weg. Die Bausteine einzeln, mit Wert dahinter.", 4,
       lambda k: eyebrow("Der Weg in 90 Tagen") + h2(f"Vier Bausteine. {m('Ein Ziel.')}", 80)
       + reihe(*[karte(tt, tx, "mint" if j == 3 else "neutral", f"Baustein 0{j + 1}", sichtbar=k > j, size=36) for j, (tt, tx) in enumerate(bausteine)], gap=24)
       + f'<div style="margin-top:22px;display:flex;gap:20px">{offen("Workshop gemeinsam oder Fragebogen + Voice-Onboarding?", "1", 18)}{offen("Monat 1 bis 3 und Wochenablauf", "1", 18)}</div>')

neu("Einmal aufbauen", "A", "Das Beste daran: Du baust dieses System einmal auf und nutzt es für den Rest deiner Selbstständigkeit. Etwas, das dir niemand mehr wegnehmen kann.",
    f'<div style="text-align:center">{eyebrow("Das Beste daran")}</div>'
    + f'<div style="margin-top:30px;text-align:center;font-size:96px;font-weight:700;letter-spacing:-0.03em;line-height:1.08">Du baust dieses System {m("einmal")} auf<br>und nutzt es für den Rest deiner Selbstständigkeit.</div>'
    + sub("Etwas, das dir niemand mehr wegnehmen kann. Kein Algorithmus, keine Krise, keine Plattform-Änderung.", 38, 50).replace("max-width:1500px", "max-width:1500px;text-align:center;margin-left:auto;margin-right:auto"),
    GRUEN.replace("justify-content:center", "justify-content:center;align-items:center"))

cases = [("[Case 1]", "Sichtbarkeit war das Thema. Mehrere Jahre gemeinsam."), ("[Case 2]", "Kalt über eine Anzeige. Kein Vertrauensvorschuss."),
         ("[Case 3]", "Neu, mit klaren Zielen. Ein Hebel, drei Monate.")]


def case_karte(j, sichtbar):
    name, text = cases[j]
    return (f'<div style="{"" if sichtbar else "visibility:hidden;"}flex:1;background:#131312;border:1px solid #34322F;border-radius:26px;padding:40px;'
            f'display:flex;flex-direction:column;align-items:center;text-align:center;gap:22px">{foto(f"case{j + 1}", 170)}'
            f'<div style="font-size:40px;font-weight:700">{name}</div><div style="font-size:24px;line-height:1.45;color:#B4AFA6">{text}</div>'
            f'<div style="{MONO}font-size:22px;color:{MINT}">[vorher] → [heute]</div></div>')


stufen("Drei Cases", "A", "Drei völlig unterschiedliche Ausgangslagen. Ein identischer Mechanismus: der Moment, in dem jemand sieht, wo er wirklich steht und was als Nächstes dran ist.", 4,
       lambda k: eyebrow("Drei Ausgangslagen") + h2(f"Drei Wege. {m('Ein Mechanismus.')}", 76)
       + reihe(*[case_karte(j, k > j) for j in range(3)], top=40)
       + f'<div style="margin-top:28px;display:flex;gap:20px;align-items:center;{"" if k >= 4 else "visibility:hidden"}">'
       + pille("Der Moment, in dem jemand sieht, wo er steht und was als Nächstes dran ist.") + "</div>"
       + f'<div style="margin-top:14px;display:flex">{offen("Freigaben, Fotos, Zahlen lokal einsetzen (Zuordnung in deck/referenzen/)", "1", 16)}</div>')

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

neu("Referenz nach Invest", "A", "Denkst du, für ihn hat es sich gelohnt?",
    eyebrow("Hat es sich gelohnt?") + f'<div style="margin-top:36px;flex:1;display:flex;gap:48px">'
    + f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">{foto("proof-invest", 200)}{h2(f"Denkst du, für [Name] hat es sich {m("gelohnt?")}", 64, 0)}</div>'
    + offen("Welcher Fall? Screenshot mit Ergebnis", "1") + "</div>")

nicht = ["… du nur mal gucken willst, was es kostet.", "… du keine [X] Stunden pro Woche investieren kannst.",
         "… du keine Ratschläge annehmen willst.", "… du nicht bereit bist, in dich selbst zu investieren.",
         "… du erst perfekt sein willst, bevor du loslegst.", "… du dir sicher bist, dass du es allein besser kannst."]
neu("Buch dir keinen Call, wenn", "A", "Ganz klare Qualifizierung. Wir nehmen nicht jeden.",
    eyebrow("Ehrlich gesagt") + h2(f"Buch dir bitte {c('keinen Call')}, wenn …", 84) + nummern(nicht, 99, CORAL)
    + f'<div style="margin-top:20px;display:flex">{offen("Stunden pro Woche festlegen", "1", 18)}</div>')

schritte = [("01", "Termin wählen", "Du suchst dir einen passenden Termin aus."),
            ("02", "Fragen beantworten", "Ein paar kurze Fragen, damit wir vorbereitet ins Gespräch gehen."),
            ("03", "Das Gespräch", "Alex oder Michi schauen mit dir, wo du stehst, wohin du willst und ob es passt. Wir arbeiten mit Machern.")]


def kalender_mock():
    return (f'<div style="flex:1;background:#F0EEE6;color:#141413;border-radius:28px;padding:36px;display:flex;flex-direction:column;gap:20px">'
            f'<div style="display:flex;justify-content:space-between;font-size:26px;font-weight:700"><span>Oktober 2026</span><span style="{MONO}font-size:16px;color:#6B665F">WOCHE</span></div>'
            f'<div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">'
            + "".join(f'<div style="display:flex;flex-direction:column;gap:12px"><div style="{MONO}font-size:16px;color:#6B665F;text-align:center">{tag}</div>{inhalt}</div>'
                      for tag, inhalt in [("MO", '<div style="height:120px;border-radius:12px;background:#DCE3EA"></div>'),
                                          ("DI", f'<div style="margin-top:60px;border-radius:14px;background:linear-gradient(160deg,#57C98C,#2E8B5A);color:#fff;padding:22px;font-size:22px;font-weight:700;line-height:1.3">Dein Strategie-Call<br><span style="font-weight:400;font-size:18px">mit Alex oder Michi</span></div>'),
                                          ("MI", '<div style="margin-top:160px;height:100px;border-radius:12px;background:#DCE3EA"></div>')])
            + "</div></div>")


neu("So läuft dein Call ab", "A/M", "Auch wenn es selbsterklärend wirkt: einmal klar benennen, wie der Strategie-Call abläuft.",
    eyebrow("Der nächste Schritt") + h2(f"So läuft dein {m('Strategie-Call')} ab.", 84)
    + f'<div style="margin-top:44px;flex:1;display:flex;gap:56px">'
    + '<div style="flex:1.1;display:flex;flex-direction:column;gap:22px">'
    + "".join(f'<div style="flex:1;display:flex;gap:30px;align-items:center;padding:0 34px;border-radius:24px;{"background:#131312;border:1.5px solid " + MINT if nr == "03" else "border:1px solid #34322F"}">'
              f'<div style="font-family:Newsreader,serif;font-style:italic;font-size:72px;color:{MINT if nr == "03" else "#2C4A3A"}">{nr}</div>'
              f'<div><div style="font-size:36px;font-weight:700">{t}</div><div style="font-size:24px;color:#B4AFA6;margin-top:6px;line-height:1.4">{x}</div></div></div>'
              for nr, t, x in schritte)
    + "</div>" + kalender_mock() + "</div>")

d.folien = [alt["Kalender offen"]]
d.ed("Kalender offen", "Nur 5 Plätze", "Nur [N] Plätze")
d.ed("Kalender offen", "250+ Kunden Erfahrung · unternehmensathleten × DigiUp", "250+ Kunden Erfahrung · unternehmensathleten")
d.ed("Kalender offen", "Du kennst den Deal — im Gespräch klären wir nur, ", "Im Strategie-Call rechnen wir dein Ergebnis und klären, ")
kal = d.folien[0]
start = kal.index('<img src="data:image/png;base64,', kal.index("width:560px;height:560px"))
ende = kal.index(">", start) + 1
kal = kal[:start] + (f'<div style="width:100%;height:100%;border:3px dashed {GELB};border-radius:20px;display:flex;align-items:center;justify-content:center;'
                     f'{MONO}font-size:26px;color:#8C6A1E;text-align:center">QR-CODE<br>STRATEGIE-CALL<br>OFFEN</div>') + kal[ende:]
d.folien = [kal]
d.notes("Kalender offen", "QR-Code zum ersten Mal, vor den Boni. Ab sofort ist unser Kalender offen. Wir nehmen nicht jeden. Im Strategie-Call rechnen wir dein Ergebnis und klären, ob es passt.")
FOLGE.append((d.folien[0], "A"))

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
      f'<span style="font-size:150px;font-weight:700;letter-spacing:.02em">[CODE]</span>'
      f'<span style="font-family:Newsreader,serif;font-size:140px;color:{MINT}">”</span></div>'
    + sub("Nenn ihn im Strategie-Call. Dein Vorteil als Webinar-Teilnehmer.", 38, 44).replace("max-width:1500px", "max-width:1500px;text-align:center;margin-left:auto;margin-right:auto")
    + f'<div style="margin-top:30px;display:flex;justify-content:center">{offen("Name des Codes und was er bringt", "0 0 auto", 18)}</div>',
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

# ---- zusammensetzen ---------------------------------------------------------------------------------
d.folien = [f for f, _ in FOLGE]
d.kuerzel([(n, n, wer) for n, (_, wer) in enumerate(FOLGE, 1)])
d.speichern(ZIEL, titel="LinkedIn Performance System 2027")
