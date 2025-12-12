from flask import render_template, request, redirect, url_for, jsonify, make_response
import jwt
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from functools import wraps
from datetime import datetime, timezone, timedelta

from models import User, Department

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
                return redirect(url_for('dashboard'))
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')

            hashed_password = bcrypt.generate_password_hash(password)

            existing_user = User.query.filter_by(name = username).first()
            
            if existing_user:
                return jsonify({'message': 'User already exists. Please login.'}), 400

            user = User(name = username, password = hashed_password, role = role)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    @app.route('/login ', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            token = request.cookies.get('jwt_token')
            if not token:
                return render_template('login.html')
            else:
                return redirect(url_for('dashboard'))
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
        if current_user.role == 'admin':
            departments = Department.query.all()
            doctors = User.query.filter(User.role == 'doctor').all()

            return render_template(
                'admin_dashboard.html', 
                current_user = current_user, 
                departments = departments,
                doctors = doctors
            )
        elif current_user.role == 'doctor':
            return render_template('doctor_dashboard.html', current_user = current_user)
        else:
            return render_template('member_dashboard.html', current_user = current_user) 
    
    # DEPARTMENT 
    @app.route('/add_department', methods=['POST', 'GET'])
    def add_department():
        if request.method == 'GET':
            doctors = User.query.filter_by(role = 'doctor').all()
            return render_template('add_department.html', doctors = doctors)
        elif request.method == 'POST':
            name = request.form['department_name']
            doctor_id = request.form['doctor_id']

            new_department = Department(
                name=name,
                doctor_id=doctor_id if doctor_id != "" else None
            )

            db.session.add(new_department)
            db.session.commit()

            return redirect(url_for('dashboard'))

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
            doctors = User.query.filter_by(role = 'doctor').all()
            return render_template('update_department.html', department=department, doctors = doctors)

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