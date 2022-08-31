from flask import Blueprint,jsonify,abort,request 
from .models import Student,db

bp = Blueprint('students',__name__,url_prefix='/students')


@bp.route('',methods=['GET'])
def index():
    students = Student.query.all()
    results = []
    for s in students:
        results.append(s.serialize())
    return jsonify(results)

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    s = Student.query.get_or_404(id)
    return jsonify(s.serialize())

@bp.route('',methods=['POST'])
def create():
    if 'name' not in request.json or 'year' not in request.json:
        return abort(400)
    
    s = Student(
        name=request.json['name'],
        year=request.json['year'] 
    )
    
    db.session.add(s)
    db.session.commit()
    
    return jsonify(s.serialize())
    
@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    s = Student.query.get_or_404(id)
    try:
        db.session.delete(s)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route("/<int:id>/registrations")
def registrations(id: int):
    student = Student.query.get_or_404(id)  
    results = []
    for r in student.registrations:
        results.append(r.serialize())
    return jsonify(results)