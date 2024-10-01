from flask import Blueprint, jsonify, request
from .models import Assignment, Teacher  # Adjust based on your ORM setup

principal_bp = Blueprint('principal', __name__)

@principal_bp.route('/assignments', methods=['GET'])
def get_assignments():
    assignments = Assignment.query.filter(
        (Assignment.state == 'SUBMITTED') | (Assignment.state == 'GRADED')
    ).all()
    return jsonify({"data": [assignment.to_dict() for assignment in assignments]}), 200

@principal_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify({"data": [teacher.to_dict() for teacher in teachers]}), 200

@principal_bp.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    data = request.get_json()
    assignment = Assignment.query.get(data['id'])
    if assignment:
        assignment.grade = data['grade']
        assignment.state = 'GRADED'
        # Assuming there's a method to save the changes
        save_assignment(assignment)
        return jsonify({"data": assignment.to_dict()}), 200
    return jsonify({"error": "Assignment not found"}), 404
