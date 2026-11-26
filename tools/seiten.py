#!/usr/bin/env python3
"""Erzeugt die Unterseiten Beratung, Anmeldung, Aktuelles, Kontakt, Impressum, Datenschutz.
Inhalte von der bisherigen Schulhomepage. Aufruf: python3 tools/seiten.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
INFOTAG = "Samstag, 13. Februar 2027"
DL = "assets/downloads/"
SCHULBEWERBUNG = "https://www.schulbewerbung.de"

def shell():
    src = (ROOT/"index.html").read_text(encoding="utf-8")
    fix = lambda s: re.sub(r'href="#(?!top")', 'href="index.html#', s).replace('href="#top"', 'href="index.html"')
    head = fix(src[src.index('<div class="draft-note"'):src.index("</header>")+9])
    foot = fix(src[src.index('<footer class="footer">'):src.index("<script>")])
    js = src[src.index("<script>")+8:src.index("// Bildungsgang-Filter")]
    return head, foot, js

def page(slug, title, desc, tag, h1, lead, nav, body):
    head, foot, js = shell()
    sub = ""
    if nav:
        sub = '<nav class="subnav" aria-label="Auf dieser Seite">' + "".join(f'<a href="#{a}">{t}</a>' for a, t in nav) + "</nav>"
    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Berufskolleg Rheydt-Mülfort</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#123b37">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="home">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{head}
<main id="inhalt" class="about">
  <section class="adv-head"><div class="wrap">
    <span class="tag">{tag}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {sub}
  </div></section>
{body}
</main>
{foot}
<script>
{js}</script>
</body>
</html>
"""
    (ROOT/f"{slug}.html").write_text(html, encoding="utf-8")
    print(slug + ".html erzeugt")

def sec(id_, h, inner, tint=False):
    cls = "section tintband" if tint else "section"
    return f'  <section class="{cls}" id="{id_}" aria-labelledby="{id_}-h"><div class="wrap">\n    <h2 id="{id_}-h">{h}</h2>\n{inner}\n  </div></section>\n'

def ul(items, cls="checks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def mail(a):
    return f'<a href="mailto:{a}">{a}</a>'

# ---------------- Beratung ----------------
def beratung():
    b = ""
    b += sec("schulsozialarbeit", "Schulsozialarbeit", f"""
    <p class="lead">Persönliche Sorgen oder Probleme in der Schule? Allein dreht man sich oft im Kreis. Die Beratung ist kostenlos, freiwillig und vertraulich. Sie richtet sich auch an Eltern, Ausbildende und Lehrkräfte.</p>
    <div class="cards two">
      <article class="card-w"><h3>Frau Zimmer</h3><p class="muted">Diplom-Sozialarbeiterin</p>
        <p><b>Zuständig für:</b> Höhere Handelsschule, Büromanagement, Automobilkaufleute, Groß- und Außenhandel, Industriekaufleute, Fachschule für Wirtschaft</p>
        <dl class="kv"><div><dt>Telefon</dt><dd><a href="tel:+4921669179254">02166 9179254</a></dd></div><div><dt>E-Mail</dt><dd>{mail("zimmer@berufskolleg.biz")}</dd></div><div><dt>Erreichbar</dt><dd>Mo–Do 7:55–16:30, Fr 7:55–15:30 und nach Vereinbarung</dd></div></dl></article>
      <article class="card-w"><h3>Herr Farhadi</h3><p class="muted">Schulsozialarbeit</p>
        <p><b>Zuständig für:</b> Ausbildungsvorbereitung, Internationale Förderklassen, Handelsschule (BFS1 und BFS2), Einzelhandel, Verkäuferinnen und Verkäufer, Automobilkaufleute</p>
        <dl class="kv"><div><dt>Telefon</dt><dd><a href="tel:+4921669179216">02166 9179216</a></dd></div><div><dt>E-Mail</dt><dd>{mail("farhadi@berufskolleg.biz")}</dd></div><div><dt>Termin</dt><dd>individuelle Absprache</dd></div></dl></article>
    </div>
    <h3 class="sub-h">Wobei wir helfen</h3>
    {ul(["Noten im Keller, Abschluss oder Versetzung gefährdet", "Hohe Fehlzeiten, Motivationsprobleme", "Angst, Mobbing oder Konflikte in Schule und Ausbildung", "Stress zu Hause oder im Freundeskreis", "Geldsorgen, Schulden, Anträge (BAföG, BAB, Kindergeld, BuT, Jobcenter)", "Gesundheitliche und psychische Probleme, Sucht", "Schwangerschaft, eigene Wohnung, Aufenthaltsstatus", "Wie geht es nach der Schule weiter?"], "checks cols")}
    <p class="docs"><a href="{DL}notfallnummern.pdf">Notfallnummern (PDF)</a></p>""")
    b += sec("bob", "Berufsorientierungsbüro (BOB)", f"""
    <div class="split top">
      <div><p class="lead">Im BOB geht es um den Übergang von der Schule in den Beruf. Das Lehrerteam berät, formuliert, korrigiert, hört zu und lobt, je nachdem, was du gerade brauchst. Alles bleibt vertraulich.</p>
      <p>Mehrere Arbeitsplätze stehen bereit, um Unterlagen fertigzustellen oder in Ruhe nach einem Ausbildungsplatz zu suchen. Regelmäßig bietet auch die Agentur für Arbeit Beratungstermine im BOB an.</p>
      <p>Am Standort Kirschhecke findest du das BOB direkt rechts neben dem Lehrerzimmer.</p>
      <p class="docs"><a href="{DL}bob-info.pdf">Für euch im BOB (PDF)</a></p></div>
      <div><img class="rounded" src="assets/img/bk-berufsorientierung-1200.webp" alt="Schülerinnen und Schüler informieren sich an Ständen von Unternehmen" width="1200" height="803" loading="lazy"><div class="card-w"><h3>Das Angebot</h3>{ul(["Berufsfindung und Berufswahl", "Bewerbungsschreiben und Online-Bewerbung", "Vorbereitung auf Bewerbungsgespräche", "Recherchieren, Telefonieren, Scannen", "Schullaufbahn- und Studienberatung", "Weiterbildungsmöglichkeiten"])}</div></div>
    </div>""", tint=True)
    b += sec("lerncoaching", "Lerncoaching", f"""
    <div class="split top">
      <div><p class="lead">Du lernst, aber es klappt nicht richtig? Dir fehlt die Motivation, du hast Angst vor einem Fach oder möchtest einfach noch besser werden?</p>
      <p>Lerncoaching begleitet deinen Weg des Lernens und findet mit dir passende Lernstrategien, die du selbst ausprobierst. Lerncoaching ist keine Nachhilfe. Die Coaches unterliegen der Schweigepflicht. Findet der Termin im Unterricht statt, bekommst du eine Bescheinigung.</p></div>
      <div class="card-w"><h3>Termin anfragen</h3><p>Schreib eine Mail an {mail("lerncoaching@berufskolleg.biz")} und bitte um einen Termin. Wir melden uns zeitnah.</p></div>
    </div>""")
    b += sec("inklusion", "Inklusion und Nachteilsausgleich", f"""
    <p class="lead">Gemeinsam lernen, gemeinsam wachsen: Alle Schülerinnen und Schüler sollen unabhängig von Ausgangslage, Herkunft, Beeinträchtigung oder Lebenssituation die gleichen Chancen haben.</p>
    <div class="cards two">
      <article class="card-w"><h3>Unsere Angebote</h3>{ul(["Lerncoaching und Lernstatt mit Sprachdiagnostik", "Lernstandsdiagnostik und individuelle Förderung", "Lernraum für konzentriertes Arbeiten", "Sonderpädagogische Beratung und Förderpläne", "Beratung zu Übergängen in Ausbildung, Studium und Beruf", "Austausch mit Integrationsfachdienst und Agentur für Arbeit"])}</article>
      <article class="card-w"><h3>Nachteilsausgleich (NTA)</h3><p>Ein NTA gleicht Nachteile durch eine längerfristige Erkrankung oder Beeinträchtigung aus. Er bringt keine besseren Noten, sondern faire Bedingungen.</p>
        <ol class="mini-steps"><li>Antrag mit dem Formular bei der Schulleitung stellen</li><li>Ärztliche Nachweise und ggf. den früheren Bescheid beilegen</li><li>Klassenleitung persönlich und per E-Mail informieren</li></ol>
        <p class="muted small">Am besten bis zum 15.10. des Schuljahres. Für IHK-Prüfungen gelten eigene Fristen.</p>
        <p class="docs"><a href="{DL}formular-nachteilsausgleich.pdf">Antrag Nachteilsausgleich (PDF)</a></p>
        <p>Inklusionsbeauftragte: Anika Kauder, {mail("kauder@berufskolleg.biz")} · Inklusionsteam: {mail("nta@berufskolleg.biz")}</p></article>
    </div>""", tint=True)
    b += sec("sv", "Schülervertretung", f"""
    <div class="cards two">
      <article class="card-w"><h3>Eure SV</h3><p>Ideen, Wünsche oder Ärger in der Klasse? Die gewählte Schülervertretung ist am Standort Kirschhecke für euch da.</p><p>E-Mail: {mail("SV@berufskolleg.biz")}</p></article>
      <article class="card-w"><h3>SV-Verbindungslehrerinnen</h3><p>Sie unterstützen die SV und helfen bei Konflikten. Sprecht sie in den Pausen an oder schreibt eine Mail.</p>
        <dl class="kv"><div><dt>Frau Boshuesen</dt><dd>{mail("boshuesen@berufskolleg.biz")}</dd></div><div><dt>Frau Zimmermann</dt><dd>{mail("zimmermann@berufskolleg.biz")}</dd></div><div><dt>Frau Boegels</dt><dd>{mail("boegels@berufskolleg.biz")}</dd></div></dl></article>
    </div>""")
    page("beratung", "Beratung", "Schulsozialarbeit, Berufsorientierungsbüro, Lerncoaching, Inklusion und Schülervertretung am Berufskolleg Rheydt-Mülfort.",
         "Beratung", "Wir helfen dir weiter.", "Ob Sorgen, Bewerbung oder Lernen: Bei uns findest du die passende Ansprechperson.",
         [("schulsozialarbeit", "Schulsozialarbeit"), ("bob", "Berufsorientierung"), ("lerncoaching", "Lerncoaching"), ("inklusion", "Inklusion &amp; NTA"), ("sv", "Schülervertretung")], b)

# ---------------- Anmeldung ----------------
def anmeldung():
    def go(items):
        return '<ul class="go">' + "".join(f'<li><a href="{h}"><span>{t}</span></a></li>' for t, h in items) + "</ul>"
    b = sec("wege", "So meldest du dich an", f"""
    <div class="cards three">
      <article class="card-w" id="vollzeit"><span class="pill">Vollzeit</span><h3>Schulabschluss in Vollzeit</h3><p>Ausbildungsvorbereitung, Handelsschule, Höhere Handelsschule</p>
        {go([("Online anmelden auf schulbewerbung.de", SCHULBEWERBUNG), ("Einwilligung Datenschutz (PDF)", DL + "einwilligung-datenschutz.pdf")])}
        <p class="muted small">Den Startcode bekommst du von deiner bisherigen Schule.</p></article>
      <article class="card-w" id="berufsschule"><span class="pill">Ausbildung</span><h3>Berufsschule</h3><p>Der Ausbildungsbetrieb meldet an.</p>
        {go([("Anmeldeformular 2027/28 (PDF)", DL + "2027_anmeldeformular_berufsschule_ausfuellbar.pdf"), ("Online anmelden auf schulbewerbung.de", SCHULBEWERBUNG)])}
        <p class="muted small">Formular ausgefüllt an {mail("info@berufskolleg.biz")}</p></article>
      <article class="card-w" id="fachschule"><span class="pill">Weiterbildung</span><h3>Fachschule für Wirtschaft</h3><p>Abgabe im Sekretariat, mit Lebenslauf und Nachweisen.</p>
        {go([("Anmeldeformular Fachschule (PDF)", DL + "anmeldeformular-fachschule.pdf"), ("Einwilligung Datenschutz (PDF)", DL + "einwilligung-datenschutz.pdf")])}</article>
    </div>
    <p class="hint">Noch unsicher, welcher Bildungsgang passt? <a href="schulberater.html">Frag unseren Schulberater.</a></p>""")
    b += sec("unterlagen", "Diese Unterlagen brauchen wir", f"""
    <div class="cards two">
      <article class="card-w"><h3>Im Sekretariat abgeben</h3>{ul(["Über schulbewerbung.de ausgedrucktes und unterschriebenes Anmeldeformular (bei Minderjährigen mit Unterschrift der Eltern)", f'Unterschriebene <a href="{DL}einwilligung-datenschutz.pdf">Einwilligungen zum Datenschutz</a>'])}</article>
      <article class="card-w"><h3>Am ersten Schultag mitbringen</h3>{ul(["Kopie des Ausbildungsvertrags (Berufsschule)", "Kopie des letzten Schulzeugnisses"])}<p class="muted small">Die Einschulungstermine stehen rechtzeitig unter <a href="aktuelles.html">Aktuelles</a>.</p></article>
    </div>""", tint=True)
    b += sec("infotag", "Lern uns kennen", f"""
    <div class="infotag"><span class="tag">Infotag</span><h3>{INFOTAG}</h3><p>Schau dir die Schule an, sprich mit Lehrkräften und Schülerinnen und Schülern und stell deine Fragen.</p></div>
    <p><a class="btn btn-soft" href="schulberater.html"><span class="arrow">Zum Schulberater</span></a></p>""")
    page("anmeldung", "Anmeldung", "So meldest du dich am Berufskolleg Rheydt-Mülfort an: Vollzeit, Berufsschule und Fachschule.",
         "Anmeldung", "Anmelden in drei Wegen.", "Wähle deinen Bereich und klick auf den Pfeil.",
         [("wege", "Anmeldewege"), ("unterlagen", "Unterlagen"), ("infotag", "Infotag")], b)

# ---------------- Aktuelles ----------------
POSTS = [
 ("infotag-2027", "Infotag", "Infotag am " + INFOTAG.split(", ")[1], [
   "Am " + INFOTAG + " öffnen wir unsere Türen am Standort Kirschhecke 10. Lerne unsere Bildungsgänge kennen, sprich mit Lehrkräften sowie Schülerinnen und Schülern und stelle deine Fragen zur Anmeldung."], None),
 ("bestes-bk-2026", "15. Oktober 2026", "Wir sind „Bestes Berufskolleg 2026“!", [
   "Große Freude an unserer Schule! Die IHK Mittlerer Niederrhein hat uns als „Bestes Berufskolleg 2026“ ausgezeichnet. Diesen Titel erhält das Berufskolleg mit den meisten ausgezeichneten Ausbildungsabsolventinnen und -absolventen.",
   "Die Preisverleihung fand am Freitag, 9. Oktober 2026, im NEW Kunstwerk in Mönchengladbach-Wickrath statt. Bei der IHK-Bestenehrung wurden die besten Auszubildenden, Ausbildungsbetriebe und Berufskollegs sowie die erfolgreichsten Fortbildungsabsolventinnen und -absolventen am Mittleren Niederrhein geehrt.",
   "Unsere Schulleiterin Stephany Kerstges nahm die Urkunde von IHK-Hauptgeschäftsführer Jürgen Steinmetz entgegen: „Dieser Preis macht uns stolz und ist ein schöner Erfolg für unsere gesamte Schulgemeinschaft.“",
   "Wir gratulieren unseren Absolventinnen und Absolventen herzlich. Ein großes Dankeschön gilt den Ausbildungsbetrieben und allen Kolleginnen und Kollegen, die unsere Auszubildenden begleitet haben."], "bk-auszeichnung-2026-1200.webp"),
 ("lernraum-workshop", "12. Dezember 2025", "Lernraum-Workshop in Wijchen (NL)", [
   "Am 24. November 2025 nahmen Schülerinnen, Schüler und Lehrkräfte an einem ganztägigen Lernraum-Workshop beim Schulmöbelhersteller Eromesmarko im niederländischen Wijchen teil. Gemeinsam entwickelten sie Ideen für moderne Lernumgebungen, die zum Beispiel selbstorganisiertes Lernen unterstützen.",
   "Die Schülerinnen und Schüler brachten inspirierende Ideen ein, die in die Planung der neuen Lernräume am Standort Kirschhecke einfließen. Danke an alle, die diesen Tag mitgestaltet haben!"], "bk-workshop-wijchen.webp"),
 ("ich-steh-auf", "10. November 2025", "Projekt ICH STEH AUF gewinnt 500 Euro", [
   "Die Elfriede Kürble Stiftung und der Integrationsrat der Stadt Mönchengladbach haben Schulprojekte zur Vielfalt in der Gesellschaft ausgezeichnet.",
   "Mit unseren Schülerinnen und Schülern haben wir einen Tag zur Demokratiebildung gestaltet und unsere Grundrechte in den Blick genommen. Entstanden sind viele Audios, die mit dem Satz „Ich steh auf für …“ enden. Dafür gab es den 2. Platz. Das Preisgeld fließt in weitere Projekte."], None),
]
ALT = {"bk-auszeichnung-2026-1200.webp": "Schulleiterin Stephany Kerstges mit der IHK-Urkunde „Bestes Berufskolleg 2026“", "bk-workshop-wijchen.webp": "Schülerinnen, Schüler und Lehrkräfte beim Lernraum-Workshop in Wijchen"}
def aktuelles():
    items = ""
    for id_, meta, h, ps, img in POSTS:
        pic = f'<img src="assets/img/{img}" alt="{ALT.get(img,"")}" loading="lazy">' if img else ""
        items += f'<article class="post" id="{id_}">{pic}<div><span class="meta">{meta}</span><h2>{h}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</div></article>\n"
    b = f'  <section class="section"><div class="wrap posts">\n{items}  </div></section>\n'
    page("aktuelles", "Aktuelles", "Neuigkeiten aus dem Berufskolleg Rheydt-Mülfort.", "Aktuelles", "Neu bei uns.",
         "Was an unserer Schule gerade passiert.", None, b)

# ---------------- Kontakt ----------------
def kontakt():
    maps = "https://www.google.com/maps/search/?api=1&amp;query=Kirschhecke+10%2C+41199+M%C3%B6nchengladbach"
    b = sec("adresse", "So erreichst du uns", f"""
    <div class="cards three">
      <article class="card-w"><h3>Adresse</h3><p>Berufskolleg Rheydt-Mülfort<br>für Wirtschaft und Verwaltung<br>Kirschhecke 10<br>41199 Mönchengladbach</p></article>
      <article class="card-w"><h3>Sekretariat</h3><dl class="kv"><div><dt>Telefon</dt><dd><a href="tel:+492166917920">02166 917920</a></dd></div><div><dt>E-Mail</dt><dd>{mail("info@berufskolleg.biz")}</dd></div><div><dt>Mo, Mi, Do</dt><dd>7:30–15:00 Uhr</dd></div><div><dt>Di, Fr</dt><dd>7:30–13:00 Uhr</dd></div></dl><p class="muted small">In den Ferien gelten besondere Zeiten (siehe Aktuelles).</p></article>
      <article class="card-w"><h3>Pausenzeiten</h3><ul class="plain"><li>09:25–09:45 Uhr</li><li>11:15–11:35 Uhr</li><li>13:05–13:15 Uhr</li><li>16:20–16:30 Uhr</li><li>18:00–18:30 Uhr</li></ul></article>
    </div>""")
    b += sec("anfahrt", "Anfahrt", f"""
    <div class="cards three">
      <article class="card-w"><h3>Mit Bus</h3><p>Ab Rheydt Hbf mit den Linien <b>001, 002 oder 026</b> bis zur Haltestelle <b>Gymnasium Odenkirchen</b>.</p><p class="muted small">Fahrpläne: <a href="https://www.new-mobil.de">new-mobil.de</a></p></article>
      <article class="card-w"><h3>Mit dem Auto</h3><p>Parkplätze gibt es an der Mülgaustraße und an der Einruhrstraße.</p></article>
      <article class="card-w"><h3>Navigation</h3><p>Route zur Kirschhecke 10 direkt in Google Maps öffnen.</p><a class="btn btn-primary" href="{maps}"><span class="arrow">Route planen</span></a></article>
    </div>""", tint=True)
    b += sec("stundenplan", "Stundenplan und Lernplattform", """
    <div class="cards two">
      <article class="card-w"><h3>Stundenplan / Untis</h3><p>Stundenplan und Klassenbuch im Browser oder in der App Untis Mobile.</p><p><a class="btn btn-soft" href="https://berufskolleg.webuntis.com/">WebUntis öffnen</a></p><p class="small"><a href="https://apps.apple.com/de/app/untis-mobile/id926186904">App Store</a> · <a href="https://play.google.com/store/apps/details?id=com.grupet.web.app">Google Play</a></p></article>
      <article class="card-w"><h3>Virtuelles Lernstudio</h3><p>Lernangebote und Materialien für den Unterricht.</p><p><a class="btn btn-soft" href="https://www.virtuelleslernstudio.de/">Zum Lernstudio</a></p></article>
    </div>""")
    page("kontakt", "Kontakt", "Adresse, Sekretariat, Anfahrt und Stundenplan des Berufskollegs Rheydt-Mülfort.", "Kontakt",
         "Wir sind für dich da.", "Kirschhecke 10 · 41199 Mönchengladbach",
         [("adresse", "Sekretariat"), ("anfahrt", "Anfahrt"), ("stundenplan", "Stundenplan")], b)

# ---------------- Impressum ----------------
def impressum():
    b = sec("angaben", "Angaben", """
    <div class="cards two">
      <article class="card-w"><h3>Anbieter</h3><p>Berufskolleg Rheydt-Mülfort für Wirtschaft und Verwaltung<br>Kirschhecke 10<br>41199 Mönchengladbach-Rheydt</p><p>Vertreten durch: OStD’ Stephany Kerstges</p></article>
      <article class="card-w"><h3>Kontakt</h3><p>Telefon: (0 21 66) 91 79 20<br>E-Mail: <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a></p><h3>Redaktionell verantwortlich</h3><p>Schulleitung: OStD’ Stephany Kerstges, Anschrift wie oben</p></article>
    </div>
    <h3 class="sub-h">Verbraucherstreitbeilegung / Universalschlichtungsstelle</h3>
    <p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>""")
    b += sec("barrierefreiheit", "Barrierefreiheit", """
    <p class="lead">Diese Seiten sind so gebaut, dass sie für möglichst alle Menschen gut nutzbar sind.</p>
    <ul class="checks"><li>Vergrößern ist jederzeit möglich, die Seiten passen sich jedem Bildschirm an.</li><li>Alle Funktionen sind mit der Tastatur bedienbar, ein Link springt direkt zum Inhalt.</li><li>Bilder haben Alternativtexte, Farben haben ausreichenden Kontrast.</li><li>Keine Animationen, wenn das Gerät „Bewegung reduzieren“ eingestellt hat.</li></ul>
    <p class="note-draft">Entwurf: Eine vollständige Erklärung zur Barrierefreiheit nach BITV NRW folgt vor der Veröffentlichung.</p>
    <p>Barrieren entdeckt? Schreib uns an <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a>.</p>""", tint=True)
    page("impressum", "Impressum", "Impressum und Hinweise zur Barrierefreiheit des Berufskollegs Rheydt-Mülfort.", "Impressum",
         "Impressum", "Angaben gemäß Telemediengesetz.", None, b)

# ---------------- Datenschutz ----------------
def datenschutz():
    b = sec("hinweise", "Datenschutz auf einen Blick", """
    <p class="note-draft">Entwurf für die neue, statische Website. Vor der Veröffentlichung von der Schulleitung und dem Datenschutzbeauftragten prüfen lassen.</p>
    <p>Diese Website kommt ohne Cookies, Tracking, Analyse-Tools, Kontaktformular und eingebettete Inhalte von Drittanbietern aus. Schriften werden lokal geladen, es besteht keine Verbindung zu Google Fonts.</p>
    <h3 class="sub-h">Hosting und Server-Logfiles</h3>
    <p>Beim Aufruf der Seiten verarbeitet der Hosting-Anbieter technisch notwendige Daten (zum Beispiel IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser). Rechtsgrundlage ist Art. 6 Abs. 1 lit. e DSGVO in Verbindung mit dem Schulgesetz NRW. <em>Angaben zum endgültigen Hosting ergänzen.</em></p>
    <h3 class="sub-h">Links zu anderen Angeboten</h3>
    <p>Einige Links führen zu Angeboten anderer Anbieter, etwa schulbewerbung.de, WebUntis, Google Maps oder dem Virtuellen Lernstudio. Dort gelten deren Datenschutzhinweise.</p>
    <h3 class="sub-h">Ihre Rechte</h3>
    <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung sowie ein Beschwerderecht bei der Aufsichtsbehörde (Landesbeauftragte für Datenschutz und Informationsfreiheit NRW).</p>""")
    b += sec("kontakt-ds", "Ansprechpersonen", """
    <div class="cards two">
      <article class="card-w"><h3>Verantwortliche Stelle</h3><p>Berufskolleg Rheydt-Mülfort für Wirtschaft und Verwaltung<br>Kirschhecke 10, 41199 Mönchengladbach-Rheydt<br>Telefon: (0 21 66) 91 79 20<br>E-Mail: <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a></p></article>
      <article class="card-w"><h3>Datenschutzbeauftragter</h3><p>Schulamt für die Stadt Mönchengladbach<br>z. H. Herrn Christoph Heussen<br>Voltastraße 2, 41050 Mönchengladbach<br>Telefon: 02161 253700<br>E-Mail: <a href="mailto:Datenschutz_an_Schulen@moenchengladbach.de">Datenschutz_an_Schulen@moenchengladbach.de</a></p></article>
    </div>""", tint=True)
    page("datenschutz", "Datenschutz", "Datenschutzhinweise des Berufskollegs Rheydt-Mülfort.", "Datenschutz",
         "Datenschutz", "Wie wir mit Daten auf dieser Website umgehen.", None, b)

for f in (beratung, anmeldung, aktuelles, kontakt, impressum, datenschutz):
    f()
