import os
from pathlib import Path
from typing import List
from functools import lru_cache
from dotenv import load_dotenv


load_dotenv()

class BaseConfiguration:
    """Core Django configuration preferences."""
    def __init__(self):
        self._secret_key=os.environ.get('DJANGO_SECRET_KEY')
        self.base_dir=Path(__file__).resolve().parent.parent.parent
        self._root_urlconf='config.urls'

        self._validate_environ()

    @staticmethod
    def _validate_environ()->None:
        """Validates required environment variabes if existent. If not, raises ValueError."""
        required:list=['DJANGO_SECRET_KEY']
        missing_variables:list=[variable for variable in required if not os.environ.get(variable)]
        if missing_variables:
            raise ValueError(f"ConfigurationError: Missing required environment variables: '{' '.join(missing_variables)}' variable.")
        
    @property
    def secret_key(self)->str:
        """Secret key variable fetcher."""
        if not self._secret_key:
            raise ValueError(f"'DJANGO_SECRET_KEY' variable expected, but not set.")
        return self._secret_key
    
    @property
    def installed_apps(self)->List[str]:
        """Fetches list of installed applications."""
        third_party:list=[
            'corsheaders', # for cross-origin communication with frontend
        ]
        project_built:list=[]

        # if len(third_party)==0 or len(project_built)==0:
        #     return []

        return third_party+project_built
    
    @property
    def middleware(self)->List[str]:
        """List of deployed middleware."""
        default:list=[
            'django.middleware.security.SecurityMiddleware',
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ]
        custom:list=[]
        
        return default+custom
    
    @property
    def root_url_configurations(self)->str:
        """URL path configurations."""
        return self._root_urlconf
    

@lru_cache(maxsize=1)
def base_config()->BaseConfiguration:
    """Fetches cached instance of BaseConfiguration."""
    return BaseConfiguration()

base_configurations:BaseConfiguration=base_config()