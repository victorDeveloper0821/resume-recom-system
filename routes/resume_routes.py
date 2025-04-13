from flask import request, jsonify
from . import resume_bp  # 匯入 Blueprint

@resume_bp.route('/resumes/<int:id>', methods=['GET'])
def get_resumes(id):
    """Fetch all the resumes"""
    return jsonify([{"id": id, "name": 'tesdt', "text": 'tesdt'} ])

@resume_bp.route('/resumes', methods=['POST'])
def add_resume():
    """Add new resumes"""
    if 'resume' not in request.files:
        return "No file part in the request", 400
    
    resume = request.files['resume']
    if resume.filename == '':
        return "No file selected", 400
    
    extension = resume.filename.split('.')[1]
    if extension not in ['html', 'pdf']: 
        return "invalid file extensions", 400
    
    return jsonify({"message": "Resume added!", "id": 'Dummy IDs'})

@resume_bp.route('/resume/recommand', methods=['GET', 'POST'])
def recommand_resume():
    """Add new resumes"""  
    if 'resume' not in request.files:
        return "No file part in the request", 400
    
    resume = request.files['resume']
    if resume.filename == '':
        return "No file selected", 400
    
    extension = resume.filename.split('.')[1]
    if extension not in ['html', 'pdf']: 
        return "invalid file extensions", 400
    
    return jsonify({"message": "Resume added!", "id": 'Dummy IDs'})