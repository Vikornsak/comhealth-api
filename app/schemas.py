from click.testing import Result
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.orm import relationship

from app import Base, ma

Physical_Exam = Base.classes.Physical_Exam
X_Ray = Base.classes.X_Ray
Lab = Base.classes.Lab
Test = Base.classes.Test
Employee = Base.classes.Employee
Services = Base.classes.Services
User = Base.classes.User
# Establish relationships

# Employee to Services
Employee.services = relationship(
    'Services',
    primaryjoin=Employee.cmsCode == Services.cmsCode,
    foreign_keys=Services.cmsCode,
    backref='employee'
)


# Services to Physical_Exam
Services.physical_exam = relationship(
    'Physical_Exam',
    primaryjoin=Services.ServiceNo == Physical_Exam.ServiceNo,
    foreign_keys=Physical_Exam.ServiceNo,
    backref='service',
    uselist=False  # Assuming one-to-one relationship
)

# Services to X_Ray
Services.x_ray = relationship(
    'X_Ray',
    primaryjoin=Services.ServiceNo == X_Ray.ServiceNo,
    foreign_keys=X_Ray.ServiceNo,
    backref='service',
    uselist=False  # Assuming one-to-one relationship
)

# Services to Labs
Services.labs = relationship(
    'Lab',
    primaryjoin=Services.ServiceNo == Lab.ServiceNo,
    foreign_keys=Lab.ServiceNo,
    backref='service'
)

# Lab to Test
Lab.test = relationship(
    'Test',
    primaryjoin=Lab.TCode == Test.TCode,
    foreign_keys=Lab.TCode,
    backref='labs'
)
# Define Marshmallow Schemas
class TestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        load_instance = True

class LabSchema(SQLAlchemyAutoSchema):
    test = auto_field()  # This will include the related Test object

    class Meta:
        model = Lab
        load_instance = True

class XRaySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = X_Ray
        load_instance = True

class PhysicalExamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Physical_Exam
        load_instance = True

class ServicesSchema(SQLAlchemyAutoSchema):
    physical_exam = auto_field()
    x_ray = auto_field()
    labs = auto_field()

    class Meta:
        model = Services
        load_instance = True

class EmployeeSchema(SQLAlchemyAutoSchema):
    services = auto_field()
    class Meta:
        model = Employee
        load_instance = True