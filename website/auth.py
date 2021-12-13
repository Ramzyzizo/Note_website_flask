from re import U
from flask import Blueprint, render_template,request,flash, redirect,url_for
#for routs,templates, GET and POST, for flash messgge
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['POST','GET']) #get for show data or template and post for take data and store
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash('Incorrect password, try again',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required #to ensure he already logged
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist',category='error')
        else:
            if len(email) < 4:
                flash('Email must be > 4 characters.', category='error')
            elif len(firstname) < 2:
                flash('First Name must be > 2 characters.', category='error')
            elif len(password1) < 3:
                flash('Password must be at least 7 characters', category='error')
            elif password1 != password2:
                flash('Password don\'t match', category='error')
            else:
                new_user = User(email=email,first_name=firstname,password=generate_password_hash(password1,method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash('Account created', category='success')
                return redirect(url_for('views.home'))

    return render_template("signup.html",user=current_user)