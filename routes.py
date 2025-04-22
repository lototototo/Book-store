import email
from click import confirm
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from unicodedata import category
from wtforms import PasswordField, StringField
from wtforms,validators import Email, EqualTo, InputRequired, Length

from db.database import session_scope
from db.models import User
from werkzeug.security import generate_password_hash, check_password_hash

main_blueprint = Blueprint(name='main', import_name=__name__)

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired(), Length(max=100, min=4)])
    email = StringField(label='Email', validators=[InputRequired(),Email()])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(max=36, min=8)])
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired(), EqualTo(fieldname='password')])

@main_blueprint.route(rule='/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(_entity=User).filter_by(email=form.email.data).first()
        if user:
            flash(message='User with this email already exists', category='danger')
            return redirect(location=url_for(endpoint='main.register', form=form))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(passwod=form.password.data)
        )
        with session_scope() as session:
            session.add(instance=user)
        return redirect(location=url_for(endpoint='main.login'))
    elif form.errors:
        flash(message=form.errors, category='danger')
    return render_template(template_name_or_list='register.html',form=form)

@main_blueprint.route(rule='/main')
def main_route():
    return render_template(template_name_or_list='home.html')

@main_blueprint.route(rule='/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(_entity=User).filter_by(email=form.email.data).first()
            if user and check_password_hash(pwhash=user.password_hash, password=form.password.data):
                login_user(user=user)
                return redirect(locarion='main.home')
    return render_template(template_name_or_list='login.html',form=form)
