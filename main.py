from flask import Flask
from config import global_config
from db import init_extensions
from routes import resume_bp

## initialize app instance
def create_app (env_name):
    # create flask api instance
    app = Flask(__name__)

    # fetch config from env name
    app.config.from_object(global_config[env_name])
    
    # Config MongoDB
    init_extensions(app=app)
    
    ## register blue print
    app.register_blueprint(resume_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    try:
        app = create_app('dev')                       
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        print(f"Error: {e}")