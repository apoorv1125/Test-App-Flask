from flask import render_template, request, redirect, url_for, jsonify, make_response
import jwt
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from functools import wraps
from sqlalchemy import func
from datetime import datetime, timezone, timedelta

from models.User.user_model import User, UserRole
from models.Department.department_model import Department
from models.Availability.availability_model import Availability
from models.Appointment.appointment_model import Appointment

# def register_route(app, db):
#     @app.route('/', methods=['POST', 'GET'])
#     def index():
#         if request.method == 'POST':
#             name = request.form['name']
#             age = request.form['age']
#             person = Person(name = name, age = age)
#             # try:
#             db.session.add(person)
#             db.session.commit()
#             persons = Person.query.all()
#             return render_template('index.html', people = persons)
#                 # return redirect('/')
#             # except:
#                 # return 'There was an issue adding your task'
#         else:
#             persons = Person.query.all()
#             return render_template('index.html', people = persons)
"""
def register_route(app, db, bcrypt):

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    # @login_manager.unauthorized_handler
    # def unauthorized_callback():
        # return redirect(url_for('index'))

    # USER AUTH
    @app.route('/signup ', methods=['POST', 'GET'])
    def signup():
        if request.method == 'GET':
            token = request.cookies.get('jwt_token')
            if not token:
                return render_template('signup.html')
            else:
                try:
                    jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                    return redirect(url_for('dashboard'))
                except:
                    return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            role = UserRole(request.form.get('role')) # (request.form.get('role'))

            hashed_password = bcrypt.generate_password_hash(password)

            existing_user = User.query.filter(                            
                func.lower(User.name) == username.lower()
            ).first()
            
            if existing_user:
                return jsonify({'message': 'User already exists. Please login.'}), 400

            user = User(name = username, password = hashed_password, role = role)

            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            except:
                return 'There was a problem with that task'

    @app.route('/login ', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            token = request.cookies.get('jwt_token')
            if not token:
                return render_template('login.html')
            else:
                try:
                    jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                    return redirect(url_for('dashboard'))
                except:
                    return render_template('login.html')
                
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.name == username).first()

            if user is None:
                return jsonify({'message': 'Invalid email or password'}), 401
            else:
                if bcrypt.check_password_hash(user.password, password):
                    # login_user(user)
                    # return redirect(url_for('index'))

                    token = jwt.encode({
                        'username': user.name,
                        'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
                        app.config['SECRET_KEY'], 
                        algorithm="HS256"
                    )

                    response = make_response(redirect(url_for('dashboard')))
                    response.set_cookie('jwt_token', token)
                    return response
                
                else:
                    return jsonify({'message': 'Invalid email or password'}), 401

    # Token decorator
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('jwt_token')

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(name = data['username']).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)
        
        return decorated

    # @app.route('/logout')
    # def logout():
        # logout_user()
        # return redirect(url_for('index'))
    
    @app.route('/logout')
    def logout():
        response = make_response(redirect(url_for('index')))
        response.set_cookie('jwt_token', '', expires=0)
        return response

    @app.route('/dashboard')
    @token_required
    def dashboard(current_user):
        if current_user.role == UserRole.ADMIN:
            departments = Department.query.all()
            doctors = User.query.filter(User.role == UserRole.DOCTOR).all()
            appointments = Appointment.query.filter().all()

            return render_template(
                'admin_dashboard.html', 
                current_user = current_user, 
                departments = departments,
                doctors = doctors,
                appointments = appointments
            )
        elif current_user.role == UserRole.DOCTOR:
            availability = User.query.filter(User.uid == current_user.uid).first()
            available_slots = Availability.query.filter(Availability.doctor_id == current_user.uid).all()
            appointments = Appointment.query.filter(Appointment.doctor_id == current_user.uid).all()

            return render_template(
                'doctor_dashboard.html', 
                availability = availability,
                available_slots = available_slots,
                appointments = appointments,
            )
        else:
            appointment = User.query.filter(User.uid == current_user.uid).first()
            appointments = Appointment.query.filter(Appointment.member_id == current_user.uid).all()

            return render_template(
                'member_dashboard.html', 
                appointment = appointment,
                appointments = appointments
            )
    
    # DEPARTMENT 
    @app.route('/add_department', methods=['POST', 'GET'])
    def add_department():
        if request.method == 'GET':
            doctors = User.query.filter_by(role = UserRole.DOCTOR).all()
            return render_template('add_department.html', doctors = doctors)
        elif request.method == 'POST':
            name = request.form['department_name']
            doctor_id = request.form['doctor_id']

            existing_department = Department.query.filter_by(
                func.lower(Department.name) == name.lower()
            ).first()

            if existing_department:
                return jsonify({'message': 'Department already exists. Please try with different name.'}), 400


            new_department = Department(
                name = name,
                doctor_id = doctor_id if doctor_id != "" else None
            )

            try:
                db.session.add(new_department)
                db.session.commit()
                return redirect(url_for('dashboard'))
            except:
                return 'There was a problem with that task'

    @app.route('/delete/department/<int:id>')
    def delete_department(id):
        department_to_delete = Department.query.get_or_404(id)

        try:
            db.session.delete(department_to_delete)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return 'There was a problem deleting that task'

    @app.route('/delete/doctor/<int:id>')
    def delete_doctor(id):
        doctor_to_delete = User.query.get_or_404(id)

        try:
            db.session.delete(doctor_to_delete)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return 'There was a problem deleting that task'

    @app.route('/update/department/<int:id>', methods=['GET', 'POST'])
    def update_department(id):
        department = Department.query.get_or_404(id)

        if request.method == 'POST':
            department.name = request.form['department_name']
            department.doctor_id = request.form['doctor_id']
            try:
                db.session.commit()
                return redirect(url_for('dashboard'))
            except:
                return 'There was a problem deleting that task'
        else:
            doctors = User.query.filter_by(role = UserRole.DOCTOR).all()
            return render_template('update_department.html', department=department, doctors = doctors)

    # Doctors Availability
    @app.route('/add_availability/<int:doctor_id>', methods=['POST', 'GET'])
    def add_availability(doctor_id):
        if request.method == 'GET':
            return render_template('add_availability.html', doctor_id = doctor_id)
        elif request.method == 'POST':
            date = request.form['date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']

            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()

            existing_slots = Availability.query.filter_by(
                doctor_id = doctor_id,
                date = date_obj
            ).all()

            for slot in existing_slots:
                if start_time_obj < slot.end_time and end_time_obj > slot.start_time:
                    return f"Conflict: Existing slot {slot.start_time}-{slot.end_time}", 400

            availability = Availability(
                date = date_obj,
                start_time = start_time_obj,
                end_time = end_time_obj,
                doctor_id = doctor_id if doctor_id != "" else None
            )

            try:
                db.session.add(availability)
                db.session.commit()
                return redirect(url_for('dashboard'))
            except:
                return 'There was a problem deleting that task'
            
    @app.route('/delete/slot/<int:id>')
    def delete_slot(id):
        slot_to_delete = Availability.query.get_or_404(id)

        try:
            db.session.delete(slot_to_delete)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return 'There was a problem deleting that task'
        
    # Members Appointment
    @app.route('/add_appointment/<int:member_id>', methods=['POST', 'GET'])
    def add_appointment(member_id):
        if request.method == 'GET':
            doctors = User.query.filter(User.role == UserRole.DOCTOR).all()
            return render_template('add_appointment.html', member_id = member_id, doctors = doctors)
        elif request.method == 'POST':
            date = request.form['date']
            doctor_id = request.form['doctor_id']
            start_time = request.form['start_time']
            end_time = request.form['end_time']

            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()

            existing_slots = Appointment.query.filter_by(
                doctor_id = doctor_id,
                date = date_obj
            ).all()

            for slot in existing_slots:
                if start_time_obj < slot.end_time and end_time_obj > slot.start_time:
                    return f"Conflict: Existing appointment in this slot {slot.start_time}-{slot.end_time}", 400
    
            existing_availability = Availability.query.filter_by(
                doctor_id = doctor_id,
                date = date_obj
            ).all()

            if not existing_availability:
                return "Doctor has no availability on this date", 400
            
            fits_in_availability = False
            for avail in existing_availability:
                if start_time_obj >= avail.start_time and end_time_obj <= avail.end_time:
                    fits_in_availability = True
                    break

            if not fits_in_availability:
                return f"Appointment time {start_time_obj}-{end_time_obj} is outside availability availability", 400

            appointment = Appointment(
                date = date_obj,
                start_time = start_time_obj,
                end_time = end_time_obj,
                doctor_id = doctor_id if doctor_id != "" else None,
                member_id = member_id if member_id != "" else None
            )

            try:
                db.session.add(appointment)
                db.session.commit()
                return redirect(url_for('dashboard'))
            except:
                return 'There was a problem that task'

    @app.route('/delete/appointment/<int:id>')
    def delete_appointment(id):
        slot_to_delete = Appointment.query.get_or_404(id)

        try:
            db.session.delete(slot_to_delete)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return 'There was a problem deleting that task'
         
    @app.route('/')
    def index():
        return render_template('index.html')
    
        if request.method == 'POST':
            name = request.form.get('name')
            role = request.form.get('role')
            password = request.form.get('password')
            user = User(name = name, password = password, role = role)

            db.session.add(user)
            db.session.commit()
            user = User.query.all()
            return render_template('index.html', user = user)
        else:
            user = User.query.all()
            return render_template('index.html', user = user)
"""