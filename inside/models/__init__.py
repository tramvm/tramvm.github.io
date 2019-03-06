# -*- coding: utf-8 -*-

from inside.models.user import User
from inside.extensions import db

db.register([User])
