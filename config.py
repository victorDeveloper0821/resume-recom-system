from dotenv import load_dotenv
import os

load_dotenv('.env')
    
class Config(object): 
    """Global config for Flask Application"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///slide_rater.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'slide_rater_secret_key')
    UPLOAD_FOLDER=" /Users/victortsai/uploads/slide_ranker/"
    ALLOWED_EXTENSIONS = {'ppt','pptx'}
    SCHEDULER_API_ENABLED = True

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