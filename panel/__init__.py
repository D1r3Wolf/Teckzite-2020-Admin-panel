from flask import *
from flask_bootstrap import Bootstrap

import onetimepass
import pyqrcode
from io import BytesIO
import os
import base64
import lxml
from lxml.html.clean import Cleaner

from panel import app
from panel.forms import *
from panel.funcs import *
from panel.decorators import *
from panel.flask_mynav import *
from panel.config import Config

app = Flask(__name__)
app.debug = 0
app.config.from_object(Config)
Bootstrap(app)
nav.init_app(app)

@app.before_request
def before_request_hook():
	scheme = request.headers.get('X-Forwarded-Proto')
	if scheme and scheme == 'http' and request.url.startswith('http://'):
		url = request.url.replace('http://', 'https://', 1)
		return redirect(url, code=301)
	if not check_active():
		if 'isLogin' in dict([(key, session.pop(key)) for key in list(session.keys())]):
			flash("Logged out due to Inactivty!... ", category="danger")
		return redirect("/")
	Parts = request.path.split("/")[1:] ; head = Parts[0]
	if head in Path_Access:
		Val = Path_Access[head](Parts)
		if Val != None:
			return redirect(url_for(Val))

@app.after_request
def after_requst_hook(response):
	# conn.close()
	return response

#########################################
#            Common Routes              #
#########################################.............................................................
@app.route('/')
def home():
	return render_template('index.html')


#########################################
#       Util Routes (no login)          #
#########################################.............................................................
@app.route("/util/login", methods=['GET', 'POST'])
def login():
	lForm = LoginForm()
	if request.method == 'POST' and lForm.validate_on_submit():
		User = lForm.username.data ; Pass = lForm.password.data;
		if not check_login(User, Pass):
			flash("Wrong Username or password !... ", category="danger")
		else:
			flash("Logged in successfully", category="success")
			if session["priority"] in [0, 1]:
				return redirect(url_for("TOTP_verify"))
			return redirect("/")
		return redirect(url_for("login"))
	return render_template("util/login.html", form=lForm)

@app.route("/util/setup_password", methods=['GET', 'POST'])
def setup_password():
	lForm = SetupPassword()
	ID = request.args.get('TokenNo', default = 0, type = int)
	token= request.args.get('token', default = '0', type = str)
	if not verify_passwd_tokens(ID, token):
		flash("Your Account reset link Expired or Not valid!. For queries please contact Web Team!.")
	if request.method == 'POST' and lForm.validate_on_submit():
		set_user_password_withid(ID, lForm.new_passwd.data)
		flash("Password setup completed. Please login to confirm !...", category="success")
		print("Password Changed for ", ID)
		return redirect(url_for("home"))
	return render_template("util/set_passwd.html", form=lForm)


#########################################
#       User Routes (/user/)            #
#########################################.............................................................
@app.route("/user/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/user/2FA/verify", methods=["GET", "POST"])
def TOTP_verify():
	tForm = TOTP_Signin_Form()
	if get_totp_setup() != 1:
		return redirect(url_for("TOTP_setup"))
	if request.method == 'POST' and tForm.validate_on_submit():
		if onetimepass.valid_totp(tForm.token.data, get_totp_secret()):
			flash("Verified successfully", category="success")
			session['isVerified'] = 1
		else:
			flash("Incorrect OTP !... ", category="danger")
		return redirect(url_for("TOTP_verify"))
	return render_template("user/topt-verify.html", form=tForm)

@app.route("/user/2FA/setup", methods=["POST", "GET"])
def TOTP_setup():
	tForm = TOTP_Signup_Form()
	if get_totp_setup() == 1:
		return redirect(url_for("TOTP_verify"))
	if request.method == 'POST' and tForm.validate_on_submit():
		if check_login(session['username'], tForm.password.data):
			if onetimepass.valid_totp(tForm.token.data, get_totp_secret()):
				set_totp_setup(1)
				flash("2FA implemented successfully", category="success")
				session['isVerified'] = 1
			else:
				flash("Incorrect OTP !...", category="danger")
		else:
			flash("Wrong password !... ", category="danger")
		return redirect(url_for("TOTP_setup"))
	return render_template("user/topt-setup.html", form=tForm)

@app.route('/user/2FA/qrcode')
def TOTP_qrcode():
	if get_totp_setup() == 1:
		abort(404)
	ss = base64.b32encode(os.urandom(10)).decode('utf-8')
	set_totp_secret(ss)
	uu = session['username']
	url = pyqrcode.create("otpauth://totp/{0}?secret={1}&issuer=Teckzite'20".format(uu, ss))
	stream = BytesIO()
	url.svg(stream, scale=5)
	return stream.getvalue(), 200, { 'Content-Type': 'image/svg+xml', 'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}

@app.route("/user/change/mail", methods=["POST", "GET"])
def change_mail():
	cForm = UserChangeEmailForm()
	if request.method == 'POST' and cForm.validate_on_submit():
		if verify_user_password(cForm.password.data):
			set_user_mail(cForm.email.data)
			flash("Email has been changed successfully !...", category="success")
			return redirect(url_for("home"))
		else:
			flash("Incorrect Password !... ", category="danger")
		return redirect(url_for("change_mail"))
	return render_template("user/change_mail.html", form=cForm)

@app.route("/user/change/password", methods=["POST", "GET"])
def change_password():
	cForm = UserChangePasswordForm()
	if request.method == 'POST' and cForm.validate_on_submit():
		if verify_user_password(cForm.cur_passwd.data):
			set_user_password(cForm.new_passwd.data)
			flash("Password has been changed successfully !...", category="success")
			return redirect(url_for("home"))
		else:
			flash("Incorrect Password !... ", category="danger")
		return redirect(url_for("change_password"))
	return render_template("user/change_password.html", form=cForm)


#########################################
#       Admin Routes (/admin/)          #
#########################################.............................................................

@app.route('/admin/users/list')
def GetUsersList_admin():
	res = conn.runQuery("SELECT u.id 'ID', u.tzid 'TZID', u.name 'Name', u.email 'Email', u.phone 'Phone', u.paid 'Paid' FROM users u")
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	return render_template('admin/users.html', listEmpty = listEmpty, dataHead = dataHead, content = content)

@app.route('/admin/dept/list')
def GetDeptAdmins_admin():
	res = conn.runQuery("""SELECT d.id 'ID', d.dept_name 'Department', a.collegeid 'College ID', a.name 'Name', a.mail 'E-Mail', a.phone 'Phone Number', d.deleted 'dd'\
							FROM admins a INNER JOIN departments d ON a.id = d.login_creds WHERE priority = 2 ORDER BY d.deleted ASC;""")
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	for i in range(len(content)): content[i].insert(1, i+1) 
	edit_token = []
	for D in res: 
		if D['dd'] == 0: x = create_token('delete_account', D['ID'])
		elif D['dd'] == 1: x = create_token('activate_account', D['ID'])
		else: x = ''
		edit_token.append(x)
	view_tokens = [create_token('view_account', D['ID']) for D in res]
	return render_template('admin/dept.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, edit_token, view_tokens))

@app.route("/admin/dept/create", methods=['GET', 'POST'])
def CreateDepartment_admin():
	aForm = AddDepartment()
	if request.method == 'POST' and aForm.validate_on_submit():
		flash("Department Added & Credentials sent to mail Successfully !...", category="success")
		dname = aForm.DName.data.upper()
		name  = aForm.StuName.data
		email = aForm.Email.data.lower()
		phone = aForm.Phone.data
		stuid = aForm.StuID.data.upper()
		create_department(dname, name, email, phone, stuid)
		return redirect(url_for("home"))
	return render_template("admin/add_dept.html", form=aForm)

@app.route("/admin/dept/<num>/delete", methods=['POST'])
def DeleteDepartment_admin(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_account", num, Token):
		return ""
	delete_department(num)
	return "OK"

@app.route("/admin/dept/<num>/activate", methods=['POST'])
def ActiveDepartment_admin(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("activate_account", num, Token):
		return ""
	activate_department(num)
	return "OK"

@app.route("/admin/dept/<num>/view", methods=['GET'])
def ViewDepartment_admin(num):
	Token = request.args.get('token')
	if num == None or Token == None or not check_token("view_account", num, Token):
		abort(404)
	res = conn.runQuery("""SELECT e.id 'ID', e.event_name 'Event Name', a.collegeid 'College ID', 
		a.name 'Name', a.mail 'E-Mail', a.phone 'Phone Number', e.deleted 'Options' 
		FROM admins a INNER JOIN events e ON a.id = e.login_creds 
		WHERE priority = 3 AND e.dept_id = %s ORDER BY e.deleted ASC;""", (num))
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	for i in range(len(content)): content[i].insert(1, i+1)
	del_tokens = []
	view_tokens = [create_token('view_event', D['ID']) for D in res]
	for D in res:
		if D['Options'] == 0 : del_tokens.append(create_token("delete_event", D['ID']))
		elif D['Options'] == 1: del_tokens.append(create_token("activate_event", D['ID']))
		else: del_tokens.append(create_token("", D['ID'])) # Not possible case
	return render_template('admin/events.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, del_tokens, view_tokens))

@app.route("/admin/event/<num>/view", methods=['GET'])
def ViewEvent_admin(num):
	Token = request.args.get('token')
	if num == None or Token == None or not check_token("view_event", num, Token):
		abort(404)
	tsize = get_team_size(num)
	about_event = get_event_about(num)
	rules = get_event_rules(num)
	tsize = get_team_size(num)
	notifs = get_event_notifications(num)
	contacts = get_event_contacts(num)
	img = get_event_image_name(num)
	return render_template('event/view.html',about_event=about_event, rules=rules, notifications=notifs, contacts=contacts, tsize=tsize, img_file=img)

@app.route('/admin/event/list')
def GetAllEvents_admin():
	res = conn.runQuery("""SELECT e.id 'ID', e.event_name 'Event', d.dept_name 'Department', a.collegeid 'College ID',
	 a.name 'Name',  a.phone 'Mobile', e.prior 'priority', e.visible 'Options' FROM events e INNER JOIN admins a ON a.id = e.login_creds 
	 INNER JOIN departments d ON d.id = e.dept_id WHERE a.priority = 3 ORDER BY e.prior ASC;""")
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	visible_tokens = []
	for D in res: 
		if D['Options'] == 0: x = create_token('active_event_56464', D['ID'])
		elif D['Options'] == 1: x = create_token('remove_event_64736', D['ID'])
		else: x = ''
		visible_tokens.append(x)
	prior_tokens = [create_token('event_priority_62776', D['ID']) for D in res]
	view_tokens = [create_token('view_event', D['ID']) for D in res]
	return render_template('admin/all_events.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, prior_tokens, visible_tokens, view_tokens))

@app.route("/admin/event/<num>/visible/enable", methods=['POST'])
def EnableEvent_admin(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("active_event_56464", num, Token):
		return ""
	enable_event(num)
	return "OK"

@app.route("/admin/event/<num>/visible/disable", methods=['POST'])
def DisableEvent_admin(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("remove_event_64736", num, Token):
		return ""
	disable_event(num)
	return "OK"

@app.route("/admin/event/<num>/priority", methods=['POST'])
def SetEventpriority_admin(num):
	Token = request.form.get('token')
	priority = request.form.get('priority')
	try:
		P = int(priority)
	except:
		return 'Please give number'
	if num == None or not (0 <= P <= 100) or priority == None or Token == None or not check_token("event_priority_62776", num, Token):
		return ""
	set_priority(num, priority)
	return "OK"

#########################################
#       Department Routes (/dept/)      #
#########################################.............................................................
@app.route('/dept/event/list')
def ListEvents_dept():
	res = conn.runQuery("""	SELECT e.id 'ID', e.event_name 'Event Name', a.collegeid 'College ID', a.name 'Name', a.mail 'E-Mail', 
							a.phone 'Phone Number', e.deleted 'Options' FROM admins a INNER JOIN events e ON a.id = e.login_creds 
							WHERE priority = 3 AND e.dept_id = %s ORDER BY e.deleted ASC;""", (session['dept_id']))
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	for i in range(len(content)): content[i].insert(1, i+1)
	del_tokens = []
	view_tokens = [create_token('view_event', D['ID']) for D in res]
	for D in res:
		if D['Options'] == 0 : del_tokens.append(create_token("delete_event", D['ID']))
		elif D['Options'] == 1: del_tokens.append(create_token("activate_event", D['ID']))
		else: del_tokens.append(create_token("", D['ID']))
	return render_template('dept/events.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, del_tokens, view_tokens))

@app.route("/dept/event/create", methods=['GET', 'POST'])
def CreateEvent_dept():
	aForm = AddEvent()
	if request.method == 'POST' and aForm.validate_on_submit():
		flash("Event Added & Credentials sent to mail Successfully !...", category="success")
		ename = aForm.Ename.data 
		name  = aForm.StuName.data
		email = aForm.Email.data.lower()
		phone = aForm.Phone.data
		stuid = aForm.StuID.data.upper()
		create_event(ename, name, email, phone, stuid)
		return redirect(url_for("home"))
	return render_template("dept/add_event.html", form=aForm)

@app.route("/dept/event/<num>/delete", methods=['POST'])
def DeleteEvent_dept(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_event", num, Token):
		return ""
	delete_event(num)
	return "OK"

@app.route("/dept/event/<num>/activate", methods=['POST'])
def ActiveEvent_dept(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("activate_event", num, Token):
		return ""
	activate_event(num)
	return "OK"

@app.route("/dept/event/<num>/view", methods=['GET'])
def ViewEvent_dept(num):
	Token = request.args.get('token')
	if num == None or Token == None or not check_token("view_event", num, Token):
		abort(404)
	tsize = get_team_size(num)
	about_event = get_event_about(num)
	rules = get_event_rules(num)
	tsize = get_team_size(num)
	notifs = get_event_notifications(num)
	contacts = get_event_contacts(num)
	img = get_event_image_name(num)
	return render_template('event/view.html',about_event=about_event, rules=rules, notifications=notifs, contacts=contacts, tsize=tsize, img_file=img)


#########################################
#       Event Org Routes (/event/)      #
#########################################.............................................................

@app.route('/event/view')
def ViewEventDetails_event():
	tsize = get_team_size()
	rules = get_event_rules()
	about_event = get_event_about()
	notifs = get_event_notifications()
	contacts = get_event_contacts()
	img = get_event_image_name()
	return render_template('event/view.html',about_event=about_event, rules=rules, notifications=notifs, contacts=contacts,tsize=tsize,img_file=img)

@app.route('/event/edit/details', methods=['GET', 'POST'])
def EditEventDetails_event():
	tForm = EventTeamSize() ; nForm = EventNotification() ; cForm = EventContact()
	tsize = get_team_size()
	contacts = get_event_contacts()
	for i in range(len(contacts)):
		contacts[i]['delete_token'] = create_token("delete_event_contact_16652", contacts[i]['id'])
	notifs = get_event_notifications()
	for i in range(len(notifs)):
		notifs[i]['delete_token'] = create_token("delete_event_notification_73816", notifs[i]['id'])
	if request.method == 'POST' and tForm.setup.data and tForm.validate_on_submit():
		if tsize[0] != -1 or tsize[1] != -1:
			flash("Number of participants is already edited, You can't update it!", category="danger")
		set_team_size(tForm.min_num.data, tForm.max_num.data)
		return redirect(url_for("EditEventDetails_event"))
	elif request.method == 'POST' and cForm.add.data  and cForm.validate_on_submit():
		set_event_contact(cForm.name.data, cForm.phone.data, cForm.email.data)
		flash("Contact Added Successfully !...", category="success")
		return redirect(url_for("EditEventDetails_event"))
	elif request.method == 'POST' and nForm.post.data  and nForm.validate_on_submit():
		set_event_notification(nForm.title.data, nForm.content.data)
		flash("Notification Posted Successfully !...", category="success")
		return redirect(url_for("EditEventDetails_event"))
	return render_template("event/details.html", tform=tForm , nform = nForm, cform = cForm, tsize=tsize, contacts = contacts, notifications=notifs)


@app.route('/event/delete/notification/<num>', methods=['POST'])
def DeleteEventNotification_event(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_event_notification_73816", num, Token):
		return ""
	delete_event_notification(num)
	return "OK"

@app.route('/event/delete/contact/<num>', methods=['POST'])
def DeleteEventContact_event(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_event_contact_16652", num, Token):
		return ""
	delete_event_contact(num)
	return "OK"


@app.route('/event/edit/rules', methods = ['GET', 'POST'])
def EditEventRules_event():
	res = get_event_rules()
	for row in res:
		row['token'] = create_token('rules_edit', row['id'])
	if request.method == 'POST':
		updated = [[row['id'], request.form.get('rule_%s_%s'%(row['id'], row['token']))] for row in res]
		new = request.form.getlist('new_rule')
		for i in new:
			if i: 
				conn.runQuery("INSERT INTO event_rules(eveid, rules) VALUES (%s, %s)", (session['event_id'], i))
		for i in updated: 
			if i[1] == None:
				conn.runQuery("DELETE FROM event_rules WHERE id = %s", (i[0]))
			else:
				conn.runQuery("UPDATE event_rules SET rules = %s WHERE id = %s", (i[1], i[0]))
		return redirect('/event/edit/rules')
	else:
		listEmpty = not bool(res)
		return render_template('event/rules.html', listEmpty = listEmpty, data = res)

@app.route('/event/edit/about', methods=["GET","POST"])
def EditEventAbout_event():
	aForm = AboutEvent()
	if request.method == 'POST' and aForm.validate_on_submit():
		cleaner = Cleaner()
		cleaner.javascript = True
		cleaner.style = True
		data = lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(aForm.content.data))).decode()
		set_event_about(data)
		flash("About Event data is updated Successfully !... ", category="success")
		return redirect(url_for("EditEventAbout_event"))
	name = session['event_name'];  desc = get_event_about()
	return render_template("event/about.html", name=name , desc=desc, form=aForm)

@app.route('/event/edit/photo', methods = ['GET', 'POST'])
def EventEditPhoto_event():
	if request.method == 'GET':
		print(os.getcwd())
		return render_template('event/photoedit.html')
	else:
		x = request.files.get('image')
		if x != None:
			x.save('/opt/lampp/htdocs/img/event_images/%s.jpg'%(MD5("photo_save_67668"+session['event_name'])))
			flash("Image uploaded Successfully !... ", category="success")
			return "OK"
		return ""



#########################################
#     Cordinators Routes (/event/)      #
#########################################.............................................................

@app.route("/head/workshop/<num>/view", methods = ['GET'])
def ViewWorkshop_head(num):
	Token = request.args.get('token')
	if num == None or Token == None or not check_token("view_workshop", num, Token):
		abort(404)
	about = get_workshop_about(num)
	rules = get_workshop_rules(num)
	topics = get_workshop_topics(num)
	notifs = get_workshop_notifications(num)
	contacts = get_workshop_contacts(num)
	return render_template('workshop/view.html',about=about, rules=rules, topics=topics, notifications=notifs, contacts=contacts)

@app.route("/head/workshop/<num>/delete", methods = ['POST'])
def DeleteWorkshop_head(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_workshop", num, Token):
		return ""
	delete_workshop(num)
	return "OK"

@app.route("/head/workshop/<num>/activate", methods = ['POST'])
def ActiveWorkshop_head(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("activate_workshop", num, Token):
		return ""
	activate_workshop(num)
	return "OK"

@app.route('/head/workshop/list')
def ListWorkshops_head():
	res = conn.runQuery("""	SELECT w.id 'ID', w.workshop_name 'Workshop Name', a.collegeid 'College ID', a.name 'Name', a.mail 'E-Mail', 
							a.phone 'Phone Number', w.deleted 'Options' FROM admins a INNER JOIN workshops w ON a.id = w.login_creds WHERE a.priority = 5 
							ORDER BY w.deleted ASC;""")
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	content = [[W[x] for x in W] for i, W in enumerate(res)]
	for i in range(len(content)): content[i].insert(1, i+1)
	del_tokens = []
	view_tokens = [create_token('view_workshop', W['ID']) for W in res]
	for W in res:
		if W['Options'] == 0 : del_tokens.append(create_token("delete_workshop", W['ID']))
		elif W['Options'] == 1: del_tokens.append(create_token("activate_workshop", W['ID']))
		else: del_tokens.append(create_token("", W['ID']))
	return render_template('head/workshops.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, del_tokens, view_tokens))

@app.route("/head/workshop/create", methods = ['GET', 'POST'])
def CreateWorkshop_head():
	aForm = AddWorkshop()
	if request.method == 'POST' and aForm.validate_on_submit():
		flash("Workshop Added, Credentials sent to mail Successfully !...", category="success")
		wname = aForm.Wname.data 
		name  = aForm.StuName.data
		email = aForm.Email.data.lower()
		phone = aForm.Phone.data
		stuid = aForm.StuID.data.upper()
		create_workshop(wname, name, email, phone, stuid)
		return redirect(url_for("home"))
	return render_template("head/add_workshop.html", form=aForm)


#########################################
#    Workshop Org Routes (/event/)      #
#########################################.............................................................

@app.route('/workshop/view')
def ViewWorkshopDetails_workshop():
	about = get_workshop_about()
	rules = get_workshop_rules()
	topics = get_workshop_topics()
	notifs = get_workshop_notifications()
	contacts = get_workshop_contacts()
	return render_template('workshop/view.html',about=about, rules=rules, topics=topics, notifications=notifs, contacts=contacts)

@app.route('/workshop/edit/details', methods=['GET', 'POST'])
def EditWorkshopDetails_workshop():
	nForm = WorkshopNotification() ; cForm = WorkshopContact()
	contacts = get_workshop_contacts()
	for i in range(len(contacts)):
		contacts[i]['delete_token'] = create_token("delete_workshop_contact_62838", contacts[i]['id'])
	notifs = get_workshop_notifications()
	for i in range(len(notifs)):
		notifs[i]['delete_token'] = create_token("delete_workshop_notification_18297", notifs[i]['id'])
	if request.method == 'POST' and cForm.add.data  and cForm.validate_on_submit():
		set_workshop_contact(cForm.name.data, cForm.phone.data, cForm.email.data)
		flash("Contact Added Successfully !...", category="success")
		return redirect(url_for("EditWorkshopDetails_workshop"))
	elif request.method == 'POST' and nForm.post.data  and nForm.validate_on_submit():
		set_workshop_notification(nForm.title.data, nForm.content.data)
		flash("Notification Posted Successfully !...", category="success")
		return redirect(url_for("EditWorkshopDetails_workshop"))
	return render_template("workshop/details.html", cform = cForm, nform = nForm, contacts = contacts, notifications=notifs)


@app.route('/workshop/delete/notification/<num>', methods=['POST'])
def DeleteWorkshopNotification_workshop(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_workshop_notification_18297", num, Token):
		return ""
	delete_workshop_notification(num)
	return "OK"

@app.route('/workshop/delete/contact/<num>', methods=['POST'])
def DeleteWorkshopContact_workshop(num):
	Token = request.form.get('token')
	if num == None or Token == None or not check_token("delete_workshop_contact_62838", num, Token):
		return ""
	delete_workshop_contact(num)
	return "OK"

@app.route('/workshop/edit/about', methods=["GET","POST"])
def EditWorkshopAbout_workshop():
	aForm = AboutWorkshop()
	if request.method == 'POST' and aForm.validate_on_submit():
		cleaner = Cleaner()
		cleaner.javascript = True
		cleaner.style = True
		data = lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(aForm.content.data))).decode()
		set_workshop_about(data)
		flash("About Workshop data is updated Successfully !... ", category="success")
		return redirect(url_for("EditWorkshopAbout_workshop"))
	name = session['workshop_name'];  desc = get_workshop_about()
	return render_template("workshop/about.html", name=name , desc=desc, form=aForm)

@app.route('/workshop/edit/rules', methods = ['GET', 'POST'])
def EditWorkshopRules_workshop():
	res = get_workshop_rules()
	for row in res:
		row['token'] = create_token('rules_edit', row['id'])
	if request.method == 'POST':
		updated = [[row['id'], request.form.get('rule_%s_%s'%(row['id'], row['token']))] for row in res]
		new = request.form.getlist('new_rule')
		for i in new:
			if i: 
				conn.runQuery("INSERT INTO workshop_rules(workshopid, rules) VALUES (%s, %s)", (session['workshop_id'], i))
		for i in updated: 
			if not i[1]:
				conn.runQuery("DELETE FROM workshop_rules WHERE id = %s", (i[0]))
			else:
				conn.runQuery("UPDATE workshop_rules SET rules = %s WHERE id = %s", (i[1], i[0]))
		return redirect('/workshop/edit/rules')
	else:
		listEmpty = not bool(res)
		return render_template('workshop/rules.html', listEmpty = listEmpty, data = res)

@app.route('/workshop/edit/topics', methods = ['GET', 'POST'])
def EditWorkshopTopics_workshop():
	aForm = WorkshopTopics()
	if request.method == 'POST' and aForm.validate_on_submit():
		cleaner = Cleaner()
		cleaner.javascript = True
		cleaner.style = True
		data = lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(aForm.content.data))).decode()
		set_workshop_topics(data)
		flash("Workshops Topics are updated Successfully !... ", category="success")
		return redirect(url_for("EditWorkshopTopics_workshop"))
	name = session['workshop_name'];  desc = get_workshop_topics()
	return render_template("workshop/topics.html", name=name , desc=desc, form=aForm)


#########################################
#       Developer Routes (/event/)      #
#########################################.............................................................

@app.route('/dev/user/list')
def AdminsList_dev():
	res = conn.runQuery("""SELECT a.id 'ID', a.username 'Username', a.name 'Name', a.collegeid 'College ID', 
		 a.mail 'E-Mail', a.phone 'Phone Number', a.totp_setup 'totp'
		FROM admins a ORDER BY a.id ASC;""")
	listEmpty = not bool(res)
	dataHead = list(res[0]) if not listEmpty else []
	dataHead += [ 'edit', 'reset']
	content = [[D[x] for x in D] for i, D in enumerate(res)]
	for i in range(len(content)): content[i].insert(1, i+1) 
	totp_tokens = []
	for D in res:
		if D['totp'] == 1 : totp_tokens.append(create_token("remove_totp_ahsdfhagsjd_189198", D['ID']))
		elif D['totp'] == 0: totp_tokens.append(create_token("activate_totp_ausadhahaa_272876", D['ID']))
		else: totp_tokens.append(".")
	reset_tokens = [create_token('reset_password_of_user_kajhskdmab_987987', D['ID']) for D in res]
	uedit_tokens = [create_token('edit_details_of_user_akjkfdhashdf_178743', D['ID']) for D in res]
	return render_template('dev/users.html', listEmpty = listEmpty, dataHead = dataHead, content_tokens = zip(content, totp_tokens, reset_tokens, uedit_tokens))

@app.route('/dev/user/create', methods=['GET', 'POST'])
def CreateUser_dev():
	cForm = CreateAdminUser()
	if request.method == 'POST' and cForm.validate_on_submit():
		uname = cForm.username.data ; upass = Hash(cForm.password.data)
		stuname = cForm.StuName.data; email = cForm.Email.data
		phone = cForm.Phone.data ; ID = cForm.StuID.data
		setup = cForm.setup.data-1 ; secret = cForm.secret.data
		priority = cForm.priority.data
		conn.runQuery("""INSERT INTO admins(username, password, name, mail, phone, collegeid, totp_setup, totp_secret, priority)
		 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (uname, upass, stuname, email, phone, ID, setup, secret, priority))
		flash("User has been created successfully !...", category="success")
		return redirect("/")
	return render_template("dev/create-user.html", form=cForm)

@app.route('/dev/user/<num>/edit', methods=['GET', 'POST'])
def EditUser_dev(num):
	Token = request.args.get("token")
	cForm = CreateAdminUser()
	if num == 0  or Token == None or not check_token("edit_details_of_user_akjkfdhashdf_178743", num, Token):
		abort(404)
	details = conn.runQuery("SELECT * FROM admins WHERE id = %s", (num))
	if len(details) != 1:
		flash("Number of rows != 1 man !.....")
		return redirect("/")
	details = details[0]
	if request.method == 'POST' and cForm.validate_on_submit():
		uname = cForm.username.data ; upass = cForm.password.data
		if len(upass) < 5: 
			upass = details['password']
		else:
			upass = Hash(cForm.password.data)
		stuname = cForm.StuName.data; email = cForm.Email.data
		phone = cForm.Phone.data ; ID = cForm.StuID.data
		setup = cForm.setup.data-1 ; secret = cForm.secret.data
		priority = cForm.priority.data
		res = conn.runQuery("""UPDATE admins SET username = %s, password = %s, name = %s, mail = %s, phone = %s, collegeid = %s,
		 totp_setup = %s, totp_secret = %s, priority = %s WHERE id = %s
		 """, (uname, upass, stuname, email, phone, ID, setup, secret, priority, num))
		print(res, num)
		flash("User has been updated successfully !...", category="success")
		return "<script>window.opener.location = '/dev/user/list';window.close();</script>"
	return render_template("dev/edit-user.html", form=cForm, row = details)

@app.route("/dev/user/<num>/password/reset", methods=['POST'])
def ResetUserPassword_dev(num):
	Token = request.form.get('token')
	if Token == None or not check_token("reset_password_of_user_kajhskdmab_987987", num, Token):
		abort(404)
	link = create_passwd_reset_link(num)
	if link == None: abort(404)
	send_password_reset_link(num, link)
	return "OK"

@app.route("/dev/user/<num>/totp/enable", methods=['POST'])
def EnableUserTOTP_dev(num=0):
	Token = request.form.get('token')
	if num == 0 or Token == None or not check_token("activate_totp_ausadhahaa_272876", num, Token):
		abort(404)	
	conn.runQuery("UPDATE admins SET totp_setup = 1 WHERE id = %s", (num))
	return "OK"

@app.route("/dev/user/<num>/totp/disable", methods=['POST'])
def  DisableTOTPSetup_dev(num=0):
	Token = request.form.get('token')
	if num == 0 or Token == None or not check_token("remove_totp_ahsdfhagsjd_189198", num, Token):
		abort(404)	
	conn.runQuery("UPDATE admins SET totp_setup = 0 WHERE id = %s", (num))
	return "OK"

@app.route("/dev/payments/volunteers", methods=["GET", "POST"])
def ListAllPaymentVolunteers_dev():
	aForm = AddPaymentVolunteer()
	if request.method == 'POST' and aForm.validate_on_submit():
		uame = aForm.Uname.data
		ID = aForm.StuID.data
		name = aForm.StuName.data
		email = aForm.Email.data
		phone = aForm.Phone.data
	return render_template("dev/payment_vol.html", form=aForm)
