from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField
from wtforms.validators import AnyOf, Length

class RegisterForm(FlaskForm):

    username = StringField("Username",validators=[Length(min=1, max=20,message="Too Long or Empty")])
    password = PasswordField("Password")
    email = StringField("Email",validators=[Length(min=1, max=50,message="Too Long or Empty")])
    first_name = StringField("First Name",validators=[Length(min=1, max=30,message="Too Long or Empty")])
    last_name = StringField("Last Name",validators=[Length(min=1, max=30,message="Too Long or Empty")])

class LogInForm(FlaskForm):

    username = StringField("Username",validators=[Length(min=1, max=20,message="Too Long or Empty")])
    password = PasswordField("Password")

class FeedbackForm(FlaskForm):

    title = StringField("Title",validators=[Length(min=1, max=100,message="Too Long or Empty")])
    content = StringField("Content",validators=[Length(min=1,message="Too Short")])