from website import db

db.drop_all()
db.create_all()
from website.models import Department

departments =["Post-department",'Deep Learning',"PID Control","ROS","Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"]

for department in departments:
	dep = Department(department=department)
	db.session.add(dep)
	db.session.commit()

