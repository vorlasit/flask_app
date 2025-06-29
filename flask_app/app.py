import logging
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='app.log',            # Log file name
    level=logging.DEBUG,           # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",     # Replace with your MySQL username
    password="your_mysql_password", # Replace with your MySQL password
    database="your_database"    # Replace with your database name
)

cursor = db.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
)
""")
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        db.commit()

        app.logger.info('User successfully registered.')
        return redirect(url_for('login'))
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return "An error occurred while creating the user."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = {
                'id': user[0],
                'name': user[1],
                'email': email
            }
            app.logger.info(f"User {email} logged in.")
            return redirect(url_for('dashboard'))
        else:
            app.logger.warning(f"Failed login attempt for {email}")
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome {session['user']['name']}! <a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    if user:
        app.logger.info(f"User {user['email']} logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)