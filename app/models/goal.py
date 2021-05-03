from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    def update(self, json):
        self.title = json["title"]

    def to_task_json(self):
        tasks = self.tasks
        task_ids = [task.task_id for task in tasks]

        return {
            "id": self.goal_id,
            "task_ids": task_ids
        }

    def to_detailed_json(self):
        result = self.to_json()

        tasks = self.tasks
        tasks_json = [task.to_json() for task in tasks]
        result["tasks"] = tasks_json

        return result

    @classmethod
    def from_json(cls, json):
        required_fields = ["title"]
        for field in required_fields:
            if field not in json:
                return None


        inst = cls(
            title=json["title"]
        )

        return inst
