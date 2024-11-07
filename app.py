from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_fee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    student_id = request.form['student_id']
    name = request.form['name']
    
    if not student_id or not name:
        return "Student ID and name cannot be empty!", 400
    if Student.query.filter_by(student_id=student_id).first():
        return f"Student with ID {student_id} already exists!", 400

    new_student = Student(student_id=student_id, name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/record_meal', methods=['POST'])
def record_meal():
    student_id = request.form['student_id']
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return f"No student found with ID {student_id}. Please add the student first.", 400

    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    meal1 = 'meal1' in request.form
    meal2 = 'meal2' in request.form
    meal3 = 'meal3' in request.form
    meal4 = 'meal4' in request.form

    new_meal = Meal(student_id=student_id, date=date, meal1=meal1, meal2=meal2, meal3=meal3, meal4=meal4)
    db.session.add(new_meal)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    from_date_str = request.form.get('from_date')
    to_date_str = request.form.get('to_date')

    if from_date_str and to_date_str:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    else:
        from_date = None
        to_date = None

    students = Student.query.all()
    billing_info = []
    if from_date and to_date:
        for student in students:
            total_days = len({meal.date for meal in Meal.query.filter(
                Meal.student_id == student.student_id,
                Meal.date >= from_date,
                Meal.date <= to_date,
                (Meal.meal1 | Meal.meal2 | Meal.meal3 | Meal.meal4)
            ).all()})
            total_fee = total_days * 200
            billing_info.append({
                'student_id': student.student_id,
                'student': student.name,
                'total_days': total_days,
                'total_fee': total_fee
            })

    return render_template('billing.html', billing_info=billing_info, from_date=from_date_str, to_date=to_date_str)

if __name__ == '__main__':
    app.run(debug=True)
