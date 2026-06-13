import sqlite3, os
db = os.path.join(os.path.dirname(__file__), 'instance', 'squalo.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT name, category, price_label, button_label FROM product")
for row in c.fetchall():
    print(row)
conn.close()
