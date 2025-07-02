from flask import render_template, request, redirect, url_for, session, current_app
from . import auth_bp

@auth_bp.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = current_app.cursor

        cursor.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = {'id': user[0], 'name': user[1], 'email': email}
            return redirect(url_for('dashboard.dashboard'))
        else:
            return "Invalid credentials."

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = current_app.cursor
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            current_app.db.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            current_app.db.rollback()
            return f"Error: {e}"

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
