from flask import Blueprint, jsonify,abort,request 
from .models import Instructor,Course,db

bp = Blueprint('courses',__name__,url_prefix='/courses')

@bp.route('',methods=['GET'])
def index():
    courses = Course.query.all()
    results = []
    for course in courses:
        results.append(course.serialize())
    return jsonify(results)

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize())

@bp.route('',methods=['POST'])
def create():
    if 'instructor_id' not in request.json or 'name' not in request.json or 'description' not in request.json:
        return abort(400)
    
    Instructor.query.get_or_404(request.json['instructor_id'])
    
    c = Course(
        instructor_id=request.json['instructor_id'],
        name=request.json['name']
    )
    
    if "description" in request.json["description"]:
         c.description=request.json["description"]
    
    if "total_credits" in request.json["total_credits"]:
        c.total_credits = request.json["total_credits"]
    
    db.session.add(c)
    db.session.commit()
    
    return jsonify(c.serialize())
    
@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    c = Course.query.get_or_404(id)
    try:
        db.session.delete(c)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    

@bp.route("/<int:id>/registrations")
def registrations(id: int):
    course = Course.query.get_or_404(id)  
    results = []
    for r in course.registrations:
        results.append(r.serialize())
    return jsonify(results)
    
    