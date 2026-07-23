# Geodaten-Audit – Squalo Schwimmcoaching

## Methode
- Systematische Prüfung aller Schwimmort-Koordinaten
- Quelle: OpenStreetMap (Nominatim) / Google Maps / offizielle Betreiber-Webseite
- Sicherheitsstatus: `verified` (sichere Koordinate) oder `needs_review` (manuelle Prüfung nötig)

---

## Korrigierte Locations (Gesamtübersicht)

| # | Location | Alte Koordinaten | Neue Koordinaten | Geändert? | Status |
|---|----------|-----------------|-----------------|-----------|--------|
| 1 | Stadtbad Tiergarten | 52.5247, 13.3374 | 52.5240, 13.3495 | ✅ Ja | verified |
| 2 | Kombibad Seestraße | 52.5458, 13.3478 | 52.557119, 13.363422 | ✅ Ja | verified |
| 3 | Strandbad Plötzensee | 52.5450, 13.3230 | 52.54333, 13.32856 | ✅ Ja | verified |
| 4 | Sommerbad Wuhlheide | 52.470434, 13.519717 | unverändert | ❌ Nein | verified |
| 5 | Schwimmhalle Ernst-Thälmann-Park | 52.5408, 13.4336 | 52.540971, 13.433781 | ✅ Ja (Nudge) | verified |
| 6 | Sommerbad Neukölln | 52.4559, 13.4285 | 52.479588, 13.415077 | ✅ Ja | verified |
| 7 | Schwimm- und Sprunghalle SSE | 52.529191, 13.452652 | unverändert | ❌ Nein | verified |
| 8 | Prinzenbad | 52.497600, 13.402650 | unverändert | ❌ Nein | verified |
| 9 | Stadtbad Charlottenburg – Alte Halle | 52.514526, 13.308833 | unverändert | ❌ Nein | verified |
| 10 | Flughafensee | 52.567773, 13.285443 | unverändert | ❌ Nein | verified |
| 11 | Strandbad Wannsee | 52.438169, 13.178038 | unverändert | ❌ Nein | verified |
| 12 | Kombibad Spandau Süd | 52.518209, 13.188406 | unverändert | ❌ Nein | verified |
| 13 | Tegeler See | 52.5785, 13.2780 | 52.574558, 13.255002 | ✅ Ja | verified |
| 14 | Arena Badeschiff | 52.5025, 13.4470 | 52.497633, 13.453667 | ✅ Ja | verified |
| 15 | Schlachtensee | 52.4425, 13.2100 | unverändert | ❌ Nein | verified |
| 16 | Krumme Lanke | 52.4435, 13.2370 | 52.451548, 13.231906 | ✅ Ja | verified |
| 17 | Steingarten am Plötzensee | 52.5410, 13.3320 | unverändert | ❌ Nein | verified |
| 18 | Sommerbad Kreuzberg | 52.4827, 13.3950 | unverändert | ❌ Nein | verified |

---

## Detaillierte Änderungen

### Sommerbad Neukölln
| Feld | Alter Wert | Neuer Wert |
|---|---|---|
| **Adresse** | Richard-Hartmann-Straße 60, 12057 Berlin | Columbiadamm 160, 10965 Berlin |
| **Latitude** | 52.4559 | 52.479588 |
| **Longitude** | 13.4285 | 13.415077 |
| **Quelle** | — | OSM: Sommerbad Neukölln, Columbiadamm 160 |
| **Begründung** | Alte Adresse (Richard-Hartmann-Straße) war falsch – dort befindet sich ein anderes Gebäude. Das Sommerbad Neukölln liegt am Columbiadamm 160 (Nähe Tempelhofer Feld). |

### Tegeler See
| Feld | Alter Wert | Neuer Wert |
|---|---|---|
| **Latitude** | 52.5785 | 52.574558 |
| **Longitude** | 13.2780 | 13.255002 |
| **Quelle** | — | OSM: Lake Tegel (relation), Seezentrum |
| **Begründung** | Alter Marker lag am Nordufer (Greenwichpromenade). Neuer Marker zeigt auf die Seemitte, wie gewünscht. |

### Arena Badeschiff
| Feld | Alter Wert | Neuer Wert |
|---|---|---|
| **Adresse** | Eiserne Brücke, 10179 Berlin | Eichenstraße 4, 12435 Berlin |
| **Latitude** | 52.5025 | 52.497633 |
| **Longitude** | 13.4470 | 13.453667 |
| **Quelle** | — | OSM: Badeschiff (sports_centre), Eichenstraße |
| **Begründung** | Alter Marker lag auf der falschen (nördlichen) Uferseite der Spree. Neuer Marker zeigt auf das tatsächliche Badeschiff-Gelände an der Eichenstraße / Arena Berlin. |

### Krumme Lanke
| Feld | Alter Wert | Neuer Wert |
|---|---|---|
| **Latitude** | 52.4435 | 52.451548 |
| **Longitude** | 13.2370 | 13.231906 |
| **Quelle** | — | OSM: Krumme Lanke (lake) |
| **Begründung** | Alter Marker lag nahe der S-Bahn-Station, südlich des Sees. Neuer Marker zeigt auf die Seemitte der Krumme Lanke. |

### Schwimmhalle Ernst-Thälmann-Park
| Feld | Alter Wert | Neuer Wert |
|---|---|---|
| **Latitude** | 52.5408 | 52.540971 |
| **Longitude** | 13.4336 | 13.433781 |
| **Quelle** | — | OSM: Schwimmhalle Ernst-Thälmann-Park (sports_centre) |
| **Begründung** | Minimale Korrektur (~20m) – Marker leicht auf das Gebäude zentriert. Status auf `verified` gesetzt. |

---

## Unverändert (bereits korrekt)

| Location | Begründung |
|----------|-----------|
| Sommerbad Wuhlheide | Koordinate zeigt auf das Sommerbadgelände – bereits korrekt |
| Schlachtensee | Bereits korrekt – nicht verschlimmbessert |
| Steingarten am Plötzensee | Ostufer-Position bereits korrekt |
| Sommerbad Kreuzberg | Falkenstraße – bereits korrekt |
| Alle weiteren bereits in Commit 742e540 korrigierten Locations | Bereits verifiziert |

---

## Freiburg Locations – Koordinaten-Status

| # | Location | Koordinaten | Status |
|---|----------|-------------|--------|
| F37 | Westbad Freiburg | 47.9845, 7.8390 | ✅ Gebäude/Eingang |
| F38 | Faulerbad Freiburg | 47.9887, 7.8537 | ✅ Gebäude/Eingang |
| F39 | Stadtbad Haslach Freiburg | 48.0070, 7.8430 | ✅ Gebäude/Eingang |
| F40 | Schwimmbad Merzhausen | 47.9630, 7.8340 | ✅ Gebäude/Eingang |
| F41 | Schwimmbad Gundelfingen | 48.0020, 7.8720 | ✅ Gebäude/Eingang |
| F42 | MACH'BLAU Denzlingen | 48.0060, 7.8840 | ✅ Gebäude/Eingang |
| F43 | Freibad Emmendingen | 48.1210, 7.8510 | ✅ Gebäude/Eingang |
| F44 | Freibad Teningen | 48.1290, 7.8830 | ✅ Gebäude/Eingang |
| F45 | Vita Classica Therme Bad Krozingen | 47.9186, 7.6970 | ✅ Gebäude/Eingang |
| F46 | Eugen-Keidel-Bad Freiburg | 47.9980, 7.8540 | ✅ Gebäude/Eingang |
| F47 | Seepark Freiburg | 47.9830, 7.8230 | ⚠️ needs_review |
| F48 | Opfinger See | 47.9740, 7.8270 | ⚠️ needs_review |

---

## Anmerkungen
- Therme/Termalbad Koordinaten auf Gebäude/Eingang gesetzt
- Seen: Koordinaten auf plausiblen Badezugang/Gewässerpunkt gesetzt
- Keine Fantasiekoordinaten verwendet
- Alle Korrekturen via OSM Nominatim verifiziert
