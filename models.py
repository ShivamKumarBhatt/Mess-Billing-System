from database import db
from datetime import datetime, timezone

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    meals = db.relationship('Meal', backref='student', lazy=True)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    meal1 = db.Column(db.Boolean, nullable=False)
    meal2 = db.Column(db.Boolean, nullable=False)
    meal3 = db.Column(db.Boolean, nullable=False)
    meal4 = db.Column(db.Boolean, nullable=False)

    def __init__(self, student_id, date, meal1, meal2, meal3, meal4):
        self.student_id = student_id
        self.date = date
        self.meal1 = meal1
        self.meal2 = meal2
        self.meal3 = meal3
        self.meal4 = meal4
