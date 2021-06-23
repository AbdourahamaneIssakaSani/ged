from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, MultipleFileField, StringField, TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class UpdateAccountForm(FlaskForm):
    first_name = TextField(label='Nom',
                           validators=[Length(min=2, max=20, message='Votre nom doit être entre 2 et 20 caractères')])
    last_name = TextField(label='Prénom',
                          validators=[Length(min=2, max=20, message='Votre prénom doit être entre 2 et 20 caractères')])
    email = TextField(label='Email', validators=[Email(message='Donnez une adresse email valide !')])
    password = PasswordField(
        label='Mot de passe',
        validators=[DataRequired(message='Mot de passe obligatoire'),
                    Length(min=6, message='Au moins six (6) caractères pour le mot de passe ')])


class NewFiles(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(label='Enregistrer')
