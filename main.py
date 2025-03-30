from flask import Flask
from config import global_config
from db import init_extensions

## initialize app instance
def create_app (env_name):
    # create flask api instance
    app = Flask(__name__)

    # fetch config from env name
    app.config.from_object(global_config[env_name])
    
    # config db
    init_extensions(app=app)

    return app

if __name__ == '__main__':
    try:
        app = create_app('dev')                       
        app.run(host='0.0.0.0', port=51800, debug=True)
    except Exception as e:
        print(f"Error: {e}")