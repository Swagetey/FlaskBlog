from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User

class NameForm(FlaskForm):
    name = StringField('Как вас зовут?', validators=[DataRequired()])
    submit = SubmitField('Отправить')
