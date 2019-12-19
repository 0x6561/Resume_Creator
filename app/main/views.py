from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
import json
from pprint import pprint 
from flask import jsonify
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Resume


@main.route('/')
def index():
    return render_template('resume.html', view='default')


@main.route('/load')
def load_resume():
    with open('resume.json') as infile:
        resume = json.dumps(json.loads(infile.read())) 
        author = current_user.email 
        resume_obj = Resume(author=author, resume=resume)
        db.session.add(resume_obj)
        db.session.commit()
        #return 'fuck'
        return jsonify({'status':'success', 'data': resume}) 

@main.route('/get')
def get_resume():
    if current_user.is_authenticated:
        resume = Resume.query.filter_by(author=current_user.email).first()
        if resume is not None and resume.resume is not None:
            resume_json = json.loads(resume.resume)
            return jsonify({'status': 'success', 'data': resume_json}) 
        else:
            return jsonify({'status': 'no resume on file... <a href="/new">creeate one</a>', 'data': ''}) 
    with open('resume.json') as infile:
        resume = json.loads(infile.read())
        return jsonify({'status':'success', 'data': resume}) 



@main.route('/edit') 
@login_required
def edit():
    return render_template('resume.html', view='edit')

@main.route('/new') 
#@login_required
def new():
    return render_template('resume.html', view='new')

@main.route('/save', methods=['GET', 'POST'])
@login_required
def save_resume():
    resume = json.dumps(request.json)
    resume_obj = Resume(author=current_user.email, resume=resume)
    db.session.add(resume_obj)
    db.session.commit()
    return jsonify({'status':'Resume saved' })


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
