from flask import jsonify, request, g, url_for, current_app
import json
from .. import db
from ..models import Resume, Permission, User, Role
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/resumes/')
def get_resumes():
    page = request.args.get('page', 1, type=int)
    pagination = Resume.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    resumes = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_resumes', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_resumes', page=page+1)
    return jsonify({
        'resumes': [resume.to_json() for resume in resumes],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/resumes/<int:id>')
def get_resume(id):
    resume = Resume.query.get_or_404(id)
    return jsonify(resume.to_json())


@api.route('/resumes/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_resume():
    resume = json.dumps(request.json)
    author = g.current_user.email
    rsm = Resume(author=author, resume=resume)
    print('Resume: - > ' + str(rsm))
    db.session.add(rsm)
    db.session.commit()
    return 'saved', 201
    #return jsonify(resume.to_json()), 201, \
    #    {'Location': url_for('api.get_resume', id=resume.id)}


@api.route('/resumes/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_resume(id):
    resume = Resume.query.get_or_404(id)
    if g.current_user != resume.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    resume.body = request.json.get('body', resume.body)
    db.session.add(resume)
    db.session.commit()
    return jsonify(resume.to_json())
