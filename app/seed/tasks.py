from app.models.task import Task
from datetime import datetime, timedelta
import random

from app import db

def load():

    def get_completed_date(base_date=None):
        base_date = base_date or datetime.now()
        offset = random.randint(0, 60 * 24 * 7)
        return base_date - timedelta(minutes=offset)

    for num in range(50):
        params = dict(
            title=f"Task {num}",
            description=f"Description {num}",
            completed_at=get_completed_date() if num % 2 else None
        )

        t = Task(**params)
        db.session.add(t)

    db.session.commit()
