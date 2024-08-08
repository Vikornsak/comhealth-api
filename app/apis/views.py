import csv
from http import HTTPStatus
from io import StringIO

import arrow as arrow
import pandas as pd
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.orm import joinedload
from . import apis
from flask_restful import Resource
from app.extensions import db
from app.schemas import *



class TokenResource(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = db.session.query(User).filter_by(username=username, password=password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, HTTPStatus.OK



@apis.route('/employees/<string:hnnumber>', methods=['GET'])
# @jwt_required()
def get_employee_with_HN(hnnumber):


    try:


        # Define the schema
        employee_schema = EmployeeSchema()
        services_schema = ServicesSchema()
        physical_exam_schema = PhysicalExamSchema()
        xray_schema = XRaySchema()
        lab_schema = LabSchema()

        # Fetch the employee with all related data
        employee = db.session.query(Employee).options(
            joinedload(Employee.services).joinedload(Services.physical_exam),
            joinedload(Employee.services).joinedload(Services.x_ray),
            joinedload(Employee.services).joinedload(Services.labs).joinedload(Lab.test)
        ).filter_by(HN=hnnumber).first()

        if employee is None:
            return jsonify({'message': 'Employee not found'}), 404

            # Serialize the employee data
        employee_data = employee_schema.dump(employee)

        for service in employee.services:
            service_data = services_schema.dump(service)
            service_data['physical_exam'] = physical_exam_schema.dump(service.physical_exam)
            service_data['x_ray'] = xray_schema.dump(service.x_ray)
            service_data['labs'] = [lab_schema.dump(lab) for lab in service.labs]

            employee_data['services'].append(service_data)

        # Serialize the data


        return jsonify(employee_data, 200)

    except Exception as e:
        return jsonify({'message': str(e)}), 500



@apis.route('/services/<string:serno>', methods=['GET'])
# @jwt_required()
def get_employee_with_services(serno):


    try:

        # Define the schemas
        services_schema = ServicesSchema()
        physical_exam_schema = PhysicalExamSchema()
        xray_schema = XRaySchema()
        lab_schema = LabSchema()

        # Fetch the employee with all related data
        # Fetch the service with all related data
        service = db.session.query(Services).options(
            joinedload(Services.physical_exam),
            joinedload(Services.x_ray),
            joinedload(Services.labs).joinedload(Lab.test)
        ).filter_by(ServiceNo=serno).first()

        if service is None:
            return jsonify({'message': 'Service not found'}), 404

        # Serialize the service data
        service_data = services_schema.dump(service)
        service_data['physical_exam'] = physical_exam_schema.dump(service.physical_exam)
        service_data['x_ray'] = xray_schema.dump(service.x_ray)
        service_data['labs'] = [lab_schema.dump(lab) for lab in service.labs]

        return jsonify(service_data, 200)

    except Exception as e:
        return jsonify({'message': str(e)}), 500




@apis.route('/serviceslabindex_testing/<string:serno>', methods=['GET'])
# @jwt_required()
def get_employee_with_serviceslabindex_test(serno):


    try:


        # Define the schema

        services_schema = ServicesSchema()
        physical_exam_schema = PhysicalExamSchema()
        xray_schema = XRaySchema()
        lab_schema = LabSchema()

        # Fetch the employee with all related data
        service = (db.session.query(Services).filter_by(ServiceNo=serno).first())

        if service is None:
            return jsonify({'message': 'Service not found'}), 404

            # Serialize the employee data
        service_data = services_schema.dump(service)



        return jsonify(service_data, 200)

    except Exception as e:
        return jsonify({'message': str(e)}), 500