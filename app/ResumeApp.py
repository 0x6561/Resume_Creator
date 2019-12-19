#from flask import Flask, session, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
#import os
#from flask_sqlalchemy import SQLAlchemy
import pprint
import json
from flask import jsonify 
from forms import NameForm 
#import config 
import flask_login
from __init__.py import app, db 

#basedir = os.path.abspath(os.path.dirname(__file__))

#app = Flask(__name__)
#app.config.from_object('config.Config') 

#db = SQLAlchemy(app)
#from models import User, Role 

# user authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


title = "Resume with Flask and MongoDB"
heading = "Edgar Aguiniga - Software Engineer"

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

print('secret key -> ' + app.secret_key)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('form.html',
        form = form, name = session.get('name'))

@app.route('/resume_view')
def index2():
    resume = read_resume()
    return render_template('r.html', resume=resume)

@app.route('/preview', methods=['POST'])
def preview():
    resume = request.json
    #return 'preview ' + str(type(resume)) + ' <-- val' 
    return 'resume_c.html'

@app.route('/edit')
def edit():
    resume = read_resume()
    return render_template('resume_js.html', resume=resume)

@app.route('/get')
def show_resume():
    #return get_resume()
    with open('resume.json') as infile:
        resume = json.loads(infile.read())
        return jsonify(resume)

@app.route('/save', methods=['POST'])
def save_resume():
    resume = request.json
    return render_template('resume.html', resume=resume)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        #return flask.redirect(flask.url_for('protected'))
        return 'can access protected'

    return 'Bad login'

# save resume to file (json)
# requires a dict as a parameter
def save_resume(resume):
    with open('resume.json', 'w') as outfile:
        json.dump(resume, outfile, indent=4, sort_keys=False, default=str)

# read resume from file (json)
# returns a dict
def read_resume():
    with open('resume.json') as infile:
        resume = json.loads(infile.read())
        return resume
