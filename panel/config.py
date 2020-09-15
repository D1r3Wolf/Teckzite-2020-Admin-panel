import os
basedir = os.path.abspath(os.path.dirname(__file__))

# =========== SALT , PEPPER for hashing passwords ==================
SALT = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
PEPPER = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# =========== Session expiry time for inactivity ==============
ACTIVE_SESSION_LIMIT = 20  # in minutes

# ========== Mail creds for sending password reset mails ==============
MAIL_SERVER = 'XXXXXXXXXXXX'
MAIL_ADDRESS = 'XXXXXXXX@mail.com'
MAIL_PASSWORD = 'XXXXXXXXXXXXXX'


# =========== MySQL creds for DB =====================
MYSQL_HOST = 'XXXXXXXXX' #localhost
MYSQL_USER = 'XXXXXXXXX'
MYSQL_PWD = 'XXXXXXXXX'
MYSQL_DB = 'XXXXXXXX' #tz2020


class Config(object):
	# =========== SECRET KEY for flask server =================
    SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'



