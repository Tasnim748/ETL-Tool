import os
from dotenv import load_dotenv

load_dotenv()

# Determine which settings to use based on DJANGO_ENV
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .dev import *
