# -*- coding: utf-8 -*-

import datetime
from flask.ext.login import UserMixin
from flask.ext.mongokit import Document
from mongokit import IS
from mongokit import ObjectId
from werkzeug import (generate_password_hash, check_password_hash)

from inside.extensions import db


class User(Document, UserMixin):
    __collection__ = 'users'
    use_dot_notation = True

    structure = {
        'login'                     : unicode,
        'first_name'        : unicode,
        'last_name'         : unicode,
        'email'             : unicode,
        'tz'                : basestring,
        'locale'            : IS(u'vi_VN', u'en_US'),
        'company'           : unicode,
        'address'           : unicode,
        'c_time'            : datetime.datetime,
        'la_time'           : datetime.datetime,
        '_password'         : basestring,
        'a_key'             : basestring,
        'role'              : [unicode],
        'phone'             : unicode,
    }
    default_values = {
        'first_name'        : u'',
        'last_name'         : u'',
        'locale'            : u'vi_VN',
        'tz'                : r'Asia/Ho_Chi_Minh',
        'a_key'             : None,
        'phone'             : u'',
    }
    required = ['login', 'email']
    indexes = [{
        'fields':['login', 'email', 'a_key'],
        'unique':True,
    },]

    def get_page(self, page=1, PER_PAGE=15):
        return db.User.find().skip(PER_PAGE*(page-1)).limit(PER_PAGE)
    def get_iduser(self, user_id):
        return db.User.find_one({'_id': ObjectId(user_id)})
    def get_login(self, user_id):
        return db.User.find_one({'_id': ObjectId(user_id)}).login

    def remove_id(self, user_id):
        return db.User.collection.remove({'_id': ObjectId(user_id)})


    def count(self):
        return db.User.find().count()


    def __repr__(self):
        return '<User %r>' % self.login

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = property(_get_password, _set_password)

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def get_id(self):
        return unicode(self.login)

    def find_user(self, login):
        """docstring for find_user"""
        return db.User.find_one({ '$or' : [{'email': login}, {'login' : login}]})

    def find_activation_key(self, key):
        """Find inactive user by activation key"""
        return db.User.find_one({'a_key': key})

    @property
    def display_name(self):
        """return Fist name + Last name or email"""
        if self.last_name == '' and self.first_name == '':
            return self.email
        return '%s %s' %(self.first_name, self.last_name)

    def is_active(self):
        return True if self.a_key is not None else False

    def authenticate(self, login, password):
        authen_id = True;
        user = db.User.find_user(login)
        if user:
            authenticated = user.check_password(password)
        else:
            authen_id = authenticated = False

        return user, authen_id, authenticated

    def get_all(self):
      return db.User.find()

    def get_content_admin_emails_n_phones(self):
        """Get all users who own Publish role"""
        # admins = db.User.find({'role': '59dc2bf5631ce45689269252'}, {'_id': 0, 'phone': 1, 'email': 1})
        admins = db.User.find({'role': '59f188fd55832008505e19df'}, {'_id': 0, 'phone': 1, 'email': 1})
        admin_emails, admin_phones = [], []
        for admin in admins:
            if admin.email:
                admin_emails.append(admin.email)
            if 'phone' in admin and admin.phone:
                admin_phones.append(admin.phone)
        return admin_emails, admin_phones
