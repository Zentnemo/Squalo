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
        "address": "Moltkestraße 32, 10785 Berlin",
        "latitude": 52.5043,
        "longitude": 13.3428,
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
        "address": "Richard-Hartmann-Straße 60, 12057 Berlin",
        "latitude": 52.4559,
        "longitude": 13.4285,
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
        "district": "Reinickendorf",
        "address": "Am Plötzensee 1, 13407 Berlin",
        "latitude": 52.5435,
        "longitude": 13.3270,
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
        "address": "Seestraße 28, 13347 Berlin",
        "latitude": 52.5458,
        "longitude": 13.3478,
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
        "address": "Paul-Heyse-Straße 2a, 10407 Berlin",
        "latitude": 52.5375,
        "longitude": 13.4256,
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
        "address": "Prinzenstraße 35, 10969 Berlin",
        "latitude": 52.4963,
        "longitude": 13.4105,
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
        "address": "Krumme Straße 2, 10585 Berlin",
        "latitude": 52.5233,
        "longitude": 13.3100,
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
        "address": "Am Flughafensee, 13405 Berlin",
        "latitude": 52.5607,
        "longitude": 13.2898,
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
        "address": "Wannseebadweg 25, 14129 Berlin",
        "latitude": 52.4317,
        "longitude": 13.1544,
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
        "address": "Am Südpark 1, 13597 Berlin",
        "latitude": 52.5379,
        "longitude": 13.1914,
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
        "address": "Am Tegeler See, 13403 Berlin",
        "latitude": 52.5822,
        "longitude": 13.2900,
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
        "address": "Am Müggelsee, 12587 Berlin",
        "latitude": 52.4350,
        "longitude": 13.6483,
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
        "address": "Friedrichshagener Straße 221, 12527 Berlin",
        "latitude": 52.4450,
        "longitude": 13.6333,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Friedrichshagen+Berlin"
    },
    {
        "name": "James Simon Stadtbad",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "address": "Unter den Linden 40, 10117 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25Â°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=James+Simon+Stadtbad+Berlin"
    },
    {
        "name": "Arena Badeschiff",
        "location_type": "Outdoor",
        "district": "Mitte",
        "address": "Eiserne Bridge 1, 10179 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28Â°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Arena+Badeschiff+Berlin"
    },
    # Step 6: Next 6 locations
    {
        "name": "Schlachtensee",
        "location_type": "See",
        "district": "Zehlendorf",
        "address": "Schlachtensee, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.2000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18Â°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Schlachtensee+Berlin"
    },
    {
        "name": "Krumme Lanke",
        "location_type": "See",
        "district": "Zehlendorf",
        "address": "Krumme Lanke, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.2000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19Â°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Krumme+Lanke+Berlin"
    },
    {
        "name": "Sommerbad Humboldthain",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "address": "BÃ¶tzowstraÃŸe 32, 10178 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22Â°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Humboldthain+Berlin"
    },
    {
        "name": "Strandbad WeiÃŸensee",
        "location_type": "Strandbad",
        "district": "WeiÃŸensee",
        "address": "Am WeiÃŸensee, 13086 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23Â°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+WeiÃŸensee+Berlin"
    },
    {
        "name": "Freibad Jungfernheide / Strandbad Jungfernheide",
        "location_type": "Outdoor",
        "district": "Charlottenburg",
        "address": "JÃ¤gerallee 55, 10785 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24Â°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Jungfernheide+Berlin"
    },
    {
        "name": "Strandbad Orankesee",
        "location_type": "Strandbad",
        "district": "MÃ¼ggelheim",
        "address": "Am Orankesee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20Â°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Orankesee+Berlin"
    },
]
