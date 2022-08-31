from flask import Blueprint,jsonify,abort,request
from .models import Instructor,Department, db 

bp = Blueprint('instructors',__name__,url_prefix='/instructors')


@bp.route('',methods=['GET'])
def index():
    instructors = Instructor.query.all()
    results = []
    for instructor in instructors:
        results.append(instructor.serialize())
    return jsonify(results)

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    instructor = Instructor.query.get_or_404(id)
    return jsonify(instructor.serialize())

@bp.route('',methods=['POST'])
def create():
    if  'name' not in request.json or 'department_id' not in request.json:
        return abort(400)
    
    Department.query.get_or_404(request.json['department_id'])
    
    new_instructor = Instructor(
        department_id=request.json['department_id'],
        name=request.json['name']
    )
    
    db.session.add(new_instructor)
    db.session.commit()
    
    return jsonify(new_instructor.serialize())
    
@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    instructor = Instructor.query.get_or_404(id)
    try:
        db.session.delete(instructor)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

@bp.route("/<int:id>/taught_courses")
def taught_courses(id: int):
    instructor = Instructor.query.get_or_404(id)  
    results = []
    for c in instructor.courses:
        results.append(c.serialize())
    return jsonify(results)