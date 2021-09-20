from flask import Flask
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from website.config import environ_config
import os

app = Flask(__name__)



app_config = {
    'SQLALCHEMY_TRACK_MODIFICATIONS':False,
    'TASKS_FILE_DOWNLOAD': os.path.join('media/tasks'),
    'SUBMITS_FILE_DOWNLOAD': os.path.join('media','submits'),
    'TASKS_FILE': os.path.join(app.root_path,'media/tasks'),
    'SUBMITS_FILE': os.path.join(app.root_path,'media','submits'),
    'PROFILE_PICS':os.path.join(app.root_path,'static/profile_pics')
}

configuration =environ_config | app_config
app.config.update(configuration)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
mail = Mail(app)

message= Message
login_manager.login_view= 'login'
login_manager.login_message = ""

from website import routes
from website import models as md

admin = Admin(index_view=routes.MyAdminIndexView(),name='IEEE-ZSB')
admin.init_app(app)
admin.add_view(routes.MyModelView(md.User,db.session,category='Users'))
admin.add_view(routes.MyModelView(md.Notifications,db.session,category='Users'))
admin.add_view(routes.MyModelView(md.Email_Settings,db.session,category='Users'))
admin.add_view(routes.MyModelView(md.Notifications_Settings,db.session,category='Users'))
admin.add_view(routes.MyModelView(md.Task,db.session,category='Tasks'))
admin.add_view(routes.MyModelView(md.Submit,db.session,category='Tasks'))
admin.add_view(routes.MyModelView(md.Excuses,db.session,category='Tasks'))
admin.add_view(routes.MyModelView(md.Missed,db.session,category='Tasks'))
admin.add_view(routes.MyModelView(md.Meetup,db.session,category='Meetings'))
admin.add_view(routes.MyModelView(md.Meetup_Info,db.session,category='Meetings'))
admin.add_view(routes.MyModelView(md.Department,db.session))
admin.add_view(routes.MyModelView(md.Announce,db.session))


