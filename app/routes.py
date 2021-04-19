from flask import Blueprint, jsonify, make_response, request

from app import db
from .models.task import Task

print(__name__)

root_bp = Blueprint("root", __name__)
bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@root_bp.route("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"] + new_hobby
    return response_body


@root_bp.route("/", methods=('GET',))
def root():
    return {
        "name": "Joe",
        "message": "Go!"
    }

@root_bp.route("/hello", methods=('GET',))
def hello():
    return make_response({ "detail":"some text" }, 201)


# https://stackoverflow.com/questions/33241050/trailing-slash-triggers-404-in-flask-path-rule
# https://searchfacts.com/url-trailing-slash/
@bp.route("/", methods=('GET', 'POST'), strict_slashes=False)
# @bp.route("/", methods=('GET', 'POST'))
# @bp.route("", methods=('GET', 'POST'))
def tasks_index():
    if request.method == 'GET':
        tasks = Task.query.all()
        json_tasks = [task.to_json() for task in tasks]

        return jsonify(json_tasks)
    elif request.method == 'POST':
        request_body = request.get_json()
        task = Task.from_json(request_body)

        if task:
            db.session.add(task)
            db.session.commit()

            return {
                "task": task.to_json()
            }
        else:
            return {
                "details": "Invalid data"
            }, 400

@bp.route("/<task_id>", methods=('GET', 'PUT', 'DELETE'))
def tasks_show(task_id):
    task = Task.query.filter(Task.task_id == task_id).one_or_none()
    # task = Task.query.get(task_id)
    if not task:
        return "", 404

    if request.method == 'GET':
        return { "task": task.to_json() }
    elif request.method == 'PUT':
        request_body = request.get_json()
        task.update(request_body)
        db.session.commit()

        return { "task": task.to_json() }
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return {
            "details": f'Task {task_id} "{task.title}" successfully deleted'
        }
