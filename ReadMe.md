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
- `.env.sample` : Environment variables file (include this when deploying).  
- `routes/` (module): Defines API endpoints.  
- `utils/` : Contains shared logic and helper functions.  
**P.S. rename .env.sample to .env or program may not be activated.**

## Start the chatbot 
- Go to mongodb Atlas and login using username: austin@hsingnan.com password: Top122489, remenber to add IP, press add IP on the top.
- Download Ollama: https://ollama.com/
- Pull model `gemma3:4b` : run command `ollama pull gemma3:4b`
- Run `streamlit run app.py`