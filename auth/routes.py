import re
from flask import Blueprint, request, render_template, url_for, session, redirect, flash
from werkzeug.security import generate_password_hash
from action_db import *

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name_company = request.form.get('name_company').strip().lower()
        password = request.form.get('password')

        if not name_company:
            flash('пароль не може бути порожнім', category='danger')
            return redirect(url_for('auth.register'))

        if (len(password) < 6 or
                not re.search(r"[a-zA-Z]", password) or
                not re.search(r"\d", password) or
                not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            flash('пароль сильно слабкий', category='danger')
            return redirect(url_for('auth.register'))

        if company_exists(name_company):
            flash('такая компания уже есть', category='danger')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)
        add_company(name_company, password_hash)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('company_name', None)
    flash('вы вышли из системи', category='info')
    return redirect(url_for('auth.login'))