from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth  = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("User Name or Password is incorrect! Please Try Again", category='error')
        else:
            flash("User does not exist!", category='error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User Name is already exists.Please enter new User Name.", category='error')
        elif len(email) < 10:# checks the validity of the username/password
            flash("Please Enter a valid Email Address!", category='error')
        elif password1 != password2:
            flash("The password you entered is incorrect.\nPlease Try Again", category='error')
        elif len(password1) < 2:
            flash("Password is too easy to guess. Try stronger", category='error')
        else:
            # add user to the Database
            newUser = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account Created!", category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)

@auth.route('/about')
def about():
    return render_template("about.html", user=current_user)