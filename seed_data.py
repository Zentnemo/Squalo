"""
Seed data for Squalo swim locations.
This file contains the swimming locations for Berlin that should be available in the Squalo webapp.
"""

# Initial Squalo swim locations (Step 1: 3 core locations)
# This list includes the first 3 locations to start with
SWIM_LOCATIONS = [
    # ── 1 ──
    {
        "name": "Stadtbad Tiergarten",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Seydlitzstraße 7, 10557 Berlin",
        "latitude": 52.527429,
        "longitude": 13.359621,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Tiergarten+Berlin"
    },
    # ── 2 ──
    {
        "name": "Sommerbad Neukölln",
        "location_type": "Sommerbad",
        "district": "Neukölln",
        "city": "Berlin",
        "address": "Columbiadamm 160, 10965 Berlin",
        "latitude": 52.479588,
        "longitude": 13.415077,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Neukölln+Berlin"
    },
    # ── 3 ──
    {
        "name": "Strandbad Plötzensee",
        "location_type": "Strandbad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Nordufer 26, 13351 Berlin",
        "latitude": 52.54333,
        "longitude": 13.32856,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Plötzensee+Berlin"
    },
    # ── 4 ──
    {
        "name": "Kombibad Seestraße",
        "location_type": "Kombibad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Seestraße 80, 13347 Berlin",
        "latitude": 52.5571194,
        "longitude": 13.3634217,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Seestraße+Berlin"
    },
    # ── 5 ──
    {
        "name": "Schwimm- und Sprunghalle im Europasportpark",
        "location_type": "Kombibad",
        "district": "Pankow",
        "city": "Berlin",
        "address": "Paul-Heyse-Straße 2a, 10407 Berlin",
        "latitude": 52.529191,
        "longitude": 13.452652,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Europasportpark+Berlin+Schwimmhalle"
    },
    # ── 6 ──
    {
        "name": "Prinzenbad",
        "location_type": "Sommerbad",
        "district": "Friedrichshain-Kreuzberg",
        "city": "Berlin",
        "address": "Prinzenstraße 35, 10969 Berlin",
        "latitude": 52.497600,
        "longitude": 13.402650,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Prinzenbad+Kreuzberg+Berlin"
    },
    # ── 7 ──
    {
        "name": "Stadtbad Charlottenburg – Alte Halle",
        "location_type": "Schwimmbad",
        "district": "Charlottenburg",
        "city": "Berlin",
        "address": "Krumme Straße 2, 10585 Berlin",
        "latitude": 52.514526,
        "longitude": 13.308833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Charlottenburg+Alte+Halle+Berlin"
    },
    # ── 8 ──
    {
        "name": "Flughafensee",
        "location_type": "See",
        "district": "Reinickendorf",
        "city": "Berlin",
        "address": "Am Flughafensee, 13405 Berlin",
        "latitude": 52.567773,
        "longitude": 13.285443,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Flughafensee+Berlin"
    },
    # ── 9 ──
    {
        "name": "Strandbad Wannsee",
        "location_type": "Strandbad",
        "district": "Steglitz-Zehlendorf",
        "city": "Berlin",
        "address": "Wannseebadweg 25, 14129 Berlin",
        "latitude": 52.438169,
        "longitude": 13.178038,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "high",
        "maps_url": "https://maps.google.com/?q=Strandbad+Wannsee+Berlin"
    },
    # ── 10 ──
    {
        "name": "Stadtbad Schöneberg",
        "location_type": "Schwimmbad",
        "district": "Schöneberg",
        "city": "Berlin",
        "address": "Hauptstraße 60–62, 10827 Berlin",
        "latitude": 52.4838,
        "longitude": 13.3520,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Schöneberg+Berlin"
    },
    # ── 11 ──
    {
        "name": "Stadtbad Wilmersdorf I",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "city": "Berlin",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.4908,
        "longitude": 13.3233,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+I+Berlin"
    },
    # ── 12 ──
    {
        "name": "Stadtbad Wilmersdorf II",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "city": "Berlin",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.4913,
        "longitude": 13.3245,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+II+Berlin"
    },
    # ── 13 ──
    {
        "name": "Kombibad Gropiusstadt – Halle",
        "location_type": "Kombibad",
        "district": "Neukölln",
        "city": "Berlin",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4250,
        "longitude": 13.4639,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Halle+Berlin"
    },
    # ── 14 ──
    {
        "name": "Kombibad Gropiusstadt – Sommerbad",
        "location_type": "Sommerbad",
        "district": "Neukölln",
        "city": "Berlin",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4240,
        "longitude": 13.4645,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Sommerbad+Berlin"
    },
    # ── 15 ──
    {
        "name": "Sommerbad Kreuzberg",
        "location_type": "Sommerbad",
        "district": "Friedrichshain-Kreuzberg",
        "city": "Berlin",
        "address": "Falkenstraße 36, 10965 Berlin",
        "latitude": 52.4827,
        "longitude": 13.3950,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Kreuzberg+Berlin"
    },
    # ── 16 ──
    {
        "name": "Sommerbad Olympiastadion",
        "location_type": "Sommerbad",
        "district": "Charlottenburg-Wilmersdorf",
        "city": "Berlin",
        "address": "Olympischer Platz 1, 14053 Berlin",
        "latitude": 52.5214,
        "longitude": 13.2545,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Olympiastadion+Berlin"
    },
    # ── 17 ──
    {
        "name": "Kombibad Spandau Süd",
        "location_type": "Kombibad",
        "district": "Spandau",
        "city": "Berlin",
        "address": "Am Südpark 1, 13597 Berlin",
        "latitude": 52.518209,
        "longitude": 13.18840606,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Spandau+S%C3%BCd+Berlin"
    },
    # ── 18 ──
    {
        "name": "Stadtbad Lankwitz",
        "location_type": "Schwimmbad",
        "district": "Steglitz-Zehlendorf",
        "city": "Berlin",
        "address": "Lankwitzer Straße 41, 12209 Berlin",
        "latitude": 52.4273,
        "longitude": 13.3463,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Lankwitz+Berlin"
    },
    # ── 19 ──
    {
        "name": "Tegeler See",
        "location_type": "See",
        "district": "Reinickendorf",
        "city": "Berlin",
        "address": "Greenwichpromenade, 13505 Berlin",
        "latitude": 52.574558,
        "longitude": 13.255002,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Tegeler+See+Berlin"
    },
    # ── 20 ──
    {
        "name": "Stadtbad Fischerinsel",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Fischerinsel 1, 10179 Berlin",
        "latitude": 52.5112,
        "longitude": 13.4055,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Fischerinsel+Berlin"
    },
    # ── 21 ──
    {
        "name": "Müggelsee",
        "location_type": "See",
        "district": "Treptow-Köpenick",
        "city": "Berlin",
        "address": "Müggelsee – Südufer (Rübezahl), 12587 Berlin",
        "latitude": 52.4365,
        "longitude": 13.6490,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=M%C3%BCggelsee+Berlin"
    },
    # ── 22 ──
    {
        "name": "Strandbad Friedrichshagen",
        "location_type": "Strandbad",
        "district": "Treptow-Köpenick",
        "city": "Berlin",
        "address": "Friedrichshagener Straße 221, 12527 Berlin",
        "latitude": 52.4450,
        "longitude": 13.6333,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Friedrichshagen+Berlin"
    },
    # ── 23 ──
    {
        "name": "James Simon Stadtbad",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Gartenstraße 5, 10115 Berlin",
        "latitude": 52.5315,
        "longitude": 13.3850,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=James+Simon+Stadtbad+Berlin"
    },
    # ── 24 ──
    {
        "name": "Arena Badeschiff",
        "location_type": "Sommerbad",
        "district": "Friedrichshain-Kreuzberg",
        "city": "Berlin",
        "address": "Eichenstraße 4, 12435 Berlin",
        "latitude": 52.497633,
        "longitude": 13.453667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Arena+Badeschiff+Berlin"
    },
    # ── 25 ──
    {
        "name": "Schlachtensee",
        "location_type": "See",
        "district": "Steglitz-Zehlendorf",
        "city": "Berlin",
        "address": "Schlachtensee – Strandbad, 14129 Berlin",
        "latitude": 52.4425,
        "longitude": 13.2100,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Schlachtensee+Berlin"
    },
    # ── 26 ──
    {
        "name": "Krumme Lanke",
        "location_type": "See",
        "district": "Steglitz-Zehlendorf",
        "city": "Berlin",
        "address": "Krumme Lanke – Hauptzugang, 14129 Berlin",
        "latitude": 52.451548,
        "longitude": 13.231906,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Krumme+Lanke+Berlin"
    },
    # ── 27 ──
    {
        "name": "Sommerbad Humboldthain",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Bötzowstraße 32, 10178 Berlin",
        "latitude": 52.5461,
        "longitude": 13.3880,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Humboldthain+Berlin"
    },
    # ── 28 ──
    {
        "name": "Strandbad Weißensee",
        "location_type": "Strandbad",
        "district": "Weißensee",
        "city": "Berlin",
        "address": "Am Weißensee, 13086 Berlin",
        "latitude": 52.5520,
        "longitude": 13.4700,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Wei%C3%9Fensee+Berlin"
    },
    # ── 29 ──
    {
        "name": "Freibad Jungfernheide / Strandbad Jungfernheide",
        "location_type": "Strandbad",
        "district": "Charlottenburg-Wilmersdorf",
        "city": "Berlin",
        "address": "Jägerallee 55, 10785 Berlin",
        "latitude": 52.5270,
        "longitude": 13.2830,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Jungfernheide+Berlin"
    },
    # ── 30 ──
    {
        "name": "Strandbad Orankesee",
        "location_type": "Strandbad",
        "district": "Lichtenberg",
        "city": "Berlin",
        "address": "Am Orankesee, 12587 Berlin",
        "latitude": 52.5480,
        "longitude": 13.5290,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Orankesee+Berlin"
    },
    # ── 31 ── Steingarten am Plötzensee – freie Badestelle (Ostufer)
    {
        "name": "Steingarten am Plötzensee",
        "location_type": "Badestelle",
        "district": "Mitte",
        "city": "Berlin",
        "address": "Am Plötzensee (Ostufer), 13355 Berlin",
        "latitude": 52.5410,
        "longitude": 13.3320,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Steingarten+am+Pl%C3%B6tzensee+Berlin"
    },
    # ── 32 ── Badestelle Grünau – freie Badestelle an der Dahme
    {
        "name": "Badestelle Grünau",
        "location_type": "Badestelle",
        "district": "Treptow-Köpenick",
        "city": "Berlin",
        "address": "Dahmeufer Nähe S Grünau, 12527 Berlin",
        "latitude": 52.4130,
        "longitude": 13.5770,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Badestelle+Gr%C3%BCnau+Dahme+Berlin"
    },
    # ── 33 ── Strandbad Schmöckwitz / Zeuthener See
    {
        "name": "Strandbad Schmöckwitz",
        "location_type": "Strandbad",
        "district": "Treptow-Köpenick",
        "city": "Berlin",
        "address": "Schmöckwitzwerder 1, 12527 Berlin",
        "latitude": 52.3770,
        "longitude": 13.6880,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Schm%C3%B6ckwitz+Berlin"
    },
    # ── 34 ── Biesdorfer Baggersee – freier Badesee in Marzahn
    {
        "name": "Biesdorfer Baggersee",
        "location_type": "See",
        "district": "Marzahn-Hellersdorf",
        "city": "Berlin",
        "address": "Am Biesdorfer Baggersee, 12683 Berlin",
        "latitude": 52.5090,
        "longitude": 13.5600,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Biesdorfer+Baggersee+Berlin"
    },
    # ── 35 ── Paracelsus-Bad – Hallenbad in Reinickendorf
    {
        "name": "Paracelsus-Bad",
        "location_type": "Schwimmbad",
        "district": "Reinickendorf",
        "city": "Berlin",
        "address": "Paracelsusstraße 15, 13409 Berlin",
        "latitude": 52.5642,
        "longitude": 13.3523,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Paracelsus-Bad+Berlin"
    },
    # ── 36 ── Stadtbad Neukölln (Hallenbad)
    {
        "name": "Stadtbad Neukölln",
        "location_type": "Schwimmbad",
        "district": "Neukölln",
        "city": "Berlin",
        "address": "Ganghoferstraße 3–5, 12043 Berlin",
        "latitude": 52.4760,
        "longitude": 13.4390,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Neuk%C3%B6lln+Berlin"
    },

    # ── Freiburg und Umgebung ──
    {
        "name": "Westbad Freiburg",
        "location_type": "Schwimmbad",
        "district": "Südstadt",
        "city": "Freiburg",
        "address": "Bissierstraße 44, 79098 Freiburg",
        "latitude": 47.9845,
        "longitude": 7.8390,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Westbad+Freiburg"
    },
    {
        "name": "Faulerbad Freiburg",
        "location_type": "Schwimmbad",
        "district": "Herdern",
        "city": "Freiburg",
        "address": "Engelberger Straße 48, 79106 Freiburg",
        "latitude": 47.9887,
        "longitude": 7.8537,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Faulerbad+Freiburg"
    },
    {
        "name": "Stadtbad Haslach Freiburg",
        "location_type": "Schwimmbad",
        "district": "Haslach",
        "city": "Freiburg",
        "address": "Bergstraße 35, 79115 Freiburg",
        "latitude": 48.0070,
        "longitude": 7.8430,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Haslach+Freiburg"
    },
    {
        "name": "Schwimmbad Merzhausen",
        "location_type": "Schwimmbad",
        "district": "Merzhausen",
        "city": "Freiburg",
        "address": "Waltenweißlerstraße 42, 79100 Freiburg",
        "latitude": 47.9630,
        "longitude": 7.8340,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Schwimmbad+Merzhausen"
    },
    {
        "name": "Schwimmbad Gundelfingen",
        "location_type": "Schwimmbad",
        "district": "Gundelfingen",
        "city": "Freiburg",
        "address": "Mühletalstraße 40, 79199 Gundelfingen",
        "latitude": 48.0020,
        "longitude": 7.8720,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Schwimmbad+Gundelfingen"
    },
    {
        "name": "MACH'BLAU Denzlingen",
        "location_type": "Schwimmbad",
        "district": "Denzlingen",
        "city": "Freiburg",
        "address": "Bahnhofstraße 24, 79311 Denzlingen",
        "latitude": 48.0060,
        "longitude": 7.8840,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=MACH+BLAU+Denzlingen"
    },
    {
        "name": "Freibad Emmendingen",
        "location_type": "Sommerbad",
        "district": "Emmendingen",
        "city": "Emmendingen",
        "address": "Im Mais 1, 79312 Emmendingen",
        "latitude": 48.1210,
        "longitude": 7.8510,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Emmendingen"
    },
    {
        "name": "Freibad Teningen",
        "location_type": "Sommerbad",
        "district": "Teningen",
        "city": "Emmendingen",
        "address": "Hardstraße 20, 79331 Teningen",
        "latitude": 48.1290,
        "longitude": 7.8830,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Freibad+Teningen"
    },
    {
        "name": "Vita Classica Therme Bad Krozingen",
        "location_type": "Therme",
        "district": "Bad Krozingen",
        "city": "Bad Krozingen",
        "address": "Rahmstraße 8, 79189 Bad Krozingen",
        "latitude": 47.9186,
        "longitude": 7.6970,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "34°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Vita+Classica+Therme+Bad+Krozingen"
    },
    {
        "name": "Eugen-Keidel-Bad Freiburg",
        "location_type": "Therme",
        "district": "Haslach",
        "city": "Freiburg",
        "address": "Höllsteig 40, 79111 Freiburg",
        "latitude": 47.9980,
        "longitude": 7.8540,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "34°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Eugen+Keidel+Bad+Freiburg"
    },
    {
        "name": "Seepark Freiburg",
        "location_type": "See",
        "district": "Mooswald",
        "city": "Freiburg",
        "address": "B31, 79111 Freiburg",
        "latitude": 47.9830,
        "longitude": 7.8230,
        "official_status": "open",
        "verified_status": "unverified",
        "water_temperature": "21°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Seepark+Freiburg"
    },
    {
        "name": "Opfinger See",
        "location_type": "See",
        "district": "Opfingen",
        "city": "Freiburg",
        "address": "Am Opfinger See, 79112 Freiburg",
        "latitude": 47.9740,
        "longitude": 7.8270,
        "official_status": "open",
        "verified_status": "unverified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Opfinger+See+Freiburg"
    },
    # ── Neu: Sommerbad Wuhlheide ──
    {
        "name": "Sommerbad Wuhlheide",
        "location_type": "Sommerbad",
        "district": "Treptow-Köpenick",
        "city": "Berlin",
        "address": "Treskowallee 211, 12459 Berlin",
        "latitude": 52.4704336,
        "longitude": 13.5197167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Wuhlheide+Berlin"
    },
    # ── Neu: Schwimmhalle Ernst-Thälmann-Park ──
    {
        "name": "Schwimmhalle Ernst-Thälmann-Park",
        "location_type": "Schwimmbad",
        "district": "Pankow",
        "city": "Berlin",
        "address": "Lilli-Henoch-Straße 20, 10405 Berlin",
        "latitude": 52.540971,
        "longitude": 13.433781,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Schwimmhalle+Ernst-Thälmann-Park+Berlin"
    },
]
