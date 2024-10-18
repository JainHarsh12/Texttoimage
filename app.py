from flask import Flask, render_template, request, redirect, url_for, session, flash # type: ignore
import mysql.connector # type: ignore
from passlib.hash import sha256_crypt # type: ignore
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "Centralperk2=")  # Replace with your MySQL password

try:
    db = mysql.connector.connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASS,
        database="image_gen_app"
    )
    cursor = db.cursor()
    print("Connected to MySQL successfully.")

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

# Route: Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Route: Authenticate User
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    try:
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and sha256_crypt.verify(password, user[1]):
            session['user_id'] = user[0]
            return redirect(url_for('prompt'))  # Update 'prompt' to the correct route
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    except mysql.connector.Error as err:
        return f"Error: {err}", 500

# Route: Register User
@app.route('/register', methods=['GET', 'POST'])  # Allow both GET and POST methods
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = sha256_crypt.hash(request.form['password'])

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            return redirect(url_for('register'))  # Redirect back to register on error
    return render_template('register.html')  # Render register.html for GET requests

# Add a route for the prompts page (if applicable)
@app.route('/prompt')
def prompt():
    return render_template('prompt.html')

if __name__ == '__main__':
    app.run(debug=True)
