from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'testrun.deltabytestech.digital'
]  # Should be restricted in a real production environment
