from flask import Flask, render_template, request, redirect, session, Response, flash
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
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

        # Initialize Failed Attempts

        if 'failed_attempts' not in session:
            session['failed_attempts'] = 0

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

            # Reset Failed Attempts
            session['failed_attempts'] = 0

            return redirect('/')

        else:

            session['failed_attempts'] += 1

            flash("Invalid username or password")

            # Brute Force Detection

            if session['failed_attempts'] >= 3:

                flash("⚠️ Possible Brute Force Attack Detected!")

            return redirect('/login')

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

    # Create CSV Response

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

# Export PDF Report

@app.route('/export_pdf')
def export_pdf():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT incident_name,
               severity,
               status,
               timestamp
        FROM incidents
    """)

    incidents = cursor.fetchall()

    conn.close()

    # Create PDF

    pdf_file = "incident_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    # Table Data

    data = [
        ["Incident", "Severity", "Status", "Timestamp"]
    ]

    for incident in incidents:

        data.append(list(incident))

    # Create Table

    table = Table(data)

    table.setStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0,0), (-1,0), 12)

    ])

    elements = [table]

    doc.build(elements)

    return Response(

        open(pdf_file, 'rb'),

        mimetype='application/pdf',

        headers={
            "Content-Disposition":
            "attachment;filename=incident_report.pdf"
        }
    )

# Home Dashboard Route

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

    cursor.execute("""
        SELECT COUNT(*)
        FROM incidents
        WHERE severity='Critical'
    """)
    critical_alerts = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM incidents
        WHERE status='Resolved'
    """)
    resolved_cases = cursor.fetchone()[0]

    # Incident Query

    query = """
        SELECT * FROM incidents
        WHERE 1=1
    """

    params = []

    # Search Feature

    if search:

        query += " AND incident_name LIKE ?"

        params.append(f"%{search}%")

    # Severity Filter

    if severity_filter:

        query += " AND severity = ?"

        params.append(severity_filter)

    # Show Newest Incidents First

    query += " ORDER BY timestamp DESC"

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
        INSERT INTO incidents
        (incident_name, severity, status)

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

    cursor.execute("""
        DELETE FROM incidents
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect('/')


# Simulate Cyber Attack

@app.route('/simulate_attack')
def simulate_attack():

    incident = random.choice(attack_types)

    incident_name = incident[0]
    severity = incident[1]

    # Flash Critical Alerts

    if severity == "Critical":

        flash(f"🚨 Critical Threat Detected: {incident_name}")

    status = "Active"

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (incident_name, severity, status)

        VALUES (?, ?, ?)
    """, (incident_name, severity, status))

    conn.commit()
    conn.close()

    return redirect('/')


# Run Flask App

if __name__ == '__main__':

    app.run(debug=True)