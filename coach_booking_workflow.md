# Coach-Terminvorschlag Workflow

Diese Dokumentation beschreibt die neue Funktion "Coach schlägt Schüler einen Termin vor" sowie
den neu angelegten Coach-Login für Clara. **Diese Datei enthält keine Passwörter.**

## 1. Wie ein Coach einen Termin vorschlägt

1. Coach loggt sich ein (Login → `/dashboard` → Link "Coach" → `/admin`).
2. Coach öffnet **Coach-Bereich → Schüler** (`/admin/students`) und klickt auf einen Schüler.
3. Auf der Schülermappe (`/admin/students/<id>`) gibt es jetzt den grünen Button
   **"🗓️ Termin vorschlagen"** (`class="btn btn-success"`).
4. Der Button führt zur neuen Route `GET/POST /admin/students/<user_id>/propose-appointment`
   (Funktion `admin_propose_appointment` in `app.py`), gerendert über das neue Template
   `templates/admin_propose_appointment.html`.
5. Im Formular sind **Schüler und Coach fest vorgegeben** (nicht editierbar):
   - Schüler = der Schüler, dessen Profil geöffnet wurde.
   - Coach = automatisch der eingeloggte Coach (siehe Abschnitt 3).
6. Der Coach trägt Datum, Uhrzeit, Dauer, Schwimmort (mit Stadtfilter Berlin/Freiburg/Alle),
   optional ein Trainingsziel und optional eine Notiz an den Schüler ein und klickt
   **"Terminvorschlag erstellen"**.
7. Der Server legt eine neue `Booking` an (siehe Abschnitt 2) und verschickt **verpflichtend**
   eine E-Mail an den Schüler (siehe Abschnitt 4).

## 2. Welcher Status wird verwendet?

Es wurde **kein bestehender Status wiederverwendet** (insbesondere nicht der halbfertige,
nirgends gesetzte Status `alternative`/`alternativvorschlag`), sondern ein neuer, minimaler Status:

```python
PROPOSED_STATUS = "vorschlag"
```

- Passt zur bestehenden deutschen Namenskonvention (`angefragt`, `bestaetigt`, `abgelehnt`).
- Wird beim Anlegen des Vorschlags gesetzt: `Booking(status=PROPOSED_STATUS, ...)`.
- Wird bei Annahme durch den Schüler auf `"bestaetigt"` geändert (siehe Abschnitt 5).
- Ist **nicht** in `CONFIRMED_STATUSES` enthalten und wird von `/admin` (offene Anfragen) und
  `/admin/week` (Wochenplan, filtert nur `CONFIRMED_STATUSES` + `angefragt`) automatisch
  **nicht** angezeigt – dadurch entstehen keine Nebenwirkungen in den bestehenden Coach-Ansichten.
- In `admin_booking_history.html` gibt es einen eigenen Badge `🗓️ Vorschlag`
  (CSS-Klasse `history-status-proposed`).

Wiederverwendete, bereits existierende `Booking`-Felder (keine Schema-Migration nötig):
- `admin_note` → Notiz des Coaches an den Schüler.
- `training_goal` → optionales Trainingsziel.
- `confirmation_email_sent_at` → Zeitpunkt der (verpflichtenden) Bestätigungs-/Vorschlagsmail;
  dient gleichzeitig als Indikator "Mail wurde verschickt".
- `preferred_coach_id`, `date_option_1`, `time_option_1`, `preferred_location_1_id`,
  `duration_minutes` → wie bei normalen Kundenbuchungen.

## 3. Wie wird der Coach automatisch erkannt?

Neue Hilfsfunktion `get_current_coach()` in `app.py`:

```python
def get_current_coach():
    email = (current_user.email or "").strip().lower()
    for coach in Coach.query.filter_by(is_active=True).all():
        if (coach.email or "").strip().lower() == email:
            return coach
    return None
```

- Das Feld `Coach.email` existierte bereits im Modell, wurde aber bisher nie befüllt.
- Beim App-Start (Seeding) wird es jetzt für Moritz und Clara automatisch gesetzt
  (`existing_coach.email = admin_email` bzw. `clara_login_email`).
- Dadurch ist **keine neue parallele User/Coach-Architektur** nötig – es wird die
  bestehende Rollenlogik (E-Mail-Abgleich) genutzt.
- Falls einem Login kein Coach-Profil zugeordnet ist, zeigt das Formular eine Warnung
  ("Deinem Login ist aktuell kein Coach-Profil zugeordnet") und der Submit-Button ist deaktiviert.

## 4. Stadtfilter Berlin/Freiburg/Alle

Im neuen Formular gibt es drei Radiobuttons ("Alle Orte", "🏊 Berlin", "🏊 Freiburg").
Eine kleine JavaScript-Funktion `filterLocationsByRegion(region)` blendet die `<option>`-Elemente
des Orts-Dropdowns anhand von `data-city` (`Location.city`, Werte `Berlin`/`Freiburg`) ein/aus.
Das ist eine an das bestehende Muster aus `booking.html` angelehnte, aber erweiterte
(3 statt 2 Optionen) Implementierung.

## 5. Verpflichtende Kundenmail (Pflicht, nicht optional)

- Neue Funktion `send_coach_proposed_appointment_email(booking, coach=None, force=False)` in `app.py`.
- Wird **automatisch und verpflichtend** bei jedem erfolgreichen Terminvorschlag aufgerufen –
  es gibt keinen Weg, einen Vorschlag ohne Mailversuch zu speichern.
- Nutzt die bestehende Mailinfrastruktur: Funktion `send_email(subject, recipient, body_text, body_html)`.
  - Ist SMTP konfiguriert (`MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`), wird die Mail per
    SMTP verschickt.
  - Ist kein SMTP konfiguriert (lokale Entwicklung), wird die Mail als "SIMULIERTE E-MAIL" in die
    Konsole geschrieben (bestehendes Verhalten, unverändert).
- Die Mail enthält: Name des Coaches, Datum, Uhrzeit, Dauer, Ort, optionale Notiz
  (wird nur angezeigt, wenn vorhanden – **kein** "None" im Text) sowie einen Dashboard-Link.
- Der Dashboard-Link wird dynamisch über die bestehende Funktion `get_public_base_url()` gebaut
  (`{base_url}/dashboard`), sodass er in Produktion automatisch auf die echte Domain zeigt.
- **Mailfehler-Verhalten:**
  - Der Termin (Booking) wird **immer gespeichert**, unabhängig vom Mailerfolg.
  - Schlägt der Mailversand fehl, sieht der Coach eine deutliche Warnung als Flash-Meldung
    ("Terminvorschlag gespeichert, aber die Mail an den Schüler konnte nicht verschickt werden...").
  - Der exakte technische Fehler wird serverseitig geloggt (Präfix `[MAIL-FEHLER]`), **ohne**
    Zugangsdaten/Secrets im Log.
  - `confirmation_email_sent_at` bleibt in diesem Fall `None` → in der Schülermappe erscheint
    "⚠️ Mail nicht verschickt" statt "📧 Mail verschickt".

## 6. Sichtbarkeit des Terminvorschlags

- **Schülermappe** (`/admin/students/<id>`): Badge "🗓️ Vorschlag" + Mail-Status-Hinweis in der
  Buchungstabelle.
- **Schüler-Dashboard** (`/dashboard`): Neuer Abschnitt **"🗓️ Vorgeschlagene Termine"** (oberhalb
  von "Offene Terminanfragen"), zeigt Datum, Ort, Coach, Dauer, Trainingsziel, Notiz sowie einen
  Button **"✅ Termin annehmen"**.
- **Annahme durch Schüler**: `POST /dashboard/bookings/<booking_id>/accept`
  (Funktion `dashboard_accept_booking`). Prüft Eigentümerschaft und Status, übernimmt
  `date_option_1`/`time_option_1`/`preferred_location_1_id` in die bestätigten Felder und setzt
  `status = "bestaetigt"`. Der Termin erscheint danach ganz normal unter "Bestätigte Termine".
- **Buchungshistorie** (`/admin/booking-history`): Eigener Badge `🗓️ Vorschlag`
  (`history-status-proposed`), fällt nicht mehr unter "Unbekannt".

## 7. Clara-Login

- Neuer User-Account: Name **Clara Marlene Zentner**, E-Mail **clara-marlene@arcor.de**,
  Rolle **admin** (es gibt im System keine separate "coach"-Rolle – Admin ist die Rolle, die
  Zugriff auf den Coach-Bereich `/admin` gewährt; genau wie bei Moritz).
- Wird beim App-Start idempotent geseedet (nur beim allerersten Anlegen wird ein Passwort
  gesetzt; bei bereits existierendem Account wird das Passwort **nicht** überschrieben).
- `Coach.email` für Claras bestehendes Coach-Profil (Standort/Fokus Freiburg) wird auf dieselbe
  E-Mail-Adresse gesetzt, wodurch `get_current_coach()` sie korrekt erkennt.
- Getestet: Login funktioniert, Clara sieht den "Coach"-Link im Menü, erreicht `/admin` und
  `/admin/students/<id>/propose-appointment`, und wird dort korrekt als "Clara Zentner"
  (statt Moritz) als Coach vorausgewählt.
- Das temporäre Passwort wurde **nur einmalig im Chat-Ergebnis** an den Auftraggeber
  ausgegeben und ist **nicht** in dieser Datei oder im Code als Klartext hinterlegt
  (nur der gehashte Wert liegt in der Datenbank).

## 8. Offene TODOs / bekannte Einschränkungen

- Der separate, selten genutzte `@app.cli.command("seed")`-Block (für `flask seed`) wurde
  **nicht** um den Clara-Account erweitert – nur der automatische Seed-Pfad in `create_app()`,
  der bei `python app.py` läuft.
- Die mobile Darstellung des neuen Formulars (`admin_propose_appointment.html`) wurde nicht
  gesondert auf kleinen Bildschirmen getestet (nutzt aber dieselben CSS-Klassen wie die
  bestehenden Formulare, sollte sich daher gleich verhalten).
- Es gibt weiterhin keinen automatischen Reminder/Ablauf-Mechanismus für unbeantwortete
  Terminvorschläge (z. B. Erinnerungsmail nach X Tagen) – falls gewünscht, wäre das ein
  zukünftiges Feature.
