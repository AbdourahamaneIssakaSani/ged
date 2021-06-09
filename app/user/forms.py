from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField, MultipleFileField, StringField
from wtforms.validators import DataRequired


class SingleFileForm(FlaskForm):
    label = StringField(label='Label', validators=[DataRequired(message='Obligatoire !')])
    description = TextAreaField(label='Description')
    submit = SubmitField(label='Enregister', id='submit')


class NewFiles(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(label='Enregistrer')
