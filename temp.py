from flask import *

app = Flask(__name__)


construction_msg  = '''
<html>
	<head>
		<title>Teckzite 2020</title>
		<link href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	</head>
	<body>
		<center>
			<h1>Site is under construction</h1>
			<h3>Please visit after some time</h3>
			<p>In case of urgency contact web team. (Ajay - <i class="fa fa-phone"></i> XXXXXXXXXX) or (Akash - <i class="fa fa-phone"></i> XXXXXXXXXX)</p>
		</center>
	</body>
	<script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
</html>
'''
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	return construction_msg


if __name__ == '__main__':
	# For developing
	app.run(host='0.0.0.0', port=8443, debug=True)