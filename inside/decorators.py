# -*- coding: utf-8 -*-

from functools import wraps

from flask import g
from flask.ext.login import current_user
from inside.extensions import db

def keep_login_url(func):
    """
    Adds attribute g.keep_login_url in order to pass the current
    login URL to login/signup links.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.keep_login_url = True
        return func(*args, **kwargs)
    return wrapper


def get_resource(list_role):
	result=[]
	for role_id in list_role:
		role = db.Role.get_by_id(role_id)
		if role:
			result.extend(role['resource_list'])
	return list(set(result))

def check_role_user(url_prefix):
	def check_role_user_decorator(func):
	    """
	    Adds attribute g.keep_login_url in order to pass the current
	    login URL to login/signup links.
	    """
	    @wraps(func)
	    def wrapper(*args, **kwargs):
	        if current_user.role:
	        	list_resource = get_resource(current_user.role)
	      
	        	if list_resource:
	        		layer = int(2)
	        		resource = db.Resource.get_by_prefix_action(url_prefix, func.func_name, layer)
	        		if resource is None or str(resource['_id']) not in list_resource:
	        			return 'permission denied', 403
	        	else:
	        		return 'permission denied', 403
	        else:
	        	return 'permission denied', 403

	        return func(*args, **kwargs)
	    return wrapper
	return check_role_user_decorator