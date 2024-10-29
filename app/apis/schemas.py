
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# from sqlalchemy.orm import relationship
#
# from app import Base, ma
#
# Physical_Exam =  Base.classes.Physical_Exam
# X_Ray = Base.classes.X_Ray
# Lab = Base.classes.Lab
# Test = Base.classes.Test
# Employee = Base.classes.Employee
# Services = Base.classes.Services
# User = Base.classes.User
#
#
#
# if Physical_Exam is None:
#     print("Physical_Exam table could not be found.")
#
# if Lab is None:
#     print("Lab table could not be found.")
#
# if X_Ray is None:
#     print("Test table could not be found.")
#
# if Employee is None:
#     print("Employee table could not be found.")
#
# if Services is None:
#     print("Services table could not be found.")
#
# if User is None:
#     print("User table could not be found.")
#
# # Establish relationships
#
# # Employee to Services
# Employee.services = relationship(
#     'Services',
#     primaryjoin=Employee.cmsCode == Services.cmsCode,
#     foreign_keys=Services.cmsCode,
#     backref='employee'
# )
#
# # Services to Physical_Exam
# Services.physical_exam = relationship(
#     'Physical_Exam',
#     primaryjoin=Services.ServiceNo == Physical_Exam.ServiceNo,
#     foreign_keys=Physical_Exam.ServiceNo,
#     backref='service',
#     uselist=False  # Assuming one-to-one relationship
# )
#
# # Services to X_Ray
# Services.x_ray = relationship(
#     'X_Ray',
#     primaryjoin=Services.ServiceNo == X_Ray.ServiceNo,
#     foreign_keys=X_Ray.ServiceNo,
#     backref='service',
#     uselist=False  # Assuming one-to-one relationship
# )
#
# # Services to Labs
# Services.labs = relationship(
#     'Lab',
#     primaryjoin=Services.ServiceNo == Lab.ServiceNo,
#     foreign_keys=Lab.ServiceNo,
#     backref='service'
# )
#
# # Lab to Test
# Lab.test = relationship(
#     'Test',
#     primaryjoin=Lab.TCode == Test.TCode,
#     foreign_keys=Lab.TCode,
#     backref='labs'
# )
# # Define Marshmallow Schemas
# class TestSchema(SQLAlchemyAutoSchema):
#     Test = auto_field()  # This will include the related Test object
#     class Meta:
#         model = Test
#         load_instance = True
#
# class LabSchema(SQLAlchemyAutoSchema):
#     Lab = auto_field()  # This will include the related Test object
#     class Meta:
#         model = Lab
#         load_instance = True
#
# class XRaySchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = X_Ray
#         load_instance = True
#
# class PhysicalExamSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Physical_Exam
#         load_instance = True
#
# class ServicesSchema(SQLAlchemyAutoSchema):
#     physical_exam = auto_field()
#     x_ray = auto_field()
#     labs = auto_field()
#
#     class Meta:
#         model = Services
#         load_instance = True
#
# class EmployeeSchema(SQLAlchemyAutoSchema):
#     services = auto_field()
#     class Meta:
#         model = Employee
#         load_instance = True
#
#
# class UserSchema(SQLAlchemyAutoSchema):
#     User = auto_field()
#     class Meta:
#         model = User
#         load_instance = True



from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields
from sqlalchemy.orm import relationship
from marshmallow import fields as ma_fields  # Avoid conflict with SQLAlchemy fields
from app import Base, ma

# Model references from Base
Physical_Exam = Base.classes.Physical_Exam
X_Ray = Base.classes.X_Ray
Lab = Base.classes.Lab
Test = Base.classes.Test
Employee = Base.classes.Employee
Services = Base.classes.Services
User = Base.classes.User

# Check if tables are found
for model, name in [(Physical_Exam, "Physical_Exam"), (Lab, "Lab"),
                    (X_Ray, "X_Ray"), (Employee, "Employee"),
                    (Services, "Services"), (User, "User")]:
    if model is None:
        print(f"{name} table could not be found.")

# Establish relationships
Employee.services = relationship(
    'Services',
    primaryjoin=Employee.cmsCode == Services.cmsCode,
    foreign_keys=Services.cmsCode,
    backref='employee'
)

Services.physical_exam = relationship(
    'Physical_Exam',
    primaryjoin=Services.ServiceNo == Physical_Exam.ServiceNo,
    foreign_keys=Physical_Exam.ServiceNo,
    backref='service',
    uselist=False  # Assuming one-to-one relationship
)

Services.x_ray = relationship(
    'X_Ray',
    primaryjoin=Services.ServiceNo == X_Ray.ServiceNo,
    foreign_keys=X_Ray.ServiceNo,
    backref='service',
    uselist=False  # Assuming one-to-one relationship
)

Services.labs = relationship(
    'Lab',
    primaryjoin=Services.ServiceNo == Lab.ServiceNo,
    foreign_keys=Lab.ServiceNo,
    backref='service'
)

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
    test = ma_fields.Nested(TestSchema)  # Map relationship to nested schema
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
    physical_exam = ma_fields.Nested(PhysicalExamSchema)
    x_ray = ma_fields.Nested(XRaySchema)
    labs = ma_fields.List(ma_fields.Nested(LabSchema))  # Mapping one-to-many as a list

    class Meta:
        model = Services
        load_instance = True

class EmployeeSchema(SQLAlchemyAutoSchema):
    services = ma_fields.List(ma_fields.Nested(ServicesSchema))  # Mapping one-to-many as a list
    class Meta:
        model = Employee
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
