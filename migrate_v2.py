"""Safe migration: add new Booking columns + create AppSetting table."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'squalo.db')
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Check existing booking columns
c.execute("PRAGMA table_info(booking)")
existing = {row[1] for row in c.fetchall()}
print(f"Existing booking columns: {existing}")

# 2. Add new columns to booking table
new_cols = {
    'priority_type': "TEXT DEFAULT 'balanced'",
    'date_option_1': 'TEXT',
    'time_option_1': 'TEXT',
    'date_option_2': 'TEXT',
    'time_option_2': 'TEXT',
    'date_option_3': 'TEXT',
    'time_option_3': 'TEXT',
    'confirmed_date': 'TEXT',
    'confirmed_time': 'TEXT',
}
for col, dtype in new_cols.items():
    if col not in existing:
        print(f"Adding column: {col}")
        c.execute(f"ALTER TABLE booking ADD COLUMN {col} {dtype}")
    else:
        print(f"Column exists: {col}")

# 3. Create app_setting table
c.execute("""CREATE TABLE IF NOT EXISTS app_setting (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT
)""")
print("AppSetting table ensured.")

# 4. Set default notification email
c.execute("SELECT COUNT(*) FROM app_setting WHERE key = 'booking_notification_email'")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO app_setting (key, value) VALUES ('booking_notification_email', 'info@squalo.local')")
    print("Default notification email set.")

conn.commit()
conn.close()
print("Migration complete.")
