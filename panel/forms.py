from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.fields import *
from wtforms.fields.html5 import EmailField

class CreateAdminUser(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),length(min=4,max=50)])
	password = PasswordField('Password', validators=[DataRequired(),length(min=8,max=20)])
	StuName= StringField('Student Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	StuID = StringField('Student ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	setup = IntegerField('TOTP Setup', validators=[DataRequired(),NumberRange(min=1, max=2)])
	secret = StringField('TOTP Secret')
	priority = IntegerField('Priority', validators=[DataRequired(),NumberRange(min=0, max=20)])
	post = SubmitField('Submit')
	
class CreateAdminUser(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),length(min=4,max=50)])
	password = PasswordField('Password', validators=[DataRequired()])
	StuName= StringField('Student Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	StuID = StringField('Student ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	setup = IntegerField('TOTP Setup', validators=[DataRequired(),NumberRange(min=1, max=2)])
	secret = StringField('TOTP Secret')
	priority = IntegerField('Priority', validators=[NumberRange(min=0, max=20)])
	post = SubmitField('Submit')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),length(min=4,max=50)])
	password = PasswordField('Password', validators=[DataRequired(),length(min=8,max=20)])
	submit = SubmitField('Sign In')

class TOTP_Signin_Form(FlaskForm):
	token = StringField('OTP', validators=[DataRequired(),Regexp(r'^[0-9]{6}$', message="Invalid OTP !..")])
	submit = SubmitField('Submit')

class TOTP_Signup_Form(FlaskForm):
	token = StringField('OTP', validators=[DataRequired(),Regexp(r'^[0-9]{6}$', message="Invalid OTP !..")])
	password = PasswordField('Password', validators=[DataRequired(),length(min=8,max=20)])
	submit = SubmitField('Submit')
	
class UserChangeEmailForm(FlaskForm):
	email = EmailField('Email address', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(),length(min=8,max=20)])
	submit = SubmitField('Submit')

class UserChangePasswordForm(FlaskForm):
	cur_passwd = PasswordField('Current Password', validators=[DataRequired(),length(min=8,max=20)])
	new_passwd = PasswordField('New Password', validators=[DataRequired(),length(min=8,max=20)])
	new_passwd2= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_passwd', message='Passwords must match')])	
	submit = SubmitField('Submit')
		
class SetupPassword(FlaskForm):
	new_passwd = PasswordField('New Password', validators=[DataRequired(),length(min=8,max=20)])
	new_passwd2= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_passwd', message='Passwords must match')])	
	submit = SubmitField('Submit')

class AddDepartment(FlaskForm):
	DName = StringField('Department Name', validators=[DataRequired(),length(min=3,max=20)])
	StuID = StringField('Organizer ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	StuName= StringField('Organizer Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	post = SubmitField('Submit')
			
class AddEvent(FlaskForm):
	Ename = StringField('Event Name', validators=[DataRequired(),length(min=3,max=50)])
	StuID = StringField('Organizer ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	StuName= StringField('Organizer Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	post = SubmitField('Submit')

class AboutEvent(FlaskForm):
	content = HiddenField('Event Name', validators=[DataRequired(),length(min=0,max=5000)])
	post = SubmitField('Submit')

class EventTeamSize(FlaskForm):
	max_num = IntegerField('Max Participants', validators=[DataRequired(),NumberRange(min=1, max=10)])
	min_num = IntegerField('Min Participants', validators=[DataRequired(),NumberRange(min=1, max=10)])
	setup = SubmitField('Setup')
	def validate_on_submit(self):
		if not Form.validate(self):
			return False
		if self.min_num.data > self.max_num.data:
			self.min_num.errors.append("Minimum Should be <= to Maximum")
			return False
		return True

class EventNotification(FlaskForm):
	title = StringField('Notification Title', validators=[DataRequired(),length(min=5, max=40)])
	content = StringField('Notification Content', validators=[DataRequired(),length(min=10, max=300)])
	post = SubmitField('Post')

class EventContact(FlaskForm):
	name = StringField('Organizer Name', validators=[DataRequired(),length(min=4, max=20)])
	phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	email = EmailField('Email address', validators=[DataRequired(), Email()])
	add = SubmitField('Add')

class AddWorkshop(FlaskForm):
	Wname = StringField('Workshop Name', validators=[DataRequired(),length(min=3,max=50)])
	StuID = StringField('Organizer ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	StuName= StringField('Organizer Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	post = SubmitField('Submit')

class AboutWorkshop(FlaskForm):
	content = HiddenField('Workshop About', validators=[DataRequired(),length(min=0,max=5000)])
	post = SubmitField('Submit')

class WorkshopTopics(FlaskForm):
	content = HiddenField('Workshop Topics', validators=[DataRequired(),length(min=0,max=5000)])
	post = SubmitField('Submit')

class WorkshopNotification(FlaskForm):
	title = StringField('Notification Title', validators=[DataRequired(),length(min=5, max=40)])
	content = StringField('Notification Content', validators=[DataRequired(),length(min=10, max=300)])
	post = SubmitField('Post')

class WorkshopContact(FlaskForm):
	name = StringField('Organizer Name', validators=[DataRequired(),length(min=4, max=20)])
	phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	email = EmailField('Email address', validators=[DataRequired(), Email()])
	add = SubmitField('Add')

class AddPaymentVolunteer(FlaskForm):
	Uname = StringField('User name', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	StuID = StringField('Organizer ID number', validators=[DataRequired(),Regexp(r'^[nN]1[4-9][0-9]{4}$', message="Invalid ID Number !..")])
	StuName= StringField('Organizer Name', validators=[DataRequired()])	
	Email = EmailField('Email address', validators=[DataRequired(), Email()])
	Phone = StringField("Mobile Number", validators=[DataRequired(), length(10), Regexp(r'^[6-9][0-9]{9}$', message="Invalid Mobile Number !..")])
	post = SubmitField('Submit')