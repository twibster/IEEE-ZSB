from flask import Flask
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from website.config import environ_config
import os

app = Flask(__name__)

file_config = {
    'TASKS_FILE_DOWNLOAD': os.path.join('media/tasks'),
    'SUBMITS_FILE_DOWNLOAD': os.path.join('media','submits'),
    'TASKS_FILE': os.path.join(app.root_path,'media/tasks'),
    'SUBMITS_FILE': os.path.join(app.root_path,'media','submits'),
    'PROFILE_PICS':os.path.join(app.root_path,'static/profile_pics')
}

configuration =environ_config | file_config
app.config.update(configuration)
mail = Mail(app)
message= Message

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message = ""

from website import routes