from flask import Flask, render_template, request, redirect, url_for # Upper case = flass. importing Flask class from flask library
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from forms import NewUserForm
import string
import random
import os
from IPython import embed;

app = Flask(__name__)
modus = Modus(app)

if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-migrate-users'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = 'any string works here'
app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=25))

class User(db.Model):
    
    __tablename__ = "users" # table name will default to name of the model

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    messages = db.relationship('Message',backref='user',lazy='dynamic')

    ## for a migration, add a unique constraint to username and email.

    # define what each instance or row in the DB will have (id is taken care of for you)
    def __init__(self, username, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "{}: {} {} {}".format(self.username, self.first_name, self.last_name, self.email)

class Message(db.Model):
	__tablename__ = "messages"

	id = db.Column(db.Integer, primary_key=True)
	msg_text = db.Column(db.String(length=100))
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	def __init__(self,msg_text,user_id):
		self.msg_text = msg_text
		self.user_id = user_id

	def __repr__(self):
		return "{} -{}".format(self.msg_text, User.query.get(self.user_id).first_name)

@app.route('/')
def root():
	return "foo"

@app.route('/users', methods=['GET','POST'])
def index():
	if request.method in ['POST',b'POST']:
		form = NewUserForm(request.form)
		if form.validate():
			new_user = User(form.data['username'],form.data['first_name'],form.data['last_name'],form.data['email'])
			db.session.add(new_user)
			db.session.commit()
		else:
			return render_template('new.html',form=form)
			# redirect(url_for('new',form=form))

	users = User.query.all()
	return render_template('index.html',users=users)

@app.route('/users/<int:user_id>',methods=['GET','PATCH','DELETE'])
def show(user_id):
	user = User.query.get_or_404(user_id)

	if request.method in ['PATCH',b'PATCH']:
		user.username = request.form['username']	
		user.first_name = request.form['first_name']	
		user.last_name = request.form['last_name']	
		user.email = request.form['email']

		db.session.add(user)
		db.session.commit()
		return redirect(url_for('show',user_id=user.id))

	if request.method in ['DELETE',b'DELETE']:
		db.session.delete(user)
		db.session.commit()
		return redirect(url_for('index'))

	return render_template('show.html',i=user)

@app.route('/users/<int:user_id>/edit')
def edit(user_id):
	user = User.query.get(user_id)
	return render_template('edit.html',i=user)

@app.route('/users/new')
def new():
	form = NewUserForm(request.form)
	return render_template('new.html',form=form)

@app.route('/users/<int:user_id>/messages',methods=['GET','POST'])
def msg_index(user_id):
	if request.method == 'POST':
		message = Message(request.form['msg_text'],user_id)
		db.session.add(message)
		db.session.commit()

	user = User.query.get(user_id)
	return render_template('messages/index.html',i=user)

@app.route('/users/<int:user_id>/messages/new')
def msg_new(user_id):
	user = User.query.get(user_id)
	return render_template('messages/new.html', i=user)

@app.route('/users/<int:user_id>/messages/<int:msg_id>',methods=['GET','PATCH','DELETE'])
def msg_show(user_id,msg_id):
	user = User.query.get(user_id)
	msg = Message.query.get(msg_id)

	if request.method in [b'PATCH','PATCH']:
		msg.msg_text = request.form['msg_text']
		db.session.add(msg)
		db.session.commit()
		return redirect(url_for('msg_show',user_id=user_id,msg_id=msg_id))

	if request.method in [b'DELETE','DELETE']:
		db.session.delete(msg)
		db.session.commit()
		return redirect(url_for('msg_index',user_id=user_id))

	return render_template('/messages/show.html',i=user,msg=msg)

@app.route('/users/<int:user_id>/messages/<int:msg_id>/edit')
def msg_edit(user_id,msg_id):
	user = User.query.get(user_id)
	msg = Message.query.get(msg_id)
	return render_template('messages/edit.html', i=user,msg=msg)


if __name__ == '__main__':
    app.run(debug=True,port=3000)