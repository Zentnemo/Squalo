# Hero-Image-Inventar – Squalo Schwimmcoaching

Kurzdokumentation: Seite → Quellordner → gewählte Bilddatei → finaler Pfad.
Alle finalen Hero-Bilder liegen in `static/images/heroes/`.

## Feste Zuordnung

| Seite | Quellordner | Quelldatei | Finaler Pfad |
|---|---|---|---|
| /coach-werden | static/images/coach-werden | gpt-image-2_...-3.jpg | static/images/heroes/coach-werden-hero.jpg |
| /dashboard | static/images/dashboard | gpt-image-2_...-1.jpg | static/images/heroes/dashboard-hero.jpg |
| /schwimmorte-berlin | static/images/badestelle-berlin | nano-banana-2_...-0.jpg | static/images/heroes/schwimmorte-berlin-hero.jpg |
| /schwimmorte-freiburg | static/images/badestelle-freiburg | nano-banana-2_...large_indoor_swimming_faci-3.jpg | static/images/heroes/schwimmorte-freiburg-hero.jpg |
| /schwimmtraining-kinder-berlin | static/images/kinder-schwimmtraining | gpt-image-2_...child_learning_to_swim_in_-0.jpg | static/images/heroes/schwimmtraining-kinder-berlin-hero.jpg |
| /kraulen-lernen-berlin | static/images/kraullernen-berlin | nano-banana-2_...sessio-2.jpg | static/images/heroes/kraulen-lernen-berlin-hero.jpg |
| /kraulen-lernen-freiburg | static/images/kraullernen-freiburg | nano-banana-2_...sessio-3.jpg | static/images/heroes/kraulen-lernen-freiburg-hero.jpg |

## Fallback-Zuordnung (kein eigener Bildordner vorhanden)

| Seite | Quellordner | Quelldatei | Finaler Pfad |
|---|---|---|---|
| /schwimmtraining-berlin | static/images/kraullernen-berlin | nano-banana-2_...sessio-2.jpg | static/images/heroes/schwimmtraining-berlin-hero.jpg |
| /schwimmtraining-freiburg | static/images/kraullernen-freiburg | nano-banana-2_...sessio-3.jpg | static/images/heroes/schwimmtraining-freiburg-hero.jpg |
| /schwimmkurs-erwachsene-berlin | static/images/kraullernen-berlin | nano-banana-2_...sessio-2.jpg | static/images/heroes/schwimmkurs-erwachsene-berlin-hero.jpg |
| /triathlon-schwimmtraining-berlin | static/images/badestelle-berlin | nano-banana-2_...-2.jpg | static/images/heroes/triathlon-schwimmtraining-berlin-hero.jpg |

## Hinweise / Entscheidungen

- Für `/schwimmtraining-berlin` war laut Fallback-Regel auch `static/images/coaches` als Quelle
  erlaubt. Das dortige Bild (`coach-header-squalo-shirt.png`) enthält jedoch verrauschte
  Pseudo-Text-Artefakte im oberen Bildbereich (verstößt gegen „keine Schrift im Bild") und wurde
  daher **nicht** verwendet. Stattdessen kommt das Kraultraining-Bild aus `kraullernen-berlin`
  zum Einsatz (Mehrfachverwendung, da der Ordner nur ein einziges, sauberes Bild enthält).
- `/schwimmkurs-erwachsene-berlin` und `/kraulen-lernen-berlin` teilen sich bewusst dasselbe
  Ausgangsbild aus `kraullernen-berlin` (Fallback-Regel sieht das explizit vor).
- `/triathlon-schwimmtraining-berlin` nutzt das zweite, bisher ungenutzte Bild aus
  `badestelle-berlin` (Seeblick mit Steg) – dadurch keine Bildüberschneidung mit
  `/schwimmorte-berlin`.
- **Bugfix Landingpages:** `templates/landing_page.html` baute den Bildpfad bisher als
  reinen String `url('{{ page.hero_image }}')` ohne `url_for('static', ...)` zusammen. Das führte
  zu 404-Fehlern für alle Hero-Bilder auf Landingpages. Fix: `url_for('static',
  filename=page.hero_image)` wird jetzt verwendet. Zusätzlich unterstützt das Template optional
  `page.hero_position` für Bild-Feineinstellung pro Seite.
- **Bugfix /coach-werden:** `static/css/style.css` enthielt Jinja-Syntax
  (`{{ url_for(...) }}`) direkt im CSS. CSS-Dateien werden von Flask nicht durch Jinja gerendert,
  wodurch das Hero-Bild dort nie lud. Fix: `url_for(...)` wurde als Inline-Style auf die
  `<section class="coach-werden-hero">` in `templates/coach_werden.html` verschoben.
- **Dashboard-Hero verbessert:** `/dashboard` nutzte bereits `dashboard-hero.jpg` per Inline-Style
  in `templates/dashboard.html`, aber `.dashboard-header` hatte weder `background-size` noch
  Mindesthöhe noch Kontrast-Overlay. CSS wurde um `background-size: cover`,
  `background-position`, `min-height`, ein abdunkelndes Overlay und weiße Textfarbe mit
  Schatten ergänzt. Dashboard-Funktionalität (Tabs, Buchungen, Trainingspläne, Uploads, Login)
  wurde nicht verändert.

## Stand: 2026-07-24 (aktualisiert)

