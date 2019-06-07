from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InputForm(FlaskForm):
    github_url = StringField('github_url',
                            validators=['DataRequired()', Length(min=12)])
    submit = SubmitField('Submit')
    