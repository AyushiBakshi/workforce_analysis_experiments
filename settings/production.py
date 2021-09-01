"""
Django settings for hcms project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
from .base import *
import sentry_sdk

# Setup
ENV_NAME = 'Production'
BASE_HOST = 'https://api.rcm360.co'
AUTH_HOST = 'https://auth.rcm360.co'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'api.rcm360.co','18.140.15.79', '127.0.0.1']

# For Password Genenration for users
GENERATE_RANDOM_PASSWORD = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hcms_real_db_15feb',
        'USER': 'postgres',
        'PASSWORD': 'i9M8FkQVkK7rQXMGwrvy',
        'HOST': 'hcms-db.caoy9b44uned.ap-southeast-1.rds.amazonaws.com',
        'PORT': '5432',
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        # }
    },
    'ttgDb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ttgDb',
        'USER': 'postgres',
        'PASSWORD': 'jpEfX3[$<GMqj7pW',
        'HOST': 'localhost',
        'PORT': '5432',
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        # }
    },

}
EMAIL_SENDING_ENABLED = True
REFRESH_DB_ENABLED = False
DB_SNAPSHOT_ENABLED = False
CWD = '/home/ubuntu/sites/hcms-backend'
BKUP_FILE_DIR_PATH = os.path.join(CWD, 'db_dumps')
ENGINE_REPORTS_DIR = os.path.join(CWD, 'engine_reports')
ENGINE_LOGS_PATH = os.path.join(CWD, 'engine_logs')

CW_WEB_APP_HOST = 'https://cw.rcm360.co'
SU_WEB_APP_HOST = 'https://su.rcm360.co'

sentry_sdk.init(
    dsn="https://85656724a9c845fe802c434170acdb54@o340621.ingest.sentry.io/5738901",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_STORAGE_BUCKET_NAME = 'attachments.rcm360.co'