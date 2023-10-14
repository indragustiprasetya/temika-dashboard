from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from Functions.connection import connect_employee
from datetime import timedelta
from bson import ObjectId

app = Flask(__name__)
app.secret_key = '42NttCWm$qTw7DzM'

def create_app():
    # Configure the app
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)
    return app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    db, _, user_coll = connect_employee()

    connected = user_coll.find_one({"username": username, "password": password})

    if connected:
        session['authenticated'] = True
        return redirect(url_for('dashboard'))
    else:
        return jsonify({"error": "Login failed. Please try again."})

    
@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('index'))

    _, employee_coll, _ = connect_employee()

    # Count the total number of employees
    employee_count = employee_coll.count_documents({})

    # Fetch employee details (example: fetching the first employee)
    first_employee = employee_coll.find_one()

    return render_template('dashboard.html', employee_count=employee_count, first_employee=first_employee)


@app.route('/employees')
def employee_page():
    if not session.get('authenticated'):
        return redirect(url_for('index'))

    _, employee_coll, _ = connect_employee()

    # Fetch all employees
    employees = list(employee_coll.find())

    return render_template('employee_page.html', employees=employees)


@app.route('/profiles/<employee_id>')
def employee_profile(employee_id):
    try:
        # Convert employee_id to a valid ObjectId
        employee_object_id = ObjectId(employee_id)
    except:
        # Handle the case where employee_id is not a valid ObjectId
        return "Invalid employee ID", 400

    _, employee_coll, _ = connect_employee()
    employee = employee_coll.find_one({"_id": employee_object_id})

    if not employee:
        return "Employee not found", 404

    return render_template('profiles.html', employee=employee)


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)


if __name__ == '__main__':
    app.run(debug=True, port=9090)
