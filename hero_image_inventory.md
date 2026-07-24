# Hero-Image-Inventar – Squalo Schwimmcoaching

Stand: aktuelle Reparatur (Hero-Bilder wiederhergestellt + einfache Rotation für Seiten mit mehreren Bildern).

## Zuordnung Seite → Quellordner → Bild(er) → Rotation/Fallback

| Seite | Route | Quellordner | Finale Datei(en) in `static/images/heroes/` | Rotation | Fallback (gemeinsames Bild mit anderer Seite) |
|-------|-------|-------------|-----------------------------------------------|----------|-----------------------------------------------|
| Schwimmorte Berlin | `/schwimmorte-berlin` | `badestelle-berlin/` | `schwimmorte-berlin-hero.jpg`, `schwimmorte-berlin-hero-2.jpg` | ✅ Ja (2 Bilder, ~7s Fade) | Nein |
| Schwimmorte Freiburg | `/schwimmorte-freiburg` | `badestelle-freiburg/` | `schwimmorte-freiburg-hero.jpg`, `schwimmorte-freiburg-hero-2.jpg` | ✅ Ja (2 Bilder, ~7s Fade) | Nein |
| Coach werden | `/coach-werden` | `coach-werden/` | `coach-werden-hero.jpg`, `coach-werden-hero-2.jpg` | ✅ Ja (2 Bilder, ~7s Fade) | Nein |
| Dashboard | `/dashboard` | `dashboard/` | `dashboard-hero.jpg`, `dashboard-hero-3.jpg` | ✅ Ja (2 Bilder, ~7s Fade) | Nein |
| Schwimmtraining Berlin | `/schwimmtraining-berlin` | `kraullernen-berlin/` | `schwimmtraining-berlin-hero.jpg` | ❌ Nein (nur 1 Quellbild) | Ja – identisch mit Kraulen lernen Berlin & Schwimmkurs Erwachsene Berlin |
| Kraulen lernen Berlin | `/kraulen-lernen-berlin` | `kraullernen-berlin/` | `kraulen-lernen-berlin-hero.jpg` | ❌ Nein | Ja – identisch mit Schwimmtraining Berlin & Schwimmkurs Erwachsene Berlin |
| Schwimmkurs Erwachsene Berlin | `/schwimmkurs-erwachsene-berlin` | `kraullernen-berlin/` | `schwimmkurs-erwachsene-berlin-hero.jpg` | ❌ Nein | Ja – identisch mit Schwimmtraining Berlin & Kraulen lernen Berlin |
| Schwimmtraining Freiburg | `/schwimmtraining-freiburg` | `kraullernen-freiburg/` | `schwimmtraining-freiburg-hero.jpg` | ❌ Nein | Ja – identisch mit Kraulen lernen Freiburg |
| Kraulen lernen Freiburg | `/kraulen-lernen-freiburg` | `kraullernen-freiburg/` | `kraulen-lernen-freiburg-hero.jpg` | ❌ Nein | Ja – identisch mit Schwimmtraining Freiburg |
| Schwimmtraining Kinder Berlin | `/schwimmtraining-kinder-berlin` | `kinder-schwimmtraining/` | `schwimmtraining-kinder-berlin-hero.jpg` | ❌ Nein (nur 1 Quellbild) | Nein |
| Triathlon Schwimmtraining Berlin | `/triathlon-schwimmtraining-berlin` | `badestelle-berlin/` (2. Bild) | `triathlon-schwimmtraining-berlin-hero.jpg` | ❌ Nein | Ja – identisch mit dem 2. Rotationsbild von Schwimmorte Berlin |

## Technische Umsetzung

- **Rotation**: Reines CSS/JS ohne Bibliotheken. Jede Hero-Sektion mit mehreren Bildern hat einen `.hero-rotator` mit mehreren `.hero-slide`-Divs. Ein kleines Inline-Script in `templates/base.html` schaltet alle ~7 Sekunden per Fade (`opacity`-Transition, ~1.4s) zum nächsten Bild um.
- **Barrierefreiheit**: Rotation wird bei `prefers-reduced-motion: reduce` automatisch deaktiviert (sowohl per CSS-Transition-Reset als auch im JS-Check).
- **Einzelbild-Seiten**: Haben nur einen `.hero-slide` – das Script erkennt `< 2` Slides und lässt sie unverändert (keine Rotation nötig).
- **Keine Bildmanipulation**: Alle Bilder werden unverändert verwendet, nur per CSS `background-size: cover` / `background-position` zugeschnitten – kein Spiegeln, Strecken oder Verzerren.
- **Geänderte Dateien**: `app.py` (hero_image/hero_images-Zuordnung), `templates/landing_page.html`, `templates/coach_werden.html`, `templates/dashboard.html` (Rotator-Markup), `templates/base.html` (Rotations-Script), `static/css/style.css` (`.hero-rotator`, `.hero-slide`, `.landing-hero*`-Klassen, Lückenfix `body.page-has-hero main.page-main`).
