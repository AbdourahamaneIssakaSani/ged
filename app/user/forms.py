from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField, MultipleFileField


class NewFile(FlaskForm):
    description = TextAreaField(label='Description')
    submit = SubmitField(label='Enregister', id='submit')

 
class NewFiles(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(label='Enregistrer')
