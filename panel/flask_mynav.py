from flask import url_for, session
from flask_nav import Nav

from panel.funcs import *

class MyNav:
	def __init__(self, mainname, ll, rl):
		self.MainName = mainname
		self.components = {"left" : ll , "right" : rl}

class SubGroup:
	def __init__(self, mainname, *args):
		self.MainName = mainname
		self.items = args

	def render(self):
		return '''
		<li>
			<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{} <span class="caret"></span></a>
			<ul class="dropdown-menu">
		'''.format(self.MainName) + '\n'.join([
				x.render() for x in self.items
			]) + '''
			</ul>
		</li>
		'''

class View:
	def __init__(self, mainname, fnName = 'home'):
		self.MainName = mainname
		self.fnName = fnName
	def render(self):
		return '<li><a href="{}">{}</a></li>'.format(url_for(self.fnName), self.MainName)

class Link:
	def __init__(self, mainname, path = '#'):
		self.MainName = mainname
		self.path = path
	def render(self):
		return '<li><a href="{}">{}</a></li>'.format(self.path, self.MainName)

class Separator:
	def render(self):
		return '<li role="separator" class="divider"></li>'		

class Label:
	def __init__(self, mainname):
		self.MainName = mainname
	def render(self):
		return '<li class="dropdown-header">{}</li>'.format(self.MainName)

nav = Nav()
@nav.navigation()
def mynavbar():
	if 'isLogin' not in session or session['isLogin'] != 1 or 'priority' not in session:
		return MyNav('Anonymous', [ 
			], [
				View('Log in', 'login')
			])
	if session['priority'] == 0:
		return MyNav(
			'Dev [ %s ]'%session['username'], [
				SubGroup(
					"Admins",
					View('Users', 'AdminsList_dev') ,
					View('Add User', 'CreateUser_dev')
				),
				SubGroup(
					"Events",
					View('Depts', 'GetDeptAdmins_admin') ,
					View('Add Dept', 'CreateDepartment_admin') ,
					View('Events', 'GetAllEvents_admin') ,
				),
				SubGroup(
					'Payments',
					View('Volunteers', 'ListAllPaymentVolunteers_dev'),
					# View('Statistics', 'PaymentStatistics_admin'),
					# View('All payments', 'ListAllPayments_admin'),
					# View('Main ticket', 'ListMainTicketPayments_admin'),
				),
				SubGroup(
					"Tz Users",
					View('List Users', 'GetUsersList_admin') ,
				),
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 1:
		return MyNav(
			'Admin', [
				SubGroup(
					"Events",
					View('Depts', 'GetDeptAdmins_admin') ,
					View('Add Dept', 'CreateDepartment_admin') ,
					View('Events', 'GetAllEvents_admin') ,
				),
				SubGroup(
					'Payments', 
					# View('Statistics', 'PaymentStatistics_admin'),
					# View('All payments', 'ListAllPayments_admin'),
					# View('Main ticket', 'ListMainTicketPayments_admin'),
				),
				View('Users', 'GetUsersList_admin') ,
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 2:
		return MyNav(
			'Dept [ %s ]'%(session['dept_name']), [
				View('Events', 'ListEvents_dept'),
				View('Add Event', 'CreateEvent_dept'),
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 3:
		return MyNav(
			'Event [ %s ]'%(session['event_name']), [
				View('View Event', 'ViewEventDetails_event'),
				SubGroup(
					'Edit Event', 
					View('Details', 'EditEventDetails_event'),
					View('About', 'EditEventAbout_event'),
					View('Rules', 'EditEventRules_event'),
					View('Photo', 'EventEditPhoto_event'),
				)
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 4:
		return MyNav(
			'Head', [
				View('Workshops', 'ListWorkshops_head'),
				View('Add Workshop', 'CreateWorkshop_head'),
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 5:
		return MyNav(
			'Workshop [ %s ]'%(session['workshop_name']), [
				View('View Workshop', 'ViewWorkshopDetails_workshop'),
				SubGroup(
					'Edit Workshop', 
					View('Details', 'EditWorkshopDetails_workshop'),
					View('About', 'EditWorkshopAbout_workshop'),
					View('Rules', 'EditWorkshopRules_workshop'),
					View('Topics', 'EditWorkshopTopics_workshop'),
				)
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])
	if session['priority'] == 6:
		return MyNav(
			'Payments [ %s ]'%(session['workshop_name']), [
				SubGroup(
					'Payments', 
					View('All payments', 'ListAllPayments_payment'),
					View('Main ticket', 'ListMainTicketPayments_payment'),
				),
				SubGroup(
					'Register', 
					View('Main ticket', 'RegisterMainTicket_payment'),
				)
			], [
				SubGroup(
					session['username'], 
					Label(get_user_name()),
					Label(get_user_mail()) ,
					Separator(), 
					View('Change mail', 'change_mail'),
					View('Change password', 'change_password'),
					Separator(), 
					View('Logout', 'logout') 
				)
			])

