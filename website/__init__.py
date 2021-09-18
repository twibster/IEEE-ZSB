from flask import Flask
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from website.email_config import mail_settings
import os

app = Flask(__name__)

def database_url_handler(url):
    ''' this function checks for an outdated postgresql url as it is not supported by sql-alchemy anymore'''
    if 'postgres://' in url:
        url.replace("postgres://", "postgresql://", 1)

    return url
    
app.config['SQLALCHEMY_DATABASE_URI'] = database_url_handler(os.environ.get('DATABASE_URL'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['GOOGLE_API']= os.environ.get('GOOGLE_API')

app.config['TASKS_FILE_DOWNLOAD'] = os.path.join('media/tasks')
app.config['SUBMITS_FILE_DOWNLOAD'] = os.path.join('media','submits')
app.config['TASKS_FILE'] = os.path.join(app.root_path,'media/tasks')
app.config['SUBMITS_FILE'] = os.path.join(app.root_path,'media','submits')
app.config['PROFILE_PICS']=os.path.join(app.root_path,'static/profile_pics')

app.config.update(mail_settings)
mail = Mail(app)
message= Message

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message = ""

from website import routes