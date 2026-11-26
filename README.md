# Entwurf: neue Homepage Berufskolleg Rheydt-Mülfort

Statischer Entwurf (HTML/CSS, ohne Framework) für eine modernisierte Homepage von www.berufskolleg.biz.

**Vorschau:** https://bk-rheydt-muelfort.github.io/Homepage/

## Aufbau
- `index.html` – Startseite mit Zielgruppen-Einstieg, Bildungsgang-Finder, Aktuelles, Schulleben, Beratung, Standorten
- `bildungsgaenge/*.html` – 12 Bildungsgang-Seiten (Steckbrief, Wochenplan, Fächer, Prüfungsgewichtung, Anschluss)
- `assets/style.css` – gesamte Gestaltung
- `tools/generate.py` – erzeugt die Bildungsgang-Seiten aus den Daten oben in der Datei:
  `python3 tools/generate.py`

## Hinweise
- Inhalte von berufskolleg.biz (Stand November 2026); Fotos von berufskolleg.biz und aus dem Schulberater „Dein Weg“.
- Schrift Dosis (SIL Open Font License) lokal eingebunden – keine Verbindung zu Google, keine Cookies, kein Tracking.
- Barrierearm: Zoom erlaubt, Sprunglink, sichtbarer Tastaturfokus, Alternativtexte, `prefers-reduced-motion`.
- Links, die noch nicht nachgebaut sind, führen auf die bisherige Seite.
