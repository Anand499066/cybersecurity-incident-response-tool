from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

# Create incidents table

cursor.execute('''
CREATE TABLE IF NOT EXISTS incidents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    incident_name TEXT NOT NULL,

    severity TEXT NOT NULL,

    status TEXT NOT NULL,

    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

)
''')

# Create users table

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert sample data
sample_data = [
    ('Malware Attack', 'Critical', 'Active'),
    ('Phishing Email', 'High', 'Resolved'),
    ('Unauthorized Access', 'Critical', 'Active'),
    ('DDoS Attempt', 'Medium', 'Resolved'),
    ('SQL Injection', 'Critical', 'Active')
]

# Default Login User

hashed_password = generate_password_hash("admin123")

cursor.execute("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", ("admin", hashed_password))

cursor.executemany('''
INSERT INTO incidents (incident_name, severity, status)
VALUES (?, ?, ?)
''', sample_data)

conn.commit()

conn.close()

print("Database initialized successfully.")