# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, ValidationError, Length, EqualTo


class LoginForm(FlaskForm):
    email = TextField(
        label='Adresse email',
        validators=[DataRequired(message='Vous devez fournir votre adresse email'),
                    Email(message='Donnez une adresse email valide !')]
    )
    password = PasswordField(label='Mot de passe',
                             validators=[DataRequired(message='Vous devez fournir votre mot de passe')])
    remember_me = BooleanField('Se souvenir de moi')


class RegisterForm(FlaskForm):
    first_name = TextField(label='Nom', validators=[DataRequired(message='Nom obligatoire'), Length(min=2, max=20,
                                                                                                    message='Votre nom doit être entre 2 et 20 caractères')])
    last_name = TextField(label='Prénom', validators=[DataRequired(message='Prénom obligatoire'), Length(min=2, max=20,
                                                                                                         message='Votre prénom doit être entre 2 et 20 caractères')])
    email = TextField(label='Email', validators=[DataRequired(message='Adresse email obligatoire'),
                                                 Email(message='Donnez une adresse email valide !')])
    password = PasswordField(
        label='Mot de passe',
        validators=[DataRequired(message='Mot de passe obligatoire'),
                    Length(min=6, message='Au moins six (6) caractères pour le mot de passe ')])
    password_confirm = PasswordField(
        label='Confirmez le mot de passe',
        validators=[DataRequired(message='Confirmation obligatoire'),
                    EqualTo(fieldname='password', message='Mot de passe doit correspondre')]
    )
    agree_terms = BooleanField(label='J’accepte les conditions d’utilisation',
                               validators=[DataRequired(message='Vous devez accepter les conditions d’utilisation')])

# //TODO : Manage terms of use page
