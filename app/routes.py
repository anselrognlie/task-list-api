from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import desc
import os

from app import db
from .models.task import Task
from .models.goal import Goal
from .slack.slack_api import SlackApi

# print(__name__)

root_bp = Blueprint("root", __name__)
bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

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
        sort = None
        if 'sort' in request.args:
            sort = 'desc' if request.args.get('sort', 'asc') == 'desc' else 'asc'

        tasks = Task.query
        if sort is not None:
            if sort == 'asc':
                tasks = tasks.order_by(Task.title)
            else:
                tasks = tasks.order_by(desc(Task.title))
        
        tasks = tasks.all()

        json_tasks = [task.to_json() for task in tasks]

        return jsonify(json_tasks)

        # title_query = request.args.get("title")
        # if title_query:
        #     tasks = Task.query.filter_by(title=title_query)
        # else:
        #     tasks = Task.query.all()

        # tasks_response = []
        # for task in tasks:
        #     tasks_response.append({
        #         "id": task.task_id,
        #         "title": task.title,
        #         "description": task.description
        #     })
 
        # return jsonify(tasks_response)

    elif request.method == 'POST':
        request_body = request.get_json()
        task = Task.from_json(request_body)

        if task:
            db.session.add(task)
            db.session.commit()

            return {
                "task": task.to_json()
            }, 201
        else:
            return {
                "details": "Invalid data"
            }, 400

@bp.route("/<task_id>", methods=('GET', 'PUT', 'DELETE'))
def tasks_show(task_id):
    # task = Task.query.filter(Task.task_id == task_id).one_or_none()
    # # task = Task.query.get(task_id)
    # if not task:
    #     return "", 404
    task = Task.query.get_or_404(task_id)

    if request.method == 'GET':
        goal = task.goal
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

@bp.route("/<task_id>/mark_complete", methods=('PATCH',))
def tasks_mark_complete(task_id):
    task = Task.query.filter(Task.task_id == task_id).one_or_none()
    if not task:
        return "", 404

    task.mark_complete()

    db.session.commit()

    api = SlackApi(os.environ.get("SLACK_TOKEN"))
    api.post_message(f"Someone just completed the task {task.title}")

    return { "task": task.to_json() }

@bp.route("/<task_id>/mark_incomplete", methods=('PATCH',))
def tasks_mark_incomplete(task_id):
    task = Task.query.filter(Task.task_id == task_id).one_or_none()
    if not task:
        return "", 404

    task.mark_incomplete()

    db.session.commit()

    return { "task": task.to_json() }


@goal_bp.route("/", methods=('GET', 'POST'), strict_slashes=False)
def handle_goals():
    if request.method == 'GET':
        goals = Goal.query.all()
        json_goals = [goal.to_json() for goal in goals]
        return jsonify(json_goals)

    elif request.method == 'POST':
        request_body = request.get_json()
        goal = Goal.from_json(request_body)

        if goal:
            db.session.add(goal)
            db.session.commit()

            return {
                "goal": goal.to_json()
            }, 201
        else:
            return {
                "details": "Invalid data"
            }, 400

@goal_bp.route("/<goal_id>", methods=('GET', 'PUT', 'DELETE'))
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return "", 404

    if request.method == 'GET':
        return { "goal": goal.to_json() }
    elif request.method == 'PUT':
        request_body = request.get_json()
        goal.update(request_body)
        db.session.commit()

        return { "goal": goal.to_json() }
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()

        return {
            "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
        }

@goal_bp.route("/<goal_id>/tasks", methods=('POST', 'GET'))
def handle_goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return "", 404

    if request.method == 'POST':
        request_body = request.get_json()
        task_ids = request_body["task_ids"]
        # for task_id in task_ids:
        #     task = Task.query.get(task_id)
        #     goal.tasks.append(task)
        # goal.tasks.extend(task_ids)
        tasks = [Task.query.get(task_id) for task_id in task_ids]
        goal.tasks = tasks

        db.session.commit()

        return goal.to_task_json()
    elif request.method == 'GET':
        return goal.to_detailed_json()
