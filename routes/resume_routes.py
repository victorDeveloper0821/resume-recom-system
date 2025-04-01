from flask import request, jsonify
from . import resume_bp  # 匯入 Blueprint

@resume_bp.route('/resumes', methods=['GET'])
def get_resumes():
    """Fetch all the resumes"""
    return jsonify([{"id": 'tesdt', "name": 'tesdt', "text": 'tesdt'} ])

@resume_bp.route('/resumes', methods=['POST'])
def add_resume():
    """Add new resumes"""
    data = request.json
    
    return jsonify({"message": "Resume added!", "id": 'Dummy IDs'})

@resume_bp.route('/resume/recommand', methods=['GET', 'POST'])
def recommand_resume():
    """Add new resumes"""  
    return jsonify({"message": "Resume added!", "id": 'Dummy IDs'})