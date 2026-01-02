from flask import Flask
from flask_migrate import Migrate
from extension import db, jwt
from presentation.auth import auth_bp
from presentation.admin.admin_department import admin_bp
from presentation.doctor.doctor_availability import doctor_bp
from presentation.member.member_appointment import member_bp
from presentation.department import department_bp
from presentation.reimbursement import reimbursement_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testuser.db'
    app.secret_key = 'SECRET'
    app.config['SECRET_KEY'] = 'SECRET'

    db.init_app(app)
    jwt.init_app(app)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(department_bp, url_prefix="/department")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(member_bp, url_prefix="/member")
    app.register_blueprint(reimbursement_bp, url_prefix="/reimbursement")

    with app.app_context():
        db.create_all()

    return app