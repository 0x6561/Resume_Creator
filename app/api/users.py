from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Resume


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/resumes/')
def get_user_resumes(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.resumes.order_by(Resume.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    resumes = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_resumes', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_resumes', id=id, page=page+1)
    return jsonify({
        'resumes': [resume.to_json() for resume in resumes],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


