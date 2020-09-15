from flask import session, url_for, request

from hashlib import sha256, md5
import os
import codecs
from datetime import datetime

from panel.sql import conn
from panel.config import SALT, PEPPER
from panel.sendmails import *

def Hash(val):
	a = md5(val.encode()).hexdigest() + SALT
	return sha256(a.encode()).hexdigest() 

def Hash2(Val):
	a = Val + PEPPER
	return sha256(a.encode()).hexdigest()

def Hash3(Val):
	return md5(Hash(Val).encode()).hexdigest()

def MD5(Val):
	return md5(Val.encode()).hexdigest()

def check_login(username, password):
	res = conn.runQuery("SELECT id, priority FROM admins WHERE username = %s AND password = %s", (username, Hash(password)))
	if len(res) == 1: 
		priority = res[0]['priority'] ; Id = res[0]['id']
		if priority == 2:
			res = conn.runQuery("SELECT id, dept_name FROM departments WHERE login_creds = %s AND deleted = 0", (Id))
			if len(res) != 1:
				return False
			session['dept_id'] = res[0]['id']
			session['dept_name'] = res[0]['dept_name']
		elif priority == 3:
			res = conn.runQuery("SELECT id, event_name FROM events WHERE login_creds = %s AND deleted = 0", (Id))
			if len(res) != 1:
				return False
			session['event_id'] = res[0]['id']
			session['event_name'] = res[0]['event_name']
		elif priority == 5:
			res = conn.runQuery("SELECT id, workshop_name FROM workshops WHERE login_creds = %s AND deleted = 0", (Id))
			if len(res) != 1:
				return False
			session['workshop_id'] = res[0]['id']
			session['workshop_name'] = res[0]['workshop_name']
		session['username'] = username
		session['isLogin'] = 1
		session['priority'] = priority
		return True
	else:
		return False

def create_token(extra, Val):
	return md5(str(Hash3(str(Val))+extra).encode()).hexdigest()

def check_token(extra, Val, token):
	return create_token(extra, str(Val)) == token

def get_totp_secret():
	res = conn.runQuery("SELECT totp_secret FROM admins WHERE username = %s", (session['username']))
	return res[0]['totp_secret']

def get_totp_setup():
	res = conn.runQuery("SELECT totp_setup FROM admins WHERE username = %s", (session['username']))
	return res[0]['totp_setup']

def get_user_name():
	res = conn.runQuery("SELECT name FROM admins WHERE username = %s", (session['username']))
	if len(res) != 1:
		return "-----"
	return res[0]['name']

def get_user_mail():
	res = conn.runQuery("SELECT mail FROM admins WHERE username = %s", (session['username']))
	if len(res) != 1:
		return "-----"
	return res[0]['mail']

def get_user_id(user = None):
	if user == None: user = session["username"]
	res = conn.runQuery("SELECT id FROM admins WHERE username = %s", (user))
	if len(res) != 1: return None
	return res[0]['id']

def get_user_password(user = None):
	if user == None: user = session['username']
	res = conn.runQuery("SELECT password FROM admins WHERE username = %s", (user))
	if len(res) != 1: return None
	return res[0]['password']

def get_user_priority(user = None):
	if user == None: user = session['username']
	res = conn.runQuery("SELECT priority FROM admins WHERE username = %s", (user))
	if len(res) != 1: return None
	return res[0]['priority']

def get_user_name_withid(ID):
	res = conn.runQuery("SELECT username FROM admins WHERE id = %s", (ID))
	if len(res) != 1: return None
	return res[0]['username']

def get_name_withid(ID):
	res = conn.runQuery("SELECT name FROM admins WHERE id = %s", (ID))
	if len(res) != 1: return None
	return res[0]['name']

def get_user_mail_withid(ID):
	res = conn.runQuery("SELECT mail FROM admins WHERE id = %s", (ID))
	if len(res) != 1: return None
	return res[0]['mail']

def get_user_password_withid(ID):
	res = conn.runQuery("SELECT password FROM admins WHERE id = %s", (ID))
	if len(res) != 1: return None
	return res[0]['password']

def set_totp_secret(secret):
	conn.runQuery("UPDATE admins SET totp_secret = %s WHERE username = %s", (secret, session['username']))

def set_totp_setup(setup):
	conn.runQuery("UPDATE admins SET totp_setup = %s WHERE username = %s", (setup, session['username']))

def set_user_mail(mail):
	res = conn.runQuery("UPDATE admins SET mail = %s WHERE username = %s", (mail, session['username']))

def set_user_password(password):
	res = conn.runQuery("UPDATE admins SET password = %s WHERE username = %s", (Hash(password), session['username']))

def set_user_password_withid(ID, password):
	res = conn.runQuery("UPDATE admins SET password = %s WHERE id = %s", (Hash(password), ID))

def verify_user_password(password):
	return Hash(password) == get_user_password()


def verify_passwd_tokens(ID, token):
	print("Passwor Reset request : " , ID, token)
	if ID == 0 or token == '0': return False
	Pass = get_user_password_withid(ID)
	if Hash2(Pass) != token:
		return False
	return True

def create_passwd_reset_link(ID):
	New = codecs.encode(os.urandom(16),'hex').decode()
	set_user_password_withid(ID, New)
	return "https://"+request.host+url_for("setup_password")+"?TokenNo="+str(ID)+"&token="+Hash2(Hash(New))

def send_password_reset_link(num, link):
	name = get_name_withid(num)
	uname = get_user_name_withid(num)
	mail = get_user_mail_withid(num)
	mail_password_reset_link(mail,name, uname, link)

def create_department(dname, name, email, phone, stuid):
	sname = dname.strip().lower()
	username = sname+"@departments"
	password = codecs.encode(os.urandom(16),'hex').decode()
	res = conn.runQuery("INSERT INTO admins(username, password, name, mail, phone, collegeid, totp_setup, totp_secret, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, Hash(password), name, email, phone, stuid, 0, '', 2))
	ID = get_user_id(username)
	if ID != None:
		res = conn.runQuery("INSERT INTO departments(dept_name, login_creds, deleted) VALUES (%s, %s, %s)",(dname,ID, 0))
	link = create_passwd_reset_link(ID)
	if link != None:
		send_password_reset_link(ID, link)

def delete_department(Id):
	res = conn.runQuery("SELECT id FROM departments	WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE departments SET deleted = 1 WHERE id = %s", (Id))


def activate_department(Id):
	res = conn.runQuery("SELECT id FROM departments	WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE departments SET deleted = 0 WHERE id = %s", (Id))

def create_event(ename, name, email, phone, stuid):
	sname = ename.strip().lower()
	username = sname+"@events"
	password = codecs.encode(os.urandom(16),'hex').decode()
	print("Inserting Event Credentails ", username)
	res = conn.runQuery("INSERT INTO admins(username, password, name, mail, phone, collegeid, totp_setup, totp_secret, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, Hash(password), name, email, phone, stuid, 0, '', 3))
	ID = get_user_id(username)
	print(username, ID, "create_event")
	if ID != None:
		res = conn.runQuery("INSERT INTO events(event_name, dept_id, login_creds, deleted) VALUES (%s, %s, %s, %s)",(ename, session['dept_id'], ID, 0))
	link = create_passwd_reset_link(ID)
	if link != None:
		send_password_reset_link(ID, link)

def delete_event(Id):
	res = conn.runQuery("SELECT id FROM events WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE events SET deleted = 1 WHERE id = %s", (Id))


def activate_event(Id):
	res = conn.runQuery("SELECT id FROM events WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE events SET deleted = 0 WHERE id = %s", (Id))

def set_event_about(data):
	conn.runQuery("UPDATE events SET about = %s WHERE id = %s", (data, session['event_id']))

def get_event_about(num=None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT about FROM events WHERE id = %s", (num))
	if len(res) != 1: return ""
	return res[0]['about']

def get_event_rules(num=None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT id, rules FROM event_rules WHERE eveid = %s", (num))
	return res

def get_team_size(num=None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT min_part, max_part FROM events WHERE id = %s", (num))
	return [res[0]['min_part'], res[0]['max_part']]

def set_team_size(Min, Max):
	res = conn.runQuery("UPDATE events SET min_part = %s, max_part = %s WHERE id = %s", (Min, Max, session['event_id']))

def get_event_contacts(num=None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT id, name, phone, email FROM event_contacts WHERE eveid = %s", (num))
	return res

def set_event_contact(name, phone, email):
	res = conn.runQuery("INSERT INTO event_contacts(eveid, name, phone, email) VALUES (%s, %s, %s, %s)", (session['event_id'], name, phone, email))

def delete_event_contact(num):
	res = conn.runQuery("DELETE FROM event_contacts WHERE id = %s AND eveid = %s", (num, session['event_id']))

def get_event_notifications(num=None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT id, title, content, time_stamp FROM event_notifications WHERE eveid = %s  ORDER BY id DESC", (num))
	for item in res: item['post_time'] = datetime.fromtimestamp(item['time_stamp']).strftime("%b-%d [ %I:%M:%p ]")
	return res

def set_event_notification(title, content):
	tm = int(datetime.now().timestamp())
	res = conn.runQuery("INSERT INTO event_notifications(eveid, title, content, time_stamp) VALUES (%s, %s, %s, %s)", (session['event_id'], title, content, tm))

def delete_event_notification(num):
	res = conn.runQuery("DELETE FROM event_notifications WHERE id = %s  AND eveid = %s", (num,session['event_id']))

def create_workshop(wname, name, email, phone, stuid):
	sname = wname.strip().lower()
	username = sname+"@workshops"
	password = codecs.encode(os.urandom(16),'hex').decode()
	res = conn.runQuery("INSERT INTO admins(username, password, name, mail, phone, collegeid, totp_setup, totp_secret, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, Hash(password), name, email, phone, stuid, 0, '', 5))
	ID = get_user_id(username)
	if ID != None:
		res = conn.runQuery("INSERT INTO workshops(workshop_name, login_creds, deleted) VALUES (%s, %s, %s)",(wname, ID, 0))
	link = create_passwd_reset_link(ID)
	if link != None:
		send_password_reset_link(ID, link)

def get_workshop_contacts(num=None):
	if num == None: num = session['workshop_id']
	res = conn.runQuery("SELECT id, name, phone, email FROM workshop_contacts WHERE workshopid = %s", (num))
	return res

def set_workshop_contact(name, phone, email):
	res = conn.runQuery("INSERT INTO workshop_contacts(workshopid, name, phone, email) VALUES (%s, %s, %s, %s)", (session['workshop_id'], name, phone, email))

def delete_workshop_contact(num):
	res = conn.runQuery("DELETE FROM workshop_contacts WHERE id = %s AND workshopid = %s", (num, session['workshop_id']))

def get_workshop_notifications(num=None):
	if num == None: num = session['workshop_id']
	res = conn.runQuery("SELECT id, title, content, time_stamp FROM workshop_notifications WHERE workshopid = %s  ORDER BY id DESC", (num))
	for item in res: item['post_time'] = datetime.fromtimestamp(item['time_stamp']).strftime("%b-%d [ %I:%M:%p ]")
	return res

def set_workshop_notification(title, content):
	tm = int(datetime.now().timestamp())
	res = conn.runQuery("INSERT INTO workshop_notifications(workshopid, title, content, time_stamp) VALUES (%s, %s, %s, %s)", (session['workshop_id'], title, content, tm))

def delete_workshop_notification(num):
	res = conn.runQuery("DELETE FROM workshop_notifications WHERE id = %s AND workshopid = %s", (num, session['workshop_id']))

def delete_workshop(Id):
	res = conn.runQuery("SELECT id FROM workshops WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE workshops SET deleted = 1 WHERE id = %s", (Id))

def activate_workshop(Id):
	res = conn.runQuery("SELECT id FROM workshops WHERE id = %s", (Id))
	if len(res) == 1 and str(res[0]['id']) == Id:
		conn.runQuery("UPDATE workshops SET deleted = 0 WHERE id = %s", (Id))

def get_workshop_rules(num=None):
	if num == None: num = session['workshop_id']
	res = conn.runQuery("SELECT id, rules FROM workshop_rules WHERE workshopid = %s", (num))
	return res

def set_workshop_about(data, num=None):
	if num == None: num = session['workshop_id']
	conn.runQuery("UPDATE workshops SET about = %s WHERE id = %s", (data, num))

def get_workshop_about(num=None):
	if num == None: num = session['workshop_id']
	res = conn.runQuery("SELECT about FROM workshops WHERE id = %s", (num))
	if len(res) != 1: return ""
	return res[0]['about']

def get_workshop_topics(num=None):
	if num == None: num = session['workshop_id']
	res = conn.runQuery("SELECT topics FROM workshops WHERE id = %s", (num))
	if len(res) != 1: return ""
	return res[0]['topics']

def set_workshop_topics(data, num=None):
	if num == None: num = session['workshop_id']
	conn.runQuery("UPDATE workshops SET topics = %s WHERE id = %s", (data, num))

def get_event_image_name(num = None):
	if num == None: num = session['event_id']
	res = conn.runQuery("SELECT event_name FROM events WHERE id = %s", (num))
	if len(res) != 1: return ''
	img = MD5("photo_save_67668"+res[0]['event_name'])
	return img

def enable_event(num):
	res = conn.runQuery("UPDATE events SET visible = 1 WHERE id = %s", (num))

def disable_event(num):
	res = conn.runQuery("UPDATE events SET visible = 0 WHERE id = %s", (num))

def set_priority(num, priority):
	res = conn.runQuery("UPDATE events SET prior = %s WHERE id = %s ", (priority, num))
