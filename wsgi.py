from base import app
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

application = DispatcherMiddleware( None, {'/':app})

if __name__ == '__main__':
        run_simple('localhost', 8001, application, user_reloader=True)

