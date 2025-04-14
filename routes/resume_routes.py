from flask import request, jsonify, current_app
from . import resume_bp  # 匯入 Blueprint
import os
from utils.ResumeParser import get_resume_parser

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
    
    extension = os.path.splitext(resume.filename)[1].lower()
    if extension.lower() not in ['.html', '.htm', '.pdf']: 
        return "invalid file extensions", 400
    Folders = current_app.config['UPLOAD_FOLDER']
    if resume : 
        file_path = os.path.join(Folders, resume.filename)
        resume.save(file_path)
        
    ### parse the resume here 
    try:
        parser = get_resume_parser(file_path=file_path)
        parsed_data = parser.extract_text()
    except Exception as e:
        return f"Failed to parse resume: {str(e)}", 500

    return jsonify({
        "message": "Resume parsed and added!",
        "parsed_data": parsed_data
    }), 200
    
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