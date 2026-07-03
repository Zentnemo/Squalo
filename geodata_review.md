# Geodaten-Review

## Batch-Review-Methode

Immer nur **5 Locations pro Batch** prüfen/korrigieren.
Nach jedem 5er-Batch:
1. Ausgabe der korrigierten Koordinaten
2. Auf Bestätigung des Users warten
3. Erst danach weitermachen

## Berliner Locations – Erster Batch (offen)

| # | Location | Status |
|---|----------|--------|
| 1 | Stadtbad Tiergarten | ⏳ Koordinaten prüfen |
| 2 | Kombibad Seestraße | ⏳ Koordinaten prüfen |
| 3 | Steingarten am Plötzensee | ⏳ Koordinaten prüfen |
| 4 | Strandbad Plötzensee | ⏳ Koordinaten prüfen |
| 5 | Strandbad Wannsee | ⏳ Koordinaten prüfen |

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
| F47 | Seepark Freiburg | 47.9830, 7.8230 | ⚠️ needs_review – Gewässerpunkt geschätzt |
| F48 | Opfinger See | 47.9740, 7.8270 | ⚠️ needs_review – Gewässerpunkt geschätzt |

## Anmerkungen

- Therme/Termalbad Koordinaten auf Gebäude/Eingang gesetzt
- Seen: Koordinaten auf plausiblen Badezugang/Gewässerpunkt gesetzt
- Bei Unsicherheit: `verified_status: "unverified"` gesetzt
- Keine Fantasiekoordinaten verwendet
