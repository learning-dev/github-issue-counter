from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InputForm(FlaskForm):
    github_url = StringField('GitHub URL',
                            validators=[DataRequired()])
    submit = SubmitField('Submit')
    