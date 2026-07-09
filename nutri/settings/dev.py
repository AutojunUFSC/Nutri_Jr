import os

from nutri.settings.base import *

# Overrite base.py settings here

# Apenas para desenvolvimento local - nao usar em produção
SECRET_KEY = 'dev-only-local-secret-key-nao-usar-em-producao'

# Replica local de produção (Postgres), restaurada a partir do backup baixado
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DEV_DB_NAME', 'nutri_dev'),
        'USER': os.environ.get('DEV_DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DEV_DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DEV_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DEV_DB_PORT', '5432'),
    }
}
