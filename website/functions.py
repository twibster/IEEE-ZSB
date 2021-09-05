import datetime,random,os,secrets
from website import mail,app,message
from flask import render_template
from threading import Thread


def days(date,to_compare = None,state = None):
    date = datetime.date(date.year,date.month,date.day)
    if to_compare:
        to_compare = datetime.date(to_compare.year,to_compare.month,to_compare.day)
        return abs((to_compare -date).days) if state =='abs' else (to_compare -date).days
    else:
        today = datetime.datetime.today()
        today_no_timestamp = datetime.date(today.year,today.month,today.day)
        return abs((today_no_timestamp -date).days) if state =='abs' else (today_no_timestamp -date).days
        
def email_data(content='reset',type=None,text=None):
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
        }
    }
    return (data[content]['subject'],data[content]['declared'],data[content]['title'],
            data[content]['text'],data[content]['footer'],data[content]['code'])

def mail_sender(recipients,content='reset',type=None,text=None):
    subject,declared,title,text,footer,code=email_data(content= content,type=type,text=text)
    msg =message(
        subject=subject,
        sender=app.config.get("MAIL_USERNAME"),
        recipients=recipients)
    msg.html=render_template('email_body.html',code =code,declared=declared,title=title,
                            text = text,footer=footer)
    thr = Thread(target=async_email, args=[app, msg])
    thr.start()

    return code

def async_email(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except AssertionError:
            print('no emails')
            pass

def save_file(form_file,location):
    if form_file:
        random_hex = secrets.token_hex(8)
        file_text, file_ext = os.path.splitext(form_file.filename)
        file_filename = file_text[:20]+random_hex + file_ext
        file_path = os.path.join(location,file_filename)
        try:
            os.makedirs(location)
        except FileExistsError:
            pass
            
        form_file.save(file_path)
        return file_filename
    else:
        return None

def noti_text(type,position=None,name=None,task=None,date=None,status=None):
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
