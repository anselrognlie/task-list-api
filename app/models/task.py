from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_json(self):
        is_complete = True if self.completed_at else False

        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    def update(self, json):
        self.title = json["title"]
        self.description = json["description"]
        self.completed_at = json["completed_at"]

    @classmethod
    def from_json(cls, json):
        required_fields = ["title", "description", "completed_at"]
        for field in required_fields:
            if field not in json:
                return None


        inst = cls(
            title=json["title"],
            description=json["description"],
            completed_at=json["completed_at"]
        )

        return inst
