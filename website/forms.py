from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from wtforms.fields.html5 import DateField,DateTimeLocalField,TimeField
from wtforms import StringField,validators,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError,Optional
from website.models import User
from flask_login import current_user
from website.functions import days

# Validators
def age_validator(self,field):
	if days(field.data,state = 'age') < 0:
		raise ValidationError("How is it there in the future?")

def future_validator(self,field):
	if days(field.data,state = 'age') > 0:
		raise ValidationError("It is better to forget the past, right?")

def space_validator(self,field):
	if " " in field.data.strip():
		raise ValidationError(f"There can't be space in {field.name}")

def upper_lower_validator(self,field):
	if  field.data.islower() or field.data.isupper():
		raise ValidationError(f"The {field.name} must contain upper and lower characters")

def username_validator(self,field):
	if current_user.is_authenticated:
		if User.query.filter_by(username = field.data,).first() is not None and current_user.username != field.data:
			raise ValidationError('This username is already taken')
	elif User.query.filter_by(username = field.data).first() is not None:
		raise ValidationError('This username is already taken')

def email_validator(self,field):
	if current_user.is_authenticated:
		if User.query.filter_by(email = field.data).first() is not None and current_user.email != field.data:
			raise ValidationError('This email has already been used')
	elif User.query.filter_by(email = field.data).first() is not None:
		raise ValidationError('This email has already been used')

def reset_exists(self,field):
	if User.query.filter_by(email = field.data).first() is None:
		raise ValidationError('This email is not registered')
# end of Validators

# Forms
class RegistrationForm(FlaskForm):
	first_name = StringField('First Name',validators = [DataRequired(),Length(min = 3)])
	last_name = StringField('Last Name',validators = [DataRequired(),Length(min = 3)])
	birthdate = DateField("Birthdate",format = "%Y-%m-%d",validators = [DataRequired(),age_validator])
	username = StringField('Username',validators = [DataRequired(),username_validator,
							space_validator,Length(min = 5,max =20)])

	email = StringField("Email",validators = [DataRequired(),Email(),email_validator])
	password = PasswordField('Password',validators = [DataRequired(),upper_lower_validator])
	confirm_pass = PasswordField("Confirm",validators = [DataRequired(),
								EqualTo('password',message = "Passwords must match")])
	team_leader = BooleanField('Are you also a Team Leader?')
	department = SelectField('Department',choices =['Select a Department',"Post-department",'Deep Learning',"PID Control","ROS",
								"Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"],
								validators = [DataRequired()])

	position = SelectField('Position',choices =['IEEE Chairman','Vice Technical',"RAS Chairman",'RAS Vice Chairman'
		,"Team Leader","Team Member","Rookie"],validators = [DataRequired()])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	username_email = StringField("Username or Email",validators = [DataRequired()])
	password = PasswordField('Password',validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class ResetRequestForm(FlaskForm):
	email = StringField("Email",validators = [DataRequired(),Email(),reset_exists])
	submit = SubmitField('Send reset code')

class AccountForm(FlaskForm):
	profile_photo = FileField('Change Profile Photo',validators = [FileAllowed(['jpg','jpeg','png'])])
	first_name = StringField("First Name",validators = [Length(min = 3)])
	last_name = StringField('Last Name',validators = [Length(min = 3)])
	username = StringField('Username',validators = [username_validator,
							space_validator,Length(min = 5,max =20)])
	email = StringField("Email",validators = [Email(),email_validator])
	password = PasswordField('New Password',validators = [upper_lower_validator])
	confirm_pass = PasswordField("Password Confirmation",validators = [
								EqualTo('password',message = "Passwords must match")])
	department = SelectField('Department',choices =['All',"Post-department",'Deep Learning',"PID Control","ROS",
								"Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"],
								validators = [Optional()])
	noti_review = BooleanField('I receive a review on my task')
	noti_task = BooleanField('I have a new task')
	noti_submit = BooleanField('A team member submits a task')
	noti_excuse = BooleanField('A team member excuses himself from a task')
	noti_missed=BooleanField('I miss a task')
	noti_announcement=BooleanField('I have an announcement')
	noti_meetup=BooleanField('I have a meeting')
	email_review = BooleanField('I receive a review on my task')
	email_task = BooleanField('I have a new task')
	email_submit = BooleanField('A team member submits a task')
	email_excuse = BooleanField('A team member excuses himself from a task')
	email_missed=BooleanField('I miss a task')
	email_announcement=BooleanField('I have an announcement')
	email_meetup=BooleanField('I have a meeting')
	position = SelectField('Position',choices =['IEEE Chairman','Vice Technical',"RAS Chairman",'RAS Vice Chairman'
		,"Team Leader","Team Member","Rookie"],validators = [Optional()])

	save = SubmitField('Save')

class ResetPasswordForm(FlaskForm):
	code = StringField("Reset Code",validators=[DataRequired(),])
	password = PasswordField('New Password',validators = [DataRequired(),upper_lower_validator])
	submit = SubmitField('Save')

class NewTaskForm(FlaskForm):
	title = StringField("Title",validators = [DataRequired(),Length(max=30)])
	content = TextAreaField("Content",validators =[DataRequired()])
	file = FileField("Upload a file")
	deadline = DateField("Deadline",format = "%Y-%m-%d",validators = [DataRequired(),future_validator])
	submit = SubmitField('Post')
	
class SubmitTaskForm(FlaskForm):
	notes = TextAreaField('Notes',validators = [Length(max = 1000)])
	file = FileField("Upload a file")
	submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
	feedback = TextAreaField('Notes',validators = [Length(max = 1000)])
	score = SelectField('Score',choices =[i for i in range(1,11)],validators = [DataRequired()])
	save = SubmitField('Save')

class FilterForm(FlaskForm):
	department = SelectField('Department',choices =["Post-department",'Deep Learning',"PID Control","ROS",
								"Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"],
								validators = [DataRequired()])
	sort = SelectField('Sort',choices = ['Submits Count','Date Posted','Deadline','Title'])
	method = SelectField('Method',choices=[('asc','↑'),('desc','↓')])
	filter = SubmitField('Filter')

class AnnouncementForm(FlaskForm):
	department = SelectField('Department',choices =['Select a department','All',"Post-department",'Deep Learning',"PID Control","ROS",
								"Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"],
								validators = [Optional()])
	content = TextAreaField('Content',validators=[DataRequired()])
	validation_date = DateField("Valid Until:", validators = [DataRequired(),future_validator])
	announce = SubmitField('Announce')

class MeetupForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(),Length(max=25)])
	state=SelectField('Type',choices=['Offline','Online'],validators=[DataRequired()])
	about = TextAreaField('About')
	department = SelectField('Department',choices =['Select a department','All',"Post-department",'Deep Learning',"PID Control","ROS",
								"Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"],
								validators = [Optional()])
	date = DateField("Date", validators = [DataRequired(),future_validator])
	time = TimeField('Time',validators =[DataRequired()])
	lat = StringField('Lat')
	long = StringField('Long')
	submit = SubmitField('Create')

class MeetupInfoForm(FlaskForm):
	notes = TextAreaField('Notes',validators = [Length(max = 1000)])
	save = SubmitField('Excuse Me!')

class ConfirmForm(FlaskForm):
	code = StringField("Confirmation Code",validators=[DataRequired(),])
	submit = SubmitField('Activate my account')

