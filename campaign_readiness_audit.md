# Campaign Readiness Audit – Flyer & Google Ads

> **Datum:** 22.07.2026  
> **Geprüft von:** Automatisierter Audit  
> **Ziel:** Feststellung, ob die Website bereit ist für Flyer-Druck und Traffic durch Google Ads.

---

## Gesamtstatus: 🟡 GELB

Die Website ist **grundsätzlich kampagnentauglich**, hat aber einige Verbesserungspunkte, die vor dem Flyer-Druck adressiert werden sollten. Keine roten Blocker.

---

## 1. Homepage (`/`)

| Prüfpunkt | Status |
|---|---|
| Hero wirkt hochwertig | ✅ |
| Hero-Unterzeile gut lesbar | ✅ |
| Alter schmaler/quadratischer Erklärblock entfernt | ✅ |
| Neuer breiter Banner ist flach und breit | ✅ |
| Preis-Funnel sichtbar und korrekt (ab 50€ / 200€) | ✅ |
| Map wird nicht zu weit nach unten gedrückt | ✅ |
| Keine doppelten störenden CTAs | ✅ |
| „Kostenlos registrieren" sinnvoll erklärt | ✅ |
| Mobile Ansicht sauber (kein horizontaler Scrollbalken) | ✅ |
| **„Moritz bestätigt" → „Squalo bestätigt" gefixt** | ✅ ✅ |

**GELB:**
- Step-Cards in „Wie funktioniert Squalo?" verlinken auf falsche Ziele:
  - Step 1 (Registrieren) → `/login` statt `/register`
  - Step 2 (Termin anfragen) → `/dashboard` statt `/booking`
  - Step 3 (Bestätigung) → `/coaches`
  - Step 4 (Trainieren) → `/dashboard`
  > *Vorschlag: Step 1 → /register, Step 2 → /booking, Step 3 → /dashboard (ok), Step 4 → /dashboard (ok)*

---

## 2. Flyer-Landingpage (`/flyer`)

| Prüfpunkt | Status |
|---|---|
| Lädt ohne Fehler (HTTP 200) | ✅ |
| Preis sichtbar (ab 50€ / 200€) | ✅ |
| CTA zu `/booking` funktioniert (mit UTM-Parametern) | ✅ |
| Text passt zu Flyer-Kampagne | ✅ |
| QR-Hinweis „Du bist über einen Flyer hier?" vorhanden | ✅ |
| Orte: Plötzensee, Tegeler See, Flughafensee, Kombibad Seestraße, Stadtbad Tiergarten | ✅ |
| Kein „Moritz bestätigt" (neutral „Squalo bestätigt") | ✅ |
| Mobil: keine horizontalen Scrollbalken | ✅ |
| Meta-Titel & Description korrekt | ✅ |

**Status: 🟢 GRÜN** – Keine Änderungen nötig.

---

## 3. QR-Ziel

| Prüfpunkt | Status |
|---|---|
| `/flyer` existiert als Route | ✅ |
| `/flyer` ist dauerhafte Route (kein temporärer Redirect) | ✅ |
| `/flyer` funktioniert lokal und remote | ✅ |

**Status: 🟢 GRÜN** – `/flyer` ist ein stabiles, dauerhaftes QR-Ziel.

---

## 4. Booking (`/booking`)

| Prüfpunkt | Status |
|---|---|
| Booking-Seite lädt (nach Login, HTTP 200) | ✅ |
| Region/Ort auswählbar | ✅ |
| Coach auswählbar | ✅ |
| Terminwunsch möglich (3 Optionen) | ✅ |
| Preis/Angebot verständlich (Live-Preisvorschau) | ✅ |
| Anfrage kann abgeschickt werden | ✅ |
| Keine Fehlermeldung bei korrekter Eingabe | ✅ |
| **„Moritz bestätigt" → „Squalo bestätigt" gefixt** | ✅ ✅ |
| **„Was soll Moritz wissen?" → „Was sollen wir wissen?" gefixt** | ✅ ✅ |

**GELB:**
- ⚠️ **Login-Wall:** `/booking` erfordert `@login_required`. Nutzer, die vom Flyer-QR-Code kommen, landen auf dem Login-Formular. Sie müssen sich erst registrieren, bevor sie eine Anfrage stellen können.
  > *Vorschlag: Prüfen, ob eine vereinfachte Vorab-Anfrage auch ohne Login möglich sein soll (z. B. Name + E-Mail + Nachricht). Dies ist jedoch kein reiner Text-Fix mehr, sondern eine Architekturentscheidung.*

---

## 5. Admin-Mail bei Buchungsanfrage

| Datenfeld | Vorhanden? |
|---|---|
| Name | ✅ |
| E-Mail | ✅ |
| Telefon | ❌ **Immer „Keine Angabe"** – User-Modell hat kein Telefonfeld, Booking-Formular fragt nicht ab |
| Region/Stadt | ✅ |
| Trainingsort | ✅ |
| Coach | ✅ |
| Dauer | ✅ |
| 3 Terminwünsche | ✅ |
| Trainingsziel | ✅ |
| Nachricht | ✅ |
| Zeitpunkt der Anfrage | ⚠️ Nicht explizit in E-Mail, nur booking.id |

**GELB:**
- ❌ Kein Telefonfeld in Booking-Formular oder User-Modell
- Empfehlung: Telefonfeld ins Booking-Formular einbauen (risikoarm, da nur HTML + Model-Erweiterung)

---

## 6. Shop-/Materialanfrage (`/shop`)

| Prüfpunkt | Status |
|---|---|
| `/shop` lädt (HTTP 200) | ✅ |
| Produkte auswählbar | ✅ |
| Preis pro Produkt sichtbar | ✅ |
| Gesamtpreis wird berechnet | ✅ |
| Name, E-Mail, Nachricht erfassbar | ✅ |
| Admin-Mail wird ausgelöst | ✅ |
| Keine None-Werte | ✅ |

| Datenfeld in Admin-Mail | Vorhanden? |
|---|---|
| Name | ✅ |
| E-Mail | ✅ |
| Telefon | ❌ **Fehlt komplett** (weder Formular noch E-Mail) |
| Produkt(e) | ✅ |
| Preis | ✅ |
| Menge | ❌ **Nicht vorhanden** (nur einfache Auswahl, kein Mengenkonzept) |
| Nachricht | ✅ |
| Zeitpunkt | ✅ |

**GELB:**
- ❌ Kein Telefonfeld im Shop-Formular
- ❌ Kein Mengenkonzept (nur Auswählen/Abwählen)
- Empfehlung: Telefonfeld ergänzen (risikoarm)

---

## 7. Coaches (`/coaches`)

| Prüfpunkt | Status |
|---|---|
| Moritz sichtbar (Berlin) | ✅ |
| Clara sichtbar (Freiburg) | ✅ |
| Tolga sichtbar (Berlin) | ✅ |
| Tolga nur Berlin | ✅ |
| Clara nur Freiburg | ✅ |
| Tolga: „über zehn Jahre Erfahrung" | ✅ |
| Tolga: „Berliner Wasserratten 1889 e.V." | ✅ |
| Tolga: „Schwimmclub Wedding" | ✅ |
| Tolga: „Deutsch und Türkisch" | ✅ |
| Tolga: „Plötzensee" | ✅ |
| Tolga: „Kombibad Seestraße" | ✅ |
| Keine Fake-Bewertungen (nur Superprof-Import) | ✅ |

**GELB:**
- ⚠️ Clara: Superprof-Link zeigt auf `None` (Broken Link)
  > *Zeile ~203 in templates/coaches.html: `<a href="None">Superprof-Profil</a>` – Hier fehlt die URL.*

---

## 8. Mobile & Responsive

| Gerät/Seite | Horizontaler Scrollbalken? | Buttons klickbar? |
|---|---|---|
| Homepage (`/`) | ❌ Nein (375×844) | ✅ |
| Flyer (`/flyer`) | ❌ Nein | ✅ |
| Booking (`/booking`) | ❌ Nein | ✅ |
| Coaches (`/coaches`) | ❌ Nein | ✅ |
| Shop (`/shop`) | ❌ Nein | ✅ |

**Status: 🟢 GRÜN** – Alle geprüften Seiten sind mobil nutzbar.

---

## 9. Sitemap / SEO

| Prüfpunkt | Status |
|---|---|
| `/sitemap.xml` lädt (HTTP 200) | ✅ |
| `/flyer` enthalten | ✅ |
| `/booking` enthalten | ✅ |
| `/coaches` enthalten | ✅ |
| Alle 9 Landingpages enthalten | ✅ |
| Private Seiten NICHT enthalten (`/admin`, `/dashboard`, `/login`, etc.) | ✅ |
| Canonical-Link in `base.html` vorhanden | ✅ |
| Meta-Descriptions auf allen geprüften Seiten | ✅ |

**Status: 🟢 GRÜN**

---

## 10. Kleine Fixes (bereits durchgeführt)

| Fix | Datei |
|---|---|
| „Moritz bestätigt" → „Squalo bestätigt" (Step 3) | `templates/index.html` |
| „Moritz bestätigt" → „Squalo bestätigt" (Subline) | `templates/booking.html` |
| „Sobald Moritz" → „Sobald Squalo" (Dashboard) | `templates/dashboard.html` |
| „Was soll Moritz wissen?" → „Was sollen wir wissen?" | `templates/booking.html` |

---

## 11. Empfehlungen vor Flyer-Druck

### Kritisch (ROT) – Keine
Es wurden keine roten Blocker gefunden, die den Flyer-Druck verhindern würden.

### Wichtig (GELB) – Vor Kampagnenstart adressieren

1. **🔶 Booking-Login-Wall** – Nutzer vom Flyer müssen sich registrieren, bevor sie buchen können. Prüfen, ob eine anonyme Vorabanfrage gewünscht ist.
2. **🔶 Telefonfeld fehlt** – Weder Booking noch Shop erfragen eine Telefonnummer. Die Admin-Mail zeigt immer „Keine Angabe".
3. **🔶 Clara: Superprof-Link defekt** (`href="None"`) in `templates/coaches.html`.
4. **🔶 Step-Card-Links** auf der Homepage zeigen auf falsche Routen.

### Optional (INFO)

- Shop: Kein Mengenkonzept – Kunde kann nicht sagen „2× Flossen".
- Admin-Mail: Zeitpunkt der Anfrage nicht explizit in E-Mail (nur booking.id).
- Confirmation-E-Mail signiert als „Moritz" (persönlich, kann so bleiben).

---

## 12. PostgreSQL / DATABASE_URL

**Status: ✅ Unangetastet** – Keine Änderungen an Datenbank-URL oder Konfiguration.

---

## 13. Preview-Test

| Seite | Status |
|---|---|
| `/` | HTTP 200 (136 KB) |
| `/flyer` | HTTP 200 (22 KB) |
| `/booking` | HTTP 200 (11 KB, nach Login) |
| `/coaches` | HTTP 200 (32 KB) |
| `/shop` | HTTP 200 (23 KB) |
| `/sitemap.xml` | HTTP 200 (15 URLs) |
| `/dashboard` | HTTP 200 (11 KB) |

Alle Seiten laden ohne Fehler. Keine Datenbankfehler. Keine 500er.

---

## 14. Commit & Push

- ✅ `git add` aller geänderten Dateien
- ✅ `git commit` – siehe unten
- ✅ `git push` zu `origin main`

---

## Fazit

> **🟡 GELB – „Kann man jetzt Flyer drucken?" → Ja, aber mit den genannten Verbesserungen wird die Conversion-Rate höher sein.**

Die Website ist technisch stabil, alle Routen funktionieren, der Flyer-Text und die Preise stimmen. Die größte UX-Hürde ist der erzwungene Login vor der Buchungsanfrage. Wenn das gewünscht ist (Registrierung als Lead-Qualifizierung), kann der Flyer sofort gedruckt werden.
