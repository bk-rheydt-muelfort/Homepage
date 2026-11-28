#!/usr/bin/env python3
"""Eigenständiger Schulberater (ohne neue Homepage). Verlinkt auf www.berufskolleg.biz.
Aufruf: python3 tools/schulberater_solo.py ZIELORDNER   (z. B. ../dein-weg/neu)"""
import json, pathlib, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"tools"))
import schulberater as sb          # erzeugt nebenbei schulberater.html der Homepage
from generate import COURSES

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT/"solo").resolve()
OLD = "https://www.berufskolleg.biz"
ANM = OLD + "/schuelerinnen-und-schueler/anmeldung/"
OLDMAP = {c["slug"]: OLD + c["old"] for c in COURSES}

html = sb.build()
# Kopf: Schullogo + Schulberater-Logo, keine Homepage-Navigation
head = f'''<header class="header solo-head">
  <div class="wrap">
    <a class="logo" href="{OLD}" aria-label="Berufskolleg Rheydt-Mülfort – Schulhomepage"><img src="assets/logo-hell.png" alt="Berufskolleg Rheydt-Mülfort für Wirtschaft und Verwaltung" width="655" height="217"></a>
    <a class="btn btn-dark" href="{ANM}">Anmeldung</a>
  </div>
</header>'''
html = html[:html.index('<div class="draft-note"')] + head + html[html.index("</header>")+9:]
foot = f'''<footer class="footer solo-foot">
  <div class="wrap">
    <div class="legal">
      <span>© 2026 Berufskolleg Rheydt-Mülfort · Kirschhecke 10 · 41199 Mönchengladbach · <a href="tel:+492166917920">02166 917920</a></span>
      <span><a href="{OLD}">www.berufskolleg.biz</a> · <a href="{OLD}/impressum/">Impressum</a> · <a href="{OLD}/datenschutzerklaerung/">Datenschutz</a></span>
    </div>
  </div>
</footer>
'''
html = html[:html.index('<footer class="footer">')] + foot + html[html.index("</footer>")+10:]
# Menü-Skript entfällt (kein Menü)
html = re.sub(r"// Mobiles Menü.*?\n(?=const D=)", "", html, flags=re.S)
html = html.replace('<meta name="robots" content="noindex, nofollow">\n', "")
html = html.replace('href="assets/style.css"', 'href="assets/style.css?v=2"')

# Daten: Anmeldetexte auf die Schulhomepage verlinken
data = json.loads(re.search(r"const D=(\{.*?\});\n", html, re.S).group(1))
data["old"] = OLDMAP
data["reg"] = {
 "voll": [["Online bewerben", 'Über <a href="https://www.schulbewerbung.de">schulbewerbung.de</a> mit dem Startcode deiner jetzigen Schule. Ohne Startcode kannst du dich dort neu registrieren.'],
          ["Unterlagen abgeben", f'Das ausgedruckte, unterschriebene Anmeldeformular und die Einwilligung zum Datenschutz im Sekretariat abgeben. <a href="{ANM}">Alle Infos und Formulare zur Anmeldung</a>']],
 "bs":   [["Anmeldung durch den Betrieb", f'Dein Ausbildungsbetrieb meldet dich an: über <a href="https://www.schulbewerbung.de">schulbewerbung.de</a> oder mit dem Anmeldeformular. <a href="{ANM}">Zum Anmeldeformular</a>'],
          ["Erster Schultag", "Bring eine Kopie des Ausbildungsvertrags und deines letzten Zeugnisses mit. Die Einschulungstermine stehen auf der Schulhomepage."]],
 "if":   data["reg"]["if"],
 "fs":   [["Anmelden ab Februar", f'Mit dem Anmeldeformular der Fachschule, Lebenslauf und Nachweisen im Sekretariat. <a href="{ANM}">Zum Anmeldeformular</a>'],
          ["Start nach den Sommerferien", "Die Einschulung ist am letzten Tag der Sommerferien."]],
}
for c in data["choices"]:
    if c.get("berufe"):
        c["berufe"] = [[n, OLDMAP[s]] for n, s in c["berufe"]]
html = re.sub(r"const D=\{.*?\};\n", lambda m: "const D=" + json.dumps(data, ensure_ascii=False) + ";\n", html, count=1, flags=re.S)
html = html.replace("'<li><a href=\"bildungsgaenge/'+s+'.html\">'+n+'</a></li>'", "'<li><a href=\"'+s+'\">'+n+'</a></li>'")
html = html.replace("more.href='bildungsgaenge/'+cur.slug+'.html'", "more.href=D.old[cur.slug]")
html = re.sub(r'href="bildungsgaenge/([a-z0-9-]+)\.html"', lambda m: f'href="{OLDMAP.get(m.group(1), ANM)}"', html)
assert "bildungsgaenge/" not in html, "interner Link übrig"
assert "assets/downloads" not in html

OUT.mkdir(parents=True, exist_ok=True)
(OUT/"assets/fonts").mkdir(parents=True, exist_ok=True)
(OUT/"assets/img").mkdir(parents=True, exist_ok=True)
(OUT/"index.html").write_text(html, encoding="utf-8")
css = (ROOT/"assets/style.css").read_text(encoding="utf-8")
css += "\n/* Eigenständiger Schulberater */\n.solo-head .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px}\n.solo-foot{padding:28px 0}.solo-foot .legal{border-top:0;margin:0;padding:0}\n"
(OUT/"assets/style.css").write_text(css, encoding="utf-8")
shutil.copy(ROOT/"assets/logo-hell.png", OUT/"assets/logo-hell.png")
shutil.copy(ROOT/"assets/img/logo-schulberater.webp", OUT/"assets/img/logo-schulberater.webp")
for f in (ROOT/"assets/fonts").iterdir():
    shutil.copy(f, OUT/"assets/fonts"/f.name)
print("Schulberater eigenständig erzeugt:", OUT/"index.html")
