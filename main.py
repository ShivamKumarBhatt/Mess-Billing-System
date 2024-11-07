from flask import Flask
from models import Student, Meal
from database import db, init_db
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_fee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

MEAL_COST_PER_DAY = 200

def add_student(name):
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()

def record_meal(student_id, meals_taken):
    new_meal = Meal(student_id=student_id, meals_taken=meals_taken)
    db.session.add(new_meal)
    db.session.commit()

def calculate_total_fee(student_id):
    total_fee = 0
    meals = Meal.query.filter_by(student_id=student_id).all()
    for meal in meals:
        if meal.meals_taken > 0:
            total_fee += MEAL_COST_PER_DAY
    return total_fee

if __name__ == "__main__":
    while True:
        print("1. Add Student")
        print("2. Record Meal")
        print("3. Calculate Total Fee")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            name = input("Enter student name: ")
            with app.app_context():
                add_student(name)
            print("Student added successfully!")
        elif choice == '2':
            student_id = int(input("Enter student ID: "))
            meals_taken = int(input("Enter number of meals taken: "))
            with app.app_context():
                record_meal(student_id, meals_taken)
            print("Meal record added successfully!")
        elif choice == '3':
            student_id = int(input("Enter student ID: "))
            with app.app_context():
                total_fee = calculate_total_fee(student_id)
            print(f"Total mess fee for student ID {student_id}: {total_fee}")
        elif choice == '4':
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
