from http import HTTPStatus
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restx import Resource
from sqlalchemy.orm import joinedload


from . import apis  # Import the apis blueprint
from app.apis.schemas import *
from flasgger.utils import swag_from

user_schema = UserSchema()
# emp_schema = EmployeeSchema()


class TokenResource(Resource):
    @swag_from({
        'tags': ['User'],
        'description': 'User Authentication',
        'parameters': [
            {
                'name': 'username',
                'in': 'body',
                'type': 'string',
                'required': True,
                'description': 'User’s username'
            },
            {
                'name': 'password',
                'in': 'body',
                'type': 'string',
                'required': True,
                'description': 'User’s password'
            }
        ],
        'responses': {
            200: {
                'description': 'Authentication successful',
                'schema': {'type': 'object', 'properties': {'access_token': {'type': 'string'}}}
            },
            401: {
                'description': 'Invalid username or password'
            }
        }
    })

    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = db.session.query(User).filter_by(username=username, password=password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK

class CustomerServices(Resource):
    @jwt_required()
    @swag_from({
        'tags': ['Customer'],
        'description': 'Require Authentication first, Fetch employee by customer ID',
        'parameters': [
            {
                'name': 'customer_number',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Customer number to retrieve employee data'
            }
        ],
        'responses': {
            200: {
                'description': 'Employee data retrieved',
                'schema': {'type': 'object',
                           "properties": {
                                "cmsCode": {"type": "string"},
                                "CustID": {"type": "string"},
                                "CID": {"type": "string"},
                                "DeptCode": {"type": "string"},
                                "email": {"type": "string", "format": "email"},
                                "EmpID": {"type": "string"},
                                "prename": {"type": "string"},
                                "Fname": {"type": "string"},
                                "Mname": {"type": "string"},
                                "Lname": {"type": "string"},
                                "OFName": {"type": "string"},
                                "OLName": {"type": "string"},
                                "Status": {"type": "string"},
                                "BirthDate": {"type": "string", "format": "date"},
                                "Age": {"type": "integer"},
                                "Sex": {"type": "string"},
                                "BldGrp": {"type": "string"},
                                "Drug_Allergy": {"type": "string"},
                                "Others": {"type": "string"},
                                "phone": {"type": "string"},
                                "Mobile": {"type": "string"},
                                "UpdateDate": {"type": "string", "format": "date-time"},
                                "EmpStatusCode": {"type": "string"},
                                "CustName": {"type": "string"},
                                "SubDept1Code": {"type": "string"},
                                "SubDept2Code": {"type": "string"},
                                "PositionName": {"type": "string"},
                                "DeptName": {"type": "string"},
                                "SubDept1Name": {"type": "string"},
                                "SubDept2Name": {"type": "string"},
                                "EmpStatusName": {"type": "string"},
                                "CompanyTXT": {"type": "string"},
                                "CompnayCode": {"type": "string"},
                                "Location": {"type": "string"},
                                "Location_CID": {"type": "string"},
                                "Tel_CID": {"type": "string"},
                                "HN": {"type": "string"}
                        }
                }
            },
            404: {
                'description': 'Employee not found'
            }
        }
    })
    def get(self) :
        custid = request.args.get("customer_number")
        employee = db.session.query(Employee).filter_by(CustID=custid).first()
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        employee_data = EmployeeSchema().dump(employee)
        return jsonify(employee_data), 200
        # try
        #     employee_schema = EmployeeSchema()
        #     employee = db.session.query(Employee).options(
        #             joinedload(Employee.services)
        #
        #         ).filter_by(CustID=custid)
        #     if employee is None:
        #         return jsonify({'message': 'Employee not found'}), 404
        #
        #     employee_data = employee_schema.dump(employee)
        #
        #
        #     return jsonify(employee_data, 200)
        #
        # except Exception as e:
        #     return jsonify({'message': str(e)}), 500


class PersonalHealthServices(Resource):
    @jwt_required()

    def get(self) :
        hn = request.json.get("hnnumber", None)
        try:

            # Define the schema
            employee_schema = EmployeeSchema()
            services_schema = ServicesSchema()
            physical_exam_schema = PhysicalExamSchema()
            xray_schema = XRaySchema()
            lab_schema = LabSchema()

            # Fetch the employee with all related data
            employee = db.session.query(Employee).options(
                joinedload(Employee.services)

            ).filter_by(HN=hn).first()

            if employee is None:
                return jsonify({'message': 'Employee not found'}), 404

            employee_data = employee_schema.dump(employee)



            return jsonify(employee_data, 200)

        except Exception as e:
            return jsonify({'message': str(e)}), 500



class PersonalHealthResultDump(Resource):
    @jwt_required()
    def get(self) :
        hn = request.json.get("hnnumber", None)
        try:

            # Define the schema
            employee_schema = EmployeeSchema()
            services_schema = ServicesSchema()
            physical_exam_schema = PhysicalExamSchema()
            xray_schema = XRaySchema()
            lab_schema = LabSchema()

            # Fetch the employee with all related data
            employee = db.session.query(Employee).options(
                joinedload(Employee.services)
                .joinedload(Services.physical_exam),
                joinedload(Employee.services).joinedload(Services.x_ray),
                joinedload(Employee.services).joinedload(Services.labs).joinedload(Lab.test)
            ).filter_by(HN=hn).first()

            if employee is None:
                return jsonify({'message': 'Employee not found'}), 404

            employee_data = employee_schema.dump(employee)

            for service in employee.services:
               service_data = services_schema.dump(service)
               service_data['physical_exam'] = physical_exam_schema.dump(service.physical_exam)
               service_data['x_ray'] = xray_schema.dump(service.x_ray)
               service_data['labs'] = [lab_schema.dump(lab) for lab in service.labs]
               employee_data['services'].append(service_data)

            return jsonify(employee_data, 200)

        except Exception as e:
            return jsonify({'message': str(e)}), 500





@apis.route('/employees/<string:hnnumber>', methods=['GET'])
@jwt_required()
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

        employee_data = employee_schema.dump(employee)

        for service in employee.services:
            service_data = services_schema.dump(service)
            service_data['physical_exam'] = physical_exam_schema.dump(service.physical_exam)
            service_data['x_ray'] = xray_schema.dump(service.x_ray)
            service_data['labs'] = [lab_schema.dump(lab) for lab in service.labs]
            employee_data['services'].append(service_data)


        return jsonify(employee_data, 200)

    except Exception as e:
        return jsonify({'message x': str(e)}), 500



@apis.route('/services/<string:serno>', methods=['GET'])
@jwt_required()
def get_employee_with_services(serno):


    try:

        # Define the schemas
        services_schema = ServicesSchema()
        physical_exam_schema = PhysicalExamSchema()
        xray_schema = XRaySchema()
        lab_schema = LabSchema()

        # Fetch the employee with all related data

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
@jwt_required()
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