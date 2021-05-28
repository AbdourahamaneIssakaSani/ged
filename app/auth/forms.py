# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired, ValidationError


class LoginForm(FlaskForm):
    email = TextField(label='Email', id='email_login', validators=[DataRequired(), Email()])
    password = PasswordField(label='Mot de passe', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    first_name = TextField(label='Nom', id='nom_create', validators=[DataRequired()])
    last_name = TextField(label='Prénom', id='prenom_create', validators=[DataRequired()])
    email = TextField(label='Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField(label='Mot de passe', id='pwd_create', validators=[DataRequired()])
    password_confirm = PasswordField(label='Confirmez le mot de passe', id='pwd_confirm', validators=[DataRequired()])
    submit = SubmitField(label='Valider')
