from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from config import db


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/admin/login/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.')
            return redirect(url_for('auth_bp.login'))
        elif not check_password_hash(user.password, password):          
            flash('Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=remember)
        return redirect(url_for('panel'))

@auth_bp.route('/admin/kayit', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
 
        if user: 
            flash('Email address already exists')
            return redirect(url_for('auth_bp.signup'))
        admin_key = '9K!cO01?LA=39uNX!'
        new_user = User(email=email, name=name, \
                        password=generate_password_hash(password, \
                        method='pbkdf2:sha256'))
        if admin_key == request.form.get('key'):
            db.session.add(new_user)
            db.session.commit()
        else:
            flash('Yanlış anahtar girdiniz.')
            return redirect(url_for('auth_bp.signup'))

        return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))