# #!/usr/bin/python3
# """
# Parent Child Association script
# """
#
# from sqlalchemy import Column, ForeignKey, String
# from sqlalchemy.orm import relationship
#
# from models.basemodel import Base
#
#
# class ParentChildAssociation(Base):
#     """
#     The ParentChildAssociation model represents the association between parents and children.
#
#     Attributes:
#         parent_id (str): The ID of the parent.
#         student_id (str): The ID of the student (child).
#         child (relationship): Relationship attribute to access the associated Student instance.
#         parent (relationship): Relationship attribute to access the associated Parent instance.
#         extra_data (str): Additional data related to the parent-child relationship.
#     """
#
#     __tablename__ = 'parent_student_association'
#
#     parent_id = Column(String, ForeignKey('parents.id'), nullable=False, primary_key=True)
#     student_id = Column(String, ForeignKey('students.id'), nullable=False, primary_key=True)
#     students = relationship('Student', back_populates='parents', )
#     parents = relationship('Parent', back_populates='students', )
#     description = Column(String(100), nullable=True)
#
#     __table_args__ = {'extend_existing': True}
