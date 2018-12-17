from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, length, Email, EqualTo, ValidationError, DataRequired
from biashara.models import User

class RegistrationForm(FlaskForm):
	username = StringField("Username", 
				validators=[InputRequired(), length(min=2, max=25)])
	email = StringField("Email", 
				validators=[InputRequired(), Email()])
	password = PasswordField("Password", 
				validators=[InputRequired()])
	confirm_password = PasswordField("Confirm Password", 
				validators=[InputRequired(), EqualTo("password")])
	submit = SubmitField("Create Account")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is taken! Choose another')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('email is taken! Choose another')

class LoginForm(FlaskForm):
	email = StringField("Email", 
				validators=[InputRequired(), Email()])
	password = PasswordField("Password", 
				validators=[InputRequired()])
	submit = SubmitField("Log in")

class BusinessRegistration(FlaskForm):
	choices = [('Service', 'Service'), ('Merchandising', 'Merchandising'), ('Manufacturing', 'Manufacturing')]
	business_name = StringField("Business Name", 
					validators=[InputRequired()])
	business_category = SelectField("Category", 
					choices=choices, validators=[DataRequired()])
	business_email = StringField("Business Email", 
					validators=[InputRequired(), Email()])
	description = TextAreaField("Description", 
					validators=[InputRequired()])
	address = TextAreaField("Address", 
					validators=[InputRequired()])
	submit = SubmitField("Add business")

class SearchForm(FlaskForm):
	choices = [('Service', 'Service'), ('Merchandising', 'Merchandising'), ('Manufacturing', 'Manufacturing')]
	search = SelectField("Search", choices=choices)
	submit = SubmitField("Go")

class UpdateProfileForm(FlaskForm):
	username = StringField("Username", 
				validators=[InputRequired(), length(min=2, max=25)])
	email = StringField("Email", 
				validators=[InputRequired(), Email()])
	submit = SubmitField("Update account")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is taken! Choose another')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email is taken! Choose another')
		
class UpdateBusinessForm(FlaskForm):
	choices = [('Service', 'Service'), ('Merchandising', 'Merchandising'), ('Manufacturing', 'Manufacturing')]
	business_name = StringField("Business Name", 
					validators=[InputRequired()])
	business_category = SelectField("Category", 
					choices=choices, validators=[DataRequired()])
	business_email = StringField("Business Email", 
					validators=[InputRequired(), Email()])
	description = TextAreaField("Description", 
					validators=[InputRequired()])
	address = TextAreaField("Address", 
					validators=[InputRequired()])
	business_submit = SubmitField("Update business")

class ReviewForm(FlaskForm):
	business_review = TextAreaField("Content")
	submit = SubmitField("Post review")
		
		
