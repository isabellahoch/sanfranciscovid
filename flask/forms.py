from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    link = StringField('link to a fast fashion item', validators=[DataRequired()])
    submit = SubmitField('GO')