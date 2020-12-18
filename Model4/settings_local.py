import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME', 'mydb'),
        'USER': os.environ.get('DBUSER', 'myuser'),
        'PASSWORD': os.environ.get('DBPASS', 'mypass'),
        'HOST': os.environ.get('DBHOST', '127.0.0.1'),
        'PORT': os.environ.get('DBPORT', '5432'),
    }
}