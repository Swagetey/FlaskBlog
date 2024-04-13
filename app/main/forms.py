from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User, Post
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('Как вас зовут?', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class EditProfileForm(FlaskForm):
    name = StringField('Ваше имя', validators=[Length(0, 64)])
    location = StringField('Местонахождение', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне', validators=[Length(0, 64)])
    submit = SubmitField('Отправить')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Имя должно содержать только буквы, цифры точки или подчеркивания')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Права', coerce=int)
    name = StringField('Настоящее имя', validators=[Length(0, 64)])
    location = StringField('Местоположение', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Отправить')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Такой Email уже зарегистрирован')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Пользователь с таким именем уже используется')


class PostForm(FlaskForm):
    body = PageDownField('Расскажите о чем-нибудь', validators=[DataRequired()])
    submit = SubmitField('Отправить')