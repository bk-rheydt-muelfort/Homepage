#!/usr/bin/env python3
"""Erzeugt schulberater.html: 1. Abschluss wählen → 2. passender Bildungsgang → 3. Anmeldung & Infotag.
Kopf/Fußzeile kommen aus index.html. Aufruf: python3 tools/schulberater.py"""
import html, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
e = html.escape

INFOTAG = "Samstag, 13. Februar 2027"
SCHULBEWERBUNG = "https://www.schulbewerbung.de"
FORM_BS = "assets/downloads/2027_anmeldeformular_berufsschule_ausfuellbar.pdf"

# Antwort auf Frage 1 → Empfehlung
CHOICES = [
 dict(id="kein", label="Noch keinen Abschluss", hint="Schulpflicht in der Sekundarstufe I erfüllt",
  slug="ausbildungsvorbereitung", name="Ausbildungsvorbereitung", goal="Erster Schulabschluss", dauer="1 Jahr",
  points=["3 Tage Praktikum (Mo–Mi), 2 Tage Schule (Do + Fr)","Intensive Begleitung durch die Schulsozialarbeit","Hilfe bei Berufswahl und Praktikumssuche"],
  then="Danach: Handelsschule (BFS1) oder direkt in eine Ausbildung.", reg="voll"),
 dict(id="esa", label="Erster Schulabschluss", hint="früher: Hauptschulabschluss nach Klasse 9",
  slug="handelsschule-bfs1", name="Handelsschule (BFS1)", goal="Erweiterter Erster Schulabschluss", dauer="1 Jahr",
  points=["Kaufmännische Grundlagen in kleinen Klassen","30 Praktikumstage, vor allem im Einzelhandel","Enge Zusammenarbeit mit der Agentur für Arbeit"],
  then="Danach: Handelsschule (BFS2) zum Mittleren Schulabschluss oder eine Ausbildung.", reg="voll"),
 dict(id="eesa", label="Erweiterter Erster Schulabschluss", hint="früher: Hauptschulabschluss nach Klasse 10",
  slug="handelsschule-bfs2", name="Handelsschule (BFS2)", goal="Mittlerer Schulabschluss", dauer="1 Jahr",
  points=["Mittlerer Schulabschluss plus berufliche Kenntnisse","Mit guten Noten: Berechtigung für die Oberstufe","30 Praktikumstage im kaufmännischen Bereich"],
  then="Danach: Höhere Handelsschule (Fachhochschulreife) oder eine Ausbildung.", reg="voll"),
 dict(id="msa", label="Mittlerer Schulabschluss (FOR)", hint="oder Versetzung in die Oberstufe am Gymnasium",
  slug="hoehere-handelsschule", name="Höhere Handelsschule", goal="Fachhochschulreife (schulischer Teil)", dauer="2 Jahre",
  points=["BWL mit Rechnungswesen, Deutsch, Mathe, Englisch","Schwerpunkt wählbar: Business-IT, Englisch, Europakunde oder Spanisch","Betriebspraktikum am Ende des ersten Jahres"],
  then="Danach: Studium an einer Fachhochschule oder eine Ausbildung mit Vorsprung.", reg="voll",
  extra="Für die Anmeldung brauchst du einen tabellarischen Lebenslauf und eine Kopie deines letzten Zeugnisses. Es gibt eine schriftliche Beratungsprüfung in Deutsch, Englisch und Mathe."),
 dict(id="neu", label="Neu in Deutschland", hint="ab 16 Jahren, du lernst noch Deutsch",
  slug="internationale-foerderklassen", name="Internationale Förderklassen", goal="Erster Schulabschluss (vergleichbar)", dauer="1–2 Jahre",
  points=["Deutsch lernen, auch die Fachsprache","Mathe, Englisch und kaufmännische Fächer","Zwei Wochen Praktikum und Berufsorientierung"],
  then="Danach: ein weiterer Bildungsgang am Berufskolleg oder eine Ausbildung.", reg="if"),
 dict(id="azubi", label="Ich habe einen Ausbildungsplatz", hint="kaufmännische Ausbildung",
  slug=None, name="Berufsschule", goal="Berufsabschluss + Berufsschulabschluss", dauer="2–3 Jahre",
  points=["Unterricht an 1–2 Tagen pro Woche, sonst im Betrieb","Fächer passend zu deinem Beruf","Abschlussprüfung vor der IHK"],
  then="Danach: Fachschule für Wirtschaft bis zum Bachelor Professional.", reg="bs",
  berufe=[("Industriekaufleute","industriekaufleute"),("Groß- und Außenhandelsmanagement","gross-und-aussenhandel"),("Kaufleute für Büromanagement","bueromanagement"),("Kaufleute im Einzelhandel","einzelhandel"),("Verkäuferinnen und Verkäufer","verkaeufer"),("Automobilkaufleute","automobilkaufleute")]),
 dict(id="beruf", label="Abgeschlossene Ausbildung", hint="und du willst dich weiterbilden",
  slug="fachschule-fuer-wirtschaft", name="Fachschule für Wirtschaft", goal="Bachelor Professional", dauer="6–8 Semester",
  points=["Berufsbegleitend: Di + Do abends, Samstagvormittag","Schwerpunkt Personalwirtschaft, inklusive Ausbildereignung","Keine Semestergebühren"],
  then="Danach: Führungsaufgaben im mittleren Management.", reg="fs",
  extra="Voraussetzung: einschlägige Ausbildung, Berufsschulabschluss, Fachoberschulreife und ein Jahr Berufstätigkeit (auch begleitend) – oder fünf Jahre Berufserfahrung."),
]

REG = {
 "voll": [("Online bewerben", f'Über <a href="{SCHULBEWERBUNG}">schulbewerbung.de</a> mit dem Startcode deiner jetzigen Schule. Ohne Startcode kannst du dich dort neu registrieren.'),
          ("Unterlagen abgeben", "Das ausgedruckte, unterschriebene Anmeldeformular und die Einwilligung zum Datenschutz im Sekretariat abgeben.")],
 "bs":   [("Anmeldung durch den Betrieb", f'Dein Ausbildungsbetrieb meldet dich an: über <a href="{SCHULBEWERBUNG}">schulbewerbung.de</a> oder mit dem <a href="{FORM_BS}">Anmeldeformular 2027/28 (PDF)</a> an info@berufskolleg.biz.'),
          ("Erster Schultag", "Bring eine Kopie des Ausbildungsvertrags und deines letzten Zeugnisses mit. Die Einschulungstermine stehen unter Aktuelles.")],
 "if":   [("Beratung bei der KI", "Die Aufnahme läuft über die Kommunale Integrationsstelle der Stadt Mönchengladbach: Fliethstraße 90, Telefon 02161 25-53784, ki@moenchengladbach.de."),
          ("Schulplatz", "Die KI vermittelt dich an unser Berufskolleg und begleitet die Anmeldung.")],
 "fs":   [("Anmelden ab Februar", 'Mit dem <a href="assets/downloads/anmeldeformular-fachschule.pdf">Anmeldeformular der Fachschule (PDF)</a>, Lebenslauf und Nachweisen im Sekretariat.'),
          ("Start nach den Sommerferien", "Die Einschulung ist am letzten Tag der Sommerferien.")],
}

def options():
    return "".join(f'<li><button type="button" class="opt" data-id="{c["id"]}"><strong>{e(c["label"])}</strong><span>{e(c["hint"])}</span></button></li>' for c in CHOICES)

def noscript():
    return "".join(f'<li><a href="bildungsgaenge/{c["slug"] or "industriekaufleute"}.html">{e(c["label"])} → {e(c["name"])}</a></li>' for c in CHOICES)

def build():
    src = (ROOT/"index.html").read_text(encoding="utf-8")
    head = src[src.index('<div class="draft-note"'):src.index("</header>")+9]
    head = re.sub(r'href="#(?!top")', 'href="index.html#', head).replace('href="#top"','href="index.html"')
    foot = src[src.index('<footer class="footer">'):src.index("<script>")]
    foot = re.sub(r'href="#(?!top")', 'href="index.html#', foot).replace('href="#top"','href="index.html"')
    menu_js = src[src.index("<script>")+8:src.index("// Bildungsgang-Filter")]
    data = json.dumps({"choices":CHOICES,"reg":REG}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Schulberater – Berufskolleg Rheydt-Mülfort</title>
<meta name="description" content="In drei Schritten zum passenden Bildungsgang am Berufskolleg Rheydt-Mülfort: Abschluss wählen, Bildungsgang finden, anmelden.">
<meta name="theme-color" content="#123b37">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="home">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{head}
<main id="inhalt" class="advisor">
  <section class="adv-head"><div class="wrap">
    <span class="tag">Schulberater</span>
    <h1>Welcher Bildungsgang passt zu dir?</h1>
    <ol class="steps" aria-label="Fortschritt">
      <li data-step="1" class="on"><b>1</b> Dein Abschluss</li>
      <li data-step="2"><b>2</b> Dein Bildungsgang</li>
      <li data-step="3"><b>3</b> Anmeldung</li>
    </ol>
  </div></section>

  <section class="wrap adv-body">
    <div id="s1" class="panel">
      <h2 tabindex="-1">Mit welchem Abschluss kommst du zu uns?</h2>
      <ul class="opts">{options()}</ul>
      <noscript><ul class="plain">{noscript()}</ul></noscript>
    </div>

    <div id="s2" class="panel" hidden>
      <button type="button" class="back" data-go="1">← Anderen Abschluss wählen</button>
      <h2 tabindex="-1">Das passt zu dir:</h2>
      <article class="result">
        <div class="r-main">
          <span class="r-from"></span>
          <h3 class="r-name"></h3>
          <ul class="checks r-points"></ul>
          <p class="r-then muted"></p>
          <p class="r-extra muted small"></p>
          <div class="r-berufe" hidden><h4>Welchen Beruf lernst du?</h4><ul class="r-blist"></ul></div>
        </div>
        <dl class="r-facts">
          <div><dt>Abschluss</dt><dd class="r-goal"></dd></div>
          <div><dt>Dauer</dt><dd class="r-dauer"></dd></div>
          <div><dt>Standort</dt><dd>Kirschhecke 10</dd></div>
        </dl>
      </article>
      <div class="btns"><a class="btn btn-soft r-more" href="#"><span class="arrow">Alle Infos zum Bildungsgang</span></a><button type="button" class="btn btn-primary" data-go="3"><span class="arrow">Weiter zur Anmeldung</span></button></div>
    </div>

    <div id="s3" class="panel" hidden>
      <button type="button" class="back" data-go="2">← Zurück zum Bildungsgang</button>
      <h2 tabindex="-1">So meldest du dich an</h2>
      <ol class="reg"></ol>
      <aside class="infotag">
        <span class="tag">Infotag</span>
        <h3>{INFOTAG}</h3>
        <p>Lerne uns vorher kennen: Bildungsgänge, Lehrkräfte und Schule live erleben. Komm einfach vorbei – Kirschhecke 10.</p>
      </aside>
      <p class="muted small">Fragen? Sekretariat: 02166 917920 · <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a></p>
    </div>
  </section>
</main>
{foot}
<script>
{menu_js}
const D={data};
let cur=null;
const $=s=>document.querySelector(s);
function show(n){{
  [1,2,3].forEach(i=>{{document.getElementById('s'+i).hidden=i!==n;const li=document.querySelector('.steps [data-step="'+i+'"]');li.classList.toggle('on',i<=n);if(i===n)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current')}});
  const h=document.querySelector('#s'+n+' h2');h.focus({{preventScroll:true}});
  document.querySelector('.adv-head').scrollIntoView({{behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});
}}
function pick(id){{
  cur=D.choices.find(c=>c.id===id);
  $('.r-from').textContent='Mit „'+cur.label+'“';
  $('.r-name').textContent=cur.name;
  $('.r-goal').textContent=cur.goal;$('.r-dauer').textContent=cur.dauer;
  $('.r-points').innerHTML=cur.points.map(p=>'<li>'+p+'</li>').join('');
  $('.r-then').textContent=cur.then;$('.r-extra').textContent=cur.extra||'';
  const b=$('.r-berufe');b.hidden=!cur.berufe;
  if(cur.berufe)$('.r-blist').innerHTML=cur.berufe.map(([n,s])=>'<li><a href="bildungsgaenge/'+s+'.html">'+n+'</a></li>').join('');
  const more=$('.r-more');more.hidden=!cur.slug;if(cur.slug)more.href='bildungsgaenge/'+cur.slug+'.html';
  $('.reg').innerHTML=D.reg[cur.reg].map(([t,x])=>'<li><h3>'+t+'</h3><p>'+x+'</p></li>').join('');
  show(2);
}}
document.querySelectorAll('.opt').forEach(b=>b.addEventListener('click',()=>pick(b.dataset.id)));
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>show(+b.dataset.go)));
</script>
</body>
</html>
"""

(ROOT/"schulberater.html").write_text(build(), encoding="utf-8")
print("schulberater.html erzeugt")
