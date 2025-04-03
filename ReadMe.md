# CSE575: Resume Recommendation System

This project is an API for a resume recommendation system, developed as part of the NLP project in CSE 575.  

## Overall System Architecture  
- **PostgreSQL**: Stores vector representations of resumes and related document details.  
- **Flask**: API service that integrates Hugging Face transformers to process resume text.  
- **Hugging Face**: Utilized for NLP tasks and model inference.  

## Project Structure  
- `requirements.txt` : Lists necessary packages for the project.  
- `main.py` : Entry point for the Python application.  
- `db.py` : Configures database connections.  
- `config.py` : Fetches environment variables from `.env`.  
- `.env` : Environment variables file (include this when deploying).  
- `routes/` (module): Defines API endpoints.  
- `utils/` : Contains shared logic and helper functions.  