from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    # print(os.environ.get('FLASK_ENV'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config or os.environ.get('FLASK_ENV') == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/task_list_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/task_list_development'

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.task import Task

    from .routes import bp
    app.register_blueprint(bp)

    return app
