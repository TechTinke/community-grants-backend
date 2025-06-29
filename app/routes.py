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

@bp.route('/applications', methods=['GET'])
def get_applications():
    grant_id = request.args.get('grant_id', type=int)
    if grant_id:
        applications = Application.query.filter_by(grant_id=grant_id).all()
    else:
        applications = Application.query.all()
    return jsonify([{
        'id': app.id,
        'grant_id': app.grant_id,
        'applicant_name': app.applicant_name,
        'applicant_email': app.applicant_email,
        'proposal': app.proposal,
        'status': app.status,
        'submitted_at': app.submitted_at.isoformat()
    } for app in applications])

@bp.route('/applications', methods=['POST'])
def create_application():
    data = request.get_json()
    if not data or not all(key in data for key in ['grant_id', 'applicant_name', 'applicant_email', 'proposal']):
        return jsonify({'error': 'Missing required fields'}), 400
    application = Application(
        grant_id=data['grant_id'],
        applicant_name=data['applicant_name'],
        applicant_email=data['applicant_email'],
        proposal=data['proposal'],
        status='pending'
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({
        'id': application.id,
        'grant_id': application.grant_id,
        'applicant_name': application.applicant_name,
        'applicant_email': application.applicant_email,
        'proposal': application.proposal,
        'status': application.status,
        'submitted_at': application.submitted_at.isoformat()
    }), 201

@bp.route('/applications/<int:id>', methods=['PUT'])
def update_application(id):
    application = Application.query.get_or_404(id)
    data = request.get_json()
    if not data or not all(key in data for key in ['grant_id', 'applicant_name', 'applicant_email', 'proposal']):
        return jsonify({'error': 'Missing required fields'}), 400
    application.grant_id = data['grant_id']
    application.applicant_name = data['applicant_name']
    application.applicant_email = data['applicant_email']
    application.proposal = data['proposal']
    application.status = data.get('status', application.status)
    db.session.commit()
    return jsonify({
        'id': application.id,
        'grant_id': application.grant_id,
        'applicant_name': application.applicant_name,
        'applicant_email': application.applicant_email,
        'proposal': application.proposal,
        'status': application.status,
        'submitted_at': application.submitted_at.isoformat()
    })

@bp.route('/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return jsonify({'message': 'Application deleted'})

@bp.route('/feedback', methods=['GET'])
def get_feedbacks():
    grant_id = request.args.get('grant_id', type=int)
    if grant_id:
        feedbacks = Feedback.query.filter_by(grant_id=grant_id).all()
    else:
        feedbacks = Feedback.query.all()
    return jsonify([{
        'id': feedback.id,
        'grant_id': feedback.grant_id,
        'commenter_name': feedback.commenter_name,
        'commenter_email': feedback.commenter_email,
        'comment': feedback.comment,
        'rating': feedback.rating
    } for feedback in feedbacks])

@bp.route('/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json()
    if not data or not all(key in data for key in ['grant_id', 'commenter_name', 'commenter_email', 'comment', 'rating']):
        return jsonify({'error': 'Missing required fields'}), 400
    feedback = Feedback(
        grant_id=data['grant_id'],
        commenter_name=data['commenter_name'],
        commenter_email=data['commenter_email'],
        comment=data['comment'],
        rating=data['rating']
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({
        'id': feedback.id,
        'grant_id': feedback.grant_id,
        'commenter_name': feedback.commenter_name,
        'commenter_email': feedback.commenter_email,
        'comment': feedback.comment,
        'rating': feedback.rating
    }), 201