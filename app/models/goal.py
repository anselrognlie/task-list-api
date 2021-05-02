from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    def update(self, json):
        self.title = json["title"]

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
