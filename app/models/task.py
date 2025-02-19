import datetime

from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))

    def to_json(self):
        is_complete = True if self.completed_at else False

        result = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

        if self.goal_id:
            result["goal_id"] = self.goal_id

        return result

    def update(self, json):
        self.title = json["title"]
        self.description = json["description"]
        self.completed_at = json["completed_at"]

    def mark_complete(self):
        self.completed_at = datetime.datetime.now()

    def mark_incomplete(self):
        self.completed_at = None

    @classmethod
    def from_json(cls, json):
        required_fields = ["title", "description", "completed_at"]
        filtered_json = {}
        for field in required_fields:
            if field not in json:
                return None
            else:
                filtered_json[field] = json[field]

        # completed_at = (
        #     datetime.datetime.fromisoformat(json["completed_at"])
        #     if json["completed_at"] else None
        # )

        inst = cls(**filtered_json)

        return inst
