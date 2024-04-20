#!/usr/bin/python3
from datetime import datetime

from models import User, Staff, Student, Parent
from models import storage

saved = len(storage.all())

print(f"{saved} has been saved so far")
print("-----------------Creating new models----------------------")
user = User(first_name="John", last_name="Ametepe",
            email='<EMAIL>', password='<PASSWORD>')

user2 = User(first_name="Ameyo", last_name="Ametepe", email="", password='<PASSWORD>')

parent1 = Parent(id=user2.id)
staff = Staff(id=user.id)
student = Student(parent_id=parent1.id,
                  expected_graduation=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  admission_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  first_name="Joan",
                  last_name="Ametepe",
                  email="", password='<PASSWORD>')

print("------------------Saving new models----------------------")
storage.new(user)
storage.new(student)
storage.new(staff)

storage.save()

print("____________________Resetting store_______________________")
storage.close()
print(f"storage is close so the store should be empty {storage.all()}")
storage.reload()

saved = len(storage.all())

print(f"{saved} has been saved so far")

print("-----------------Printing saved models----------------------")

for key, value in storage.all().items():
    print(f"{key}: {value}")
    print()
