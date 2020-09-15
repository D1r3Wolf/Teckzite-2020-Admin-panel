import pymysql
import pymysql.cursors

from panel.config import MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB


class SQLConnection:
	credentials = {'host': MYSQL_HOST, 'user': MYSQL_USER, 'passwd' : MYSQL_PWD, 'db': MYSQL_DB}
	def __init__(self, Format = 'dict', **kwargs):
		self.Format = Format
	def runQuery(self, query, params = None):
		if self.Format == 'list': self.conn = pymysql.Connect(**self.credentials)
		elif self.Format == 'dict': self.conn = pymysql.Connect(**self.credentials, cursorclass = pymysql.cursors.DictCursor) 
		
		try:
			self.cursor = self.conn.cursor()
			if params: self.cursor.execute(query, params)
			else: self.cursor.execute(query)
			self.conn.commit()
			A = [row for row in self.cursor.fetchall()]
		except:
			A = []
		finally:
			self.conn.close()
		return A

conn = SQLConnection ()

