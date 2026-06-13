import sqlite3, os
db = os.path.join(os.path.dirname(__file__), 'instance', 'squalo.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print([r[0] for r in c.fetchall()])
conn.close()
