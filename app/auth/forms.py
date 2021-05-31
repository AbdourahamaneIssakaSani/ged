# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, ValidationError, Length, EqualTo


class LoginForm(FlaskForm):
    email = TextField(
        label='Email',
        id='email_login',
        validators=[DataRequired(), Email(message='Donnez une adresse email valide !')]
    )
    password = PasswordField(label='Mot de passe', id='pwd_login', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField(label='Se connecter')


class CreateAccountForm(FlaskForm):
    first_name = TextField(label='Nom', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = TextField(label='Prénom', validators=[DataRequired(), Length(min=2, max=20)])
    email = TextField(label='Email', validators=[DataRequired(message='Adresse email obligatoire'), Email(message='Donnez une adresse email !')])
    password = PasswordField(
        label='Mot de passe',
        validators=[DataRequired(message='Mot de passe obligatoire'), Length(min=6, message='Au moins six (6) caractères pour le mot de passe ')])
    password_confirm = PasswordField(
        label='Confirmez le mot de passe',
        validators=[DataRequired(message='Confirmation obligatoire'), EqualTo(fieldname=password, message='Mot de passe doit correspondre')]
    )
    agree_terms = BooleanField(label='J’accepte les conditions d’utilisations', validators=[DataRequired()])

    submit = SubmitField(label='Valider')
# //TODO : Raise validation error in frontend
# //TODO : Manage terms of use page
