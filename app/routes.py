from flask import Blueprint, jsonify, request
from . import db
from .models import Grant, Application, Feedback

bp = Blueprint('routes', __name__)

@bp.route('/grants', methods=['GET'])
def get_grants():
    grants = Grant.query.order_by(Grant.id).all()
    return jsonify([{
        'id': grant.id,
        'title': grant.title,
        'description': grant.description,
        'eligibility': grant.eligibility,
        'deadline': grant.deadline.isoformat(),
        'category': grant.category
    } for grant in grants])

@bp.route('/grants/<int:id>', methods=['GET'])
def get_grant(id):
    grant = Grant.query.get_or_404(id)
    return jsonify({
        'id': grant.id,
        'title': grant.title,
        'description': grant.description,
        'eligibility': grant.eligibility,
        'deadline': grant.deadline.isoformat(),
        'category': grant.category
    })

@bp.route('/applications', methods=['POST'])
def create_application():
    data = request.get_json()
    application = Application(
        grant_id=data['grant_id'],
        applicant_name=data['applicant_name'],
        applicant_email=data['applicant_email'],
        proposal=data['proposal']
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Application submitted'}), 201

@bp.route('/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback = Feedback(
        grant_id=data['grant_id'],
        commenter_name=data['commenter_name'],
        commenter_email=data['commenter_email'],
        comment=data['comment'],
        rating=data['rating']
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted'}), 201