# Statement for enabling the development environment
DEBUG = False
NOMAIL = False
NODB = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
MAIL_SERVER = "secure.pigeonpost.com.au"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEBUG = False
MAIL_USERNAME = 'lg@idealcs.com.au'
MAIL_PASSWORD = 'h289andd'
WTF_CSRF_ENABLED = True
SECRET_KEY = '95d6eadcb8c171a323d9208013a8d619077420e3cd67bcc9'
WTF_CSRF_SECRET_KEY = '95d6eadcb8c171a323d9208013a8d619077420e3cd67bcc9'
