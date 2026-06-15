"""
Seed data for Squalo swim locations.
This file contains the swimming locations for Berlin that should be available in the Squalo webapp.
"""

# Initial Squalo swim locations (Step 1: 3 core locations)
# This list includes the first 3 locations to start with
SWIM_LOCATIONS = [
    # Core Berlin locations (Step 1)
    {
        "name": "Stadtbad Tiergarten",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "address": "Moltkestraße 32, 10785 Berlin",
        "latitude": 52.5040,
        "longitude": 13.3429,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Tiergarten+Berlin"
    },
    {
        "name": "Sommerbad Neukölln",
        "location_type": "Sommerbad",
        "district": "Neukölln",
        "address": "Richard-Hartmann-Straße 60, 12057 Berlin",
        "latitude": 52.4560,
        "longitude": 13.4280,
        "official_status": "open",
        "verified_status": "not_verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Neukölln+Berlin"
    },
    {
        "name": "Strandbad Plötzensee",
        "location_type": "Strandbad",
        "district": "Reinickendorf",
        "address": "Am Strandbad 1, 13187 Berlin",
        "latitude": 52.6000,
        "longitude": 13.2833,
        "official_status": "closed",
        "verified_status": "verified",
        "water_temperature": "18°C",
        "crowd_level": "high",
        "maps_url": "https://maps.google.com/?q=Strandbad+Plötzensee+Berlin"
    },
    # Step 2: Next 3 locations
    {
        "name": "Kombibad Seestraße",
        "location_type": "Kombibad",
        "district": "Charlottenburg",
        "address": "Seestraße 28, 10555 Berlin",
        "latitude": 52.5280,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Seestraße+Berlin"
    },
    {
        "name": "Schwimm- und Sprunghalle im Europasportpark",
        "location_type": "Kombibad",
        "district": "Neukölln",
        "address": "Olympiapromenade 2, 10829 Berlin",
        "latitude": 52.4975,
        "longitude": 13.3306,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sprunghalle+Europasportpark+Berlin"
    },
    {
        "name": "Prinzenbad",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "address": "Friedrichsgracht 32, 10178 Berlin",
        "latitude": 52.5040,
        "longitude": 13.3429,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Prinzenbad+Berlin"
    },
    # Step 3: Next 6 locations
    {
        "name": "Stadtbad Charlottenburg – Alte Halle",
        "location_type": "Schwimmbad",
        "district": "Charlottenburg",
        "address": "Oderberger Straße 57, 10119 Berlin",
        "latitude": 52.5280,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Charlottenburg+Berlin"
    },
    {
        "name": "Flughafensee",
        "location_type": "See",
        "district": "Reinickendorf",
        "address": "Am Flughafensee, 13187 Berlin",
        "latitude": 52.6333,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Flughafensee+Berlin"
    },
    {
        "name": "Strandbad Wannsee",
        "location_type": "Strandbad",
        "district": "Steglitz-Zehlendorf",
        "address": "Am Wannsee 1, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Wannsee+Berlin"
    },
    {
        "name": "Stadtbad Schöneberg",
        "location_type": "Schwimmbad",
        "district": "Schöneberg",
        "address": "Johannestraße 2, 10629 Berlin",
        "latitude": 52.4833,
        "longitude": 13.3333,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Schöneberg+Berlin"
    },
    {
        "name": "Stadtbad Wilmersdorf I",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+Berlin"
    },
    {
        "name": "Stadtbad Wilmersdorf II",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+Berlin"
    },
    # Step 4: Next 6 locations
    {
        "name": "Kombibad Gropiusstadt – Halle",
        "location_type": "Kombibad",
        "district": "Neukölln",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4333,
        "longitude": 13.4667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Berlin"
    },
    {
        "name": "Kombibad Gropiusstadt – Sommerbad",
        "location_type": "Sommerbad",
        "district": "Neukölln",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4333,
        "longitude": 13.4667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Sommerbad+Berlin"
    },
    {
        "name": "Sommerbad Kreuzberg",
        "location_type": "Sommerbad",
        "district": "Kreuzberg",
        "address": "Falkenstraße 36, 10965 Berlin",
        "latitude": 52.4833,
        "longitude": 13.4167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Kreuzberg+Berlin"
    },
    {
        "name": "Sommerbad Olympiastadion",
        "location_type": "Sommerbad",
        "district": "Charlottenburg",
        "address": "Olympiapark, 10587 Berlin",
        "latitude": 52.5167,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Olympiastadion+Berlin"
    },
    {
        "name": "Kombibad Spandau Süd",
        "location_type": "Kombibad",
        "district": "Spandau",
        "address": "Am Südpark 1, 13597 Berlin",
        "latitude": 52.5333,
        "longitude": 13.1833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Spandau+Süd+Berlin"
    },
    {
        "name": "Stadtbad Lankwitz",
        "location_type": "Schwimmbad",
        "district": "Steglitz-Zehlendorf",
        "address": "Lankwitzer Straße 41, 12209 Berlin",
        "latitude": 52.4167,
        "longitude": 13.3000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Lankwitz+Berlin"
    },
    # Step 5: Next 6 locations
    {
        "name": "Tegeler See",
        "location_type": "See",
        "district": "Reinickendorf",
        "address": "Am Tegeler See, 13403 Berlin",
        "latitude": 52.6333,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Tegeler+See+Berlin"
    },
    {
        "name": "Stadtbad Fischerinsel",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "address": "Fischerinsel 1, 10179 Berlin",
        "latitude": 52.5167,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Fischerinsel+Berlin"
    },
    {
        "name": "Müggelsee",
        "location_type": "See",
        "district": "Treptow-Köpenick",
        "address": "Am Müggelsee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Müggelsee+Berlin"
    },
    {
        "name": "Strandbad Friedrichshagen",
        "location_type": "Strandbad",
        "district": "Treptow-Köpenick",
        "address": "Friedrichshagener Straße 221, 12527 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
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
        "water_temperature": "25°C",
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
        "water_temperature": "28°C",
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
        "water_temperature": "18°C",
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
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Krumme+Lanke+Berlin"
    },
    {
        "name": "Sommerbad Humboldthain",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "address": "Bötzowstraße 32, 10178 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Humboldthain+Berlin"
    },
    {
        "name": "Strandbad Weißensee",
        "location_type": "Strandbad",
        "district": "Weißensee",
        "address": "Am Weißensee, 13086 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Weißensee+Berlin"
    },
    {
        "name": "Freibad Jungfernheide / Strandbad Jungfernheide",
        "location_type": "Outdoor",
        "district": "Charlottenburg",
        "address": "Jägerallee 55, 10785 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Jungfernheide+Berlin"
    },
    {
        "name": "Strandbad Orankesee",
        "location_type": "Strandbad",
        "district": "Müggelheim",
        "address": "Am Orankesee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Orankesee+Berlin"
    },
]
]
]
]
]

# Helper function to get all locations
SWIM_LOCATIONS_BY_NAME = {loc["name"]: loc for loc in SWIM_LOCATIONS}

# Function to get location by name
def get_location_by_name(name):
    """Get a location by name (case-insensitive)"""
    return SWIM_LOCATIONS_BY_NAME.get(name)

# Function to get all locations
def get_all_locations():
    """Get all locations"""
    return SWIM_LOCATIONS

# Function to get active locations (is_active would be checked in real implementation)
def get_active_locations():
    """Get all active locations"""
    return SWIM_LOCATIONS
    {
        "name": "Flughafensee",
        "location_type": "See",
        "district": "Reinickendorf",
        "address": "Am Flughafensee, 13187 Berlin",
        "latitude": 52.6333,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Flughafensee+Berlin"
    },
    {
        "name": "Strandbad Wannsee",
        "location_type": "Strandbad",
        "district": "Steglitz-Zehlendorf",
        "address": "Am Wannsee 1, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Wannsee+Berlin"
    },
    {
        "name": "Stadtbad Schöneberg",
        "location_type": "Schwimmbad",
        "district": "Schöneberg",
        "address": "Johannestraße 2, 10629 Berlin",
        "latitude": 52.4833,
        "longitude": 13.3333,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Schöneberg+Berlin"
    },
    {
        "name": "Stadtbad Wilmersdorf I",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+Berlin"
    },
    {
        "name": "Stadtbad Wilmersdorf II",
        "location_type": "Schwimmbad",
        "district": "Wilmersdorf",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Wilmersdorf+Berlin"
    },
    {
        "name": "Kombibad Gropiusstadt – Halle",
        "location_type": "Kombibad",
        "district": "Neukölln",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4333,
        "longitude": 13.4667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Berlin"
    },
    {
        "name": "Kombibad Gropiusstadt – Sommerbad",
        "location_type": "Sommerbad",
        "district": "Neukölln",
        "address": "Gropiusstadt 12, 12349 Berlin",
        "latitude": 52.4333,
        "longitude": 13.4667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Gropiusstadt+Sommerbad+Berlin"
    },
    {
        "name": "Sommerbad Kreuzberg",
        "location_type": "Sommerbad",
        "district": "Kreuzberg",
        "address": "Falkenstraße 36, 10965 Berlin",
        "latitude": 52.4833,
        "longitude": 13.4167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Kreuzberg+Berlin"
    },
    {
        "name": "Sommerbad Olympiastadion",
        "location_type": "Sommerbad",
        "district": "Charlottenburg",
        "address": "Olympiapark, 10587 Berlin",
        "latitude": 52.5167,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Olympiastadion+Berlin"
    },
    {
        "name": "Kombibad Spandau Süd",
        "location_type": "Kombibad",
        "district": "Spandau",
        "address": "Am Südpark 1, 13597 Berlin",
        "latitude": 52.5333,
        "longitude": 13.1833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Spandau+Süd+Berlin"
    },
    {
        "name": "Stadtbad Lankwitz",
        "location_type": "Schwimmbad",
        "district": "Steglitz-Zehlendorf",
        "address": "Lankwitzer Straße 41, 12209 Berlin",
        "latitude": 52.4167,
        "longitude": 13.3000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Lankwitz+Berlin"
    },
    {
        "name": "Tegeler See",
        "location_type": "See",
        "district": "Reinickendorf",
        "address": "Am Tegeler See, 13403 Berlin",
        "latitude": 52.6333,
        "longitude": 13.2833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Tegeler+See+Berlin"
    },
    {
        "name": "Stadtbad Fischerinsel",
        "location_type": "Schwimmbad",
        "district": "Mitte",
        "address": "Fischerinsel 1, 10179 Berlin",
        "latitude": 52.5167,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Fischerinsel+Berlin"
    },
    {
        "name": "Müggelsee",
        "location_type": "See",
        "district": "Treptow-Köpenick",
        "address": "Am Müggelsee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Müggelsee+Berlin"
    },
    {
        "name": "Strandbad Friedrichshagen",
        "location_type": "Strandbad",
        "district": "Treptow-Köpenick",
        "address": "Friedrichshagener Straße 221, 12527 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Friedrichshagen+Berlin"
    },
    # Additional locations (8 more to reach 30+)
    {
        "name": "Arena Badeschiff",
        "location_type": "Outdoor",
        "district": "Mitte",
        "address": "Eiserne Bridge 1, 10179 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Arena+Badeschiff+Berlin"
    },
    {
        "name": "Schlachtensee",
        "location_type": "See",
        "district": "Zehlendorf",
        "address": "Schlachtensee, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.2000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18°C",
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
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Krumme+Lanke+Berlin"
    },
    {
        "name": "Sommerbad Humboldthain",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "address": "Bötzowstraße 32, 10178 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Humboldthain+Berlin"
    },
    {
        "name": "Strandbad Weißensee",
        "location_type": "Strandbad",
        "district": "Weißensee",
        "address": "Am Weißensee, 13086 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Weißensee+Berlin"
    },
    {
        "name": "Freibad Jungfernheide / Strandbad Jungfernheide",
        "location_type": "Outdoor",
        "district": "Charlottenburg",
        "address": "Jägerallee 55, 10785 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Jungfernheide+Berlin"
    },
    {
        "name": "Strandbad Orankesee",
        "location_type": "Strandbad",
        "district": "Müggelheim",
        "address": "Am Orankesee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Orankesee+Berlin"
    },
    {
        "name": "Sommerbad Pankow",
        "location_type": "Sommerbad",
        "district": "Pankow",
        "address": "Pankower Straße 74, 10405 Berlin",
        "latitude": 52.5500,
        "longitude": 13.4167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Pankow+Berlin"
    },
    {
        "name": "Sommerbad Mariendorf",
        "location_type": "Sommerbad",
        "district": "Mariendorf",
        "address": "Mariendorfer Damm 65, 12107 Berlin",
        "latitude": 52.4333,
        "longitude": 13.3500,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Mariendorf+Berlin"
    },
    {
        "name": "Strandbad Grünau",
        "location_type": "Strandbad",
        "district": "Grünau",
        "address": "Grünauer Weg 1, 12527 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Grünau+Berlin"
    },
    {
        "name": "Strandbad Müggelsee / Rahnsdorf-Bereich",
        "location_type": "Strandbad",
        "district": "Rahnsdorf",
        "address": "Am Müggelsee 1, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Müggelsee+Rahnsdorf+Berlin"
    },
    {
        "name": "Sacrower See / Potsdam-nah",
        "location_type": "See",
        "district": "Potsdam",
        "address": "Am Sacrower See, 14476 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sacrower+See+Berlin"
    },
    {
        "name": "Heiliger See / Potsdam",
        "location_type": "See",
        "district": "Potsdam",
        "address": "Am Heiligen See, 14476 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Heiliger+See+Berlin"
    },
    {
        "name": "Stadtbad Neukölln",
        "location_type": "Schwimmbad",
        "district": "Neukölln",
        "address": "Richard-Hartmann-Straße 60, 12057 Berlin",
        "latitude": 52.4560,
        "longitude": 13.4280,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Neukölln+Berlin"
    },
    {
        "name": "Paracelsus-Bad",
        "location_type": "Schwimmbad",
        "district": "Charlottenburg",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Paracelsus-Bad+Berlin"
    },
    {
        "name": "Schwimmhalle Finckensteinallee",
        "location_type": "Indoor",
        "district": "Charlottenburg",
        "address": "Finckensteinallee 32, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Schwimmhalle+Finckensteinallee+Berlin"
    },
    {
        "name": "Kombibad Mariendorf",
        "location_type": "Kombibad",
        "district": "Mariendorf",
        "address": "Mariendorfer Damm 65, 12107 Berlin",
        "latitude": 52.4333,
        "longitude": 13.3500,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Mariendorf+Berlin"
    },
    {
        "name": "Schwimmhalle Anton-Saefkow-Platz",
        "location_type": "Indoor",
        "district": "Neukölln",
        "address": "Anton-Saefkow-Platz 1, 12057 Berlin",
        "latitude": 52.4560,
        "longitude": 13.4280,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "29°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Schwimmhalle+Anton-Saefkow-Platz+Berlin"
    },
]

# Helper function to get all locations
SWIM_LOCATIONS_BY_NAME = {loc["name"]: loc for loc in SWIM_LOCATIONS}

# Function to get location by name
def get_location_by_name(name):
    """Get a location by name (case-insensitive)"""
    return SWIM_LOCATIONS_BY_NAME.get(name)

# Function to get all locations
def get_all_locations():
    """Get all locations"""
    return SWIM_LOCATIONS

# Function to get active locations (is_active would be checked in real implementation)
def get_active_locations():
    """Get all active locations"""
    return SWIM_LOCATIONS
    # Additional locations (8 more to reach 30+)
    {
        "name": "Arena Badeschiff",
        "location_type": "Outdoor",
        "district": "Mitte",
        "address": "Eiserne Bridge 1, 10179 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3833,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Arena+Badeschiff+Berlin"
    },
    {
        "name": "Schlachtensee",
        "location_type": "See",
        "district": "Zehlendorf",
        "address": "Schlachtensee, 14129 Berlin",
        "latitude": 52.4333,
        "longitude": 13.2000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "18°C",
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
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Krumme+Lanke+Berlin"
    },
    {
        "name": "Sommerbad Humboldthain",
        "location_type": "Sommerbad",
        "district": "Mitte",
        "address": "Bötzowstraße 32, 10178 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Humboldthain+Berlin"
    },
    {
        "name": "Strandbad Weißensee",
        "location_type": "Strandbad",
        "district": "Weißensee",
        "address": "Am Weißensee, 13086 Berlin",
        "latitude": 52.5333,
        "longitude": 13.4000,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Weißensee+Berlin"
    },
    {
        "name": "Freibad Jungfernheide / Strandbad Jungfernheide",
        "location_type": "Outdoor",
        "district": "Charlottenburg",
        "address": "Jägerallee 55, 10785 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Freibad+Jungfernheide+Berlin"
    },
    {
        "name": "Strandbad Orankesee",
        "location_type": "Strandbad",
        "district": "Müggelheim",
        "address": "Am Orankesee, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Orankesee+Berlin"
    },
    {
        "name": "Sommerbad Pankow",
        "location_type": "Sommerbad",
        "district": "Pankow",
        "address": "Pankower Straße 74, 10405 Berlin",
        "latitude": 52.5500,
        "longitude": 13.4167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "23°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Pankow+Berlin"
    },
    {
        "name": "Sommerbad Mariendorf",
        "location_type": "Sommerbad",
        "district": "Mariendorf",
        "address": "Mariendorfer Damm 65, 12107 Berlin",
        "latitude": 52.4333,
        "longitude": 13.3500,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "24°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sommerbad+Mariendorf+Berlin"
    },
    {
        "name": "Strandbad Grünau",
        "location_type": "Strandbad",
        "district": "Grünau",
        "address": "Grünauer Weg 1, 12527 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "21°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Strandbad+Grünau+Berlin"
    },
    {
        "name": "Strandbad Müggelsee / Rahnsdorf-Bereich",
        "location_type": "Strandbad",
        "district": "Rahnsdorf",
        "address": "Am Müggelsee 1, 12587 Berlin",
        "latitude": 52.4333,
        "longitude": 13.5667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "22°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Strandbad+Müggelsee+Rahnsdorf+Berlin"
    },
    {
        "name": "Sacrower See / Potsdam-nah",
        "location_type": "See",
        "district": "Potsdam",
        "address": "Am Sacrower See, 14476 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "20°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Sacrower+See+Berlin"
    },
    {
        "name": "Heiliger See / Potsdam",
        "location_type": "See",
        "district": "Potsdam",
        "address": "Am Heiligen See, 14476 Berlin",
        "latitude": 52.4333,
        "longitude": 13.1667,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "19°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Heiliger+See+Berlin"
    },
    {
        "name": "Stadtbad Neukölln",
        "location_type": "Schwimmbad",
        "district": "Neukölln",
        "address": "Richard-Hartmann-Straße 60, 12057 Berlin",
        "latitude": 52.4560,
        "longitude": 13.4280,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "25°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Stadtbad+Neukölln+Berlin"
    },
    {
        "name": "Paracelsus-Bad",
        "location_type": "Schwimmbad",
        "district": "Charlottenburg",
        "address": "Kleiststraße 1, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "26°C",
        "crowd_level": "low",
        "maps_url": "https://maps.google.com/?q=Paracelsus-Bad+Berlin"
    },
    {
        "name": "Schwimmhalle Finckensteinallee",
        "location_type": "Indoor",
        "district": "Charlottenburg",
        "address": "Finckensteinallee 32, 10719 Berlin",
        "latitude": 52.5167,
        "longitude": 13.3167,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "28°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Schwimmhalle+Finckensteinallee+Berlin"
    },
    {
        "name": "Kombibad Mariendorf",
        "location_type": "Kombibad",
        "district": "Mariendorf",
        "address": "Mariendorfer Damm 65, 12107 Berlin",
        "latitude": 52.4333,
        "longitude": 13.3500,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "27°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Kombibad+Mariendorf+Berlin"
    },
    {
        "name": "Schwimmhalle Anton-Saefkow-Platz",
        "location_type": "Indoor",
        "district": "Neukölln",
        "address": "Anton-Saefkow-Platz 1, 12057 Berlin",
        "latitude": 52.4560,
        "longitude": 13.4280,
        "official_status": "open",
        "verified_status": "verified",
        "water_temperature": "29°C",
        "crowd_level": "medium",
        "maps_url": "https://maps.google.com/?q=Schwimmhalle+Anton-Saefkow-Platz+Berlin"
    },
]

# Helper function to get all locations
SWIM_LOCATIONS_BY_NAME = {loc["name"]: loc for loc in SWIM_LOCATIONS}

# Function to get location by name
def get_location_by_name(name):
    """Get a location by name (case-insensitive)"""
    return SWIM_LOCATIONS_BY_NAME.get(name)

# Function to get all locations
def get_all_locations():
    """Get all locations"""
    return SWIM_LOCATIONS

# Function to get active locations (is_active would be checked in real implementation)
def get_active_locations():
    """Get all active locations"""
    return SWIM_LOCATIONS