import os

environ_config = {
    "MAIL_SERVER": os.environ.get('MAIL_SERVER'),
    "MAIL_PORT": os.environ.get('MAIL_PORT'),
    "MAIL_USE_TLS": os.environ.get('MAIL_USE_TLS'),
    "MAIL_USE_SSL": os.environ.get('MAIL_USE_SSL'),
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SQLALCHEMY_TRACK_MODIFICATIONS':False,
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'GOOGLE_API': os.environ.get('GOOGLE_API'),
    'ADMIN_USERNAME':os.environ.get('ADMIN_USERNAME'),
    'FLASK_ADMIN_SWATCH': 'Cerulean'
}
defaults={
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    'SECRET_KEY': os.urandom(16),
    'SQLALCHEMY_DATABASE_URI':'sqlite:///site.db'
}

for key,value in environ_config.items():
    if not value:
        environ_config[key] = defaults.get(key)
    elif 'postgres://' in value:
        ''' this checks for an outdated postgresql url as it is not supported by sql-alchemy anymore'''
        environ_config[key] = value.replace("postgres://", "postgresql://", 1)
