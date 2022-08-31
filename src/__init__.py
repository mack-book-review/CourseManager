import os 
from flask import Flask 
from flask_migrate import Migrate 
from . import courses,students,departments,instructors

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    from .models import Course,Instructor,Student,Department
    
    from .models import db 
    db.init_app(app)
    migrate = Migrate(app,db)
    
    #register blueprints
    app.register_blueprint(courses.bp)
    app.register_blueprint(instructors.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(departments.bp)

    return app