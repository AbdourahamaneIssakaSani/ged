from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField, MultipleFileField


class NewFile(FlaskForm):
    file = FileField('Fichier')
    description = TextAreaField(label='Description')
    submit = SubmitField(label='Enregister')


class NewFiles(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(label='Enregistrer')
