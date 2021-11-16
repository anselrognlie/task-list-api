from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, BadRequest
from dotenv import load_dotenv
import os


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

# def handle_invalid_usage(error):
#     response = jsonify(error.description)
#     response.status_code = error.code
#     return response
    
def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # if test_config:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_test'
    # else:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_development'

    # db.init_app(app)
    # migrate.init_app(app, db)

    # from .models.task import Task

    from .routes import root_bp, bp, goal_bp
    app.register_blueprint(root_bp)
    app.register_blueprint(bp)
    app.register_blueprint(goal_bp)

    # app.errorhandler(NotFound)(handle_invalid_usage)
    # app.errorhandler(BadRequest)(handle_invalid_usage)

    @app.errorhandler(NotFound)
    @app.errorhandler(BadRequest)
    def handle_invalid_usage(error):
        return jsonify(None), error.code  # terrible

    return app
