# Berlin Swimmers Club – Workflow-Dokumentation

## Übersicht
Neue, eigenständige öffentliche Landingpage für ein Community-Projekt ("Berlin Swimmers Club"),
inklusive Signup/Voting-Formular, öffentlicher aggregierter Abstimmungs-Anzeige und einer
Coach/Admin-Übersicht. Kein Verein, keine Buchungslogik – rein informativ + Interessensbekundung.

## Route der Landingpage
- `GET/POST /berlin-swimmers-club` (Endpoint: `berlin_swimmers_club`)
- **Nicht** Teil des generischen `LANDING_PAGES`-SEO-Systems (dieses unterstützt keine Formulare/DB-Schreibzugriffe),
  sondern eine eigene, dedizierte Route + eigenes Template `templates/berlin_swimmers_club.html`.
- Template erbt von `base.html`, ist standardmäßig indexierbar (kein `noindex`), Canonical-URL wird automatisch
  über `base.html` (`get_public_base_url()` + `request.path`) generiert.
- Wurde manuell in `sitemap_xml()` ergänzt (`/berlin-swimmers-club`, priority 0.8, weekly), da nicht Teil
  der automatischen `LANDING_PAGES`-Sitemap-Schleife.
- `/robots.txt` blockiert die Seite nicht (nur `/admin`, `/dashboard`, `/feed`, `/login`, `/register` sind gesperrt).

## Formularfelder (Signup/Voting)
Pflichtfelder: `name`, `email`, `swim_level`, `preferred_format`, `preferred_region`, `preferred_time`
Optional: `interest_type` (Swim Meet / Map-Updates / 1:1 Coaching / Alles interessant), `comment`, `consent_updates` (Checkbox)

Auswahloptionen:
- Schwimmlevel: Anfänger, Wiedereinsteiger, Fortgeschritten, Triathlon, Freiwasser
- Format: Pool, See, Open Water, Egal
- Region: Nord, Südwest, Mitte, Ost, Egal
- Zeit: Werktag Abend, Samstag, Sonntag, Egal

Bei fehlenden Pflichtfeldern wird der Request abgelehnt (Flash-Fehlermeldung, kein DB-Eintrag).

## Datenmodell
Neue Tabelle `swim_club_interest` (SQLAlchemy-Model `SwimClubInterest` in `models.py`):
- `id`, `created_at`, `name`, `email`, `swim_level`, `preferred_format`, `preferred_region`,
  `preferred_time`, `interest_type`, `comment`, `consent_updates` (bool), `source` (default `website`),
  `confirmation_email_sent_at` (Duplikatschutz + Anzeige "Mail gesendet?" im Admin-Overview).
- Wird automatisch von `db.create_all()` beim App-Start angelegt (keine manuelle Migration nötig,
  da neue Tabelle – bestehende Tabellen/Daten bleiben unangetastet).

## Bestätigungsmail
- Funktion `send_swim_club_confirmation_email(entry, force=False)` in `app.py`, nach dem Muster
  von `send_coach_proposed_appointment_email` (gleiche `[MAIL]` / `[MAIL-FEHLER]`-Logging-Konvention).
- Nutzt bestehende `send_email()`-Infrastruktur (SMTP, mit Konsolen-Fallback wenn keine Mail-Env-Variablen gesetzt sind).
- Duplikatschutz über `confirmation_email_sent_at` (verhindert Mehrfachversand).
- Mail-Inhalt: Dank für das Interesse, Hinweis auf geplantes erstes Swim Meet ("Wochenende um den 22. August"),
  Link zur Schwimmorte-Berlin-Seite (`get_public_base_url()` + `/schwimmorte-berlin`), Signatur mit
  `hello@squalo-schwimmcoaching.com`.
- Schlägt der Versand fehl, wird der Eintrag trotzdem gespeichert; der Nutzer erhält eine Warnmeldung
  statt der Erfolgsmeldung.

## Admin/Coach-Übersicht
- `GET /admin/swim-club` (Endpoint: `admin_swim_club`), `@login_required` + Rollenprüfung (`role == 'admin'`),
  identisch zum bestehenden Muster in `admin_shop_orders`/`admin_booking_history`.
- Zeigt Gesamtzahl, Aggregate nach Level/Format/Region/Zeit sowie die vollständige Liste aller Einträge
  (Datum, Name, E-Mail, Präferenzen, Kommentar, Mail-Status).
- Zusätzlich: CSV-Export unter `GET /admin/swim-club/export.csv`.
- Verlinkt im Coach Panel (`templates/admin.html`) über einen neuen Tab-Link "🏊‍♀️ Swimmers Club".

## Öffentliche aggregierte Voting-Anzeige
- Auf der Landingpage selbst (kein separater Endpoint), berechnet direkt in der `berlin_swimmers_club()`-View
  beim GET-Request (Zählung nach `preferred_time`, `preferred_format`, `preferred_region`).
- Zeigt **keine** personenbezogenen Daten – nur aggregierte Balken/Zahlen pro Option.
- Fallback-Text "Noch keine Stimmen – sei eine/r der Ersten." wenn noch keine Einträge existieren.

## Homepage-Teaser
- Neuer Block `<section class="swc-teaser">` in `templates/index.html`, eingefügt zwischen der
  Community-Box (`.community-feed`) und "Warum Schwimmen?" (`.swim-knowledge`) – beide Boxen bleiben
  unverändert, nur die Reihenfolge wurde um den neuen Teaser ergänzt.
- Enthält Headline, Subheadline, Info-Zeile zum geplanten ersten Treffen sowie zwei CTAs
  (Formular-Sprung-Link `#swc-signup` und Link zur vollen Landingpage).

## Map / Map-Vorschau
- Kleine, eigenständige Read-only-Leaflet-Vorschaukarte (`#swc-map`) auf der neuen Landingpage,
  nutzt die global bereits geladene Leaflet-Bibliothek (aus `base.html`) sowie echte Berliner
  `Location`-Daten (nur Name/Koordinaten, keine Status-Berechnung, keine neuen/erfundenen Orte).
  CTA-Button verlinkt zusätzlich auf `/schwimmorte-berlin` für die vollständige, interaktive Karte.
- Keine Änderungen an der bestehenden Homepage-Karte, den Geodaten oder `berlin_districts.geojson`.

## Footer & Sitemap
- Footer-Link "Berlin Swimmers Club" in `templates/base.html` ergänzt (`.footer-seo-links`).
- Sitemap-Eintrag siehe oben.

## Geänderte/neue Dateien
- `models.py` – neues Model `SwimClubInterest`
- `app.py` – Model-Import, `send_swim_club_confirmation_email()`, Routen `berlin_swimmers_club`,
  `admin_swim_club`, `admin_swim_club_export`, Sitemap-Ergänzung
- `templates/berlin_swimmers_club.html` – neu
- `templates/admin_swim_club.html` – neu
- `templates/index.html` – Homepage-Teaser eingefügt
- `templates/admin.html` – neuer Nav-Tab-Link
- `templates/base.html` – neuer Footer-Link
- `static/css/style.css` – neue `.swc-*`-Klassen + `.flash-warning`

## Offene TODOs / bewusst nicht umgesetzt
- Kein Reddit-Bezug in der Bullet-Liste (bewusst zurückhaltend formuliert).
- Kein automatischer Versand einer "Ort & Zeit stehen fest"-Mail – dies müsste manuell/zukünftig
  über eine weitere Coach-Aktion ausgelöst werden (aktuell nur die erste Bestätigungsmail).
- Keine Änderungen an Buchungs-, Shop-, Preis- oder Coach-Logik, keine Änderungen an Geodaten/Hero-Bildern.
- PostgreSQL/`DATABASE_URL`, bestehende Kunden-/Buchungs-/Schüler-/Trainingsplan-/Rechnungsdaten unangetastet.
- Keine Secrets, keine SQLite-Dateien, kein `git init` verwendet.
