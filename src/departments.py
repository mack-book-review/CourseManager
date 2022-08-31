from flask import Blueprint,abort,jsonify,request
from .models import Department,db


bp = Blueprint('departments',__name__,url_prefix='/departments')

@bp.route('',methods=['GET'])
def index():
    departments = Department.query.all()
    results = []
    for d in departments:
        results.append(d.serialize())
    return jsonify(results)

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    d = Department.query.get_or_404(id)
    return jsonify(d.serialize())

@bp.route('',methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)
    
    
    d = Department(
        name=request.json['name']
    )
    
    db.session.add(d)
    db.session.commit()
    
    return jsonify(d.serialize())
    
@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    d = Department.query.get_or_404(id)
    try:
        db.session.delete(d)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    
@bp.route("/<int:id>/instructors")
def department_instructors(id: int):
    department = Department.query.get_or_404(id)  
    results = []
    for d in department.instructors:
        results.append(d.serialize())
    return jsonify(results)