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
ENV_NAME = 'Staging'
BASE_HOST = 'http://api.staging.rcm360.co'
AUTH_HOST = 'http://auth.staging.rcm360.co'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.staging.rcm360.co','localhost', '127.0.0.1']

# For Password Genenration for users
GENERATE_RANDOM_PASSWORD = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hcms_staging_db',
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
        'PASSWORD': 'Y=FxaMB7%Rt-zpbz',
        'HOST': 'localhost',
        'PORT': '5432',
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        # }
    },

}

REFRESH_DB_ENABLED = True
DB_SNAPSHOT_ENABLED = True
CWD = '/home/ubuntu/sites/hcms-backend'
BKUP_FILE_DIR_PATH = os.path.join(CWD, 'db_dumps')
ENGINE_REPORTS_DIR = os.path.join(CWD, 'engine_reports')
ENGINE_LOGS_PATH = os.path.join(CWD, 'engine_logs')


CW_WEB_APP_HOST = 'http://cw.staging.rcm360.co'
SU_WEB_APP_HOST = 'http://su.staging.rcm360.co'

sentry_sdk.init(
    dsn="https://85477f84e3684fd2b95c73d0005b3e25@o340621.ingest.sentry.io/5740562",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_STORAGE_BUCKET_NAME = 'attachments.staging.rcm360.co'
