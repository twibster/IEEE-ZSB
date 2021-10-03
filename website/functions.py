import datetime,random,os,secrets
from PIL import Image
from website import mail,app,message,db
from website.models import Notifications
from flask import render_template,url_for,request,redirect
from flask_login import current_user
from threading import Thread
from urlextract import URLExtract
from functools import wraps

def display_time(date):
    now =datetime.datetime.utcnow()
    time =round((now-date).total_seconds())
    if time <120:
        display ='Just now' 
    elif time<3600:
        display= f'{round(time/60)}m ago'
    elif time<86400:
        display= f'{round((time/60)/60)}h ago'
    elif time<172800:
        display= f"Yesterday at {date.strftime('%I:%M %p')}"
    elif date.year ==now.year:
        display= date.strftime('%b %d at %I:%M %p')
    else:
        display= date.strftime('%B %d, %Y')
    return display

def noti_clearer(noti):
    '''mark a notification as clicked (seen)'''
    if noti != 0:
        Notifications.query.get(noti).clicked = True
        db.session.commit()

def noti_fetcher():
    '''return user's notifications if logged in, if not, return nothing'''
    if current_user.is_authenticated:
        notifications = Notifications.query.filter_by(to_id = current_user.id).order_by(Notifications.date.desc())
        return notifications
    else:
        return None

## decorators
def confirmation_required(f):
    '''check if the user's email is confirmed and if not, send him to the confirmaiton page'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('confirm'))
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    '''check if the user is logged out and if not, send him back to the home page'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def confirm_view(f):
    '''check if the user's email is not confirmed or the user is not the admin'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed or current_user.email =='admin':
            return redirect(url_for('admin.index')) if current_user.email =='admin' else redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
## end of decorators

def row2dict(row):
    '''this function converts a given row of a query to a dictionary'''
    allowed =['department','tasks','first_name','last_name','username','position',
            'image_file','title','deadline','file','date_posted','content','user_id','id']
    dict = {}
    for column in row.__table__.columns:
        name = column.name
        if name in allowed:
            dict[column.name] = str(getattr(row, column.name))
            if name =='date_posted' or name == 'date_created':
                dict[name]= getattr(row, column.name).strftime("%d/%m/%Y, %H:%M")
        if name =='user_id':
            dict.update(row2dict(row.author))
    return dict

def dict_generator(query,key,identifier=''):
    '''this function converts a query into a dictionary'''
    results={}
    for row in query:
        row_as_dict =row2dict(row)
        if not (row_as_dict['department'] == 'N/A'):
            results[row_as_dict[key]+identifier]=row_as_dict
    return results

def url_extractor(data):
    '''this function extracts urls from given strings and replaces them a link tag'''
    extractor = URLExtract()
    urls = extractor.find_urls(data)
    for url in urls:
        if ('http' or 'https') in url:
            html =f"<a href='{url}' target='_blank' rel='noopener noreferrer'>{url}</a>"
        else:
            html =f"<a href='//{url}' target='_blank' rel='noopener noreferrer'>{url}</a>"
        data =data.replace(url,html)
    return data

def days(date,to_compare = None,state = None):
    '''this function return date in days and if provided compares two dates and returns the time in days'''
    date = datetime.date(date.year,date.month,date.day)
    if to_compare:
        to_compare = datetime.date(to_compare.year,to_compare.month,to_compare.day)
        return abs((to_compare -date).days) if state =='abs' else (to_compare -date).days
    else:
        today = datetime.datetime.today()
        today_no_timestamp = datetime.date(today.year,today.month,today.day)
        return abs((today_no_timestamp -date).days) if state =='abs' else (today_no_timestamp -date).days
        
def email_data(content='reset',type=None,text=None):
    '''this generates the data for the email body'''
    data={
        'tech':{
            'subject':f'A new {type}',
            'declared':f'You have a new {type}',
            'title':f'A new {type}',
            'text':text,
            'footer':'You received this email because you enabled this type of email, to disable them, kindly visit your account and navigate to settings',
            'code':None
        },
        'reset':{
            'subject':'Password Reset Request',
            'declared':'A request has been recieved to change the password of your account.',
            'title':"Reset Your Password",
            'text':"Use the code below to reset your password. If you didn't request a new password, you can safely delete this email.",
            'footer':"You received this email because we received a request to reset the password of your account. If you didn't request that, you can safely delete this email.",
            'code':int(''.join(map(str,random.sample(range(0,10),6))))
        },
        'confirm':{
            'subject':'Email Confirmation',
            'declared':'A confirmation email to validate your account',
            'title':"Confirm your account",
            'text':"Use the code below to confirm your account. This code expires 10 minutes from now.",
            'footer':"You received this email because you signed up in our website. If you didn't do that, you can safely delete this email.",
            'code':int(''.join(map(str,random.sample(range(0,10),6))))
        }
    }
    return (data[content]['subject'],data[content]['declared'],data[content]['title'],
            data[content]['text'],data[content]['footer'],data[content]['code'])
    
def mail_sender(recipients,content='reset',type=None,text=None):
    '''this function configures e-mails with varying content and recipients to be sent later'''
    subject,declared,title,text,footer,code=email_data(content= content,type=type,text=text)
    msg =message(
        subject=subject,
        sender=app.config.get("MAIL_USERNAME"),
        recipients=recipients)
    msg.html=render_template('email_body.html',code =code,declared=declared,title=title,
                            text = text,footer=footer,website=request.host_url+'account')
    thr = Thread(target=async_email, args=[app, msg])
    thr.start()

    return code

def async_email(app,msg):
    '''this sends the emails provided in sync'''
    with app.app_context():
        try:
            mail.send(msg)
        except AssertionError:
            pass

def save_file(form_file,location):
    '''saves the provided file in the provived location and if the loction doesn't exisit, creates it'''
    if form_file:
        random_hex = secrets.token_hex(8)
        file_text, file_ext = os.path.splitext(form_file.filename)
        file_filename = file_text[:5]+random_hex + file_ext
        file_path = os.path.join(location,file_filename)
        try:
            os.makedirs(location)
        except FileExistsError:
            pass
            
        images = ['.jpg','.jpeg','.png']
        if file_ext in images:
            form_file = Image.open(form_file)
            width, height = form_file.size
            if width > 700 and height >700: 
                left = round((width - 800)/2)
                top = round((height - 800)/2)
                x_right = round(width - 800) - left
                x_bottom = round(height - 800) - top
                right = width - x_right
                bottom = height - x_bottom
                form_file = form_file.crop((left, top, right, bottom))
            
        form_file.save(file_path)
        return file_filename
    else:
        return None

def noti_text(type,position=None,name=None,task=None,date=None,status=None):
    '''generates the text of the notifications'''
    data ={
        'Team Member':{
            'task':{'text':f'You have a new task from {name} due {date} days',
                    'route':'view_task'},
            'review':{'text':f'Your submit for the {task} task has been reviewd by {name}',
                       'route':'view_task'},
            'missed':{'text':f"You missed the {task} task's deadline",
                       'route':'view_task'}
        },
        'Team Leader':{
            'submit':{'text':f'You have a new submition for {task} from {name}',
                      'route':'view_submit'},
            'excuse':{'text':f'{name} has excused himeself from {task} task',
                      'route':'view_task'}
        },
        'announcement':{'text':f'You have a new announcement from {name} valid for {date} days',
                        'route':'announcements'},
        'meetup':{'text':f'You have a new {status} meeting from {name} in {date} days',
                  'route':'meetup'}
    }  
    return (type,data[position][type]['text'], data[position][type]['route']) if position else (type,data[type]['text'],data[type]['route'])
