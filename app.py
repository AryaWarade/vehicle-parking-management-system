import os
from dotenv import load_dotenv
from flask import Flask, render_template , flash, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.parking_controller import parking_bp
from controllers.admin_controller import admin_bp
from models import db,User, ParkingLot, ParkingSpot, Reservation
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.jinja_env.globals.update(now=datetime.now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vdatabase.db'  
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  

# link db to app
db.init_app(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(user=current_user)


def create_admin():
    user_exists = User.query.filter_by(is_admin=True).first()
    if not user_exists:
        admin = User(
            email='admin@example.com', 
            password=generate_password_hash('passadmin'),  
            is_admin=True, 
            full_name='Admin User', 
            address='123 Admin Street',  
            pin_code='123456'  
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin created')
    else:
        print('Admin already exists')


app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(parking_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('landing.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)
