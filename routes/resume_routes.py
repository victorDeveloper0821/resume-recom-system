from flask import request, jsonify, current_app
from . import resume_bp  # import blueprints
import os
import pandas as pd
from utils.ResumeParser import get_resume_parser
from db import get_resume_collection
from utils.SerialUtils import generate_serial_id
import numpy as np

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
    
    ## get file extensions 
    extension = os.path.splitext(resume.filename)[1].lower()
    if extension.lower() not in ['.html', '.htm', '.pdf']: 
        return "invalid file extensions", 400
    
    ## upload folders
    Folders = current_app.config['UPLOAD_FOLDER']
    if resume : 
        file_path = os.path.join(Folders, resume.filename)
        resume.save(file_path)

    ### parse the resume here 
    try:
        parser = get_resume_parser(file_path=file_path)
        ## parse data into json format
        parsed_data = parser.extract_text()
    except Exception as e:
        return f"Failed to parse resume: {str(e)}", 500
    serialID = generate_serial_id(secret_key=current_app.config['SECRET_KEY'],prefix="RES")
    parsed_data['serialID'] = serialID
    ## insert one data to mongodb 
    collection = get_resume_collection()
    collection.insert_one(parsed_data)
    parsed_data.pop('_id', None)
    return jsonify({
        "message": "Resume parsed and added!",
        "data": parsed_data,
        "SerialID": serialID
    }), 200
    
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

@resume_bp.route('/resume/import', methods=['POST'])
def import_trainingData ():
    """Import training csv data"""
    collection = get_resume_collection()
    
    if 'training' not in request.files: 
        return "No file part in the request", 400
    trainingData = request.files['training']
    if trainingData.filename == '':
        return "No file selected", 400
    
    ## get file extensions 
    extension = os.path.splitext(trainingData.filename)[1].lower()
    if extension.lower() not in ['.csv']: 
        return "unsupported file extensions", 400
    
    ## upload folders
    Folders = current_app.config['UPLOAD_FOLDER']
    if trainingData : 
        file_path = os.path.join(Folders, trainingData.filename)
        trainingData.save(file_path)
    
    ## Training data sets 
    train_df = pd.read_csv(file_path)
    
    if 'Resume_html' not in train_df.columns: 
         return "html texts not exist", 401
    
    htmls = train_df['Resume_html'].to_list()
    training = list()
    for html in htmls:
        serialID = generate_serial_id(secret_key=current_app.config['SECRET_KEY'],prefix="RES")
        resumeObj = get_resume_parser(html_text=html).extract_text()
        resumeObj["SerialID"] = serialID
        training.append(resumeObj)
    collection.insert_many(training)
    return 'Insert successful', 200