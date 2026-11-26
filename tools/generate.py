#!/usr/bin/env python3
"""Erzeugt die Bildungsgang-Seiten unter bildungsgaenge/ aus den Daten unten.
Kopf- und Fußzeile werden aus index.html übernommen.
Aufruf:  python3 tools/generate.py   (im Projektordner)
Inhalte: www.berufskolleg.biz (Stand November 2026)."""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = "https://www.berufskolleg.biz"
ANMELDUNG = OLD + "/schuelerinnen-und-schueler/anmeldung/"
FORM_BS = OLD + "/wp-content/uploads/2026/01/2026_anmeldeformular_berufsschule_ausfuellbar.pdf"

# Wochentage: S = Schule, P = Praktikum/Betrieb, - = frei, A = Abend
COURSES = [
 dict(slug="ausbildungsvorbereitung", old="/ausbildungsvorbereitung/", cat="Vollzeit", tag="schule",
  title="Ausbildungsvorbereitung", short="AV", img="bg-av",
  claim="Drei Tage Praxis, zwei Tage Schule – und dein Erster Schulabschluss.",
  intro="In der Ausbildungsvorbereitung arbeitest du an drei von fünf Wochentagen in einem Praktikum und lernst kaufmännische Berufe von innen kennen. Gleichzeitig kannst du den Hauptschulabschluss nach Klasse 9 erwerben. Viele ehemalige Schülerinnen und Schüler finden so einen Ausbildungsplatz.",
  facts=[("Abschluss","Erster Schulabschluss (Hauptschulabschluss nach Klasse 9)"),("Dauer","1 Jahr"),("Voraussetzung","Kein Schulabschluss, Sekundarstufe I beendet, kein Ausbildungsverhältnis. Auch als 10. Pflichtschuljahr möglich."),("Unterricht","Do und Fr, 7:55–14:00 Uhr"),("Standort","Kirschhecke 10")],
  week=dict(Mo="P",Di="P",Mi="P",Do="S",Fr="S"), weeknote="Montag bis Mittwoch arbeitest du im Praktikum, Donnerstag und Freitag hast du Unterricht. Noch keinen Praktikumsplatz? Wir suchen gemeinsam mit dir.",
  highlights=["Intensive Begleitung durch die Schulsozialarbeit","Individuelle Förderung in persönlichen Gesprächen","Fachunterricht kombiniert mit wirtschaftlichen Lernsituationen","Hilfe bei der Berufswahl","Praktikum als ständige Vor-Ort-Bewerbung – wird begleitet und benotet"],
  subjects=[("Berufsbezogen",["Geschäftsprozesse","Personalbezogene Prozesse","Mathematik","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Politik / Gesellschaftslehre","Religion"])],
  next=[("Handelsschule (BFS1)","handelsschule-bfs1","Das Abschlusszeugnis berechtigt zum Besuch der Handelsschule."),("Ausbildung","#","Mit Praktikum und Abschluss in eine Berufsausbildung starten.")],
  contacts=["Frau Danaci","Frau Kauder"],
  docs=[("Flyer in einfacher Sprache (PDF)", OLD+"/wp-content/uploads/2025/01/40_Ausbildungsvorbereitung_Flyer_einfache-Sprache-3.pdf")]),

 dict(slug="handelsschule-bfs1", old="/handelsschule-bfs1/", cat="Vollzeit", tag="schule",
  title="Handelsschule (BFS1)", short="HS9", img="bg-bfs1",
  claim="Kaufmännisches Know-how plus Erweiterter Erster Schulabschluss.",
  intro="Mit dem Erweiterten Ersten Schulabschluss und einer Bescheinigung über berufliche Kenntnisse verbesserst du deine Chancen auf dem Ausbildungsmarkt. Im 30-tägigen Praktikum lernst du kaufmännische Berufe kennen, vor allem im Einzelhandel.",
  facts=[("Abschluss","Erweiterter Erster Schulabschluss"),("Dauer","1 Jahr (einmal wiederholbar)"),("Voraussetzung","Vollzeitschulpflicht erfüllt und Erster Schulabschluss oder gleichwertig"),("Unterricht","Mo–Fr ab 7:55 Uhr, 30–35 Stunden pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="S",Di="S",Mi="S",Do="S",Fr="S"), weeknote="Unterricht an fünf Tagen in kleinen Klassen. Das Praktikum umfasst 30 Tage: eine Woche nach den Herbstferien und danach 25 Wochen lang je einen Tag.",
  highlights=["Kleine Klassen und berufsnahe Handlungssituationen","30-tägiges Praktikum","Methoden, Teamarbeit und moderne Informationssysteme","Enge Zusammenarbeit mit der Agentur für Arbeit"],
  subjects=[("Berufsbezogen",["Geschäftsprozesse","Personalbezogene Prozesse","Mathematik","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"]),("Differenzierung",["Kaufmännisches Rechnen","Projektkurs"])],
  next=[("Handelsschule (BFS2)","handelsschule-bfs2","Im zweiten Jahr den Mittleren Schulabschluss erwerben."),("Ausbildung","#","Direkt in eine kaufmännische Ausbildung starten.")],
  contacts=["Stefanie Hölscher","Birgit Hares","Violetta Boegel"],
  docs=[("Flyer Handelsschule Typ I (PDF)", OLD+"/wp-content/uploads/2025/01/40_Berufskolleg_Handelsschule-BFS1_Flyer.pdf")]),

 dict(slug="handelsschule-bfs2", old="/handelsschule-bfs2/", cat="Vollzeit", tag="schule",
  title="Handelsschule (BFS2)", short="HS10", img="bg-bfs2",
  claim="Mittlerer Schulabschluss – mit guten Noten sogar mit Q-Vermerk.",
  intro="Mit dem Mittleren Schulabschluss und einer Bescheinigung über berufliche Kenntnisse verbesserst du deine Chancen auf dem Ausbildungsmarkt in besonderem Maße. Mit guten Noten erwirbst du zusätzlich die Berechtigung zur gymnasialen Oberstufe.",
  facts=[("Abschluss","Mittlerer Schulabschluss (Fachoberschulreife), ggf. mit Berechtigung zur gymnasialen Oberstufe"),("Dauer","1 Jahr (einmal wiederholbar)"),("Voraussetzung","Erweiterter Erster Schulabschluss oder gleichwertig, oder Oberstufenberechtigung nach Klasse 9 am Gymnasium"),("Unterricht","Mo–Fr ab 7:55 Uhr, 30–35 Stunden pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="S",Di="S",Mi="S",Do="S",Fr="S"), weeknote="Unterricht an fünf Tagen. Dazu kommt ein 30-tägiges Praktikum: eine Woche nach den Herbstferien und danach 25 Wochen lang je einen Tag.",
  highlights=["Oberstufenberechtigung bei mindestens „gut“ in Deutsch, Mathe und Englisch (oder „befriedigend“ in diesen und drei weiteren Fächern)","30-tägiges Praktikum, vor allem im Einzelhandel","Allgemeinbildung und Berufsvorbereitung in einem Jahr","Kleine Klassen"],
  subjects=[("Berufsbezogen",["Geschäftsprozesse","Gesamtwirtschaftliche Prozesse","Personalbezogene Prozesse","Mathematik","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"]),("Differenzierung",["Kaufmännisches Rechnen","Verkaufskunde"])],
  next=[("Höhere Handelsschule","hoehere-handelsschule","In zwei Jahren zur Fachhochschulreife."),("Ausbildung","#","Mit dem Mittleren Schulabschluss in die Ausbildung.")],
  contacts=["Sonja Grieger","Violetta Boegel","Birgit Hares"],
  docs=[("Flyer Handelsschule (PDF)", OLD+"/wp-content/uploads/2025/01/40_Berufskolleg_Handelsschule-BFS2_Flyer.pdf")]),

 dict(slug="hoehere-handelsschule", old="/hoehere-handelsschule/", cat="Vollzeit", tag="fhr",
  title="Höhere Handelsschule", short="HH", img="bg-hbfs",
  claim="Wirtschaft verstehen und die Fachhochschulreife holen.",
  intro="Anhand realitätsnaher betriebswirtschaftlicher Situationen erwirbst du fundiertes Wirtschaftswissen. Das verbessert deine Chancen auf einen attraktiven Ausbildungsplatz und schafft die schulischen Voraussetzungen für ein Fachhochschulstudium.",
  facts=[("Abschluss","Schulischer Teil der Fachhochschulreife"),("Dauer","2 Jahre (1. Jahr mit Betriebspraktikum)"),("Voraussetzung","Mittlerer Schulabschluss oder Oberstufenberechtigung nach Klasse 9 am Gymnasium. Schriftliche Beratungsprüfung in Deutsch, Englisch, Mathematik."),("Unterricht","Mo–Fr im Klassenverband"),("Standort","Kirschhecke 10")],
  week=dict(Mo="S",Di="S",Mi="S",Do="S",Fr="S"), weeknote="Unterricht an fünf Tagen. Am Ende des ersten Schuljahres absolvierst du ein schulisch begleitetes Betriebspraktikum.",
  highlights=["Eigene Schwerpunkte: Business-IT, Englisch, Europakunde oder Spanisch","Berufsorientierung mit Ausbildungsbetrieben und Agentur für Arbeit","Förderkurse in Deutsch, Mathe, Englisch und BWL","Volle Fachhochschulreife nach Praktikum oder Ausbildung"],
  subjects=[("Berufsbezogen",["BWL mit Rechnungswesen","Volkswirtschaftslehre","Informationswirtschaft","Mathematik","Physik","Englisch","Business-IT / Englisch / Europakunde / Spanisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"]),("Wahlpflicht",["Förderkurse D, M, E, BWL"])],
  exam=dict(title="Abschlussprüfung", note="Für den schulischen Teil der Fachhochschulreife müssen diese Prüfungsfächer bestanden werden:", parts=[("BWL mit Rechnungswesen",1),("Deutsch",1),("Mathematik",1),("Englisch",1)], equal=True),
  next=[("Studium","#","Mit voller Fachhochschulreife an Fachhochschulen studieren."),("Ausbildung","#","Mit Vorsprung in eine kaufmännische Ausbildung.")],
  contacts=["Sophie Benczek","Moritz Elsen"],
  docs=[("Flyer Höhere Handelsschule (PDF)", OLD+"/wp-content/uploads/2025/01/40_Berufskolleg_Hoehere-Handelsschule_Flyer.pdf")]),

 dict(slug="internationale-foerderklassen", old="/internationale-foerderklassen/", cat="Vollzeit", tag="schule",
  title="Internationale Förderklassen", short="IF", img="bg-if",
  claim="Deutsch lernen und den Weg in Schule und Beruf finden.",
  intro="Die Internationalen Förderklassen sind für neu zugewanderte Jugendliche ab 16 Jahren, die zum ersten Mal eine deutschsprachige Schule besuchen. Im Mittelpunkt stehen Deutschkenntnisse, auch in der Fachsprache, und berufliche Orientierung.",
  facts=[("Abschluss","Vergleichbar mit dem Ersten Schulabschluss"),("Dauer","1 Jahr, bei geringen Deutschkenntnissen 2 Jahre"),("Voraussetzung","Ab 16 Jahren, neu zugewandert. Aufnahme nur über die Kommunale Integrationsstelle (KI)."),("Kontakt KI","Fliethstraße 90, Mönchengladbach · 02161 25-53784 · ki@moenchengladbach.de"),("Standort","Kirschhecke 10")],
  highlights=["Deutsch als Zweitsprache, inklusive Fachsprache","Zweiwöchiges Praktikum mit Vor- und Nachbereitung","Unterstützung durch Berufsorientierungsbüro (BOB), Schulsozialarbeit und Jugendberufsagentur","Teilnahme an „Kein Abschluss ohne Anschluss“ (KAoA)"],
  subjects=[("Berufsbezogen",["Mathematik","Englisch","Geschäftsprozesse","Personalbezogene Prozesse","Gesamtwirtschaftliche Prozesse"]),("Berufsübergreifend",["Deutsch / Kommunikation","Politik / Gesellschaftslehre","Religionslehre","Sport / Gesundheit"]),("Differenzierung",["Mathe-Förderung","Alltagswissen"])],
  next=[("Weiterer Bildungsgang","handelsschule-bfs1","Danach einen höheren Abschluss am Berufskolleg anstreben."),("Ausbildung","#","Mit beruflichen Grundkenntnissen in eine Ausbildung.")],
  contacts=["Dilay Tasgin","Alicia Rodriguez"], docs=[]),

 dict(slug="industriekaufleute", old="/industriekaufleute/", cat="Berufsschule", tag="beruf",
  title="Industriekaufleute", short="IK", img="schueler-gruppe",
  claim="Multitalente für jede Branche.",
  intro="Industriekaufleute arbeiten in allen Branchen und Unternehmensgrößen: in Beschaffung, Produktion und Absatz ebenso wie in Controlling, Personal- oder Finanzmanagement. Einer der beliebtesten und anspruchsvollsten kaufmännischen Ausbildungsberufe.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","3 Jahre"),("Unterricht","Unter- und Mittelstufe 2 Tage, Oberstufe 1 Tag pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="S",Di="P",Mi="S",Do="P",Fr="P"), weeknote="Beispielwoche Unter-/Mittelstufe: zwei Tage Berufsschule, drei Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Industrielle Geschäftsprozesse","Industrielle Steuerung und Kontrolle","Wirtschafts- und Sozialprozesse","Fremdsprachliche Kommunikation"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"]),("Differenzierung",["Datenverarbeitung"])],
  exam=dict(title="Gestreckte Abschlussprüfung (IHK)", note="Teil 1 zu Beginn des 4. Ausbildungshalbjahres, Teil 2 am Ende der Ausbildung. In der Fachaufgabe präsentierst du ein eigenes Projekt aus deinem Betrieb.", parts=[("Teil 1: Leistungserstellung, Logistik, Beschaffung, Buchhaltung · 90 Min.",25),("Marketing, Vertrieb, Personal, Steuerung · 150 Min.",35),("Wirtschafts- und Sozialkunde · 60 Min.",10),("Fachaufgabe im Einsatzgebiet · 30 Min.",30)]),
  next=[("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Nach Ausbildung und Berufspraxis zum Bachelor Professional.")],
  contacts=["Markus Sauviller"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="gross-und-aussenhandel", old="/gross-und-aussenhandelskaufleute/", cat="Berufsschule", tag="beruf",
  title="Kaufleute im Groß- und Außenhandelsmanagement", short="GH", img="teamuebung",
  claim="Vom Hersteller bis in die Innenstadt.",
  intro="Kaufleute im Groß- und Außenhandel sorgen dafür, dass Produkte vom Hersteller zum Handel kommen. Du verhandelst mit Kunden und Lieferanten, organisierst die Logistikkette und vermarktest Leistungen, egal ob mit Kleidung, Stahl, Holz, Lebensmitteln oder Elektronik.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","3 Jahre"),("Unterricht","Unter- und Mittelstufe 2 Tage, Oberstufe 1 Tag pro Woche; Englisch in niveaugleichen Gruppen"),("Standort","Kirschhecke 10")],
  week=dict(Mo="P",Di="S",Mi="P",Do="S",Fr="P"), weeknote="Beispielwoche Unter-/Mittelstufe: zwei Tage Berufsschule, drei Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Großhandelsprozesse","Kaufmännische Steuerung und Kontrolle","Wirtschafts- und Sozialprozesse","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"])],
  exam=dict(title="Gestreckte Abschlussprüfung (IHK)", note="Teil 1 in der Regel nach 18 Monaten über die Inhalte der ersten 15 Monate.", parts=[("Teil 1 · 90 Min.",25),("Großhandelsgeschäfte · 120 Min.",30),("Kaufm. Steuerung und Kontrolle · 90 Min.",15),("Wirtschafts- und Sozialprozesse · 60 Min.",10),("Fallbezogenes Fachgespräch · ca. 30 Min.",20)]),
  next=[("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Nach Ausbildung und Berufspraxis zum Bachelor Professional.")],
  contacts=["Thomas Hurtz","Marcel Kelmes"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="bueromanagement", old="/kaufleute-fuer-bueromanagement/", cat="Berufsschule", tag="beruf",
  title="Kaufleute für Büromanagement", short="BM", img="bg-bfs2",
  claim="Organisationstalent für jede Abteilung.",
  intro="Als Kauffrau oder Kaufmann für Büromanagement arbeitest du in der Verwaltung von Unternehmen aller Wirtschaftsbereiche: im Vertrieb, Einkauf, Personal, in der Logistik oder im Rechnungswesen. Du organisierst Büro- und Geschäftsprozesse, wertest Statistiken aus und verfasst Berichte.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","3 Jahre"),("Unterricht","Unter- und Mittelstufe 2 Tage, Oberstufe 1 Tag pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="S",Di="P",Mi="P",Do="S",Fr="P"), weeknote="Beispielwoche Unter-/Mittelstufe: zwei Tage Berufsschule, drei Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Büroprozesse","Geschäftsprozesse","Steuerung und Kontrolle"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre","Englisch"]),("Differenzierung",["Informationsverarbeitung"])],
  exam=dict(title="Gestreckte Abschlussprüfung (IHK)", note="Teil 1 nach der Hälfte der Ausbildung, Teil 2 am Ende.", parts=[("Teil 1: Informationstechnisches Büromanagement · 120 Min.",25),("Kundenbeziehungsprozesse · 150 Min.",30),("Wirtschafts- und Sozialkunde · 60 Min.",10),("Fachaufgabe in der Wahlqualifikation · ca. 30 Min.",35)]),
  next=[("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Nach Ausbildung und Berufspraxis zum Bachelor Professional.")],
  contacts=["Petra Riefers","Jutta Auler-Roelen"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="einzelhandel", old="/einzelhandelskaufleute/", cat="Berufsschule", tag="beruf",
  title="Kaufleute im Einzelhandel", short="EH", img="schulhof-gruppe",
  claim="Mehr als Verkauf: Sortiment, Marketing, Kennzahlen.",
  intro="Neben dem Verkauf steuerst du Daten- und Warenfluss, gestaltest Sortimente, planst Werbeaktionen und den Personaleinsatz und kontrollierst den Verkaufserfolg mit Kennzahlen. Ein abwechslungsreicher Beruf für Menschen, die gern mit Menschen arbeiten.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","3 Jahre, nach Verkäufer-Ausbildung 1 Jahr (Stufenausbildung)"),("Unterricht","Unter- und Oberstufe 1 Tag, Mittelstufe 2 Tage pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="P",Di="P",Mi="S",Do="P",Fr="P",Sa="P"), weeknote="Beispielwoche Unterstufe: ein Tag Berufsschule, die übrigen Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Kundenkommunikation und Service","Wirtschafts- und Sozialprozesse","Kaufm. Steuerung und Kontrolle","Warenbezogene Prozesse","Datenverarbeitung","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Politik","Religion","Sport / Gesundheit"])],
  exam=dict(title="Gestreckte Abschlussprüfung (IHK)", note="Teil 1 am Ende des 2. Ausbildungsjahres (meist Ende April/Anfang Mai), Teil 2 am Ende des 3. Jahres.", parts=[("Verkauf und Marketing · 90 Min.",15),("Wirtschafts- und Sozialprozesse · 60 Min.",10),("Warenwirtschaft und Rechnungswesen · 60 Min.",10),("Geschäftsprozesse im Einzelhandel · 105 Min.",25),("Fallbezogenes Fachgespräch · ca. 30 Min.",40)]),
  next=[("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Nach Ausbildung und Berufspraxis zum Bachelor Professional.")],
  contacts=["Shahriar Parvizi","Marie-Claire Heitmann"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="verkaeufer", old="/verkaeuferinnen-und-verkaeufer/", cat="Berufsschule", tag="beruf",
  title="Verkäuferinnen und Verkäufer", short="VK", img="bg-bfs1",
  claim="Zwei Jahre bis zum Berufsabschluss – mit Option auf mehr.",
  intro="Du verkaufst nicht nur Waren, sondern Lösungen: Beratung, Kasse, Warenannahme, Lager, Verkaufsraumgestaltung und Inventur. Nach zwei Jahren kannst du in nur einem weiteren Jahr Kauffrau oder Kaufmann im Einzelhandel werden.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","2 Jahre"),("Unterricht","Unterstufe 1 Tag, Oberstufe 2 Tage pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="P",Di="S",Mi="P",Do="P",Fr="P",Sa="P"), weeknote="Beispielwoche Unterstufe: ein Tag Berufsschule, die übrigen Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Kundenkommunikation und Service","Wirtschafts- und Sozialprozesse","Kaufm. Steuerung und Kontrolle","Warenbezogene Prozesse","Datenverarbeitung","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Politik","Religion","Sport / Gesundheit"])],
  exam=dict(title="Abschlussprüfung (IHK)", note="Zwischenprüfung zu Beginn des 2. Ausbildungsjahres (90 Min., Multiple Choice). Abschlussprüfung am Ende des 2. Jahres:", parts=[("Verkauf und Marketing · 90 Min.",25),("Wirtschafts- und Sozialprozesse · 60 Min.",10),("Warenwirtschaft und Rechnungswesen · 60 Min.",15),("Fallbezogenes Fachgespräch · ca. 30 Min.",50)]),
  next=[("Kaufleute im Einzelhandel","einzelhandel","Stufenausbildung: nur noch das dritte Jahr anhängen.")],
  contacts=["Shahriar Parvizi","Marie-Claire Heitmann"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="automobilkaufleute", old="/automobilkaufleute/", cat="Berufsschule", tag="beruf",
  title="Automobilkaufleute", short="AK", img="bg-hbfs",
  claim="Menschen, Autos und Zahlen.",
  intro="Du berätst Kundinnen und Kunden rund um Fahrzeugkauf und Service, organisierst die Buchführung und disponierst den Einkauf. Du arbeitest meist in Autohäusern, bei Herstellern oder Importeuren und brauchst Gespür für Marketing und etwas Technikverständnis.",
  facts=[("Abschluss","Berufsabschluss (IHK) und Berufsschulabschluss"),("Dauer","3 Jahre"),("Unterricht","Unter- und Mittelstufe 2 Tage, Oberstufe 1 Tag pro Woche"),("Standort","Kirschhecke 10")],
  week=dict(Mo="P",Di="S",Mi="P",Do="P",Fr="S"), weeknote="Beispielwoche Unter-/Mittelstufe: zwei Tage Berufsschule, drei Tage im Betrieb. Die genauen Tage stehen im Stundenplan.",
  subjects=[("Berufsbezogen",["Kernprozesse in der Automobilwirtschaft","Kaufmännische Unterstützungsprozesse","Wirtschafts- und Sozialprozesse","Englisch"]),("Berufsübergreifend",["Deutsch / Kommunikation","Religionslehre","Sport / Gesundheit","Politik / Gesellschaftslehre"]),("Differenzierung",["Kfz-Technik","Methodenkompetenz","Datenverarbeitung"])],
  exam=dict(title="Gestreckte Abschlussprüfung (IHK)", note="Teil 1 im Mai des 2. Ausbildungsjahres (bei Verkürzung im November), Teil 2 am Ende des 3. Jahres.", parts=[("Teil 1: Warenwirtschafts- und Werkstattprozesse · 90 Min.",20),("Fahrzeugvertrieb und Finanzdienstleistungen · 90 Min.",25),("Kaufm. Unterstützungsprozesse · 90 Min.",25),("Wirtschafts- und Sozialkunde · 60 Min.",10),("Fallbezogenes Fachgespräch · max. 20 Min.",20)]),
  next=[("Fachschule für Wirtschaft","fachschule-fuer-wirtschaft","Nach Ausbildung und Berufspraxis zum Bachelor Professional.")],
  contacts=["Andreas Vandelaar"], docs=[("Anmeldeformular Berufsschule (PDF)", FORM_BS)]),

 dict(slug="fachschule-fuer-wirtschaft", old="/fachschule-fuer-wirtschaft/", cat="Weiterbildung", tag="weiter",
  title="Fachschule für Wirtschaft", short="FS", img="bk-fachschule",
  claim="Berufsbegleitend zum Bachelor Professional.",
  intro="Die Fachschule baut auf Ausbildung und Berufserfahrung auf und bereitet auf Führungsaufgaben im mittleren Management vor. Mit dem Schwerpunkt Personalwirtschaft und inklusive Ausbildereignung. Es fallen keine Semestergebühren an.",
  facts=[("Abschluss","Bachelor Professional (Staatlich geprüfte/r Betriebswirt/in) und Ausbildereignung"),("Dauer","8 Semester, mit Fachhochschulreife ggf. 6"),("Voraussetzung","Einschlägige Ausbildung, Berufsschulabschluss, 1 Jahr Berufstätigkeit (auch begleitend) und Fachoberschulreife – oder 5 Jahre einschlägige Berufstätigkeit"),("Unterricht","Di und Do 18:30–21:30 Uhr, Sa 7:45–12:05 Uhr"),("Start","Nach den Sommerferien, Anmeldung ab Februar"),("Standort","Kirschhecke 10")],
  week=dict(Mo="-",Di="A",Mi="-",Do="A",Fr="-",Sa="S"), weeknote="Zwei Abende und der Samstagvormittag. In den Schulferien ist kein Unterricht. Dazu E-Learning im Virtuellen Lernstudio.",
  highlights=["Schwerpunkt Personalwirtschaft","Freistellung von der Ausbildereignungsprüfung (IHK)","Projektarbeit mit ca. 160 Stunden – Thema und Note stehen im Zeugnis","Seminare mit dem Trainernetzwerk anders.beraten","Keine laufenden Semestergebühren"],
  subjects=[("3./4. Semester",["Personalwirtschaft","BWL","Wirtschaftsinformatik","Rechnungswesen","Deutsch","Englisch","Mathematik"]),("5./6. Semester",["Personalwirtschaft","BWL","Wirtschaftsinformatik","Existenzgründung","Englisch","Mathematik"]),("7./8. Semester",["Personalwirtschaft","BWL","Rechnungswesen","Wirtschafts- und Arbeitsrecht","Finanzwirtschaft","VWL","Mathematik"])],
  next=[("Führungsaufgaben","#","Personalverantwortung im mittleren Management oder Selbstständigkeit.")],
  contacts=["Bildungsgangleitung Fachschule"],
  docs=[("Anmeldeformular Fachschule (PDF)", OLD+"/wp-content/uploads/2026/01/2026_anmeldeformular_fachschule.pdf"),("Einwilligung Datenschutz (PDF)", OLD+"/wp-content/uploads/2025/01/Einwilligungen-bei-Anmeldung-V2.pdf"),("Flyer Fachschule (PDF)", OLD+"/wp-content/uploads/2025/01/40_Berufskolleg_Personalwirtschaft_Flyer-2.pdf")]),
]

e = html.escape
DAYS = ["Mo","Di","Mi","Do","Fr","Sa"]
DAYLBL = {"S":"Schule","P":"Betrieb","A":"Abend","-":"frei"}

def shell():
    src = (ROOT/"index.html").read_text(encoding="utf-8")
    head = src[src.index('<div class="draft-note"'):src.index("</header>")+9]
    foot = src[src.index('<footer class="footer">'):src.index("<script>")]
    script = src[src.index("<script>"):src.index("</body>")]
    def fix(s):
        s = re.sub(r'href="#(?!top")', 'href="../index.html#', s)
        s = s.replace('href="#top"', 'href="../index.html"')
        s = s.replace('src="assets/', 'src="../assets/')
        s = s.replace('href="bildungsgaenge/', 'href="')
        return s
    return fix(head), fix(foot), script

def page(c, head, foot, script):
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k,v in c["facts"])
    week = ""
    if c.get("week"):
        codes = {"S":"s","P":"p","A":"a","-":"f"}
        days = [d for d in DAYS if d != "Sa" or "Sa" in c["week"]]
        cells = "".join(f'<li class="d-{codes[c["week"].get(d,"-")]}"><b>{d}</b><span>{DAYLBL[c["week"].get(d,"-")]}</span></li>' for d in days)
        week = f'<section class="block"><h2>So sieht deine Woche aus</h2><ul class="week">{cells}</ul><p class="muted">{e(c["weeknote"])}</p></section>'
    hl = ""
    if c.get("highlights"):
        hl = '<section class="block"><h2>Das erwartet dich</h2><ul class="checks">' + "".join(f"<li>{e(h)}</li>" for h in c["highlights"]) + "</ul></section>"
    subj = '<section class="block"><h2>Fächer</h2><div class="subjects">' + "".join(
        f'<div><h3>{e(g)}</h3><ul class="tags">' + "".join(f"<li>{e(s)}</li>" for s in items) + "</ul></div>" for g,items in c["subjects"]) + "</div></section>"
    exam = ""
    if c.get("exam"):
        x = c["exam"]
        if x.get("equal"):
            bars = '<ul class="tags">' + "".join(f"<li>{e(p)}</li>" for p,_ in x["parts"]) + "</ul>"
        else:
            segs = "".join(f'<span class="seg s{i}" style="flex:{w}" title="{e(p)}: {w} %">{w} %</span>' for i,(p,w) in enumerate(x["parts"]))
            legend = "".join(f'<li><i class="sw s{i}"></i>{e(p)} <b>{w} %</b></li>' for i,(p,w) in enumerate(x["parts"]))
            bars = f'<div class="examscale" role="img" aria-label="Gewichtung der Prüfungsteile">{segs}</div><ul class="legend">{legend}</ul>'
        exam = f'<section class="block"><h2>{e(x["title"])}</h2><p class="muted">{e(x["note"])}</p>{bars}</section>'
    nxt = '<section class="block"><h2>Wie geht es danach weiter?</h2><ul class="next">' + "".join(
        f'<li><a href="{s + ".html" if s != "#" else "../index.html#bildungsgaenge"}"><strong>{e(t)}</strong><span>{e(d)}</span></a></li>' for t,s,d in c["next"]) + "</ul></section>"
    contacts = "".join(f"<li>{e(p)}</li>" for p in c["contacts"])
    docs = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t,u in c["docs"])
    anm = FORM_BS if c["tag"]=="beruf" else ANMELDUNG
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['title'])} – Berufskolleg Rheydt-Mülfort</title>
<meta name="description" content="{e(c['claim'])} {e(c['title'])} am Berufskolleg Rheydt-Mülfort in Mönchengladbach.">
<meta name="theme-color" content="#123b37">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body class="sub">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{head}
<main id="inhalt">
  <section class="course-hero">
    <picture>
      <source media="(max-width:700px)" srcset="../assets/img/{c['img']}-640.webp">
      <img src="../assets/img/{c['img']}-1200.webp" alt="" width="1200" height="675">
    </picture>
    <div class="wrap">
      <nav class="crumbs" aria-label="Brotkrumen"><a href="../index.html">Start</a> / <a href="../index.html#bildungsgaenge">Bildungsgänge</a> / <span aria-current="page">{e(c['title'])}</span></nav>
      <span class="pill">{e(c['cat'])}</span>
      <h1>{e(c['title'])}</h1>
      <p>{e(c['claim'])}</p>
    </div>
  </section>
  <div class="wrap course-layout">
    <div class="course-main">
      <section class="block"><p class="intro">{e(c['intro'])}</p></section>
      {week}{hl}{subj}{exam}{nxt}
      <p class="muted small">Ausführliche Informationen auch auf der <a href="{OLD}{c['old']}">bisherigen Seite</a>.</p>
    </div>
    <aside class="course-side" aria-label="Steckbrief">
      <div class="card">
        <h2>Steckbrief</h2>
        <dl class="facts">{facts}</dl>
        <a class="btn btn-primary wide" href="{anm}"><span class="arrow">{"Azubi anmelden" if c['tag']=="beruf" else "Jetzt anmelden"}</span></a>
      </div>
      <div class="card">
        <h2>Ansprechpersonen</h2>
        <ul class="people">{contacts}</ul>
        <p class="muted small">Kontakt über das Sekretariat: <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a> · 02166 917920</p>
        {f'<h2 class="mt">Downloads</h2><ul class="docs">{docs}</ul>' if docs else ''}
      </div>
    </aside>
  </div>
</main>
{foot}{script}</body>
</html>
"""

def main():
    head, foot, script = shell()
    out = ROOT/"bildungsgaenge"; out.mkdir(exist_ok=True)
    for c in COURSES:
        (out/f"{c['slug']}.html").write_text(page(c, head, foot, script), encoding="utf-8")
    # Links der Startseite auf die neuen Unterseiten umbiegen
    idx = (ROOT/"index.html").read_text(encoding="utf-8")
    for c in COURSES:
        idx = idx.replace(f'href="{OLD}{c["old"]}"', f'href="bildungsgaenge/{c["slug"]}.html"')
    (ROOT/"index.html").write_text(idx, encoding="utf-8")
    print(len(COURSES), "Seiten erzeugt")

if __name__ == "__main__":
    main()
