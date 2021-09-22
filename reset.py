import os,shutil,bcrypt
from website import db,app

# reinitialize database tables
def clear_database():

	db.drop_all()
	db.create_all()

	return 'Database cleared successfully'

# add the departments to their table (important to avoid errors in the registration view)
from website.models import Department,User
def add_departments():
	departments =["Post-department",'Deep Learning',"PID Control","ROS","Kinematics","Embedded Systems","Maze Solving Algorithm","Mechanical"]

	for department in departments:
		dep = Department(department=department)
		db.session.add(dep)
		db.session.commit()

	return 'Departments added successfully'

def add_admin():

	admin={
	'username':os.environ.get('ADMIN_USERNAME'),
	'password':os.environ.get('ADMIN_PASSWORD')
	}

	for key,value in admin.items():
		if not value:
			admin[key] = 'admin'

	admin = User(username = admin['username'], email = 'admin',department ='All',
				password = bcrypt.hashpw(admin['password'].encode('utf-8'),bcrypt.gensalt()),)
	
	db.session.add(admin)
	db.session.commit()
	db.session.close()

	return 'Admin added successfully'
# clear media directory
def clear_media():
	media_path =os.path.join(os.getcwd(),'website','media')
	shutil.rmtree(media_path,ignore_errors=True)

	return 'Media directory cleared successfully'

# clear cache directory
def clear_cache():
	cache_path =os.path.join(os.getcwd(),'website','__pycache__')
	shutil.rmtree(cache_path,ignore_errors=True)

	return 'Cache directory cleared successfully'

# clear profile_pics folder
def clear_profile_pics():
	profile_pics_path = os.path.join(os.getcwd(),'website','static','profile_pics')

	for pic in os.listdir(profile_pics_path):
		if pic != 'default.jpg':
			os.remove(os.path.join(profile_pics,pic))

	return 'Profile Pictures folder cleared successfully'

print(clear_database(),add_departments(),add_admin(),clear_media(),clear_cache(),clear_profile_pics(),sep='\n')