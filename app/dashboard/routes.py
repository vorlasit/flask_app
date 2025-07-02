from flask import render_template, session, redirect, url_for
from . import dashboard_bp

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
