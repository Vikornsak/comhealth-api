from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.orm import relationship

from app import Base, ma

Lab = Base.classes.Lab
Test = Base.classes.Test
Employee = Base.classes.Employee
Services = Base.classes.Services

Services.employee = relationship(Employee,
                                 primaryjoin=Employee.cmsCode == Services.cmsCode,
                                 foreign_keys=Services.cmsCode,
                                 remote_side=Employee.cmsCode,
                                 backref='services')

Lab.service = relationship(Services,
                           primaryjoin=Services.ServiceNo == Lab.ServiceNo,
                           foreign_keys=Lab.ServiceNo,
                           remote_side=Services.ServiceNo,
                           backref='results'
                           )


class TestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        load_instance = True


test_schema = TestSchema()
tests_schema = TestSchema(many=True)


class LabSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Lab
        load_instance = True


lab_schema = LabSchema()
labs_schema = LabSchema(many=True)


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True

    services = auto_field()


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Services
        load_instance = True

    results = auto_field()

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("apis.serviceresource", values=dict(service_no="<ServiceNo>")),
        }
    )


service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
