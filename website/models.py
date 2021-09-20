from datetime import datetime
from website import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key= True)
    first_name =db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String, unique = True)
    birthdate = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique = True)
    image_file = db.Column(db.String, default ='default.jpg')
    password = db.Column(db.LargeBinary,nullable = False)
    department = db.Column(db.String)
    position = db.Column(db.String)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    score = db.Column(db.Integer,default=0)
    tasks = db.relationship('Task', backref = "author", cascade="all, delete")
    tasks_submitted = db.relationship('Submit',backref = "submitter", cascade="all, delete")
    tasks_missed = db.relationship('Missed',backref = "misser")
    announcements = db.relationship('Announce',backref = "announcer", cascade="all, delete")
    meetups = db.relationship('Meetup',backref = "organizer", cascade="all, delete")
    meetup_case = db.relationship('Meetup_Info',backref = "caser", cascade="all, delete")
    excuses = db.relationship('Excuses',backref = "excuser")
    notifications = db.relationship('Notifications',backref = "sender", cascade="all, delete")
    noti_settings = db.relationship('Notifications_Settings',backref = "user",lazy='dynamic', cascade="all, delete")
    email_settings = db.relationship('Email_Settings',backref = "user",lazy='dynamic', cascade="all, delete")

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"
    
class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    type = db.Column(db.String, nullable = False)
    data = db.Column(db.Text,nullable = False)
    route = db.Column(db.String, nullable = False)
    data_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    clicked = db.Column(db.Boolean,default =False)
    to_id = db.Column(db.Integer)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Notifications('{self.id}','{self.type}','{self.data}','{self.data_id}','{self.to_id}','{self.from_id}')"

class Notifications_Settings(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    task = db.Column(db.Boolean,default =True)
    review = db.Column(db.Boolean,default =True)
    missed = db.Column(db.Boolean,default =True)
    submit = db.Column(db.Boolean,default =True)
    excuse = db.Column(db.Boolean,default =True)
    announcement = db.Column(db.Boolean,default =True)
    meetup = db.Column(db.Boolean,default =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Notifications('{self.task}','{self.review}','{self.missed}','{self.submit}','{self.excuse}','{self.announcement}','{self.meetup}')"

class Email_Settings(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    task = db.Column(db.Boolean,default =True)
    review = db.Column(db.Boolean,default =True)
    missed = db.Column(db.Boolean,default =True)
    submit = db.Column(db.Boolean,default =True)
    excuse = db.Column(db.Boolean,default =True)
    announcement = db.Column(db.Boolean,default =True)
    meetup = db.Column(db.Boolean,default =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Notifications('{self.task}','{self.review}','{self.missed}','{self.submit}','{self.excuse}','{self.announcement}','{self.meetup}')"
        
class Department(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    department = db.Column(db.String)
    tasks= db.Column(db.Integer,default=0)
    submits =db.Column(db.Integer,default=0)
    excuses =db.Column(db.Integer,default=0)
    announcements=db.Column(db.Integer,default=0)
    meetups=db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"Department('{self.id}','{self.department}','{self.tasks}','{self.submits}','{self.excuses}','{self.announcements}','{self.meetups}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    department = db.Column(db.String, nullable = False)
    content = db.Column(db.Text,nullable = False)
    file = db.Column(db.String)
    deadline = db.Column(db.DateTime,nullable = False)
    submits_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submits = db.relationship('Submit', backref = "task",lazy='dynamic', cascade="all, delete")
    excuses = db.relationship('Excuses', backref = "task",lazy='dynamic', cascade="all, delete")
    missed = db.relationship('Missed', backref = "task",lazy='dynamic', cascade="all, delete")
    noti = db.relationship('Notifications', backref = "task", cascade="all, delete")

    def __repr__(self):
        return f"Task('{self.id}','{self.title}','{self.date_posted}','{self.content}','{self.file}','{self.deadline}','{self.user_id}','{self.submits}')"

class Excuses(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    notes = db.Column(db.Text)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f"Excuses('{self.id}','{self.type}','{self.notes}','{self.user_id}','{self.task_id}')"

class Missed(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f"Missed('{self.id}','{self.user_id}','{self.task_id}')"

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date_submitted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    notes = db.Column(db.Text)
    file = db.Column(db.String)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f"Submit('{self.id}','{self.notes}','{self.date_submitted}','{self.file}','{self.task_id}','{self.user_id}')"

class Announce(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date_announced = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    department = db.Column(db.String, nullable = False)
    content = db.Column(db.Text)
    validation_date = db.Column(db.DateTime,nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Announce('{self.id}','{self.date_announced}','{self.department}','{self.content}','{self.validation_date}','{self.user_id}')"

class Meetup(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    department = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    state =db.Column(db.String,nullable=False)
    about = db.Column(db.Text)
    date = db.Column(db.DateTime,nullable = False)
    long=db.Column(db.Integer,default=0)
    lat=db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    info = db.relationship('Meetup_Info',backref = "meetup", cascade="all, delete")


    def __repr__(self):
        return f"Meetup('{self.id}','{self.date_created}','{self.department}','{self.title}','{self.about}','{self.date}','{self.long}','{self.lat}','{self.user_id}')"

class Meetup_Info(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    type = db.Column(db.String)
    notes = db.Column(db.Text)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    meetup_id = db.Column(db.Integer, db.ForeignKey('meetup.id'))

    def __repr__(self):
        return f"Meetup_Info('{self.id}','{self.type}','{self.notes}','{self.user_id}')"
