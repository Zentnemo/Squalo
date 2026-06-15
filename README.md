# 🏊 Squalo Schwimmcoaching Berlin – MVP Web-App

Eine einfache, lokal lauffähige Flask-Web-App für Squalo Schwimmcoaching Berlin mit Kernfunktionen:

1. **Öffentliche Startseite** – Schwimmort-Übersicht mit Berliner Bädern und Seen
2. **User-Registrierung & Login** – Kostenlose Anmeldung für Mitglieder
3. **Terminwunsch-System** – Nutzer buchen Schwimmstunden mit Wunschortsauswahl
4. **Admin-Panel** – Moritz bestätigt/lehnt Anfragen ab und wählt finalen Ort

---

## 🚀 Schnelstart

### 1. Installation

```bash
cd squalo_webapp
pip install -r requirements.txt
```

### 2. Datenbank initialisieren

```bash
python -m flask --app app seed
```

Das erstellt die SQLite-DB und seeded 9 Berliner Schwimmorte + Admin-User.

### 3. App starten

```bash
python app.py
```

App läuft unter **http://127.0.0.1:5000**

---

## 📋 Admin-Login (zum Testen)

**E-Mail:** `admin@squalo.local`  
**Passwort:** `admin123`

⚠️ **WICHTIG:** Diese Daten sind nur für lokale Entwicklung! Vor Launch unbedingt ändern!

---

## 🗂️ Projektstruktur

```
squalo_webapp/
├── app.py                      # Flask-App, alle Routen
├── models.py                   # SQLAlchemy Models
├── config.py                   # Flask Config (liest ENV-Vars)
├── wsgi.py                     # WSGI Entry Point (für Gunicorn/Render)
├── requirements.txt            # Python Dependencies
├── .env.example                # Environment-Variablen-Vorlage
├── .gitignore                  # Git-ignore Dateien
├── README.md                   # Diese Datei
├── instance/
│   └── squalo.db              # SQLite Datenbank
├── static/
│   ├── css/style.css
│   ├── images/
│   └── data/berlin_districts.geojson
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── booking.html
    ├── admin.html
    ├── admin_week.html
    ├── admin_settings.html
    └── shop.html
```

---

## 💾 Datenbank-Schema

### User
- `id` – Primary Key
- `name` – Nutzername
- `email` – Eindeutige E-Mail
- `password_hash` – Gehashed (Werkzeug)
- `role` – `"user"` oder `"admin"`
- `created_at` – Timestamp

### Location
- `id` – Primary Key
- `name` – Name des Schwimmortes
- `location_type` – Schwimmbad, Sommerbad, See, Strandbad
- `district` – Bezirk (Mitte, Charlottenburg, etc.)
- `address` – Straße/Ort
- `official_status` – offen, geschlossen, unbekannt
- `verified_status` – verifiziert, nicht verifiziert
- `water_temperature` – z.B. "25°C"
- `crowd_level` – niedrig, mittel, hoch
- `maps_url` – Google Maps Link

### Booking
- `id` – Primary Key
- `user_id` – Foreign Key zu User
- `requested_start` – Gewünschtes Datum + Uhrzeit
- `preferred_location_1_id` – 1. Wunschort (FK)
- `preferred_location_2_id` – 2. Wunschort (FK, optional)
- `preferred_location_3_id` – 3. Wunschort (FK, optional)
- `confirmed_location_id` – Admin-Entscheidung (FK, optional)
- `training_goal` – Trainingsziel-Text
- `user_note` – Nutzer-Notiz
- `admin_note` – Admin-Notiz
- `status` – angefragt, bestätigt, abgelehnt
- `created_at`, `updated_at` – Timestamps

---

## 🛣️ Routen

### Öffentlich
- **`GET /`** – Startseite mit Schwimmort-Übersicht
- **`GET /login`** – Login-Formular
- **`POST /login`** – Login verarbeiten
- **`GET /register`** – Registrierungs-Formular
- **`POST /register`** – Registrierung verarbeiten
- **`GET /logout`** – Abmelden

### Mitglieder (login_required)
- **`GET /dashboard`** – Dashboard mit eigenen Terminwünschen
- **`GET /booking`** – Formular für neuen Terminwunsch
- **`POST /booking`** – Terminwunsch speichern

### Admin (login_required + role=="admin")
- **`GET /admin`** – Admin-Panel mit allen Terminwünschen
- **`POST /admin/booking/<id>/confirm`** – Termin bestätigen
- **`POST /admin/booking/<id>/reject`** – Termin ablehnen

---

## 🎨 Design

**Farben:**
- Dunkelblau: `#003d4d`
- Türkis: `#00a8cc`
- Light Turquoise: `#00d4ff`
- Weiß: `#ffffff`
- Light Gray: `#f5f5f5`

**Features:**
- Responsive Design (Mobile-freundlich)
- Klare, schlichte Buttons
- Status-Badges für Termine (angefragt, bestätigt, abgelehnt)
- Location-Karten-ähnliche Grid-Ansicht (keine externe Map API)

---

## ✅ Was funktioniert aktuell

✅ Öffentliche Startseite mit Schwimmort-Übersicht (9 Orte seeded)  
✅ User-Registrierung (Name, E-Mail, Passwort)  
✅ User-Login mit Flask-Login  
✅ User-Dashboard mit Terminübersicht  
✅ Terminwunsch-Formular (Datum, Zeit, 3 Wunschorte, Trainingsziel, Notiz)  
✅ Admin-Panel zum Verwalten aller Anfragen  
✅ Termin bestätigen / ablehnen  
✅ Status-Tracking (angefragt → bestätigt/abgelehnt)  
✅ Responsive CSS mit Dunkelblau/Türkis Theme  

---

## ❌ Bewusst NICHT eingebaut (MVP-Fokus)

- Feed / Community
- Shop
- Fitnesswatch-Integration
- Trainingsvideos
- Produktverwaltung
- Komplexe Kalenderlogik (nur date+time Input)
- Trainingsnotizen nach Buchung
- Nutzer-Profile
- Email-Versand
- Externe Map-APIs (Google Maps Link reicht)
- Zahlung/Shopify

---

## 📝 CLI Commands

```bash
# Datenbank initialisieren (leer)
python -m flask --app app initdb

# Datenbank + Seed-Daten (Admin + 9 Orte)
python -m flask --app app seed

# App im Debug-Modus starten
python app.py
```

---

## 🔐 Sicherheitshinweise

- **Passwörter** werden mit `werkzeug.security` gehasht (nicht plaintext)
- **Secret Key** sollte in `.env` gespeichert und nicht hardcoded sein
- **Admin-Passwort** (`admin123`) muss vor Production-Launch geändert werden!

---

## 🚀 Deployment auf Render (Empfohlen)

### Schritt 1: GitHub-Repo erstellen

```bash
cd squalo_webapp
git init
git add .
git commit -m "Initial commit: Squalo MVP"
```

Dann auf GitHub ein neues Repository erstellen und pushen:

```bash
git remote add origin https://github.com/DEIN_USERNAME/squalo-webapp.git
git push -u origin main
```

### Schritt 2: Render-Konto erstellen

1. Auf [render.com](https://render.com) einloggen (GitHub-Login)
2. **New +** → **Web Service** klicken
3. GitHub-Repo verbinden
4. Einstellungen:

| Feld | Wert |
|---|---|
| **Name** | `squalo-webapp` |
| **Region** | `Frankfurt (EU)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |

### Schritt 3: Umgebungsvariablen in Render setzen

In Render → **Environment** → **Environment Variables**:

| Key | Wert |
|---|---|
| `SECRET_KEY` | (zufälligen String generieren, z.B. `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | `sqlite:///instance/squalo.db` |
| `FLASK_ENV` | `production` |
| `BOOKING_NOTIFICATION_EMAIL` | `zentner.moritz@gmail.com` |

> ⚠️ `SECRET_KEY` niemals in Git speichern!

### Schritt 4: Automatisches Deployment

Nach dem ersten Push deployt Render automatisch. Jeder neue Push auf `main` löst ein Re-Deploy aus.

---

## 🌐 Domain verbinden (Namecheap)

### Option A: Hauptdomain zeigt direkt auf Flask-App

In Namecheap → Domain → **Advanced DNS** → **Host Records**:

| Typ | Host | Value | TTL |
|---|---|---|---|
| CNAME | `@` | `squalo-webapp.onrender.com` | Automatic |
| CNAME | `www` | `squalo-webapp.onrender.com` | Automatic |

> Render gibt dir nach dem ersten Deployment die exakte URL (z.B. `squalo-webapp.onrender.com`).

### Option B: Framer auf Hauptdomain, Flask auf Subdomain

| Typ | Host | Value | TTL |
|---|---|---|---|
| A | `@` | (Framer IP) | Automatic |
| CNAME | `app` | `squalo-webapp.onrender.com` | Automatic |

Dann läuft die Flask-App unter `https://app.squalo-schwimmcoaching.com`.

> ⚠️ **Keine DNS-Werte erfinden.** Die konkreten Werte werden vom Hosting-Anbieter vorgegeben.

---

## 🎨 Framer + Flask Kombination

Wenn Framer für die Marketing-Landingpage genutzt wird:

- **Framer** → `squalo-schwimmcoaching.com` (Landingpage mit CTA "Termin anfragen")
- **Flask** → `app.squalo-schwimmcoaching.com` (Login, Booking, Admin)
- Framer-Landingpage bekommt Button/Link zur Flask-App

---

## 📱 Lokaler Handy-Test im WLAN

```bash
python app.py
```

Dann auf dem Handy im selben WLAN:

```
http://DEINE-PC-IP:5000
```

IP-Adresse finden: `ipconfig` (Windows) oder `ifconfig` (Mac/Linux)

---

## 🔐 Sicherheit vor Launch

- [ ] `SECRET_KEY` in `.env` setzen (nicht hardcoded)
- [ ] Admin-Passwort ändern (`devpassword` → sicheres Passwort)
- [ ] `debug=True` in Production deaktiviert (über ENV-Var)
- [ ] HTTPS aktiviert (automatisch via Render)

---

## ✅ Launch-Checkliste

- [ ] GitHub-Repo erstellt und Code gepusht
- [ ] Render-Konto erstellt
- [ ] Web Service auf Render angelegt
- [ ] Environment-Variablen gesetzt
- [ ] Erstes Deployment erfolgreich
- [ ] App erreichbar über Render-URL
- [ ] Domain in Namecheap DNS konfiguriert
- [ ] HTTPS funktioniert
- [ ] Login/Registrierung funktioniert
- [ ] Buchung funktioniert
- [ ] Admin-Bereich funktioniert
- [ ] Mobile-Test bestanden
- [ ] Admin-Passwort geändert
- [ ] Impressum/Datenschutz (optional, aber empfohlen)

---

## 🏊 Squalo Swim Locations Database

### Location Seed Data

The Squalo webapp now includes a comprehensive database of **30+ Berlin swimming locations** for the MVP launch:

#### Core Berlin Locations (23 locations)
- Stadtbad Tiergarten
- Kombibad Seestraße
- Schwimm- und Sprunghalle im Europasportpark
- Sommerbad Neukölln
- Prinzenbad
- Stadtbad Charlottenburg – Alte Halle
- Strandbad Plötzensee
- Flughafensee
- Strandbad Wannsee
- Stadtbad Schöneberg
- Stadtbad Wilmersdorf I
- Stadtbad Wilmersdorf II
- Kombibad Gropiusstadt – Halle
- Kombibad Gropiusstadt – Sommerbad
- Sommerbad Kreuzberg
- Sommerbad Olympiastadion
- Kombibad Spandau Süd
- Stadtbad Lankwitz
- Tegeler See
- Stadtbad Fischerinsel
- Müggelsee
- Strandbad Friedrichshagen
- James Simon Stadtbad

#### Additional Berlin Locations (8+ locations)
- Arena Badeschiff
- Schlachtensee
- Krumme Lanke
- Sommerbad Humboldthain
- Strandbad Weißensee
- Freibad Jungfernheide / Strandbad Jungfernheide
- Strandbad Orankesee
- Sommerbad Pankow
- Sommerbad Mariendorf
- Strandbad Grünau
- Strandbad Müggelsee / Rahnsdorf-Bereich
- Sacrower See / Potsdam-nah
- Heiliger See / Potsdam
- Stadtbad Neukölln
- Paracelsus-Bad
- Schwimmhalle Finckensteinallee
- Kombibad Mariendorf
- Schwimmhalle Anton-Saefkow-Platz

### Database Features

- **Idempotent Seeding**: Locations are only created if they don't already exist
- **Data Updates**: Existing locations are updated if data is missing
- **Comprehensive Coverage**: All locations include coordinates, addresses, and detailed information
- **Map Integration**: All locations are available for the interactive map

### Location Data Structure

Each location includes:
- `name` – Location name
- `location_type` – Schwimmbad, Sommerbad, Strandbad, See, etc.
- `district` – Berlin district
- `address` – Full address
- `latitude` – GPS coordinates
- `longitude` – GPS coordinates
- `official_status` – offen, geschlossen, unbekannt
- `verified_status` – verifiziert, nicht verifiziert
- `water_temperature` – Typical water temperature
- `crowd_level` – niedrig, mittel, hoch
- `maps_url` – Google Maps link

### Map Features

The interactive map displays all locations with:
- Custom markers for each location type
- Popup information with name, type, district, and address
- Google Maps links for navigation
- Responsive design for mobile devices

### Database Management

#### Local Development
```bash
# Initialize database with seed data
python -m flask --app app seed
```

#### Render Deployment
The database is automatically initialized on Render startup:
- Instance directory is created automatically
- Database tables are created if missing
- All locations are seeded if not present
- Existing locations are updated with missing data

#### Environment Variables
For production deployment, set these environment variables in Render:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key (generate random string) |
| `DATABASE_URL` | Database URL (leave empty for SQLite auto-setup) |
| `FLASK_ENV` | Flask environment (production) |
| `BOOKING_NOTIFICATION_EMAIL` | Email for booking notifications |

### Location Categories

**Indoor Pools:**
- Stadtbad Tiergarten
- Stadtbad Charlottenburg – Alte Halle
- Stadtbad Schöneberg
- Stadtbad Wilmersdorf I & II
- Paracelsus-Bad
- Schwimmhalle Finckensteinallee
- Schwimmhalle Anton-Saefkow-Platz

**Summer Pools:**
- Sommerbad Neukölln
- Prinzenbad
- Sommerbad Kreuzberg
- Sommerbad Olympiastadion
- Sommerbad Humboldthain
- Sommerbad Pankow
- Sommerbad Mariendorf

**Combination Pools:**
- Kombibad Seestraße
- Schwimm- und Sprunghalle im Europasportpark
- Kombibad Gropiusstadt – Halle & Sommerbad
- Kombibad Spandau Süd
- Kombibad Mariendorf

**Natural Waters:**
- Strandbad Plötzensee
- Flughafensee
- Strandbad Wannsee
- Tegeler See
- Schlachtensee
- Krumme Lanke
- Strandbad Weißensee
- Strandbad Orankesee
- Strandbad Grünau
- Strandbad Müggelsee / Rahnsdorf-Bereich
- Sacrower See
- Heiliger See
- Müggelsee
- Strandbad Friedrichshagen

**Special Locations:**
- Arena Badeschiff
- James Simon Stadtbad
- Stadtbad Neukölln
- Stadtbad Lankwitz
- Stadtbad Fischerinsel
- Kombibad Gropiusstadt – Halle
- Kombibad Spandau Süd
- Kombibad Mariendorf
