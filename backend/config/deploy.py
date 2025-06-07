"""Configuration module manager for application deployment. Works as DJANGO_SETTINGS_MODULE and loads configurations to `manage.py`."""

from pathlib import Path
from base import base_configurations
from development import development_configurations
from sqlconfig import get_sqlite_database_config

# Environment-specific configurations- to configure dynamic module loading
DEBUG:bool=development_configurations.debug     # to be set as environment-specific configuration
ALLOWED_HOSTS:list=development_configurations.allowed_hosts # this is to be set as an environment-specific configuration

# Base Django application configurations
INSTALLED_APPS:list=base_configurations.installed_apps
MIDDLEWARE:list=base_configurations.middleware
SECRET_KEY:str=base_configurations.secret_key
BASE_DIR:Path=base_configurations.base_dir
ROOT_URLCONF:str=base_configurations.root_url_configurations

# Database configurations- to re-configure to accept dynamic loading of configurations
DATABASES={
    'default':get_sqlite_database_config('db.sqlite3'),
    'analytics':get_sqlite_database_config('analytics.sqlite3', max_connections=15)
}

CORS_ALLOW_ALL_ORIGINS=development_configurations.cors_allow_all_origins
CORS_ALLOWED_ORIGINS=[
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'http://localhost:5000',
]

# other settings
LANGUAGE:str='en-us'
USE_TZ:bool=True
USE_L10N:bool=True
USE_I10N:bool=True

print(MIDDLEWARE)