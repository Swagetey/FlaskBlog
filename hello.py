# from flask import Flask, render_template, session, url_for, redirect, flash
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from datetime import datetime
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# import os
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_mail import Mail, Message
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'generatedstring'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)
# migrate = Migrate(app, db)
#
# app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'Glavniyzavhoz@yandex.ru'
# app.config['MAIL_PASSWORD'] = 'esadrsznlsbyeuel'
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = 'Flasky'
# app.config['FLASKY_MAIL_SENDER'] = 'Glavniyzavhoz@yandex.ru'
#
# mail = Mail(app)
#
# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients = [to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     mail.send(msg)
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#
# class NameForm(FlaskForm):
#     name = StringField('Как вас зовут?', validators=[DataRequired()])
#     submit = SubmitField('Отправить')
#
#
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#             if app.config['FLASKY_ADMIN']:
#                 send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))
#
#
# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html', name=name)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
