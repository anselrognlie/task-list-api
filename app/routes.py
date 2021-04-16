from flask import Blueprint, jsonify, make_response, request

from app import db
from .models.task import Task

bp = Blueprint("bp", __name__)


@bp.route("/", methods=('GET',))
def root():
    return {
        "name": "Joe",
        "message": "Go!"
    }


@bp.route("/tasks", methods=('GET', 'POST'))
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

@bp.route("/tasks/<task_id>", methods=('GET', 'PUT', 'DELETE'))
def tasks_show(task_id):
    task = Task.query.filter(Task.task_id == task_id).one_or_none()
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
