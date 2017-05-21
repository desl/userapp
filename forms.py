from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, validators

class NewUserForm(FlaskForm):
    username = StringField('Name', [validators.Length(min=1)], render_kw={"placeholder": "JaneRocks1984"})
    first_name = StringField('First Name', [validators.Length(min=1)], render_kw={"placeholder": "Jane"})
    last_name = StringField('Last Name', [validators.Length(min=1)], render_kw={"placeholder": "Doe"})
    email = StringField('E-mail', [validators.Length(min=6, max=35)], render_kw={"placeholder": "jane@aol.com"})

class DeleteUserForm(FlaskForm):
    username = StringField('Name', render_kw={"placeholder": "JaneRocks1984"})