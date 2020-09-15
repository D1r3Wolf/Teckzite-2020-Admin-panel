import smtplib
from email.message import EmailMessage

from panel.config import MAIL_SERVER, MAIL_ADDRESS, MAIL_PASSWORD

class User:
	def __init__(self, email, name, uname):
		self.email = email
		self.name = name
		self.uname = uname

	def sendPwdResetMail(self, server_conn, from_mail, reset_token_link):
		body = EmailMessage()
		body['Subject'] = 'Teckzite 2020 - Password reset request'
		body['From'] = from_mail
		body['To'] = self.email
		body.set_content('Password reset Link : {0}'.format(reset_token_link))
		body.add_alternative(
			'''
			<div style="padding: 10px;">
				<h1>Password reset?</h1>
				<h3> Username : %s</h2>
				<h4>If you requested a password reset for %s, click the link below. If you didn't make this request, ignore this email.<h4>
				<a href="%s">
					<button style="height: 40px; width: 150px; color: #fff; background-color: #007bff; border-color: #007bff; cursor: pointer;">Password reset</button>
				</a>
				<br><br>
				If the above button doesn't work, click the below url.
				<br>
				%s
			</div>
		'''%(self.uname, self.uname, reset_token_link, reset_token_link),
		subtype = 'html')
		server_conn.send_message(body)

def mail_password_reset_link(mail,name, uname, link):
	with smtplib.SMTP_SSL(MAIL_SERVER , 465) as server:
		server.login(MAIL_ADDRESS , MAIL_PASSWORD)
		u = User(mail, name, uname)
		u.sendPwdResetMail(server, MAIL_ADDRESS, link)
		print('Mail sent to {0:20} [{1}]'.format(u.name, u.email))