from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from models import User

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
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('index'))

    @app.route('/signup ', methods=['POST', 'GET'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(name = username, password = hashed_password, role = "1")

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))

    @app.route('/login ', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.name == username).first()

            if user is None:
                return 'Failed'
            else:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    return 'Failed'

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/secret')
    @login_required
    def secret():
        if current_user.role == "1":
            return 'Secret Message'
        elif current_user.role == "2":
            return 'Secret Message 2'
        else:
            return 'Open Message'

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
        


    