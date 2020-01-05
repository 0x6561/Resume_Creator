from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
import json
from pprint import pprint 
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Resume


@main.route('/')
def index():
    return render_template('resume.html', view='default')


@main.route('/load')
@login_required
def load_resume():
    if current_user.is_authenticated and current_user.email == 'edgar.ea6561@gmail.com':
        with open('resume.json') as infile:
            resume = json.dumps(json.loads(infile.read())) 
            author = current_user.email 
            resume_obj = Resume(author=author, resume_title='starting resume', resume=resume)
            db.session.add(resume_obj)
            db.session.commit()
            return jsonify({'status':'success', 'data': resume}) 
    else:
        return jsonify({'status':'?', 'data': '?'}) 


@main.route('/get', methods=['GET'])
def get_resume():
    resume = None
    if current_user.is_authenticated:
        resume = Resume.query.filter_by(author=current_user.email).first()
        if resume is not None and resume.resume is not None:
            return jsonify({'status': 'success', 'data': resume.to_json()}) 
        else:
            return jsonify({'status': 'no resume on file... <a href="/new">creeate one</a>', 'data': ''}) 
    with open('resume.json') as infile:
        resume = json.loads(infile.read())
        return jsonify({'status':'success', 'data': resume}) 

@main.route('/get/<resume_id>', methods=['GET'])
@login_required
def get_resume_with_id(resume_id):
    resume = None
    resume = Resume.query.filter_by(id=resume_id, author=current_user.email).first()
    #resume = Resume.query.get(resume_id)
    if resume is not None and resume.resume is not None:
        return jsonify({'status': 'success', 'data': resume.to_json()}) 
    else:
        return jsonify({'status': 'no resume on file... <a href="/new">creeate one</a>', 'data': ''}) 


@main.route('/get_all')
@login_required
def get_all_resume():
    if current_user.is_authenticated:
        resumes = Resume.query.filter_by(author=current_user.email).all()
        if resumes is not None:
            resumes_json = [ r.to_json() for r in resumes ]
            return jsonify({'status': 'success', 'data': resumes_json }) 
        else:
            return jsonify({'status': 'no resume on file... <a href="/new">creeate one</a>', 'data': ''}) 


@main.route('/edit/<id>') 
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
    status = None
    data = None
    if current_user.role.name != 'Administrator':
        resume_ct = Resume.query.filter_by(author=current_user.email).count()
        if resume_ct >= 10:
            return jsonify({'status':'Quota Exceeded', 'data':
                """You can only have 10 Resumes on file, 
            The current resume will exceed that limit.
            Please Cancel or select a Resume to Delete."""})
    try:
        resume_str = json.dumps(request.json)
        resume_jsn = json.loads(resume_str)
        resume_obj = Resume(author=current_user.email, resume_title=resume_jsn['resume_title'], resume=resume_str)
        #resume_obj = Resume.from_json(resume)
        db.session.add(resume_obj)
        db.session.commit()
        status = 'Resume Saved'
        data = resume_obj.id
        return jsonify({'status': status, 'data': data})
    except Exception as e:
         status = 'Error'
         #data = str(e) 
         data = 'Something went wrong :( '
         return jsonify({'status': status, 'data': data})
    #except AttributeError as ae:
    #     status = 'AttributeError'
    #     data = ae 
    #except TypeError as te:
    #     status = 'TypeError'
    #     data = te
    #except IndexError as ie:
    #     status = 'IndexError'
    #     data = ie
    #except KeyError as ke:
    #     status = 'KeyError'
    #     data = ke
    #return jsonify({'status': status, 'data': data})


@main.route('/delete/<resume_id>', methods=['DELETE'])
@login_required
def delete_resume_with_id(resume_id):
    Resume.query.filter(Resume.id == resume_id).delete()
    db.session.commit()
    return jsonify({'status': 'resume deleted', 'data': ''}) 

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


def log(s):
    print('\n')
    print(type(s))
    print(s)
    print('\n')

