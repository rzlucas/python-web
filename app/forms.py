from wtforms import Form
from wtforms import StringField, PasswordField

class LoginForm (Form):
    username = StringField ('Username')
    password = PasswordField ('Password')

    
