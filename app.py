from flask import Flask, render_template, request, redirect, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import csv
app = Flask(__name__)

app.secret_key = "cybersecurity_secret_key"

# Sample Attack Simulations

attack_types = [

    ("Ransomware Attack", "Critical"),
    ("Phishing Email", "High"),
    ("SQL Injection", "Critical"),
    ("Brute Force Attempt", "Medium"),
    ("Malware Infection", "High"),
    ("DDoS Attack", "Critical"),
    ("Suspicious Login", "Low"),
    ("Unauthorized Access", "High")

]

# Login Route

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username=?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/')

        else:
            return "Invalid username or password"

    return render_template('login.html')

# Logout Route

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')

# Export Incident Report CSV

@app.route('/export_csv')
def export_csv():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents")

    incidents = cursor.fetchall()

    conn.close()

    # Create CSV response
    def generate():

        data = []

        # CSV Header
        data.append("ID,Incident Name,Severity,Status\n")

        # CSV Rows
        for incident in incidents:

            row = f"{incident[0]},{incident[1]},{incident[2]},{incident[3]}\n"

            data.append(row)

        return data

    return Response(
        generate(),
        mimetype='text/csv',
        headers={
            "Content-Disposition":
            "attachment;filename=incident_report.csv"
        }
    )
    
@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    search = request.args.get('search', '')
    severity_filter = request.args.get('severity', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Dashboard Counts
    cursor.execute("SELECT COUNT(*) FROM incidents")
    total_incidents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM incidents WHERE severity='Critical'")
    critical_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status='Resolved'")
    resolved_cases = cursor.fetchone()[0]

    # Incident Query
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []

    # Search Feature
    if search:
        query += " AND incident_name LIKE ?"
        params.append(f"%{search}%")

    # Severity Filter
    if severity_filter:
        query += " AND severity = ?"
        params.append(severity_filter)

    cursor.execute(query, params)

    incidents = cursor.fetchall()
# Severity Analytics
    cursor.execute("""
    SELECT severity, COUNT(*)
    FROM incidents
    GROUP BY severity
  """)
    severity_data = cursor.fetchall()    
    conn.close()

    return render_template(
    'index.html',
    total_incidents=total_incidents,
    critical_alerts=critical_alerts,
    resolved_cases=resolved_cases,
    incidents=incidents,
    severity_data=severity_data
)

# Add Incident Route
@app.route('/add_incident', methods=['POST'])
def add_incident():

    incident_name = request.form['incident_name']
    severity = request.form['severity']
    status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents (incident_name, severity, status)
        VALUES (?, ?, ?)
    """, (incident_name, severity, status))

    conn.commit()
    conn.close()

    return redirect('/')
# Delete Incident Route
@app.route('/delete_incident/<int:id>')
def delete_incident(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM incidents WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')
# Simulate Cyber Attack

@app.route('/simulate_attack')
def simulate_attack():

    incident = random.choice(attack_types)

    incident_name = incident[0]
    severity = incident[1]

    status = "Active"

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents (incident_name, severity, status)
        VALUES (?, ?, ?)
    """, (incident_name, severity, status))

    conn.commit()
    conn.close()

    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)