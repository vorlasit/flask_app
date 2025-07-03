# install flask python on ubuntu server 

# update ubuntu
    sudo apt update && sudo apt upgrade -y
# install python
    sudo apt install python3 python3-pip python3-venv -y
# install libary for postgres
    pip install psycopg2-binary
# install flask
    pip install Flask --ignore-installed --break-system-packages
# install postgres
    sudo apt install postgresql postgresql-contrib -y
# create user
    createuser --createdb --username postgres --no-createrole --superuser --pwprompt flaskuser 
# make directory
    mkdir /opt/flaskapp && cd /opt/flaskapp
# Create a Python Virtual Environment
    python3 -m venv venv
# active Environment
    source venv/bin/activate 
# create requirements.txt
      Flask==3.1.1
      psycopg2-binary==2.9.9
# ✅ วิธีใช้งาน  
      pip install -r requirements.txt

# install gunicorn for run flask
    pip install gunicorn

# create app/__init__.py

    from flask import Flask
    from .db import init_db
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    
    def create_app():
        app = Flask(__name__)
        app.secret_key = 'your_secret_key'
    
        init_db(app)  # setup DB connection
    
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)

        return app
     
# create app/db.py
    import psycopg2

    def init_db(app):
        app.db = psycopg2.connect(
            host="localhost",
            user="your_postgres_user",
            password="your_postgres_password",
            dbname="your_database"
        )
        app.cursor = app.db.cursor()
    
        app.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            )
        """)
        app.db.commit()
# create app/templates/layout.html
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title>{% block title %}My Flask App{% endblock %}</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
      </head>
      <body>
      
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <div class="container-fluid">
              <a class="navbar-brand" href="#">FlaskApp</a>
              <div class="collapse navbar-collapse">
                  <ul class="navbar-nav ms-auto">
                      {% if session.user %}
                          <li class="nav-item">
                              <a class="nav-link" href="{{ url_for('dashboard.dashboard') }}">Dashboard</a>
                          </li>
                          <li class="nav-item">
                              <a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a>
                          </li>
                      {% else %}
                          <li class="nav-item">
                              <a class="nav-link" href="{{ url_for('auth.login') }}">Login</a>
                          </li>
                          <li class="nav-item">
                              <a class="nav-link" href="{{ url_for('auth.register') }}">Register</a>
                          </li>
                      {% endif %}
                  </ul>
              </div>
          </div>
      </nav>
      
      <div class="container mt-4">
          {% block content %}
          {% endblock %}
      </div>
      
      <footer class="bg-light text-center py-3 mt-5 border-top">
          &copy; 2025 My Flask App
      </footer>
      
      </body>
      </html>
# create app/auth/__init__.py
      from flask import Blueprint
      
      auth_bp = Blueprint('auth', __name__, template_folder='templates')
      
      from . import routes

# create app/auth/routes.py
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

# create app/auth/templates/login.html
      {% extends 'layout.html' %}
      {% block title %}Login{% endblock %}
      
      {% block content %}
      <h2 class="mb-4">Login</h2>
      <form method="POST" action="{{ url_for('auth.login') }}" class="col-md-6 mx-auto">
          <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" name="email" class="form-control" required>
          </div>
          <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" name="password" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <p class="text-center mt-3">Don't have an account? <a href="{{ url_for('auth.register') }}">Register</a></p>
      {% endblock %}

# create app/auth/templates/register.html
      {% extends 'layout.html' %}
      {% block title %}Register{% endblock %}
      
      {% block content %}
      <h2 class="mb-4">Register</h2>
      <form method="POST" action="{{ url_for('auth.register') }}" class="col-md-6 mx-auto">
          <div class="mb-3">
              <label class="form-label">Name</label>
              <input type="text" name="name" class="form-control" required>
          </div>
          <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" name="email" class="form-control" required>
          </div>
          <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" name="password" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-success w-100">Register</button>
      </form>
      <p class="text-center mt-3">Already have an account? <a href="{{ url_for('auth.login') }}">Login</a></p>
      {% endblock %}

# create app/dashboard/__init__.py
      from flask import Blueprint

      dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
      
      from . import routes
# Create app/dashboard/routes.py
      from flask import render_template, session, redirect, url_for
      from . import dashboard_bp
      
      @dashboard_bp.route('/dashboard')
      def dashboard():
          if 'user' not in session:
              return redirect(url_for('auth.login'))
          return render_template('dashboard.html')
# create app/dashboard/templates/dashboard.html
      {% extends 'layout.html' %}
      {% block title %}Dashboard{% endblock %}
      
      {% block content %}
      <div class="text-center">
          <h2 class="mb-4">Welcome {{ session.user.name }}!</h2>
          <p class="lead">You are now logged into your dashboard.</p>
      </div>
      {% endblock %}
# create run.py (entry point)
      from app import create_app

      app = create_app()
      
      if __name__ == '__main__':
          app.run(debug=True)

# create service 
      sudo nano /etc/systemd/system/flaskapp.service
      
    ใส่เนื้อหาดังนี้ (แก้ตาม environment ของคุณ):

      [Unit]
      Description=Flask App running with Gunicorn
      After=network.target
      
      [Service]
      User=root
      WorkingDirectory=/opt/flask
      Environment="PATH=/opt/flask/venv/bin"
      ExecStart=/opt/flask/venv/bin/python /opt/project_flask/run.py
      Restart=always
      
      [Install]
      WantedBy=multi-user.target

#  รีโหลดและเปิดใช้งาน Service 
      sudo systemctl daemon-reexec
      sudo systemctl daemon-reload
      sudo systemctl enable flaskapp
      sudo systemctl start flaskapp
# ตรวจสอบสถานะ 
      sudo systemctl status flaskapp
# ดู log เพิ่มเติมได้ที่: 
      journalctl -u flaskapp -f
    
    gunicorn --bind 0.0.0.0:8000 run:app
    
    
    
