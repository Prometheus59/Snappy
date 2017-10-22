from flask import Flask, render_template, request, session, redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash, secure_filename
import os
import datetime
import time

app = Flask(__name__)
mysql = MySQL()

app.secret_key = 'super secret key thacks2'
app.config['SESSION_TYPE'] = 'filesystem'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'thacks2@'
app.config['MYSQL_DATABASE_DB'] = 'thacks2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = '/home/thacks2/instagram/images/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql.init_app(app)

@app.route("/")
def index():
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login_user():
	print "test"
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		print email
		print password
		cur = mysql.connect().cursor()
		query = "SELECT * FROM users where email = '%s' and password = '%s';" % (email, password)
		cur.execute(query)
		data = cur.fetchall()
		print "data"
		print data[0]
		if len(data) == 1:
			print "login correct"
			print data[0][0]
			session['logged_in'] = True
			session['user_id'] = data[0][0]
			return redirect('/dashboard')
		else:
			print "incorrect"

		return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	session['user_id'] = Null
	return redirect('/')

@app.route('/dashboard')
def dashboard():
	cur = mysql.connect().cursor()
	query = "SELECT username, id from ig_accounts where account_id = '%s';" % session['user_id'] 
	cur.execute(query)
	ig = cur.fetchall()
	query = "SELECT * from post where ig_account_id = '%s';" % ig[0][1]
	cur.execute(query)
	posts = cur.fetchall()
	data = session['user_id']
	return render_template('dashboard.html', data=data, ig_acc=ig, posts=posts)

@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
	con = mysql.connect()
	cur = con.cursor()
	if request.method == 'POST':
		print 'add post'
		print app.config['UPLOAD_FOLDER']
		f = request.files['file']
		_post_caption = request.form['post_caption']
		_date = request.form['date']
		_time = request.form['time']
		_ig_account = 1
		filename = secure_filename(f.filename)
		cur.execute("""INSERT INTO post(filename, caption, date, time, ig_account_id) values(%s, %s, %s, %s, %s)""", (filename, _post_caption, _date, _time, _ig_account))
		# con.commit()
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return redirect('/dashboard')
	else:
		return render_template('add_post.html')

@app.route('/add_ig', methods=['POST', 'GET'])
def add_ig():
	if request.method == 'POST':
		print "ig post"
		ig_user = request.form['ig_username']
		ig_pass = request.form['ig_password']
		print ig_user
		print ig_pass
		redirect ('/')
	else:
		return render_template('add_ig.html')

	
@app.route('/profile')#, methods=['GET', 'POST'])
def viewProfile():
	#if request.method == 'GET':
	return render_template('profile.html')
	'''else:
		
		# idk how to do this without ORM #
		username = profile.name
		picture = profile.picture
		website = profile.website
		email = profile.email
		company = profile.company
		
		return render_template('profile.html', username = username, picture = picture, website=website, email=email)
'''


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)

