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
Pflichtfelder: `name`, `email`, `swim_level`, `preferred_format`, `preferred_region`, mindestens ein
Tag aus `preferred_dates` (Checkbox-Mehrfachauswahl) und mindestens ein Zeitfenster aus
`preferred_time_slots` (Checkbox-Mehrfachauswahl).
Optional: `interest_type` (Swim Meet / Map-Updates / 1:1 Coaching / Alles interessant), `comment`, `consent_updates` (Checkbox)

Auswahloptionen:
- Schwimmlevel: Anfänger, Wiedereinsteiger, Fortgeschritten, Triathlon, Freiwasser
- Format: Pool, See, Open Water, Egal
- Region: Nord, Südwest, Mitte, Ost, Egal
- Tage (Mehrfachauswahl, `SWC_DATES` in `app.py`): Freitag 28.08.2026 bis Freitag 04.09.2026 (8 Tage,
  inkl. Montag 31.08.2026)
- Zeitfenster (Mehrfachauswahl, `SWC_TIME_SLOTS` in `app.py`): 3 Wochentag-Abendslots
  (17–19, 18–20, 19–21 Uhr) + 5 Wochenend-Slots (09–11, 11–13, 13–15, 15–17, 17–19 Uhr)

Das alte einzelne `preferred_time`-Feld (Werktag Abend/Samstag/Sonntag/Egal) wurde durch die neue
Mehrfachauswahl ersetzt und wird für neue Einträge nicht mehr befüllt (Spalte bleibt aus
Kompatibilitätsgründen in der DB erhalten, siehe Datenmodell).

Bei fehlenden Pflichtfeldern wird der Request abgelehnt (Flash-Fehlermeldung, kein DB-Eintrag).

## Datenmodell
Neue Tabelle `swim_club_interest` (SQLAlchemy-Model `SwimClubInterest` in `models.py`):
- `id`, `created_at`, `name`, `email`, `swim_level`, `preferred_format`, `preferred_region`,
  `preferred_time` (legacy, wird nicht mehr befüllt), `preferred_dates` (Text, kommasepariert,
  z. B. `2026-08-28,2026-08-29`), `preferred_time_slots` (Text, kommasepariert, z. B.
  `weekend_11_13,weekday_18_20`), `interest_type`, `comment`, `consent_updates` (bool),
  `source` (default `website`), `confirmation_email_sent_at` (Duplikatschutz + Anzeige
  "Mail gesendet?" im Admin-Overview).
- Wird automatisch von `db.create_all()` beim App-Start angelegt (keine manuelle Migration nötig,
  da neue Tabelle – bestehende Tabellen/Daten bleiben unangetastet).
- Die zwei neuen Spalten `preferred_dates`/`preferred_time_slots` wurden nachträglich additiv per
  `ALTER TABLE` migriert (gleiches Muster wie alle anderen additiven Migrationen in `app.py`,
  `try/except` mit Spalten-Existenzprüfung über `sqlalchemy.inspect`) – kein `drop_all()`, keine
  bestehenden Daten wurden verändert oder gelöscht.
- Speicherformat bewusst als kommaseparierter Text (nicht JSON), um SQLite/PostgreSQL-Kompatibilität
  ohne datenbankspezifische JSON-Spaltentypen sicherzustellen.

## Bestätigungsmail
- Funktion `send_swim_club_confirmation_email(entry, force=False)` in `app.py`, nach dem Muster
  von `send_coach_proposed_appointment_email` (gleiche `[MAIL]` / `[MAIL-FEHLER]`-Logging-Konvention).
- Nutzt bestehende `send_email()`-Infrastruktur (SMTP, mit Konsolen-Fallback wenn keine Mail-Env-Variablen gesetzt sind).
- Duplikatschutz über `confirmation_email_sent_at` (verhindert Mehrfachversand).
- Mail-Inhalt: Dank für das Interesse, Hinweis auf geplantes erstes Swim Meet ("Ende August / Anfang
  September"), Dank für die angegebenen Tage/Zeitfenster, ausdrücklich kein fixes Datum versprochen,
  Link zur Schwimmorte-Berlin-Seite (`get_public_base_url()` + `/schwimmorte-berlin`), Signatur mit
  `hello@squalo-schwimmcoaching.com`.
- Schlägt der Versand fehl, wird der Eintrag trotzdem gespeichert; der Nutzer erhält eine Warnmeldung
  statt der Erfolgsmeldung.

## Admin/Coach-Übersicht
- `GET /admin/swim-club` (Endpoint: `admin_swim_club`), `@login_required` + Rollenprüfung (`role == 'admin'`),
  identisch zum bestehenden Muster in `admin_shop_orders`/`admin_booking_history`.
- Zeigt Gesamtzahl, Aggregate nach Level/Format/Region sowie neu Tage/Zeitfenster (jeweils absteigend
  nach Stimmenzahl sortiert) sowie die vollständige Liste aller Einträge (Datum, Name, E-Mail,
  Präferenzen, ausgewählte Tage, ausgewählte Zeitfenster, Kommentar, Mail-Status) – die
  Tage/Zeitfenster werden pro Eintrag lesbar aufbereitet (z. B. "Samstag, 29.08.2026, Montag,
  31.08.2026").
- Zusätzlich: CSV-Export unter `GET /admin/swim-club/export.csv`, inkl. der Spalten "Tage" und
  "Zeitfenster" (ersetzt die alte einzelne "Zeit"-Spalte).
- Verlinkt im Coach Panel (`templates/admin.html`) über einen neuen Tab-Link "🏊‍♀️ Swimmers Club".

## Öffentliche aggregierte Voting-Anzeige
- Auf der Landingpage selbst (kein separater Endpoint), berechnet direkt in der `berlin_swimmers_club()`-View
  beim GET-Request (Zählung nach `preferred_dates`, `preferred_time_slots`, `preferred_format`, `preferred_region`).
- "Beliebteste Tage" und "Beliebteste Zeitfenster" werden absteigend nach Stimmenzahl sortiert
  angezeigt ("Welche Tage/Zeitfenster liegen vorne?"); Format/Region bleiben wie bisher in
  fester Options-Reihenfolge.
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

## Nachträgliches visuelles Polishing (Hero-Bild, Logo-Branding, Map-Styling)
Reiner Styling-Nachzieher auf `/berlin-swimmers-club` – **keine neuen Features, keine Logik-Änderungen**.

- **Hero-Bild:** Wiederverwendung des bereits vorhandenen Fotos
  `static/images/heroes/schwimmorte-berlin-hero-2.jpg` (Seeidylle mit Steg, bereits auf
  `/schwimmorte-berlin` im Einsatz) über das bestehende, seitenweite `.hero-rotator`/`.hero-slide`-Muster.
  Keine neuen Bilddateien angelegt.
- **Logo-Branding:** Das bestehende `squalo-logo.png` wird zusätzlich als dezentes, halbtransparentes
  Wasserzeichen (`<img class="swc-hero-logo-watermark">`) rechts im Hero eingeblendet
  (Opacity ~0.14, `pointer-events: none`, `z-index` zwischen Overlay-Tint und Text-Container –
  liegt also sichtbar "durch" den Farbverlauf, aber nie über dem Text). Mobile: kleiner/dezenter.
- **Map-Styling (identisch zur Homepage "Squalo Baywatch"):**
  - Karten-Container teilt sich jetzt die ID `id="map"` mit der Homepage-Karte → automatisch identische
    Höhe (550px Desktop, responsive 450px/480px/280px je nach Breakpoint), Border-Radius, Box-Shadow,
    Hover-Effekt – ganz ohne neues CSS.
    Umschließender Abschnitt nutzt zusätzlich die Klasse `.map-section` (gleicher Card-Look:
    Gradient-Hintergrund, Border-Radius, Schatten wie auf der Startseite).
  - **Legende** wurde in ein gemeinsames Partial ausgelagert: `templates/partials/swim_map_legend.html`,
    eingebunden sowohl auf der Startseite (`index.html`, reiner Refactor ohne Output-Änderung) als auch
    auf `/berlin-swimmers-club` – dadurch garantiert identisches Aussehen an einer einzigen Quelle.
  - **Marker-Styling** (`squalo-marker-lake/-beach/-summer/-indoor/-therme`) wird durch lokale
    `getMarkerClass()`/`getMarkerIcon()`-Hilfsfunktionen im Vorschau-Karten-Skript exakt nachgebildet
    (gleiche CSS-Klassen wie auf der Startseite), inkl. Popup im gleichen `.popup-card`/`.popup-title`/
    `.popup-meta`-Look.
  - **Bewusst NICHT übernommen** (um Buchungslogik/neue Map-Logik nicht anzufassen): Regionen-Filterleiste,
    Geolocation-Button, sowie die reichhaltigen Status-/Wassertemperatur-/Auslastungs-/Buchungs-Popups der
    Startseiten-Karte. Die Vorschau-Popups zeigen nur Name, Typ und Bezirk.
  - Alte, jetzt ungenutzte Klasse `.swc-map-preview` wurde aus `static/css/style.css` entfernt (war durch
    die ID-Wiederverwendung überflüssig geworden).
- **Copy-Updates** in `templates/berlin_swimmers_club.html`: Subheadline, die 4 Hero-Badges
  ("Kein Verein", "Alle Level willkommen", "Pool & Open Water", "Erstes Treffen: Wochenende um den
  22. August"), Kartenabschnitt-Text und CTA-Button-Label ("Zur vollständigen Schwimmorte-Karte")
  wurden auf den vorgegebenen Wortlaut angepasst.
- **Getestet:** Desktop- und Mobile-Screenshots von Hero + Karte, Popup-Klick auf der Vorschaukarte,
  HTTP-Statuscheck für `/`, `/berlin-swimmers-club`, `/schwimmorte-berlin`, `/sitemap.xml`,
  `/robots.txt`, `/shop` (alle 200) sowie `/dashboard`, `/booking`, `/admin/swim-club` (alle korrekt
  302 Redirect zum Login, keine 500er). Homepage-Karte inkl. Regionen-Filter unverändert funktionsfähig.
- **Unverändert:** Geodaten, Marker-Anzahl/-Koordinaten, Buchungs-/Shop-/Preis-/Coach-Logik, DB-Inhalte,
  PostgreSQL/`DATABASE_URL`.

## Update: Voting-Daten, Zeitfenster & Texte (Ende August / Anfang September)
Reiner Daten-/Text-/Auswertungs-Nachzieher – **keine Änderungen an Hero-Bild, Logo, Karte,
Buchungs-/Shop-/Preis-/Coach-Logik**.

- **Kein festes Datum mehr:** Alle 4 Fundstellen von "22. August" wurden entfernt und durch
  "Ende August / Anfang September" ersetzt: Hero-Badge, FAQ-Antwort ("Wann findet das erste Treffen
  statt?"), Homepage-Teaser (`templates/index.html`) und Bestätigungsmail-Text.
- **Voting-Zeitraum:** Neuer Abstimmungs-Zeitraum Freitag 28.08.2026 bis Freitag 04.09.2026
  (8 konkrete Tage, inkl. Montag 31.08.2026), definiert als `SWC_DATES`-Konstante in `app.py`.
- **Zeitfenster:** 8 konkrete Zeitfenster (`SWC_TIME_SLOTS`-Konstante in `app.py`) – 3 Wochentag-
  Abendslots (17–19, 18–20, 19–21 Uhr) und 5 Wochenend-Slots (09–11, 11–13, 13–15, 15–17, 17–19 Uhr).
- **Formular:** Das alte `preferred_time`-Auswahlfeld wurde durch zwei neue Checkbox-Gruppen ersetzt
  ("Welche Tage würden für dich passen?" / "Welche Zeitfenster passen dir grundsätzlich?"),
  jeweils mit Hinweistext ("Du kannst mehrere ... auswählen.") und neuer CSS (`.swc-checkbox-grid`,
  `.swc-checkbox-option`, `.swc-form-hint` in `static/css/style.css`).
- **Speicherung:** Mehrfachauswahl wird als kommaseparierter Text in den neuen Spalten
  `preferred_dates`/`preferred_time_slots` gespeichert (additive, nicht-destruktive `ALTER TABLE`-
  Migration, gleiches Muster wie alle bisherigen Migrationen in `app.py`). Das alte `preferred_time`-
  Feld bleibt in der DB erhalten (Altdaten unangetastet), wird für neue Einträge aber nicht mehr
  benötigt/befüllt.
- **Auswertung:** Öffentliche Voting-Anzeige und Admin-Übersicht zeigen jetzt zusätzlich
  "Beliebteste Tage" und "Beliebteste Zeitfenster" (absteigend nach Stimmenzahl sortiert), berechnet
  über eine neue Multi-Value-Tally-Funktion, die die kommaseparierten Werte aufsplittet und zählt.
  Weiterhin keine personenbezogenen Daten in der öffentlichen Anzeige.
- **CSV-Export:** Spalten "Tage" und "Zeitfenster" ersetzen die alte einzelne "Zeit"-Spalte.
- **Getestet:** Lokaler Testeintrag über die Playwright-Browsersteuerung (mehrere Tage + Zeitfenster
  ausgewählt), erfolgreiche Speicherung, korrekte Bestätigungsmail (Konsolen-Fallback, neuer
  Wortlaut, keine "22. August"-Erwähnung mehr), korrekte öffentliche Aggregation (sortiert, keine
  personenbezogenen Daten), korrekte Admin-Übersicht (Stat-Karten + Tabellen-Spalten), CSV-Export
  200 OK, Regressions-Sweep über `/`, `/schwimmorte-berlin`, `/dashboard`, `/sitemap.xml`,
  `/robots.txt`, `/berlin-swimmers-club`, `/admin/swim-club`, `/shop`, `/coaches` (alle 200/302 wie
  erwartet, keine 500er), Mobile-Viewport-Screenshot der neuen Checkbox-Gruppen (sauberes
  Ein-Spalten-Layout). Test-Eintrag anschließend aus der lokalen SQLite-DB wieder entfernt.
- **Unverändert:** Hero-Bild, Logo-Wasserzeichen, Map-Styling/-Logik/-Koordinaten, Buchungs-/Shop-/
  Preis-/Coach-Logik, keine DB-Resets/`drop_all()`, keine SQLite-Dateien committet, PostgreSQL/
  `DATABASE_URL` unangetastet.
