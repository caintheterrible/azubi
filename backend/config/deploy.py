from pathlib import Path
from config.base import base_configurations
from config.development import development_configurations
# from config.sqlconfig import get_sqlite_database_config

# Environment-specific configurations (to be configured later for dynamic loading)
DEBUG:bool=development_configurations.debug
ALLOWED_HOSTS:list=development_configurations.allowed_hosts
CORS_ALLOW_ALL_ORIGINS:bool=development_configurations.cors_allow_all_origins
# CORS_ALLOWED_ORIGINS:list=development_configurations.cors_allowed_origins

# Base Django configurations
INSTALLED_APPS:list=base_configurations.installed_apps
MIDDLEWARE:list=base_configurations.middleware
SECRET_KEY:str=base_configurations.secret_key
BASE_DIR:Path=base_configurations.base_dir
ROOT_URLCONF:str=base_configurations.root_url_configurations

# Database configurations (to be reconfigured to accept dynamic loading of preferred configurations)
# DATABASES={
#     'default':get_sqlite_database_config('db.sqlite3'),
#     'analytics':get_sqlite_database_config('analytics.sqlite3'),
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'azubiPass@22',  # may escape this if needed
        'HOST': 'db.sbqtkuxgbpadbemnbjyf.supabase.co',
        'PORT': '5432',
    }
}


# Other settings
LANGUAGE:str='en-us'
USE_TZ:bool=True
USE_L10N:bool=True
USE_I10N:bool=True