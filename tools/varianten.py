#!/usr/bin/env python3
"""Erzeugt drei Gestaltungsvarianten der Startseite unter varianten/ (a, b, c)."""
import pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "varianten"; OUT.mkdir(exist_ok=True)
e = html.escape
OLD = "https://www.berufskolleg.biz"
BG = "../bildungsgaenge/"

GROUPS = [
 ("Schulabschluss", "Vollzeit, 1–2 Jahre", [
   ("Ausbildungsvorbereitung","ausbildungsvorbereitung","Erster Schulabschluss"),
   ("Handelsschule (BFS1)","handelsschule-bfs1","Erweiterter Erster Schulabschluss"),
   ("Handelsschule (BFS2)","handelsschule-bfs2","Mittlerer Schulabschluss"),
   ("Höhere Handelsschule","hoehere-handelsschule","Fachhochschulreife"),
   ("Internationale Förderklassen","internationale-foerderklassen","Deutsch lernen und Abschluss")]),
 ("Ausbildung", "Berufsschule im dualen System", [
   ("Industriekaufleute","industriekaufleute","3 Jahre"),
   ("Groß- und Außenhandelsmanagement","gross-und-aussenhandel","3 Jahre"),
   ("Kaufleute für Büromanagement","bueromanagement","3 Jahre"),
   ("Kaufleute im Einzelhandel","einzelhandel","3 Jahre"),
   ("Verkäuferinnen und Verkäufer","verkaeufer","2 Jahre"),
   ("Automobilkaufleute","automobilkaufleute","3 Jahre")]),
 ("Weiterbildung", "Berufsbegleitend, abends", [
   ("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Bachelor Professional")]),
]
NEWS = [
 ("bk-auszeichnung-2026-1200.webp","9. Oktober 2026","Wir sind „Bestes Berufskolleg 2026“!",OLD+"/","Schulleiterin Stephany Kerstges mit der IHK-Urkunde"),
 ("bk-erasmus-1200.webp","Europaschule","Unterwegs mit Erasmus+",OLD+"/ueber-uns/europaschule/eu-projekte/","Gruppenfoto eines Erasmus-Austauschs"),
 ("bk-berufsorientierung-640.webp","Berufsorientierung","Unternehmen stellen sich vor",OLD+"/","Schülerinnen und Schüler an Ständen von Unternehmen"),
]
NAV = [("Bildungsgänge","#bildungsgaenge"),("Aktuelles","#aktuelles"),("Beratung",OLD+"/schuelerinnen-und-schueler/beratung/schulsozialarbeit/"),("Über uns",OLD+"/ueber-uns/auszeichnungen/"),("Kontakt","#kontakt")]
ANM = OLD + "/schuelerinnen-und-schueler/anmeldung/"

def nav():
    return "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in NAV)

def page(key, name, css, main, logo="logo.png"):
    other = "".join(f'<a href="{k}.html"{" aria-current=page" if k==key else ""}>Variante {k.upper()}</a>' for k in "abc")
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Variante {key.upper()} – Berufskolleg Rheydt-Mülfort</title>
<style>
@font-face{{font-family:"Dosis";src:url("../assets/fonts/dosis-latin.woff2") format("woff2");font-weight:200 800;font-display:swap}}
*{{box-sizing:border-box}}img{{max-width:100%;display:block;height:auto}}
body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-size:17px;line-height:1.6;overflow-x:hidden}}
h1,h2,h3{{margin:0;line-height:1.1;font-family:"Dosis",system-ui,sans-serif}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left,0px))}}
@media(min-width:760px){{.wrap{{padding:0 32px}}}}
.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
:focus-visible{{outline:3px solid currentColor;outline-offset:3px}}
.vswitch{{position:sticky;top:0;z-index:60;display:flex;gap:6px;justify-content:center;align-items:center;flex-wrap:wrap;background:#ffd166;color:#3b2a00;font:600 .85rem system-ui;padding:6px 10px}}
.vswitch a{{color:#3b2a00;padding:3px 10px;border-radius:999px;text-decoration:none;border:1px solid rgba(0,0,0,.25)}}
.vswitch a[aria-current]{{background:#3b2a00;color:#ffd166}}
.hdr .wrap{{display:flex;align-items:center;justify-content:space-between;gap:16px;height:80px}}
.hdr img{{height:50px;width:auto}}
.hdr ul{{list-style:none;display:flex;gap:6px;margin:0;padding:0}}
.hdr nav a{{display:block;padding:8px 14px;border-radius:999px;text-decoration:none;font-weight:600}}
@media(max-width:1000px){{.hdr nav{{display:none}}.hdr img{{height:40px}}.hdr .wrap{{height:66px}}}}
.btn{{display:inline-flex;align-items:center;gap:8px;font-weight:700;text-decoration:none;padding:13px 22px;border-radius:999px;line-height:1.2;border:2px solid transparent}}
.arrow::after{{content:"→";margin-left:4px}}
{css}
</style></head>
<body class="v{key}">
<div class="vswitch" role="navigation" aria-label="Varianten">Entwurf · {e(name)} · {other} <a href="../index.html">Aktuelle Fassung</a></div>
<header class="hdr"><div class="wrap"><a href="#"><img src="../assets/{logo}" alt="Berufskolleg Rheydt-Mülfort für Wirtschaft und Verwaltung" width="655" height="217"></a>
<nav aria-label="Hauptnavigation"><ul>{nav()}</ul></nav><a class="btn cta" href="{ANM}">Anmelden</a></div></header>
<main>{main}</main>
<footer class="ftr"><div class="wrap"><span>Berufskolleg Rheydt-Mülfort · Kirschhecke 10 · 41199 Mönchengladbach</span><span><a href="{OLD}/impressum/">Impressum</a> · <a href="{OLD}/datenschutzerklaerung/">Datenschutz</a></span></div></footer>
</body></html>"""

def news_list(cls):
    return f'<ul class="{cls}">' + "".join(f'<li><a href="{u}"><img src="../assets/img/{i}" alt="{e(a)}" loading="lazy"><span class="meta">{e(d)}</span><h3>{e(t)}</h3></a></li>' for i,d,t,u,a in NEWS) + "</ul>"

CONTACT = f"""<dl><div><dt>Telefon</dt><dd>02166 917920</dd></div><div><dt>E-Mail</dt><dd><a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a></dd></div><div><dt>Sekretariat</dt><dd>Mo, Mi, Do 7:30–15:00 · Di, Fr 7:30–13:00</dd></div></dl>"""

# ---------- Variante A: Klar & hell ----------
def var_a():
    cols = "".join(f'<div class="col"><h3>{e(g)}</h3><p>{e(sub)}</p><ul>' + "".join(f'<li><a href="{BG}{s}.html"><span>{e(t)}</span><small>{e(x)}</small></a></li>' for t,s,x in items) + "</ul></div>" for g,sub,items in GROUPS)
    main = f"""
<section class="hero"><div class="wrap grid">
  <div class="txt"><p class="eyebrow">Berufskolleg für Wirtschaft und Verwaltung · Mönchengladbach</p>
  <h1>Mehr als eine Schule.</h1>
  <p class="lead">Vom Schulabschluss über die Ausbildung bis zur Weiterbildung.</p>
  <div class="btns"><a class="btn pri" href="#bildungsgaenge"><span class="arrow">Bildungsgang finden</span></a><a class="btn sec" href="https://bk-rheydt-muelfort.github.io/dein-weg/">Schulberater</a></div>
  <p class="award"><b>IHK</b> Bestes Berufskolleg 2026</p></div>
  <div class="pic"><img src="../assets/img/schulhof-gruppe-1200.webp" alt="Schülerinnen und Schüler vor dem Schulgebäude" width="1200" height="675"></div>
</div></section>
<section class="sec" id="bildungsgaenge"><div class="wrap"><h2>Unsere Bildungsgänge</h2><div class="cols">{cols}</div></div></section>
<section class="sec alt" id="aktuelles"><div class="wrap"><div class="head"><h2>Aktuelles</h2><a href="{OLD}/blog/"><span class="arrow">Alle Beiträge</span></a></div>{news_list("news")}</div></section>
<section class="sec" id="kontakt"><div class="wrap contact"><div><h2>Kontakt</h2><p>Kirschhecke 10 · 41199 Mönchengladbach</p></div>{CONTACT}</div></section>"""
    css = """
body{background:#fff;color:#14213d}
a{color:#0c71c3}
.hdr{border-bottom:1px solid #e6ebf2;background:#fff}
.hdr nav a{color:#14213d}.hdr nav a:hover{color:#0c71c3}
.cta{background:#0c71c3;color:#fff}
.hero{padding:64px 0 72px}
.hero .grid{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:center}
.eyebrow{font-weight:700;color:#0c71c3;font-size:.9rem;margin:0 0 14px}
.hero h1{font-size:clamp(2.6rem,6vw,4.6rem);font-weight:700;color:#0b2545}
.lead{font-size:1.2rem;color:#4a5872;margin:16px 0 28px}
.btns{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.pri{background:#0c71c3;color:#fff}.sec{border-color:#c9d6e6;color:#0b2545}
.award{margin:34px 0 0;font-weight:600;color:#4a5872;display:flex;gap:10px;align-items:center}
.award b{background:#e8f1fb;color:#0c71c3;border-radius:6px;padding:2px 8px;font-size:.8rem}
.pic img{border-radius:24px;aspect-ratio:4/3;object-fit:cover;width:100%}
.sec{padding:80px 0}.alt{background:#f4f7fb}
.sec h2{font-size:clamp(2rem,4vw,2.8rem);color:#0b2545;margin-bottom:34px}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.col h3{font-size:1.5rem;color:#0b2545}.col>p{margin:2px 0 14px;color:#6a7790;font-size:.95rem}
.col ul{list-style:none;margin:0;padding:0;border-top:2px solid #0b2545}
.col a{display:flex;justify-content:space-between;gap:12px;padding:14px 2px;border-bottom:1px solid #e1e7f0;text-decoration:none;color:#14213d;font-weight:600}
.col a:hover span{color:#0c71c3}.col small{color:#6a7790;font-weight:500;text-align:right}
.head{display:flex;justify-content:space-between;align-items:baseline}.head a{font-weight:700;text-decoration:none}
.news{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.news a{text-decoration:none;color:#14213d;display:grid;gap:6px}
.news img{aspect-ratio:3/2;object-fit:cover;width:100%;border-radius:16px;margin-bottom:8px}
.meta{font-size:.85rem;color:#0c71c3;font-weight:700}.news h3{font-size:1.3rem;color:#0b2545}
.contact{display:grid;grid-template-columns:1fr 2fr;gap:30px;align-items:start}.contact h2{margin-bottom:8px}
.contact dl{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin:0}
dt{font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6a7790}dd{margin:4px 0 0;font-weight:600}
.ftr{background:#0b2545;color:#c8d3e6;padding:26px 0;font-size:.92rem}.ftr .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}.ftr a{color:#fff}
@media(max-width:900px){.hero .grid,.cols,.news,.contact,.contact dl{grid-template-columns:1fr}.hero .grid{gap:30px}.pic{order:-1}}
"""
    return page("a", "Klar & hell", css, main)

# ---------- Variante B: Frisch & freundlich ----------
def var_b():
    tiles = "".join(f'<li class="tile t{i}"><h3>{e(g)}</h3><p>{e(sub)}</p><ul>' + "".join(f'<li><a href="{BG}{s}.html">{e(t)}</a></li>' for t,s,x in items) + "</ul></li>" for i,(g,sub,items) in enumerate(GROUPS))
    main = f"""
<section class="hero"><div class="photo"><img src="../assets/img/schueler-gruppe-1200.webp" alt="Schülerinnen und Schüler arbeiten gemeinsam am Laptop" width="1200" height="675"></div>
<div class="wrap"><div class="card"><span class="tag">Bestes Berufskolleg 2026 · IHK</span><h1>Dein Weg in Wirtschaft und Verwaltung.</h1>
<p>Schulabschluss, Ausbildung oder Weiterbildung: Wir begleiten dich.</p>
<a class="btn pri" href="#bildungsgaenge"><span class="arrow">Los geht's</span></a></div></div></section>
<section class="sec" id="bildungsgaenge"><div class="wrap"><h2>Was möchtest du erreichen?</h2><ul class="tiles">{tiles}</ul>
<p class="hint">Noch unsicher? <a href="https://bk-rheydt-muelfort.github.io/dein-weg/">Frag den Schulberater „Dein Weg“.</a></p></div></section>
<section class="sec" id="aktuelles"><div class="wrap"><h2>Neu bei uns</h2>{news_list("news")}</div></section>
<section class="sec contact" id="kontakt"><div class="wrap"><h2>Wir sind für dich da.</h2><p class="addr">Kirschhecke 10 · 41199 Mönchengladbach</p>{CONTACT}</div></section>"""
    css = """
body{background:#f3faf8;color:#123b37}
a{color:#0e7c72}
.hdr{background:#f3faf8}
.hdr nav a{color:#123b37}.hdr nav a:hover{background:#dff3ee}
.cta{background:#123b37;color:#fff}
.hero{position:relative;padding:0 0 40px}
.photo{margin:0 16px;border-radius:32px;overflow:hidden;height:min(62vw,560px)}
.photo img{width:100%;height:100%;object-fit:cover}
.card{position:relative;margin-top:-140px;background:#fff;border-radius:28px;padding:36px 40px;max-width:620px;box-shadow:0 20px 50px rgba(18,59,55,.14)}
.tag{display:inline-block;background:#ffe9a8;color:#5a4300;font-weight:700;font-size:.85rem;border-radius:999px;padding:4px 12px;margin-bottom:14px}
.card h1{font-size:clamp(2.1rem,4.6vw,3.4rem);font-weight:700;color:#123b37}
.card p{font-size:1.15rem;color:#47706b;margin:14px 0 24px}
.pri{background:#14b8a6;color:#062b27}
.sec{padding:72px 0}
.sec h2{font-size:clamp(1.9rem,4vw,2.7rem);margin-bottom:28px;color:#123b37}
.tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tile{border-radius:26px;padding:28px}
.t0{background:#d9f4ee}.t1{background:#dcebfb}.t2{background:#fff0c7}
.tile h3{font-size:1.7rem;color:#123b37}.tile p{margin:2px 0 16px;color:#47706b}
.tile ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.tile a{display:block;background:rgba(255,255,255,.75);border-radius:14px;padding:11px 14px;text-decoration:none;color:#123b37;font-weight:600}
.tile a:hover{background:#fff}.tile a::after{content:" →";color:#0e7c72}
.hint{margin-top:22px;text-align:center}
.news{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.news a{display:grid;gap:4px;background:#fff;border-radius:24px;padding:12px 12px 20px;text-decoration:none;color:#123b37}
.news img{aspect-ratio:3/2;object-fit:cover;width:100%;border-radius:16px;margin-bottom:10px}
.news .meta,.news h3{padding:0 8px}.meta{font-size:.85rem;color:#0e7c72;font-weight:700}.news h3{font-size:1.3rem}
.contact{background:#123b37;color:#dff3ee}.contact h2{color:#fff;margin-bottom:6px}.addr{margin:0 0 24px}
.contact dl{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:0}.contact a{color:#9ff0e2}
dt{font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#9fc9c2}dd{margin:4px 0 0;font-weight:600}
.ftr{background:#0c2926;color:#9fc9c2;padding:24px 0;font-size:.92rem}.ftr .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}.ftr a{color:#fff}
@media(max-width:900px){.tiles,.news,.contact dl{grid-template-columns:1fr}.card{margin:-60px 0 0;padding:26px}}
"""
    return page("b", "Frisch & freundlich", css, main)

# ---------- Variante C: Kräftig & modern ----------
def var_c():
    rows = ""
    for g,sub,items in GROUPS:
        rows += f'<li class="grp">{e(g)}</li>' + "".join(f'<li><a href="{BG}{s}.html"><span class="n">{e(t)}</span><span class="x">{e(x)}</span></a></li>' for t,s,x in items)
    main = f"""
<section class="hero"><div class="wrap grid">
  <div><p class="eyebrow">Bestes Berufskolleg 2026 · IHK Mittlerer Niederrhein</p>
  <h1>Mehr als<br>eine <span>Schule.</span></h1>
  <a class="btn pri" href="#bildungsgaenge"><span class="arrow">Alle Bildungsgänge</span></a></div>
  <div class="stack"><img class="i1" src="../assets/img/teamuebung-640.webp" alt="" ><img class="i2" src="../assets/img/bk-erasmus-1200.webp" alt=""><img class="i3" src="../assets/img/schulhof-gruppe-640.webp" alt=""></div>
</div></section>
<section class="sec" id="bildungsgaenge"><div class="wrap two"><div class="side"><h2>Bildungs&shy;gänge</h2><p>12 Wege zu Schulabschluss, Beruf und Aufstieg – alle an der Kirschhecke.</p><a href="https://bk-rheydt-muelfort.github.io/dein-weg/"><span class="arrow">Schulberater starten</span></a></div><ul class="index">{rows}</ul></div></section>
<section class="sec dark" id="aktuelles"><div class="wrap"><h2>Aktuelles</h2>{news_list("news")}</div></section>
<section class="sec" id="kontakt"><div class="wrap contact"><h2>Kontakt</h2><div><p class="addr">Kirschhecke 10, 41199 Mönchengladbach</p>{CONTACT}</div></div></section>"""
    css = """
body{background:#fff;color:#111827}
a{color:#2f54eb}
.hdr{background:#0f1235}.hdr nav a{color:#e5e7ff}.hdr nav a:hover{background:rgba(255,255,255,.1)}
.cta{background:#ff6b4a;color:#fff}
.hero{background:#0f1235;color:#fff;padding:60px 0 90px;overflow:hidden}
.hero .grid{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:center}
.eyebrow{color:#a5b4fc;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.85rem;margin:0 0 18px}
.hero h1{font-size:clamp(3rem,9vw,6.6rem);font-weight:800;letter-spacing:-.02em;line-height:.95;margin-bottom:34px}
.hero h1 span{color:#ff6b4a}
.pri{background:#fff;color:#0f1235}
.stack{position:relative;height:420px}
.stack img{position:absolute;object-fit:cover;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,.35)}
.i1{width:55%;height:55%;top:0;right:0}.i2{width:62%;height:50%;bottom:0;left:0}.i3{width:40%;height:38%;bottom:12%;right:4%;border:4px solid #0f1235}
.sec{padding:84px 0}
.sec h2{font-size:clamp(2.2rem,5vw,3.4rem);font-weight:800;letter-spacing:-.01em}
.two{display:grid;grid-template-columns:1fr 2fr;gap:48px}
.side p{color:#4b5563;margin:14px 0}.side a{font-weight:700;text-decoration:none}
.index{list-style:none;margin:0;padding:0}
.index .grp{font-size:.8rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:#ff6b4a;padding:26px 0 8px}
.index .grp:first-child{padding-top:0}
.index a{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:14px 0;border-bottom:1px solid #e5e7eb;text-decoration:none;color:#111827}
.index .n{font-family:"Dosis",system-ui,sans-serif;font-size:1.45rem;font-weight:700}
.index .x{color:#6b7280;font-size:.92rem;text-align:right}
.index a:hover .n{color:#2f54eb}.index a:hover .n::after{content:" →"}
.dark{background:#0f1235;color:#fff}.dark h2{margin-bottom:30px}
.news{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.news a{text-decoration:none;color:#fff;display:grid;gap:6px}
.news img{aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:18px;margin-bottom:8px}
.meta{color:#a5b4fc;font-size:.85rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em}.news h3{font-size:1.4rem}
.contact{display:grid;grid-template-columns:1fr 2fr;gap:48px}.addr{font-size:1.3rem;font-weight:600;margin:0 0 20px}
.contact dl{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:0}
dt{font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6b7280}dd{margin:4px 0 0;font-weight:600}
.ftr{background:#0f1235;color:#a5b4fc;padding:24px 0;font-size:.92rem;border-top:1px solid rgba(255,255,255,.1)}.ftr .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}.ftr a{color:#fff}
@media(max-width:900px){.hero .grid,.two,.news,.contact,.contact dl{grid-template-columns:1fr}.stack{height:300px}}
"""
    return page("c", "Kräftig & modern", css, main, logo="logo-hell.png")

for k,f in (("a",var_a),("b",var_b),("c",var_c)):
    (OUT/f"{k}.html").write_text(f(), encoding="utf-8")
print("ok")
