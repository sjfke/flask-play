from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__, static_folder='static')


@auth.get('/login')
def login():
    return render_template('login.html')


@auth.post('/login')
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.get_quizzes'))


@auth.get('/signup')
def signup():
    return render_template('signup.html')


@auth.post('/signup')
def signup_post():

    _SPECIAL_CHARACTERS = "$@_()%*/[]{}^<>!#"

    def criteria_check(password_str):
        """
        Verify the string is 8-20 characters long, uses mixed case, special characters and numbers
        :param password_str: UTF-8 character string to be checked
        :type password_str: str
        :return: whether the proposed password is considered secure
        :rtype: bool
        """

        (_length, _lower, _upper, _digit, _special) = (False, False, False, False, False)
        _length = True if 8 <= len(password_str) <= 20 else False

        for _letter in password_str:
            if _letter.islower():
                _lower = True
            elif _letter.isupper():
                _upper = True
            elif _letter.isdigit():
                _digit = True
            elif _letter in _SPECIAL_CHARACTERS:
                _special = True
            else:
                return False

        return _length and _lower and _upper and _digit and _special

    import uuid

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #  cif = "CIF-{0}".format(str(uuid.uuid4())) # Only MongoDB is using prefixed UUID's
    cif = f"{uuid.uuid4()}"

    user = User.query.filter_by(email=email).first()  # if returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if not criteria_check(password):
        flash('Password fails criteria check')
        flash('8-20 characters long, uses mixed case, special characters and numbers')
        flash(f"special characters: '{_SPECIAL_CHARACTERS}'")
        return redirect(url_for('auth.signup'))

    _timezone = 'Europe/Zurich'
    # later from request.form: const tzid = Intl.DateTimeFormat().resolvedOptions().timeZone;

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='scrypt'),
        cif=cif,
        timezone=_timezone,
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))