from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, MultipleFileField, StringField
from wtforms.validators import DataRequired


class NewFolderForm(FlaskForm):
    name = StringField(label='Nom du dossier', validators=[DataRequired(message='Obligatoire !')])
    submit = SubmitField(label='Créer')


class NewFiles(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(label='Enregistrer')
