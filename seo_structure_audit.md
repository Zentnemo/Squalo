# SEO Structure Audit – Squalo Schwimmcoaching

Dieses Dokument hält fest, welche Seiten neue Textabschnitte erhalten haben, welche
Aussagen bewusst allgemein gehalten wurden, welche Fakten noch verifiziert werden
sollten und welche Seiten nach inhaltlichen Änderungen erneut in der Google Search
Console eingereicht werden sollten.

## 1. Seiten mit neuen Textabschnitten (Stand: 2026-07-25)

| Seite | Neuer Abschnitt | Ort im Layout |
|---|---|---|
| `/coaches` | Sortierung geändert: Moritz Zentner steht jetzt immer an erster Stelle (Gründer, meiste Bewertungen), gefolgt von Clara und Tolga alphabetisch. Kein neuer Text, nur Reihenfolge. | – |
| `/coach-werden` | „Werde Squalo Coach" – Motivations-/Vergütungssektion inkl. 10 %-Kommissionsbeispiel | Direkt nach dem Hero, vor „Für wen ist das?" |
| `/schwimmtraining-kinder-berlin` | „Warum 1:1-Schwimmcoaching für Kinder sinnvoll sein kann" | Nach „Für wen geeignet", vor „Trainingsansatz" |
| `/schwimmorte-berlin` | „Schwimmen in Berlin: Becken, Freibad oder Freiwasser?" | Nach „Schwimmbäder & Seen in Berlin", vor „Training in ganz Berlin" |
| `/schwimmorte-freiburg` | „Schwimmtraining in Freiburg und Umgebung" | Nach „Schwimmorte in Freiburg & Umgebung", vor „Training in Freiburg und Umgebung" |
| `/kraulen-lernen-berlin` | „Warum Kraulen lernen so viel bringt" | Nach „Für wen eignet sich Kraultraining?", vor „Unser Kraul-Ansatz" |
| `/kraulen-lernen-freiburg` | „Warum Kraulen lernen so viel bringt" (Freiburg-neutral, „unsere erfahrenen Coaches") | Nach „Für wen eignet sich Kraultraining?", vor „Unser Kraul-Ansatz" |
| `/triathlon-schwimmtraining-berlin` | „Warum Schwimmen im Triathlon oft der entscheidende Baustein ist" | Nach „Für wen eignet sich das Training?", vor „Unser Ansatz" |

Technisch wurden alle neuen Textabschnitte über ein neues, optionales Feld
`extra_section` (Titel + Absätze) im `LANDING_PAGES`-Dict in `app.py` sowie einen
neuen, generischen Rendering-Block (`.landing-extra`) in `templates/landing_page.html`
umgesetzt. Dadurch ist die Struktur für alle SEO-Landingpages konsistent und
zukünftige Seiten können denselben Mechanismus nutzen.

## 2. Bewusst allgemein gehaltene Aussagen

- **Schwimmorte Berlin**: Es werden keine konkreten Zahlen zu Besucherzahlen,
  Wasserqualität-Messwerten oder historischen "ältestes Bad"-Behauptungen genannt.
  Der Hinweis zur Wasserqualität verweist bewusst allgemein auf "offizielle Quellen
  der zuständigen Stellen", statt konkrete Grenzwerte oder Ämter zu benennen.
- **Schwimmorte Freiburg**: Keine Aussagen zu Neueröffnungen oder Renovierungen von
  Bädern (z. B. Westbad, Freibad Emmendingen), da dies im Projekt nicht verifiziert ist.
- **Kraulen lernen (Berlin & Freiburg)**: Keine historischen Behauptungen dazu, wer
  Kraulen "erfunden" hat. Keine wissenschaftlichen Aussagen ohne Quelle.
- **Coach werden**: Kein "garantierter Verdienst" – explizit als Beispielrechnung
  gekennzeichnet, mit Disclaimer, dass die tatsächliche Stundenzahl von Nachfrage,
  Region und eigener Verfügbarkeit abhängt.
- **Kinder-Schwimmtraining**: Keine medizinischen/therapeutischen Versprechen, keine
  Sicherheitsgarantien ("es kann nichts passieren"). Bewusst mit "eng begleitet",
  "geschützter Rahmen", "individuelle Aufmerksamkeit" formuliert.
- **Triathlon-Schwimmtraining**: Keine Garantie auf Wettkampferfolg, keine
  medizinischen Versprechen.

## 3. Fakten, die noch verifiziert werden sollten (TODO)

- [ ] **"Über 50 Kundinnen und Kunden haben mit Squalo bereits Kraultechnik
      aufgebaut oder verbessert"** (verwendet auf `/kraulen-lernen-berlin` und
      `/kraulen-lernen-freiburg`) – dies ist eine bewusst gesetzte interne
      Richtzahl. Sollte mit echten Kunden-/Buchungsdaten abgeglichen und bei
      Bedarf angepasst werden, sobald verlässliche Zahlen vorliegen. Aktuell an
      beiden Stellen konsistent gehalten.
- [ ] **Wasserqualität an Berliner Badestellen** – aktuell nur als allgemeiner
      Hinweis auf offizielle Quellen formuliert. Falls eine konkrete, verifizierte
      Quelle (z. B. Land Berlin / Senatsverwaltung) referenziert werden soll, bitte
      hier ergänzen.
- [ ] **Historische Fakten zu einzelnen Bädern** (z. B. "ältestes Schwimmbad
      Berlins") – bewusst nicht verwendet, da im Projekt keine verifizierte Quelle
      vorliegt. Falls gewünscht, mit einer geprüften Quelle nachträglich ergänzen.

## 4. Seiten, die nach diesen Änderungen erneut in der Search Console geprüft/eingereicht werden sollten

- `/coach-werden`
- `/schwimmtraining-kinder-berlin`
- `/schwimmorte-berlin`
- `/schwimmorte-freiburg`
- `/kraulen-lernen-berlin`
- `/kraulen-lernen-freiburg`
- `/triathlon-schwimmtraining-berlin`
- `/coaches` (geänderte Reihenfolge, kein Textinhalt geändert – niedrige Priorität)

## 5. Nicht angefasste Bereiche (zur Erinnerung)

Hero-Bilder, Geodaten/Koordinaten, Map-Logik, Booking-Logik, Shop-Logik, Preise
(außer dem erklärten Kommissionsbeispiel), Datenbank-Resets, `drop_all()`,
PostgreSQL/`DATABASE_URL`-Konfiguration – all das wurde in diesem Durchgang nicht
verändert.
