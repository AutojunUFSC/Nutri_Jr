from nutri.settings.base import *

# Overrite base.py settings here
import django_heroku

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'sistema-nutrijr.herokuapp.com']

# Manual: "Set environment variables"
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Application definition

INSTALLED_APPS += [
    # Manualmente colocados:
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE += [
    # Manualmente colocados:
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#Outra nova propriedade pra ajudar o django a achar os arquivos staticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Faz a conexão com o Heroku
django_heroku.settings(locals())

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
