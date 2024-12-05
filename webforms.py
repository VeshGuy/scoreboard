from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class NamerForm(FlaskForm):
	name = StringField("Team Name", validators=[DataRequired()])
	score = IntegerField("Enter Score")
	submit = SubmitField("Submit")
	
class LoginForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	password = StringField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")
	
