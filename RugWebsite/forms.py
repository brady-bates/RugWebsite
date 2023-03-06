from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField(validators  =[InputRequired(),
                                         Length(min=4, max=20)],
                                         render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(),
                                         Length(min=4, max=20)],
                                         render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(),
                                         Length(min=4, max=20)])
    submit   = SubmitField("Register")
