from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Имя пользователя должно содержать только буквы, цифры или подчеркивания')])
    password = PasswordField('Пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Поавторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такой email уже используется')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Такое имя пользователя уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[InputRequired()])
    password = PasswordField('Новый пароль', validators=[
        InputRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Повторите новый пароль', validators=[InputRequired()])
    submit = SubmitField("Обновить пароль")

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Сбросить пароль')

class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Новый пароль', validators=[
        InputRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Такого пароля не существует')