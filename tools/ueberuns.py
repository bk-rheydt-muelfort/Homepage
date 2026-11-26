#!/usr/bin/env python3
"""Erzeugt ueber-uns.html (Leitbild, Organigramm, Auszeichnungen, Europa, Kooperationen).
Inhalte von berufskolleg.biz. Aufruf: python3 tools/ueberuns.py"""
import html, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
e = html.escape

LEITBILD = [
 ("Zukunftsfähige Abschlüsse", ["Wir arbeiten gemeinsam daran, dass junge Menschen bei uns ihren Weg in die berufliche Zukunft finden. Wir ermöglichen unseren Schülerinnen und Schülern zukunftsfähige Abschlüsse und bereiten sie darauf vor, die Gesellschaft, in der wir leben, verantwortungsvoll mitzugestalten."]),
 ("Guter Unterricht", ["Wir schaffen Rahmenbedingungen, damit Schülerinnen und Schüler Verantwortung für ihren eigenen Lernprozess übernehmen können. Dabei unterstützen wir jede und jeden individuell darin, die eigenen Stärken auszubauen. In unserem Handeln orientieren wir uns an den aktuellen Anforderungen der beruflichen Praxis."]),
 ("Unterstützung durch digitale Medien", ["Wir sehen die zunehmende Digitalisierung als große Herausforderung für das Lehren und Lernen und begegnen ihr, indem wir offen sind für neue Medien und Unterrichtskonzepte, die Mensch und Technologie zusammenbringen. Daher richtet sich unsere Ausstattung an den aktuellen Anforderungen aus und unterstützt die Schülerinnen und Schüler in der Bewältigung ihrer digitalen Lebenswelt."]),
 ("Erfolgreiche Kooperation", ["Wir fördern die persönlichen Stärken und Interessen unserer Schülerinnen und Schüler optimal, indem wir uns in den Lehrerteams eng abstimmen und mit unseren außerschulischen Partnern eng kooperieren.",
   "In unserer Schule institutionalisieren wir eine vertrauensvolle Zusammenarbeit durch gemeinsame Unterrichtsentwicklung und -evaluation in langfristig kooperierenden Lehrerteams. So sind wir verlässliche Partner für Eltern, Ausbildungsbetriebe, IHK und unsere Partnerschulen in Europa. Diese Zusammenarbeit lebt von Kontinuität und offenen Dialogen."]),
 ("Gelingendes Miteinander", ["Wir wollen, dass unsere Schülerinnen und Schüler gerne zu uns kommen. Deshalb stellen wir den respektvollen, wertschätzenden und unterstützenden Dialog miteinander in den Mittelpunkt unserer Zusammenarbeit an dieser Schule, unabhängig von Position, Herkunft, Kultur, Religion, Hautfarbe, Geschlecht oder Überzeugung.",
   "Diese Verpflichtung zum Dialog schließt ein, dass unsere Regeln für das Schulleben – gemeinsam festgelegte sowie vorgegebene – eingehalten werden und dass wir unsere Werte transparent vermitteln. Wir gehen lösungsorientiert und vertrauensvoll miteinander um."]),
 ("Europäischer Gedanke", ["Wir sind in Europa zu Hause und heißen Europa in unserem Hause willkommen.",
   "Durch die Zusammenarbeit mit unseren Partnerschulen in vielen europäischen Ländern schauen wir über den heimischen Tellerrand und lassen uns von neuen Ideen und Entwicklungen inspirieren.",
   "Wir sind aber auch stolz darauf, uns und unser Wirken zu präsentieren. Gemeinsame Projekte und Besuche stärken den Zusammenhalt und zeigen, dass die Chancen unserer Schülerinnen und Schüler insbesondere in der Vielfalt liegen. Sprachenlernen und sprachliche Zertifizierung sind für uns Werkzeug und Schlüssel für das Leben und Arbeiten im Vereinigten Europa."]),
]

PARTNER = [
 ("Polen","Zespół Szkół Nr 7 im. Szczepana Bońkowskiego, Warschau"),
 ("Slowakei","Stredná odborná škola, Nové Mesto nad Váhom"),
 ("Ungarn","Borbély Lajos Vocational Secondary School"),
 ("Türkei","Tekirdağ Mesleki ve Teknik Anadolu Lisesi"),
 ("Spanien","IES Santiago Hernández und IES Pablo Serrano, Saragossa · IES Universidad Laboral, Albacete · Miguel Altuna, Bergara"),
 ("Italien","Istituto Don Milani-Pertini, Grottaglie und Crispiano"),
 ("Frankreich","Lycée professionnel Émile Zola, Aix-en-Provence"),
 ("Malta","MCAST"),
 ("Großbritannien","Stratford-upon-Avon College"),
 ("Finnland","Oulun Seudun Ammattiopisto, Oulu · Lapin ammattiopisto, Rovaniemi"),
 ("Schweden","Frans Suell och Jörgen Kocks Gymnasium, Malmö"),
 ("Niederlande","Gilde Opleidingen"),
]

def build():
    src = (ROOT/"index.html").read_text(encoding="utf-8")
    fix = lambda s: re.sub(r'href="#(?!top")', 'href="index.html#', s).replace('href="#top"','href="index.html"')
    head = fix(src[src.index('<div class="draft-note"'):src.index("</header>")+9])
    foot = fix(src[src.index('<footer class="footer">'):src.index("<script>")])
    menu_js = src[src.index("<script>")+8:src.index("// Bildungsgang-Filter")]
    lb = "".join(f'<li><h3>{e(t)}</h3>' + "".join(f"<p>{e(p)}</p>" for p in ps) + "</li>" for t,ps in LEITBILD)
    esl = "".join(f'<div><dt>{n}</dt><dd><a href="mailto:{m}@berufskolleg.biz">{m}@berufskolleg.biz</a></dd></div>' for n,m in [("Frau Hares","hares"),("Herr Schiffer","schiffer"),("Herr Vandelaar","vandelaar"),("Herr Ufert","ufert"),("Herr Schwarz","schwarz"),("Herr Elsen","elsen"),("Frau Boegel","boegel")])
    pt = "".join(f"<li><b>{e(l)}</b><span>{e(n)}</span></li>" for l,n in PARTNER)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Über uns – Berufskolleg Rheydt-Mülfort</title>
<meta name="description" content="Leitbild, Organigramm, Auszeichnungen und Partnerschulen des Berufskollegs Rheydt-Mülfort in Mönchengladbach.">
<meta name="theme-color" content="#123b37">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="home">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{head}
<main id="inhalt" class="about">
  <section class="adv-head"><div class="wrap">
    <span class="tag">Über uns</span>
    <h1>Wer wir sind</h1>
    <p class="lead">Berufskolleg für Wirtschaft und Verwaltung in Mönchengladbach. Schulleiterin: Stephany Kerstges.</p>
    <nav class="subnav" aria-label="Auf dieser Seite">
      <a href="#team">Team</a><a href="#leitbild">Leitbild</a><a href="#organigramm">Organigramm</a><a href="#auszeichnungen">Auszeichnungen</a><a href="#europa">Europaschule</a><a href="#kooperationen">Hochschulkooperationen</a>
    </nav>
  </div></section>

  <section class="section" id="team" aria-labelledby="team-h"><div class="wrap">
    <h2 id="team-h">Ansprechpersonen</h2>
    <div class="cards three">
      <article class="card-w"><h3>Schulleitung</h3><p><b>OStD’ Stephany Kerstges</b><br>Schulleiterin</p><p class="muted small">Termine über das Sekretariat</p></article>
      <article class="card-w"><h3>Erweiterte Schulleitung</h3><dl class="kv">{esl}</dl></article>
      <article class="card-w"><h3>Schulverwaltung</h3><dl class="kv"><div><dt>Sekretariat</dt><dd>Frau Meuter, Frau Jost</dd></div><div><dt>Gebäudemanagement</dt><dd>Herr Conen</dd></div><div><dt>Telefon</dt><dd><a href="tel:+492166917920">02166 917920</a></dd></div><div><dt>E-Mail</dt><dd><a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a></dd></div></dl></article>
    </div>
    <p class="muted small">Alle Zuständigkeiten im Detail zeigt das <a href="#organigramm">Organigramm</a>.</p>
  </div></section>

  <section class="section tintband" id="leitbild" aria-labelledby="lb-h"><div class="wrap">
    <h2 id="lb-h">Unser Leitbild</h2>
    <ol class="leitbild">{lb}</ol>
    <p class="motto">Das ist unser Auftrag – und daran lassen wir uns messen.</p>
  </div></section>

  <section class="section" id="organigramm" aria-labelledby="org-h"><div class="wrap">
    <div class="sec-head"><h2 id="org-h">Organigramm</h2><span class="muted small">Stand: 18.11.2026</span></div>
    <a class="orgchart" href="assets/img/bk-organigramm-2026.webp" aria-label="Organigramm in voller Größe öffnen">
      <img src="assets/img/bk-organigramm-2026.webp" width="2000" height="1125" loading="lazy" alt="Organigramm des Berufskollegs: Schulleitung, Stabsbereiche, schulisches Beratungs- und Unterstützungssystem, Querschnittsbereiche und Bildungsgänge mit den jeweils verantwortlichen Personen.">
    </a>
    <p class="muted small">Zum Vergrößern auf das Bild tippen.</p>
  </div></section>

  <section class="section tintband" id="auszeichnungen" aria-labelledby="az-h"><div class="wrap">
    <h2 id="az-h">Auszeichnungen</h2>
    <ul class="awards">
      <li><img src="assets/img/logo-ihk.webp" alt="IHK Mittlerer Niederrhein – Bestes Berufskolleg" width="500" height="300" loading="lazy"><h3>Bestes Berufskolleg der IHK</h3><p>2012, 2013, 2016, 2017, 2018, 2021, 2023 und 2026 – das Berufskolleg mit den meisten ausgezeichneten Ausbildungsabsolventinnen und -absolventen.</p></li>
      <li><img src="assets/img/logo-europaschule.webp" alt="Europaschule in NRW" width="400" height="250" loading="lazy"><h3>Europaschule in NRW</h3><p>Seit 2009 – als erstes Berufskolleg in Mönchengladbach und als zwölftes landesweit.</p></li>
      <li><img src="assets/img/logo-sor.webp" alt="Schule ohne Rassismus – Schule mit Courage" width="400" height="250" loading="lazy"><h3>Schule ohne Rassismus – Schule mit Courage</h3><p>Seit 2014 Mitglied im Netzwerk. Wir setzen uns aktiv gegen Diskriminierung und Rassismus ein.</p></li>
    </ul>
  </div></section>

  <section class="section" id="europa" aria-labelledby="eu-h"><div class="wrap split">
    <div>
      <h2 id="eu-h">Unsere Partnerschulen in Europa</h2>
      <p class="lead">Durch den Austausch von Lehrkräften, Schülerinnen und Schülern und gemeinsame Projekte sind nicht nur Arbeitsbeziehungen, sondern auch echte Freundschaften entstanden.</p>
      <ul class="partners">{pt}</ul>
    </div>
    <div class="photo"><img src="assets/img/bk-erasmus-1200.webp" alt="Gruppenfoto eines Erasmus-Austauschs" width="750" height="488" loading="lazy"></div>
  </div></section>

  <section class="section tintband" id="kooperationen" aria-labelledby="ko-h"><div class="wrap">
    <h2 id="ko-h">Hochschulkooperationen</h2>
    <p class="lead">Der Abschluss der Fachschule für Wirtschaft (Staatlich geprüfte/r Betriebswirt/in) entspricht im Deutschen und Europäischen Qualifikationsrahmen dem Bachelor (Niveau 6). Wer zusätzlich den akademischen Titel möchte, kann verkürzt und nebenberuflich weiterstudieren:</p>
    <ul class="coops">
      <li><h3>Rheinische Fachhochschule Neuss</h3><p>Präsenzstudium, Bachelor nach 3–4 Semestern</p></li>
      <li><h3>Europäische Fachhochschule (EU-FH)</h3><p>Präsenzstudium, Bachelor nach 3–4 Semestern</p></li>
      <li><h3>Wilhelm Büchner Hochschule</h3><p>Fernstudium, Bachelor of Science nach 3 Semestern</p></li>
    </ul>
    <p class="muted small">Ein anschließendes nebenberufliches Masterstudium ist an allen drei Hochschulen möglich.</p>
  </div></section>
</main>
{foot}
<script>
{menu_js}</script>
</body>
</html>
"""

(ROOT/"ueber-uns.html").write_text(build(), encoding="utf-8")
print("ueber-uns.html erzeugt")
