# KI-Suche / LLM-Findability-Audit für Squalo Schwimmcoaching

**Datum:** 2026-07-22  
**Projekt:** Squalo Schwimmcoaching (https://squalo-schwimmcoaching.com)

---

## 1. robots.txt — Status

| Crawler | Allow | Disallow |
|---------|-------|----------|
| `User-agent: *` | `/` | `/admin`, `/dashboard`, `/feed`, `/login`, `/register`, `/logout` |
| `User-agent: OAI-SearchBot` | `/` | `/admin`, `/dashboard`, `/login`, `/register` |
| `User-agent: OAI-AdsBot` | `/` | `/admin`, `/dashboard`, `/login`, `/register` |
| `User-agent: ChatGPT-User` | `/` | `/admin`, `/dashboard`, `/login`, `/register` |

✅ **Alle wichtigen KI-Crawler sind explizit erlaubt.**  
✅ **Sitemap wird korrekt referenziert.**  
✅ **Private Bereiche werden blockiert.**

---

## 2. Sitemap — Status

**Dynamisch generiert** aus `LANDING_PAGES`-Dictionary + festen Seiten.

### Enthaltene öffentliche Seiten:

| Seite | Priority | Changefreq |
|-------|----------|------------|
| `/` | 1.0 | daily |
| `/coaches` | 0.8 | weekly |
| `/shop` | 0.6 | weekly |
| `/booking` | 0.5 | monthly |
| `/impressum` | 0.3 | monthly |
| `/schwimmtraining-berlin` | 0.7 | monthly |
| `/kraulen-lernen-berlin` | 0.7 | monthly |
| `/schwimmkurs-erwachsene-berlin` | 0.7 | monthly |
| `/schwimmtraining-kinder-berlin` | 0.7 | monthly |
| `/triathlon-schwimmtraining-berlin` | 0.7 | monthly |
| `/schwimmtraining-freiburg` | 0.7 | monthly |
| `/kraulen-lernen-freiburg` | 0.7 | monthly |
| `/schwimmorte-berlin` | 0.7 | monthly |
| `/schwimmorte-freiburg` | 0.7 | monthly |

### Nicht enthalten (private/geschützte Seiten):
`/admin`, `/dashboard`, `/feed`, `/login`, `/logout`, `/register`, `/students`, `/invoices`, `/calendar`

✅ **Sitemap vollständig und aktuell.**  
✅ **Keine privaten Seiten enthalten.**

---

## 3. Crawlbarkeit wichtiger Inhalte

**Alle Inhalte sind als normaler HTML-Code im DOM sichtbar** – keine JavaScript-Abhängigkeit für Texte.

| Thema | Sichtbar in | Status |
|-------|-------------|--------|
| Coach-Namen (Moritz, Clara, Tolga) | `/coaches` | ✅ |
| Städte Berlin/Freiburg | Alle Seiten | ✅ |
| Schwimmtraining | Landingpages, Startseite | ✅ |
| Schwimmcoaching | Landingpages, Startseite | ✅ |
| Kraulen lernen | `/kraulen-lernen-berlin`, `/kraulen-lernen-freiburg` | ✅ |
| Triathlon-Schwimmtraining | `/triathlon-schwimmtraining-berlin` | ✅ |
| Schwimmtraining Erwachsene | `/schwimmkurs-erwachsene-berlin` | ✅ |
| Schwimmtraining Kinder | `/schwimmtraining-kinder-berlin` | ✅ |
| Türkischsprachiges Coaching | `/coaches` (Tolga-Profil) | ✅ |
| Schwimmorte Berlin/Freiburg | `/schwimmorte-berlin`, `/schwimmorte-freiburg` | ✅ |

✅ **Keine versteckten Keywords oder unsichtbaren Texte.**  
✅ **Alle KI-relevanten Inhalte sind crawlbar.**

---

## 4. Strukturierte Daten / JSON-LD — Status

### Vorhanden:

| Seite | Schema-Typ | Status |
|-------|-----------|--------|
| `/` (Startseite) | `Organization` + `SportsActivityLocation` (mit @graph) | ✅ Neu |
| Landingpages | `FAQPage`, `Question`, `Answer` (Microdata) | ✅ Bestehend |

### Details zum Startseiten-JSON-LD:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://squalo-schwimmcoaching.com/#organization",
      "name": "Squalo Schwimmcoaching",
      "description": "Personal Schwimmtraining, Techniktraining und Triathlon-Coaching in Berlin und Freiburg.",
      "url": "https://squalo-schwimmcoaching.com",
      "areaServed": ["Berlin", "Freiburg"],
      "sport": "Swimming",
      "foundingDate": "2025",
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "email": "info@squalo-schwimmcoaching.com"
      }
    },
    {
      "@type": "SportsActivityLocation",
      "@id": "https://squalo-schwimmcoaching.com/#location",
      "name": "Squalo Schwimmcoaching Berlin",
      "areaServed": ["Berlin"],
      "parentOrganization": { "@id": "https://squalo-schwimmcoaching.com/#organization" }
    },
    {
      "@type": "SportsActivityLocation",
      "@id": "https://squalo-schwimmcoaching.com/#location-freiburg",
      "name": "Squalo Schwimmcoaching Freiburg",
      "areaServed": ["Freiburg"],
      "parentOrganization": { "@id": "https://squalo-schwimmcoaching.com/#organization" }
    }
  ]
}
```

⚠️ **Keine Fake-Bewertungen (`AggregateRating`) – bleibt so.**  
⚠️ **Keine erfundenen Standorte – `areaServed` korrekt auf Berlin/Freiburg beschränkt.**

### Empfehlung:
- Für **Coaches-Seite** könnte später ein `Person`-Schema für jeden Coach ergänzt werden (optional).

---

## 5. Meta / OpenGraph / Canonicals — Status

| Element | Status | Details |
|---------|--------|---------|
| Title | ✅ Individuell pro Seite | Über `{% block title %}` |
| Meta Description | ✅ Individuell pro Seite | Über `{% block meta_description %}` |
| Canonical URL | ✅ Dynamisch | Nutzt `get_public_base_url()` + `request.path` |
| OpenGraph Title | ✅ | Überschreibbar pro Seite |
| OpenGraph Description | ✅ | Überschreibbar pro Seite |
| OpenGraph Image | ✅ | `squalo-logo.png` |
| Twitter Card | ✅ | `summary_large_image` |
| Robots Meta | ✅ | `index, follow` (public) / `noindex` (admin) |

✅ **Keine `localhost`- oder `onrender.com`-Canonicals im Produktionsbetrieb**  
✅ **Canonical-URLs zeigen auf Hauptdomain (`squalo-schwimmcoaching.com`)** bei gesetzter `PUBLIC_BASE_URL`-Env-Variable.

---

## 6. FAQ-Abschnitte — Analyse

### Vorhandene FAQs auf Landingpages:

| Landingpage | Anzahl FAQs | Beispielfragen |
|-------------|------------|----------------|
| `/schwimmtraining-berlin` | 5 | Für wen?, Wie läuft erste Stunde?, Kraulen als Erwachsener?, Wo?, Termin anfragen? |
| `/kraulen-lernen-berlin` | 4 | Noch nie gekrault?, Wie lange?, Erwachsene vs Kinder?, Kondition nötig? |
| `/schwimmkurs-erwachsene-berlin` | 3 | Erwachsener lernen?, Erste Stunde?, Wie viele Stunden? |
| `/schwimmtraining-kinder-berlin` | 3 | Ab welchem Alter?, Muss Kind können?, Eltern zuschauen? |
| `/triathlon-schwimmtraining-berlin` | 4 | Zeit verbessern?, Offenes Wasser?, Anfänger?, Wie oft? |
| `/schwimmtraining-freiburg` | 4 | Für wen?, Wo in Freiburg?, Erste Stunde?, Termin anfragen? |
| `/kraulen-lernen-freiburg` | 3 | Noch nie gekrault?, Wie lange?, Erwachsene schwerer? |
| `/schwimmorte-berlin` | 3 | Für Anfänger?, Badesee?, Freibad Winter? |
| `/schwimmorte-freiburg` | 3 | Beste Bäder?, Badeseen?, Außerhalb Freiburg? |

### Fehlende FAQ-Fragen (vorgeschlagen für Ergänzung):

- „Was kostet Schwimmtraining bei Squalo?" → Könnte auf Startseite oder eigener FAQ-Seite beantwortet werden.
- „Kann ich auf Türkisch trainieren?" → Tolga-Profil auf Coaches-Seite erwähnt es bereits, aber keine eigene FAQ.
- „Wie werde ich Coach bei Squalo?" → `/coach-werden`-Seite existiert noch nicht.
- „Gibt es Schwimmstunden für Kinder?" → Wird in `/schwimmtraining-kinder-berlin` beantwortet, aber separate Frage könnte helfen.

✅ **Bestehende FAQs sind schema.org-konform ausgezeichnet (FAQPage, Question, Answer).**  
⚠️ **Kein Eingriff in bestehende Landingpages – Empfehlungen für später notiert.**

---

## 7. Bing Webmaster Tools — Vorbereitung

Bing Webmaster Tools sollte eingerichtet werden, damit Squalo in Bing/Copilot-Suchen besser sichtbar ist.

### Manuelle Schritte:

1. **Bing Webmaster Tools öffnen:** https://www.bing.com/webmasters
2. **Domain hinzufügen:** `squalo-schwimmcoaching.com`
3. **Besitz bestätigen:** Über DNS-Eintrag, Meta-Tag oder Datei-Upload.
4. **Sitemap einreichen:** `https://squalo-schwimmcoaching.com/sitemap.xml`
5. **Indexierung prüfen:** Nach einigen Tagen prüfen, ob Seiten indexiert sind.
6. **AI Performance / Search Performance beobachten:** Bing bietet eigene Reports für AI Visibility.

✅ **Keine API-Integration nötig – nur manuelle Einrichtung.**  
✅ **Sitemap und robots.txt sind bereits Bing-kompatibel.**

---

## 8. Referrer-Tracking für KI-Quellen — Status

### Aktuell:
- Die App speichert `last_path` und `last_seen` für Besucher.
- `referrer` wird **aktuell nicht explizit gespeichert**.

### Empfehlung:
Ein einfaches Referrer-Tracking einbauen, um zu erkennen, ob Nutzer von KI-Quellen kommen:

| Quelle | Referrer-String |
|--------|----------------|
| ChatGPT | `chatgpt.com` |
| Perplexity | `perplexity.ai` |
| Claude | `claude.ai` |
| Copilot | `copilot.microsoft.com` |
| Bing | `bing.com` |
| Google | `google.com` |

**Umsetzung (Folge-Task):**  
- `referrer` aus `request.headers.get('Referer')` speichern.
- In der Admin-Ansicht oder einem Analytics-Dashboard anzeigen.
- Bots/Admin-Traffic aus echten Besucherzahlen ausschließen.

✅ **Aktuell nicht vorhanden – als Folge-Task dokumentiert.**  
⚠️ **Keine große Analytics-Umstellung jetzt – nur Notiz.**

---

## 9. llms.txt — Status

Eine `/llms.txt`-Datei wurde optional ergänzt unter:

```
https://squalo-schwimmcoaching.com/llms.txt
```

Inhalt: Kurze Projektbeschreibung + Liste der wichtigsten öffentlichen URLs.

⚠️ **llms.txt ist kein offizieller SEO-Standard, aber eine LLM-freundliche Ergänzung.**  
✅ **Risikoarm umgesetzt.**

---

## 10. Folge-Tasks (Empfehlungen)

### Kurzfristig (niedriges Risiko):
1. ✅ **robots.txt verbessert** – OAI-SearchBot, OAI-AdsBot, ChatGPT-User explizit erlaubt (erledigt).
2. ✅ **JSON-LD erweitert** – Organization + SportsActivityLocation mit @graph-Struktur (erledigt).
3. ✅ **llms.txt ergänzt** – Universelle LLM-Übersicht (erledigt).
4. ✅ **Sitemap-Audit** – Alle Landingpages enthalten, private Seiten ausgeschlossen (erledigt).

### Mittelfristig:
5. **Bing Webmaster Tools einrichten** – Manuell (s. Teil 7).
6. **Referrer-Tracking für KI-Quellen** – Einfaches Speichern des Referrer-Headers in der Session/Besuchertabelle.
7. **FAQ-Seite „Was kostet Schwimmtraining?"** – Könnte auf Startseite oder als Mini-FAQ ergänzt werden.
8. **FAQ „Türkischsprachiges Training"** – Auf Coaches-Seite oder eigener Landingpage.

### Langfristig:
9. **Person-Schema für Coaches** – Strukturierte Daten für jeden Coach auf `/coaches`.
10. **Coach-werden-Seite** – `/coach-werden` als Landingpage mit FAQ „Wie werde ich Coach bei Squalo?".
11. **Google Search Console – KI-Insights beobachten** – Google Search Console zeigt ggf. „AI Overviews"-Daten.

---

## Zusammenfassung

| Bereich | Bewertung | Status |
|---------|-----------|--------|
| robots.txt | ✅ Hervorragend – alle Crawler erlaubt, private Bereiche geschützt | 🔧 Verbessert |
| Sitemap | ✅ Vollständig – alle öffentlichen Seiten enthalten | ✅ |
| Crawlbarkeit | ✅ Alle Inhalte im HTML sichtbar, kein JS-required | ✅ |
| JSON-LD | ✅ Organization + SportsActivityLocation vorhanden | 🔧 Verbessert |
| Meta/OG/Canonical | ✅ Individuell pro Seite, saubere Canonicals | ✅ |
| FAQ-Schema | ✅ FAQPage auf allen Landingpages mit Microdata | ✅ |
| Fake-Bewertungen | ❌ Keine – bewusst weggelassen | ✅ |
| Hidden Keywords | ❌ Keine – bewusst weggelassen | ✅ |
| Prompt Injection | ❌ Keine – bewusst weggelassen | ✅ |
| Bing Webmaster Tools | ⚠️ Noch nicht eingerichtet | 📋 Folge-Task |
| Referrer-Tracking | ⚠️ Noch nicht für KI-Quellen | 📋 Folge-Task |
| llms.txt | ✅ Optional ergänzt | 🔧 Neu |
