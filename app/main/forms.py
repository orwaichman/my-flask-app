from flask_wtf import Form
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length

from app import Session
from db.models import User


class LoginForm(Form):
    username = StringField('Username',
                           validators=[DataRequired(), Length(3, 32)],
                           render_kw={'placeholder': "Username",
                                      'class': "u-border-2 u-border-white u-input u-input-rectangle u-radius-50 u-white"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'placeholder': "Password",
                                        'class': "u-border-2 u-border-white u-input u-input-rectangle u-radius-50 u-white"})
    submit = SubmitField('Log In', render_kw={'class': "u-form-control-hidden", 'wfd-invisible': "true"})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = Session.query(User).filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Username does not exist')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True


class RegisterForm(Form):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)],
                           render_kw={'placeholder': "Username",
                                      'class': "u-input u-input-rectangle u-white u-input-1"})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=3, max=32)],
                             render_kw={'placeholder': "Password",
                                        'class': "u-input u-input-rectangle u-white u-input-2"})
    confirm = PasswordField('Verify password',
                            validators=[DataRequired(), EqualTo('password',
                                                                message='Passwords must match')],
                            render_kw={'placeholder': "Confirm Password",
                                       'class': "u-input u-input-rectangle u-white u-input-3"})

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = Session.query(User).filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        return True
