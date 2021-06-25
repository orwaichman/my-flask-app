from flask import g, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app import Session
from app.main import main
from app.main.forms import LoginForm, RegisterForm
from db.models import User


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
def index():
    return redirect(url_for('main.home'))


@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/play')
@login_required
def play():
    return render_template('play.html')  # Image source is needed to be provided


@main.route('/login', methods=["GET", "POST"])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('main.home'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Session.query(User).filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data)
        Session.add(new_user)
        Session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)
