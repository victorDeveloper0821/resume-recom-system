from dotenv import load_dotenv
import os

load_dotenv('.env')
    
class Config(object): 
    """Global config for Flask Application"""
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', "/Users/victortsai/uploads/CSE575/")
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'resume_db')
    SCHEDULER_API_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "ResumeRecommand")
    
class DevelopmentConfig(Config):
    """Development env"""
    DEBUG = True

class ProductionConfig(Config):
    """Production env"""
    DEBUG = False

global_config = {
    'dev': DevelopmentConfig,
    'prod':ProductionConfig,
}