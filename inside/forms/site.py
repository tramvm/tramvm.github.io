# -*- coding: utf-8 -*-

from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, TextField, Label,
                          ValidationError, required, optional, equal_to, email,
                          length)
from flask.ext.babel import gettext, lazy_gettext as _
from inside.extensions import db

class LoginForm(Form):
    next        = HiddenField()
    remember    = BooleanField('Remember me')
    login       = TextField('Username or email address', [required()])
    password    = PasswordField('Password', [required(), length(min=6, max=16)])
    submit      = SubmitField('Login')
    id_error    = Label('server',text=_('Invalid Id'))
    pass_error  = Label('server',text=_('Invalid Password'))


class SignupForm(Form):
    next            = HiddenField()
    login           = TextField(_('Username'), [required()])
    password        = PasswordField(_('Password'), [required(), length(min=6, max=16)])
    password_again  = PasswordField(_('Password again'), [required(), length(min=6, max=16), equal_to('password')] )
    email           = TextField(_('Email address'), [required(), email(message=_('A valid email address is required'))])
    submit          = SubmitField(_('Sign up'))

    def validate_name(self, field):
        if db.User.find_one({'login_name': field.data}) is not None:
            raise ValidationError, gettext('This username is taken')

    def validate_email(self, field):
        if db.User.find_one({'email' : field.data}) is not None:
            raise ValidationError, gettext('This email is taken')

   
    

class RecoverPasswordForm(Form):
    email = TextField(_('Your email'), validators=[
                      email(message=_('A valid email address is required'))])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField('Password', validators=[
                             required(message=_('Password is required'))])
    password_again = PasswordField('Password again', validators=[
                                   equal_to('password', message=\
                                            _("Passwords don't match"))])
    submit = SubmitField(_('Save'))


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField('Password', [required(), length(min=6, max=16)])
    submit = SubmitField('Re-Authenticate')
