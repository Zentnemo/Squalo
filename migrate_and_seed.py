"""Migration script: create Product, FeedPost, TrainingNote tables + seed 4 shop products."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'squalo.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Create Product table if not exists (with all new fields)
c.execute("""CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    price_label TEXT,
    variant_label TEXT,
    note TEXT,
    image_path TEXT,
    button_label TEXT DEFAULT 'Anfragen',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME,
    price REAL,
    external_url TEXT
)""")
print("Product table ensured.")

# 2. Create FeedPost table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS feed_post (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    text TEXT,
    image_path TEXT,
    is_pinned BOOLEAN DEFAULT 0,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id)
)""")
print("FeedPost table ensured.")

# 3. Create TrainingNote table if not exists
c.execute("""CREATE TABLE IF NOT EXISTS training_note (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    text TEXT,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id)
)""")
print("TrainingNote table ensured.")

# 5. Clear old dummy products and seed the 4 real ones
c.execute("DELETE FROM product WHERE name = 'Squalo Swim Cap'")
c.execute("SELECT COUNT(*) FROM product")
count = c.fetchone()[0]
print(f"Current product count after cleanup: {count}")

if count == 0:
    products = [
        (
            "Arena Cobra Ultra Swipe Schwimmbrille",
            "Basics",
            "Hochwertige Wettkampf-Schwimmbrille mit Anti-Beschlag-Beschichtung. Ideal für regelmäßiges Training und Wettkämpfe.",
            "ca. 45–70 €",
            "Klar / Bunt",
            "Verschiedene Farben verfügbar. Preis kann je nach Händler variieren.",
            "Anfragen"
        ),
        (
            "Kurze Schwimmflossen",
            "Trainingsausrüstung",
            "Kurze Flossen für effizientes Beintraining im Pool. Verbessern Technik und Ausdauer.",
            "ca. 20–35 €",
            "S / M / L",
            "Silikon, geeignet für Pool-Training.",
            "Anfragen"
        ),
        (
            "Squalo Merch-Handtuch",
            "Squalo Merch",
            "Großes Schwimmtuch mit Squalo-Logo. Perfekt nach dem Training.",
            "Preis folgt",
            None,
            "Bald verfügbar – INTERESSE VORMERKEN!",
            "Interesse vormerken"
        ),
        (
            "Squalo T-Shirt",
            "Squalo Merch",
            "Cotton-Blend T-Shirt mit Squalo-Design. Für Training und Alltag.",
            "Preis folgt",
            None,
            "Bald verfügbar – INTERESSE VORMERKEN!",
            "Interesse vormerken"
        ),
    ]
    for name, cat, desc, price_label, variant, note, btn_label in products:
        c.execute(
            """INSERT INTO product (name, category, description, price_label, variant_label, note, button_label, is_active, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1, datetime('now'))""",
            (name, cat, desc, price_label, variant, note, btn_label)
        )
    print(f"Seeded {len(products)} products.")
else:
    print("Products already exist, skipping seed.")

conn.commit()
conn.close()
print("Migration + seed complete.")
