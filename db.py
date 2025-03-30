from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

## initialize database configs
def init_extensions(app):
    db.init_app(app)