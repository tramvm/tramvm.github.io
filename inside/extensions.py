# -*- coding: utf-8 -*-

from flask import current_app, session

from flask.ext.mongokit import MongoKit
db = MongoKit()

from flask.ext.mail import Mail
mail = Mail()

#from flask.ext.cache import Cache
#cache = Cache()

from redis import Redis
import os
REDIS_CACHE_HOST = os.environ['CACHE_REDIS_HOST']
REDIS_CACHE_PORT = os.environ['CACHE_REDIS_PORT']
REDIS_CACHE_DB = os.environ['CACHE_REDIS_DB']
redis_cache = Redis(host=REDIS_CACHE_HOST, port=REDIS_CACHE_PORT, db=REDIS_CACHE_DB)

from flask.ext.login import LoginManager, current_user, AnonymousUser
login_manager = LoginManager()

class Anonymous(AnonymousUser):
    def _get_locale(self):
        if 'locale' in session:
            return session['locale']
        else:
            return current_app.config.get('BABEL_DEFAULT_LOCALE')

    def _set_locale(self, locale):
        """docstring for _set_locale"""
        session['locale'] = locale

    locale = property(_get_locale, _set_locale)

login_manager.anonymous_user = Anonymous

from flask import Flask


app = Flask(__name__)

# Sentry for log
from raven import Client
sentry_client = Client(os.environ['SENTRY_DSN'])

# Redis recommend
# from redis import Redis
# redis_recommend = Redis(host="redis_test", port=6379)

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/webapps/inside/inside/client_key.json"

from .libs import TaskClient

#task_client = TaskClient()
