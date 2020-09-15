from flask import session, redirect, flash

from time import time
import functools

from panel.config import ACTIVE_SESSION_LIMIT


def login_required(func):
	@functools.wraps(func)
	def inner(*args, **kwargs):
		print("%"*200)
		if 'isLogin' not in session or session['isLogin'] != 1:
			return redirect("/login")
		return func(*args, **kwargs)
	return inner

def no_login(L):
	if 'isLogin' in session and session['isLogin'] == 1:
		flash("You are already logged in !...", category="warning")
		return "home"
	return None

def user_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if L[1] == "2FA" and 'isVerified' in session and session['isVerified'] == 1:
		return "home"
	return None

def admin_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'isVerified' not in session or session['isVerified'] != 1:
		return "TOTP_verify"
	if 'priority' not in session or session['priority'] not in [0, 1]:
		return "home"
	return None

def dev_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'isVerified' not in session or session['isVerified'] != 1:
		return "TOTP_verify"
	if 'priority' not in session or session['priority'] != 0:
		return "home"
	return None

def dept_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'priority' not in session or session['priority'] != 2:
		return "home"
	if 'dept_id' not in session or 'dept_name' not in session:
		return "home"
	return None

def event_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'priority' not in session or session['priority'] != 3:
		return "home"
	if 'event_id' not in session or 'event_name' not in session:
		return "home"
	return None

def workshop_admin_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'priority' not in session or session['priority'] != 4:
		return "home"
	return None

def workshop_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'priority' not in session or session['priority'] != 5:
		return "home"
	if 'workshop_id' not in session or 'workshop_name' not in session:
		return "home"
	return None

def payment_login(L):
	if 'isLogin' not in session or session['isLogin'] != 1:
		return "login"
	if 'priority' not in session or session['priority'] != 6:
		return "home"
	return None

def check_active():
	T = 0
	if 'time' in session:
		T = int(time()) - session['time']
	session['time'] = int(time())
	return T < ACTIVE_SESSION_LIMIT * 60

Path_Access = {
	"util" : no_login,
	"user" : user_login,
	"dev" : dev_login,
	"admin" : admin_login,
	"dept" : dept_login,
	"event" : event_login,
	"head" : workshop_admin_login,
	"workshop" : workshop_login,
	"payment" : payment_login
}

