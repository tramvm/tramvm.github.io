# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

from datetime import datetime, timedelta
from flask import current_app, request, url_for
from flask.ext.babel import gettext, lazy_gettext as _
from inside.extensions import db, sentry_client
from flask.ext.login import current_user
from math import ceil
from inside.extensions import app
from difflib import SequenceMatcher
from jsondiff import diff
from flask.ext.wtf import SelectField, SelectMultipleField
import hashlib
import urllib2
import os
import requests, json, traceback
import re
import ast
import base64
from slugify import slugify
from unidecode import unidecode
from paypalrestsdk import Order, ResourceNotFound
from rijndael.cipher.crypt import new as newRij
from rijndael.cipher.blockcipher import MODE_CBC
import uuid


VARCHAR_LEN_128 = 128


def get_current_time():
    return datetime.now()

def is_ascii(s):
    #use for checking no unicode character in string
    return all(ord(c) < 128 for c in s)

def is_special_character(s):
    if set("`~!@#$%^&*()+={}[];:\'\"|,<.>?").intersection(s):
        return True
    return False

def check_available_chracter_url(url):
    if is_ascii(url) and not is_special_character(url):
        return True
    return False

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = _('just now')

    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, _('year'), _('years')),
        (diff.days / 30, _('month'), _('months')),
        (diff.days / 7, _('week'), _('weeks')),
        (diff.days, _('day'), _('days')),
        (diff.seconds / 3600, _('hour'), _('hours')),
        (diff.seconds / 60, _('minute'), _('minutes')),
        (_('some'), _('seconds'), _('seconds')),
    )

    for period, singular, plural in periods:

        if not period:
            continue
        if period == (_('some')):
            return u'%s %s %s' %(period, plural, _('ago'))
        elif period == 1:
            return u'%d %s %s' %(period, singular, _('ago'))
        else:
            return u'%d %s %s' %(period, plural, _('ago'))

    return default

def pretty_duration(text_in_sec):
    """
    Returns string representing "video duration pretty" e.g.
    1 giờ 25 phút
    """

    try:
        secs    = int(text_in_sec.split('.')[0])
    except:
        return ''

    full_time   = str(timedelta(seconds=secs)) #will return as 00:45:21
    full_time   = full_time.split(':')
    hours       = full_time[0]
    mins        = full_time[1]
    secs        = full_time[2]
    return_text = u''
    if hours:
        return_text += unicode(hours) + u' giờ'
    if mins:
        return_text += u' ' + unicode(mins) + u' phút'
    if secs:
        return_text += u' ' + unicode(secs) + u' giây'
    return return_text.strip()

def convert_id_of_list_item_to_date(items):
    result = []
    for vl in items:
        the_date    = ''
        if '_id' in vl:
            the_date    = vl['_id'].generation_time
            the_date    = the_date.strftime("%d/%m/%Y %H:%M:%S")
        vl['create_time']   = the_date
        result.append(vl)
    return result

def add_months(sourcedate,months):
    import calendar
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime(year,month,day)

def url_external(filename='/'):
  host = 'http://kokokoco.com.canh/'
  full_url = host+filename
  return full_url

def convert_duration_string_to_seconds(duration_text):
    if not duration_text:
        return ''
    duration    = int(0)
    d_list      = duration_text.split(' ')
    d_list      = [d.strip(' ') for d in d_list]
    value_dict  = {u'giờ' : int(3600), u'phút' : int(60), u'giây' : int(1)}  #by second
    temp    = int(0)
    for i in d_list:
        if i in value_dict:
            duration    += temp*value_dict[i]
        else:
            try:
                temp    = int(i)
            except:
                temp    = int(0)
    print '=============duration to seconds============='
    print duration
    return str(duration) if duration > 0 else ''

def create_file_with_data(path, file_name, data_by_lines=None):
    import subprocess
    #check and create path if not exist
    if not os.path.exists(path):
        result = subprocess.call('/bin/mkdir -pv ' + path, shell = True )
    file_to_write = path + file_name
    file = open(file_to_write, 'w+')
    for i in range(0,len(data_by_lines)):
        file.write(data_by_lines[i])
        if i<(len(data_by_lines)-1):
            file.write('\n')
    file.close()
    return "DONE"

def break_line_html(text=""):
    new_text = text.split("\n")
    return new_text

def slugit(text=""):
    from slugify import slugify
    from unidecode import unidecode
    return slugify(unicode(unidecode(text)))

def get_resource(list_role):
    result=[]
    for role_id in list_role:
        role = db.Role.get_by_id(role_id)
        if role:
            result.extend(role['resource_list'])
    return list(set(result))

def get_user_role():
    #list all resource user
    list_resource = get_resource(current_user.role)
    #parser resourto to tree
    menu = db.Resource.get_menu_role(list_resource)
    user_role = {}
    if menu:
        user_role['prefix_action'] = []
        prefix_action = db.Resource.get_list_prefix_action(list_resource)
        if prefix_action:
            filter_prefix_action = []
            #list action allow for user
            for x in prefix_action:
                filter_prefix_action.append(x['prefix']+'_'+x['action'])
            user_role['prefix_action'] = filter_prefix_action
        user_role['menu'] = menu
        return user_role
    else:
        return 'false'

def log_user_action(action, old_obj=None, new_obj=None):
    from datetime import datetime
    user = unicode(current_user.login)
    time_now = datetime.now()
    log_text = unicode(action)
    if old_obj and new_obj:
        if new_obj!=old_obj:
            log_text += u' changing to:    ' + unicode(new_obj)
        else:
            log_text += u' with no change: ' + unicode(old_obj)
    elif old_obj and not new_obj:
        log_text += u': ' + unicode(old_obj)
    log_file_path = '/webapps/inside/inside/logs/user_action_log.txt'
    db.logging_user_action.insert({'time': time_now, 'user':user, 'action': log_text})
    return "DONE"

def log_activity(obj_prev, obj_after, obj_type, action_type, action_name, action_detail, action_source=''):
    log_obj = db.ActivityLog()
    log_obj.set_timestamp()
    log_obj.action_type         = action_type
    log_obj.action_name         = action_name
    log_obj.action_detail       = unicode(action_detail)
    log_obj.action_source       = action_source
    if obj_after:
        log_obj.object_id       = str(obj_after['_id'])
        result                  = log_obj.set_obj_after(obj_after)
    if obj_prev:
        result                  = log_obj.set_obj_prev(obj_prev)
    if obj_type:
        log_obj.object_type     = obj_type
    log_obj.user                = unicode(current_user.login)

    if   obj_type=='vod':
        log_obj.object_title    = obj_after.title
        log_obj.important_fields.append({'name': 'status', 'value': str(obj_after.status)})
        log_obj.important_fields.append({'name': 'platform', 'value': ', '.join(obj_after.platforms)})
        log_obj.important_fields.append({'name': 'geoip', 'value': ', '.join(obj_after.GEOIP_COUNTRY_CODE_availability)})
        log_obj.important_fields.append({'name': 'business_rule', 'value': obj_after.business_rule})
        #check and save episodes that have been added
        if len(obj_after.link)>len(obj_prev.link):
            log_obj.action_detail   += u' Add episode: '
            prev_ep_title_list  = [e['title'] for e in obj_prev.link]
            add_list            = [e2['title'] for e2 in obj_after.link if e2['title'] not in prev_ep_title_list ]
            log_obj.action_detail   += unicode(', '.join(add_list))
        elif len(obj_after.link)<len(obj_prev.link):
            log_obj.action_detail   += u'Delete episode:'
            after_ep_title_list = [e['title'] for e in obj_after.link]
            del_list            = [e2['title'] for e2 in obj_prev.link if e2['title'] not in after_ep_title_list ]
            log_obj.action_detail   += unicode(', '.join(del_list))
    elif obj_type=='livetv':
        log_obj.object_title    = obj_after.name
        log_obj.important_fields.append({'name': 'status', 'value': str(obj_after.status)})
        log_obj.important_fields.append({'name': 'platform', 'value': ', '.join(obj_after.platforms)})
        log_obj.important_fields.append({'name': 'geoip', 'value': ', '.join(obj_after.GEOIP_COUNTRY_CODE_availability)})
    elif obj_type=='event':
        log_obj.object_title    = obj_after.content.title
    elif obj_type=='highlight' and obj_after:
        log_obj.object_title    = obj_after.livetv_content.title if obj_after.type=='livetv' else obj_after.vod_content.title
    elif obj_type=='structure':
        log_obj.object_title    = obj_after.name
        log_obj.important_fields.append({'name': 'status', 'value': str(obj_after.publish)})
        log_obj.important_fields.append({'name': 'platform', 'value': ', '.join(obj_after.platforms)})
        log_obj.important_fields.append({'name': 'geoip', 'value': ', '.join(obj_after.GEOIP_COUNTRY_CODE_availability)})
    elif obj_type.find('verimatrix') != -1 :
        pass

    log_obj.save()
    return 'done'


def sentry_log_activity(msg, data, level='info'):
    sentry_client.captureMessage('Sale space: ' + msg, data=data, level=level)

    return 'done'


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def page_url(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def get_start_of_day(the_date):
    convert = the_date.strftime("%d/%m/%Y")
    convert = datetime.strptime(convert, '%d/%m/%Y')
    return convert

#-------------------------celery functions----------------------------
def queue_celery(streamName, outputFile,outputPath, start_time, duration):
    import requests
    import json
    from datetime import timedelta, datetime
    from inside.extensions import queue_celery_url

    if not (streamName and outputFile and start_time and duration):
        return False
    stop_time  = start_time + timedelta(minutes=duration)
    start_time = start_time.strftime('%d-%m-%Y %H-%M-%S')
    stop_time  = stop_time.strftime('%d-%m-%Y %H-%M-%S')

    #set output path
    outputPath = outputPath.replace('..', '')
    outputPath = '/media/record/' + outputPath

    post_para  = {'streamname':streamName, 'outputfile':outputFile,'outputpath': outputPath, 'start_time':start_time, 'stop_time':stop_time}
    r = requests.post(queue_celery_url, params=post_para)
    return r.json()

def delete_queue_celery(start_id, stop_id):
    import requests
    from inside.extensions import queue_celery_url

    if not (start_id and stop_id):
        return False
    the_para  = {'task_start_id':start_id, 'task_stop_id':stop_id}
    r = requests.delete(queue_celery_url, params=the_para)
    return True

def push_msg_celery(pushMsg_obj):
    import requests
    import json
    #from inside.extensions import push_msg_celery_url

    if not pushMsg_obj:
        return False

    for i in range(len(pushMsg_obj.platform)):
        for j in range(len(pushMsg_obj.app_name)):
            post_para  = {'title':pushMsg_obj.title, 'message':pushMsg_obj.message,'platform': pushMsg_obj.platform[i], 'msg_id': str(pushMsg_obj['_id']), 'app_name':pushMsg_obj.app_name[j], 'url': pushMsg_obj.url}
            #r = requests.post(push_msg_celery_url, params=post_para)
            url = current_app.config['IAPI_SERVER'] + 'push_notification/push_message'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(post_para), headers=headers, timeout=10)
            #only push once for ios
            if pushMsg_obj.platform[i] == 'ios':
                break

    return str(r)
#-----------------------------------end of celery function---------------------------

def check_file_exist(url=''):
  if (url.find('\\')!=-1) or (url.find(' ')!=-1):
    return int(0)
  
  video_url_check = 'http://118.69.250.114:8888/checkfile/' + url
  req = urllib2.Request(url=video_url_check)
  f = urllib2.urlopen(req)
  return int(f.read())

def export_excel(data=None):
    ''' data structure
    data: {
        'title_row': [unicode],
        'work_book': {
            'name': string,
            'sheets': [
                {
                    'name': unicode,
                    'rows': [
                        [int/unicode]
                    ]
                }
            ]
        }
    }
    '''
    import xlwt
    import os
    from inside.extensions import app
    #create work books
    book = xlwt.Workbook()
    #create sheets with sending name
    for s in data['work_book']['sheets']:
        #replace special character in name
        s['name'] = replace_multiple(s['name'])
        sh = book.add_sheet(cap(s['name'], 20))
        #create first row - the title row
        for i in range(0, len(data['title_row'])):
            sh.write(0, i, data['title_row'][i])
        #writing video list
        for i in range(0, len(s['rows'])):
            for j in range(0, len(s['rows'][i])):
                sh.write(i+1, j, s['rows'][i][j])
    #setting workbook name and save to xls file
    book_file_name = data['work_book']['name'] + '.xls'
    save_path = os.path.join(app.config['EXPORT_EXCEL_FOLDER'], book_file_name)
    book.save(save_path)

    result = 'export_files/excel/'+book_file_name
    return result

def cap(s, l):
    #capping the string by inputted length
    return s if len(s)<=l else s[0:l-3]+'...'

def replace_multiple(s, list=["`","~","!","@","#","$","%","^","&","*","(",")","+","=","{","}","[","]",";",":","'","\\","/",",","|","<",".",">","?"], r='-'):
    #replace multiple character to one
    for l in list:
        s = s.replace(l, r)
    return s

def check_download_link(text, save_path):
    import subprocess
    import urllib
    if not text:
        return ''
    if not 'http' in text:
        return text
    allowed_extension   = ['jpg', 'jpeg', 'png']
    #http in text, this is a link, download the return a path
    needed_file = text.split('/')[-1].split('.')
    file_name   = slugit(needed_file[0]) + '_' + datetime.now().strftime("%d-%m-%Y_%Hg%M-%S")
    file_ext    = slugit(needed_file[-1] if len(needed_file)>0 else 'unknown')
    for a in allowed_extension:
        if a in file_ext:
            file_ext    = a
    if file_ext not in allowed_extension:
        file_ext    = 'jpg'
    full_file   = file_name + '.' + file_ext
    file_path   = 'download/' + datetime.now().strftime("%d-%m-%Y") + '/'
    save_path  += '/' + file_path
    #check and create path if not exist
    result      = subprocess.call('/bin/mkdir -pv ' + save_path, shell = True )
    save_path  += full_file
    try:
        urllib.urlretrieve(text, save_path)
    except:
        print 'download file failed: %s' % text
        return ""
    return "%s%s" % (file_path, full_file)


def slugify_filename(filename, slugname=None, add_date=None):
    name_split = os.path.splitext(filename)
    the_name   = ''
    the_filetype   = name_split[-1]
    the_filetype = the_filetype.strip()

    #prevent unexpected character in filetype
    replace_list = "`~!@#$%^&*()+={}[];:',|<>? "
    the_filetype = replace_multiple(the_filetype, replace_list, '')

    for i in name_split[0:-1]:
        the_name += i
    now_time = ''
    if add_date == 'yes':
        now_time      = datetime.now().strftime("%d-%m-%Y_%Hg%M-%S")
    elif add_date == 'date_only':
        now_time = datetime.now().strftime("_%d-%m-%Y")
    if slugname:
        the_name = slugit(the_name)
    else:
        replace_list = ["`","~","!","@","#","$","%","^","&","*","(",")","+","=","{","}","[","]",";",":","'",",","|","<",".",">","?", " "]
        the_name = replace_multiple(the_name, replace_list, '_')
        the_name = the_name.strip()
    full_name = the_name + now_time + the_filetype
    return full_name

#------------------------------------------------------------------

def hash_video_name(video_name, time_text=None):
    video_hash = hashlib.md5()
    video_hash.update(video_name)
    if time_text:
        video_hash.update(time_text)
    return video_hash.hexdigest()

#------------------ Format phone number ---------------------------
def format_phone_number(phone):
    if not phone or not phone.isdigit():
        return ''
    phone_split = phone.split('.')
    phone = ''.join(map(str, phone_split))
    if phone[0] == '0' and len(phone) >= 10:
        phone = '84' + phone[1:]
    return phone
    """
    elif phone[:2] != '84':
        phone = '84' + phone
        return phone
    elif phone[:2] == '84':
        return phone
    """
#------ Call Front-end API when Content adds, edits, or delete WC U20 showtimes ------
def call_remove_match_api(match_id):
    """
    Call front-end API when content deletes a World Cup U20 showtime
    """
    if not match_id:
        return False

    del_url = current_app.config['E_BALL_API'] + 'apibackend/removematch'
    payload = {'id': match_id}
    headers = {
        'Content-Type': 'application/json',
        'X-BACKEND': '8b3cc6532d339d019b8359f77d40c484',
        'X-TOKEN': 'imdbn8mEe7ExzjTBPhkb'
    }

    try:
        resp = requests.post(del_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code != 200:
            print "Failed to call front-end API to delete match. Status code: {}".format(resp.status_code)
            return False
        result_json = resp.json()

        # If call api successful
        if result_json and int(result_json['code']) == 4:
            print "Call API to delete match {} successful".format(match_id)
            return True

        # Call failed
        print "Failed to call api to delete match {}".format(match_id)
        print 'Returned error code: {}'.format(result_json['code']) if result_json['code'] else ''
        print u''.join((result_json['message']) ).encode('utf-8').strip()

    except:
        print "Request to front-end api failed. Either the server is down or request timeout after 10 seconds."
    return False

def call_edit_match_api(match_id, name_team_1, name_team_2, short_name_1, short_name_2, avarta_1, avarta_2, start_time, finished, goal_team_1, goal_team_2):
    """
    Call front-end API when content edits a World Cup U20 showtime
    """
    if not match_id:
        return False

    edit_url = current_app.config['E_BALL_API'] + 'apibackend/setmatch'
    payload = {
        'id': match_id,
        'name_team_1': name_team_1,
        'name_team_2': name_team_2,
        'start_time': start_time,
        'finished': finished,
        'goal_team_1': goal_team_1,
        'goal_team_2': goal_team_2,
        'avatar_team_1': avarta_1,
        'avatar_team_2': avarta_2,
        'short_name_team_1': short_name_1,
        'short_name_team_2': short_name_2,
    }

    headers = {
        'Content-Type': 'application/json',
        'X-BACKEND': '8b3cc6532d339d019b8359f77d40c484',
        'X-TOKEN': 'imdbn8mEe7ExzjTBPhkb'
    }

    try:
        resp = requests.post(edit_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code != 200:
            print "Failed to call front-end API to edit match. Status code: {}".format(resp.status_code)
            return False
        result_json = resp.json()

        # If call api successful
        if result_json and int(result_json['code']) in [2, 7]:
            print "Call API to edit match {} successful".format(match_id)
            return True

        # Call failed
        print "Failed to call api to edit match {}".format(match_id)
        print 'Returned error code: {}'.format(result_json['code']) if result_json['code'] else ''
        print u''.join((result_json['message']) ).encode('utf-8').strip()

    except:
        print "Request to front-end api failed. Either the server is down or request timeout after 10 seconds."
        traceback.print_exc()
    return False

def str_to_bool(s):
    """
    Convert string to boolean
    """
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError("Cannot convert {} to a bool".format(s))

def call_id_check_otp(phone):
    """
    Call ID api to check otp for a phone number
    """
    if not phone:
        return False
    else:
        phone = format_phone_number(phone)

    call_url = current_app.config['ID_SERVER'] + 'api/id_ver5/otp/check_otp_phone'
    headers  = {'Content-Type': 'application/json'}
    payload  = {
        'secret_key': '3n.T/P9@zV_9 Qj8^-f?',
        'phone': phone
    }

    try:
        resp = requests.post(call_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code != 200:
            print "Failed to call ID API to check OTP info. Status code: {}".format(resp.status_code)
            return False

        result_json = resp.json()
        # If call api successful
        if result_json and int(result_json['status']) == 1:
            print "Call ID API to get OTP info for {} successful".format(phone)
            return result_json['otp_info']

        # Call failed
        print 'Returned error code: {}'.format(result_json['error_code']) if result_json['error_code'] else ''
        print u''.join((result_json['msg']) ).encode('utf-8').strip()
        return False

    except:
        traceback.print_exc()
        return False


def call_id_post(payload, url):
    """
    Call ID api to get list
    """

    call_url = current_app.config['ID_SERVER'] + url
    headers  = {'Content-Type': 'application/json'}
    if 'secret_key' not in payload:
        payload['secret_key'] = '3n.T/P9@zV_9 Qj8^-f?'

    try:
        resp = requests.post(call_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()

        print "Failed to call ID API. Status code: {}".format(resp.status_code)
        return False

    except:
        traceback.print_exc()

    return False


def call_iapi_send_email(title, content, to_emails=[]):
    """
        Call Internal api to send emails to a group of users
    """
    request_ok = True
    if to_emails:
        url = current_app.config['IAPI_SERVER'] + 'mailer/send_email_common'

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'title': title,
            'content': content,
            'email': to_emails,
        }

        try:
            res = requests.post(url, data=json.dumps(data), headers=headers, timeout=2)
            res_json = res.json()

            if not res_json['error_code'] == 0:
                request_ok = False
        except:
            request_ok = False
            traceback.print_exc()
    else:
        print 'Does not provide destination emails'
        request_ok = False

    return request_ok


def call_iapi_send_sms(content, phone, admin_note='Content Publish Confirmation'):
    """
        Call Internal api to send SMS to a VN phone number
    """

    payload = {
        'content': content,
        'phone': phone,
        'admin_note': admin_note
    }

    # resp = task_client.crete_task('/taskqueue/sms/send', "POST", payload, current_app=current_app)
    # if not resp:
    #     print 'Fail send SMS.'
    #     return False
    #
    # return True


def send_publish_request_sms_n_email(video_edit_url, old_obj, video_obj, admin_emails, admin_phones, notes='',
                                     form=None):
    if not old_obj or old_obj.status != int(1):
        mail_title = 'Content Publish Request'
    else:
        mail_title = 'Content Update'
    vod_changed, mail_content = build_vod_publish_mail_content(video_edit_url, old_obj, video_obj, notes, form)
    if not vod_changed:
        print 'Don\'t send email. No changes in video object.'
    else:
        request_ok = call_iapi_send_email(mail_title, mail_content, admin_emails)
        if request_ok:
            print 'Call IAPI send email done'
            # for phone in admin_phones:
            #     sms_content = 'Content Publish Request ' + video_edit_url
            #     request_ok = call_iapi_send_sms(sms_content, phone)
            #     if request_ok:
            #         print 'Call IAPI send sms done for phone ', phone


def html_diff(s1, s2, diff_whole=False):
    def get_append_text(sequence, start, end, out):
        append_text = ''
        try:
            # Handle the case input is list
            if type(sequence) is list:
                append_text = ','.join(sequence[start:end])
                if out:
                    append_text = ',' + append_text
            # Handle the case input is string
            else:
                append_text = sequence[start:end]
        except:
            print 'Get append text exception on', sequence
            traceback.print_exc()
        return append_text

    diff_ok, out1, out2 = True, u'', u''
    if diff_whole:
        out1 = '<span style="background-color: #D2691E">' + unicode(s1) + '</span>'
        out2 = '<span style="background-color: #FFD700">' + unicode(s2) + '</span>'
    else:
        try:
            s1 = unicode(s1) if type(s1) is int else s1
            s2 = unicode(s2) if type(s2) is int else s2
            s = SequenceMatcher(None, s1, s2, autojunk=False)
            for op_code in s.get_opcodes():
                append_html_1, append_html_2 = u'', u''
                if op_code[0] == 'equal':
                    out1 += get_append_text(s1, op_code[1], op_code[2], out1)
                    out2 += get_append_text(s2, op_code[3], op_code[4], out2)
                if op_code[0] == 'replace':
                    append_html_1 = '<span style="background-color: #D2691E">' + get_append_text(s1, op_code[1], op_code[2], out1) + '</span>'
                    out1 += append_html_1
                    append_html_2 = '<span style="background-color: #FFD700">' + get_append_text(s2, op_code[3], op_code[4], out2) + '</span>'
                    out2 += append_html_2
                if op_code[0] == 'insert':
                    append_html_2 = '<span style="background-color: #FFD700">' + get_append_text(s2, op_code[3], op_code[4], out2) + '</span>'
                    out2 += append_html_2
                if op_code[0] == 'delete':
                    append_html_1 = '<span style="background-color: #D2691E">' + get_append_text(s1, op_code[1], op_code[2], out1) + '</span>'
                    out1 += append_html_1
        except:
            traceback.print_exc()
            print 'Expception HTML Diff', s1, s2
            diff_ok = False
    return diff_ok, re.sub('\r\n|\r|\n', '<br>', out1), re.sub('\r\n|\r|\n', '<br>', out2)


def get_key_changed(dict1, dict2, ignore_keys=[]):
    '''This is for comparing 2 dictionaries to find out values of which keys change'''
    dict_diff = diff(dict1, dict2, syntax='explicit', dump=True)
    keys_changed = list(ast.literal_eval(dict_diff)['$update'].iterkeys())
    return list(set(keys_changed) - set(ignore_keys))


def build_vod_publish_mail_content(video_edit_url, old_obj, video_obj, notes, form):
    vod_changed = True
    notes = re.sub('\r\n|\r|\n', '<br>', notes)
    standing_img_url = app.config["VIDEO_IMG_DOMAIN"] + video_obj.standing_img if video_obj.standing_img else ''
    small_img_url = app.config["VIDEO_IMG_DOMAIN"] + video_obj.small_img if video_obj.small_img else ''
    uploader = (
        current_user.login + " (" + current_user.first_name + " " + current_user.last_name + ")") if current_user else ""
    mail_content = "<a href='" + video_edit_url + "'>" + video_edit_url + "</a>" + "<br><strong>Title origin:</strong> " \
                   + video_obj.title_origin + "<br><strong>Vietnamese title:</strong> " + video_obj.title_vie \
                   + u"<br><strong>Poster đứng:</strong> " + "<a href='" + standing_img_url + "'>" + standing_img_url + "</a>" \
                   + u"<br><strong>Poster ngang:</strong> " + "<a href='" + small_img_url + "'>" + small_img_url + "</a>" \
                   + "<br><strong>Notes:</strong> " + "<br>" + notes \
                   + "<br><strong>Uploader:</strong> " + uploader; \

    if old_obj:
        # Get changes between the old and new object
        keys_diff = get_key_changed(json.loads(old_obj.to_json()), json.loads(video_obj.to_json()),
                                    ignore_keys=['last_video_add_date', '_id', 'actors_detail', 'directors_detail',
                                                 'manufacturers_detail', 'payment', 'priority', 'structure_id',
                                                 'slug', 'slug_title', 'like', 'recommended_videos', 'nations_list'])
        # If there are changes, build the mail content
        if keys_diff:
            notes = re.sub('\r\n|\r|\n', '<br>', notes)
            standing_img_url = app.config["VIDEO_IMG_DOMAIN"] + video_obj.standing_img if video_obj.standing_img else ''
            small_img_url = app.config["VIDEO_IMG_DOMAIN"] + video_obj.small_img if video_obj.small_img else ''
            uploader = (
                current_user.login + " (" + current_user.first_name + " " + current_user.last_name + ")") if current_user else ""
            mail_content = "<a href='" + video_edit_url + "'>" + video_edit_url + "</a>" + "<br><strong>Title origin:</strong> " \
                           + video_obj.title_origin + "<br><strong>Vietnamese title:</strong> " + video_obj.title_vie \
                           + u"<br><strong>Poster đứng:</strong> " + "<a href='" + standing_img_url + "'>" + standing_img_url + "</a>" \
                           + u"<br><strong>Poster ngang:</strong> " + "<a href='" + small_img_url + "'>" + small_img_url + "</a>" \
                           + "<br><strong>Notes:</strong> " + "<br>" + notes \
                           + "<br><strong>Uploader:</strong> " + uploader; \

            mail_content += '<br>'
            mail_content += '<table style="width:100%" border="1">'
            mail_content += '<tr><th></th><th>Old</th><th>New</th></tr>'

            # Special handle for some fields, does not provide diff on these fields
            special_keys = {
                'link': 'Episodes',
                'advertisement': {
                    0: 'No',
                    1: 'Yes',
                }
            }

            for key in keys_diff:
                is_select_field = False
                # Handle special keys
                if key in special_keys.iterkeys():
                    if key == 'advertisement':
                        mail_content += '<tr><td>' + key + '</td><td valign="top">' + '<span style="background-color: #D2691E">' + special_keys[key][old_obj.advertisement['enable_ads']] \
                                        + '</span>' + '</td><td valign="top">' + '<span style="background-color: #FFD700">' + special_keys[key][video_obj.advertisement['enable_ads']]\
                                        + '</span>' + '</td></tr>'
                    else:
                        mail_content += '<tr><td>' + key + '</td><td>''</td><td>' + 'Update ' + special_keys[
                            key] + '</td></tr>'
                else:
                    try:
                        # From value, get label of SelectField fields provided in form for displaying
                        form_field = getattr(form, key)
                        if form_field:
                            if isinstance(form_field, SelectMultipleField) and form_field.choices:
                                for index, val in enumerate(old_obj[key]):
                                    for choice in form_field.choices:
                                        if choice[0] == val:
                                            old_obj[key][index] = unicode(choice[1])
                                for index, val in enumerate(video_obj[key]):
                                    for choice in form_field.choices:
                                        if choice[0] == val:
                                            video_obj[key][index] = unicode(choice[1])
                            elif isinstance(form_field, SelectField) and form_field.choices:
                                is_select_field = True
                                for choice in form_field.choices:
                                    if choice[0] == old_obj[key]:
                                        old_obj[key] = unicode(choice[1])
                                    if choice[0] == video_obj[key]:
                                        video_obj[key] = unicode(choice[1])
                    except:
                        traceback.print_exc()
                        print 'Video form exception on key', key

                    diff_ok, old_html, new_html = html_diff(old_obj[key], video_obj[key], is_select_field)
                    if diff_ok:
                        mail_content += '<tr><td>' + key + '</td><td valign="top">' + old_html + '</td><td valign="top">' + new_html + '</td></tr>'
            mail_content += '</table>'
        else:
            # No changes in video object
            vod_changed = False
    return vod_changed, mail_content


def call_iapi(method, uri, data):
    """
        Call Internal api to do something
    """
    url = current_app.config['IAPI_SERVER'] + uri

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        if method == 'post':
            r = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
        else:
            r = requests.get(url, params=data, headers=headers, timeout=10)

        return True
    except:
        return False
        traceback.print_exc()


def encrypt_uid(str):
    if (len(str) < 6):
        str_len = 6 - len(str)
        str_sub = "0"
        for i in range(1, str_len):
            str_sub += "0"

        str = str_sub + str

    str_all = "94087512639408751263"
    str_all_num = "67803541296780354129"
    final_str = ""

    j = 0
    for i in range(1,len(str)+1):
        if (j == 0):
            text = str[0:1]
        else:
            text = str[i-1:i]

        if (i % 2 == 0):
            temp = (int(text) - i - len(str) + 100) % 10
            final_str += str_all_num[temp:temp+1]
        else:
            temp = (int(text) + i + len(str) + 100) % 10
            final_str += str_all[temp:temp+1]

        j = 1
    return final_str


def decrypt_uid(euid):
    str_all = '94087512639408751263'
    str_all_num = '67803541296780354129'
    final_str = ''
    j = 0
    for i in range(1, len(euid) + 1):
        if j == 0:
            text = euid[:1]
        else:
            text = euid[i - 1:i]
        if i % 2 == 0:
            if type(str_all_num.index(text)) == int:
                val = ((str_all_num.index(text) + i + len(euid)) + 100) % 10
                final_str += str(val)[:1]
            else:
                return 0
        else:
            if type(str_all.index(text)) == int:
                val = ((str_all.index(text) - i - len(euid)) + 100) % 10
                final_str += str(val)[:1]
            else:
                return 0
        j = 1
    if len(final_str) == 6:
        # print (final_str)
        if final_str[:5] == '00000':
            final_str = final_str[5:]

        if final_str[:4] == '0000':
            final_str = final_str[4:]

        if final_str[:3] == '000':
            final_str = final_str[3:]

        if final_str[:2] == '00':
            final_str = final_str[2:]

        if final_str[:1] == '0':
            final_str = final_str[1:]
    return final_str


api_domain = 'https://api.fptplay.net'
user_token = ''
static_ip = '172.129.14.79'
secure_key = 'kvTPsISSkvBe3dG7sx7krUMqs02Nsxow'


def secure_link_url(url):
    """
    https://api.fptplay.net/api/v5.1_pana_ng/vod/5b8ca9b95583201989b9a976?version=fptplay_2.20&device=Panasonic(version:,model:)&nettype=wifi&e=1537345797&st=JLolD-4VnOJ5vYWBW859JA
    :param url:
    :return:
    """

    expire_time = (datetime.utcnow() + timedelta(minutes=60, hours=+7)) - datetime(1970, 1, 1)
    expire_time = str(int(expire_time.total_seconds()))

    uri = url.replace(api_domain, '')

    uri_secure = uri
    if uri.find('?') > -1:
        uri_secure = uri[0: uri.find('?')]

    # print secure_key, expire_time, uri_secure
    secure_link = secure_key + expire_time + uri_secure

    secure_link = hashlib.md5(secure_link).digest()
    # print "secure link:", secure_link
    secure_link = base64.b64encode(secure_link)
    secure_link = secure_link.replace("+", "-")
    secure_link = secure_link.replace("/", "_")
    secure_link = secure_link.replace("=", "")
    # print "secure link:", secure_link
    browserName = 'smart-tv(version:null,model:null)'

    user = 'null'
    ip = '&ip=' + static_ip

    if uri.find('?') > -1:
        url = url + '&st=' + secure_link + '&e=' + expire_time + '&version=fptplay_2.20&device=' + browserName + '&nettype=wifi&user_id=' + user + ip
    else:
        url = url + '?st=' + secure_link + '&e=' + expire_time + '&version=fptplay_2.20&device=' + browserName + '&nettype=wifi&user_id=' + user + ip

    return url


def get_episode_detail(video_id, epi_id, profile="auto_vip"):
    url = api_domain + "/api/v5.1_ssam_ng/stream/vod/" + video_id + "/" + str(epi_id) + "/" + profile
    url = secure_link_url(url)
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DID'] = 'null'
    headers['Authorization'] = 'Bearer ' + user_token
    # print headers
    print url
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code in [200, 201]:
            temp_vod = resp.json()
            if temp_vod and temp_vod['status'] == 1:
                stream_url = temp_vod["data"]["url"]
                data = {
                    "stream_url": stream_url
                }
                return data
            print temp_vod
        else:
            print 'request status:', resp.status_code
    except:
        traceback.print_exc()

    return None


def get_video_detail(video_id):
    url = api_domain + "/api/v5.1_ssam_ng/vod/" + video_id
    url = secure_link_url(url)
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DID'] = 'null'
    headers['Authorization'] = 'Bearer ' + user_token
    # print headers
    print url
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code in [200, 201]:
            #print resp.json()
            temp_vod = resp.json()
            if temp_vod['result']:
                temp_vod = temp_vod['result']
                vod_obj = {
                    "_id": video_id,
                    "status": int(1),
                    "content_rating": str(temp_vod["content_rating"]) if 'content_rating' in temp_vod else "",
                    "recommended_videos": [],
                    "business_rule": "",  # TODO Default or user manual select business rule
                    "tags_genre": temp_vod["tags_genre"] if 'tags_genre' in temp_vod else [],
                    "description_foreign": temp_vod['description_foreign'] if 'description_foreign' in temp_vod else '',
                    "episode_latest": int(temp_vod["episode_latest"]) if 'episode_latest' in temp_vod else int(1),
                    "crawl_source": "fptplay",
                    "last_video_add_date": datetime.strptime(temp_vod['last_episode_update'], '%d/%m/%Y %H:%M') if 'last_episode_update' in temp_vod else datetime.utcnow().strftime('%d/%m/%Y %H:%M'),
                    "platforms": [
                        "appletv",
                        "amazon",
                        "ott-box",
                        "smarttv-android",
                        "smarttv-lg",
                        "smarttv-sn",
                        "smarttv-ss",
                        "platform-verify"
                    ],
                    "tvod": int(0),
                    "episode_current": int(temp_vod['episode_current']) if 'episode_current' in temp_vod else int(1),
                    "source_provider": [
                        "nguoi-dung"
                    ],
                    "age_min": int(0),
                    "duration": temp_vod['duration'] if 'duration' in temp_vod else "",
                    "directors_detail": temp_vod['directors_detail'] if 'directors_detail' in temp_vod else [],
                    "avrg_duration": temp_vod['avrg_duration'] if 'avrg_duration' in temp_vod else "",
                    "viewCount": int(0),
                    "category": [
                        "VOD"
                    ],
                    "actors_detail": temp_vod['actors_detail'] if 'actors_detail' in temp_vod else [],
                    "slug_title": str(temp_vod['slug']) if 'slug' in temp_vod else '',
                    "sub": int(temp_vod['sub']) if 'sub' in temp_vod else int(-1),
                    "rating_total_count": "",
                    "title": temp_vod['title'] if 'title' in temp_vod else '',
                    "notification": "",
                    "dub": int(temp_vod['dub']) if 'dub' in temp_vod else int(-1),
                    "manufacturers": temp_vod["manufacturers"] if 'manufacturers' in temp_vod else [],
                    "directors": temp_vod['directors'] if 'directors' in temp_vod else [],
                    "payment": {
                        "requirement": []
                    },
                    "priority": {},
                    "description_banner": temp_vod['description_banner'] if 'description_banner' in temp_vod else '',
                    "manufacturers_detail": temp_vod[
                        'manufacturers_detail'] if 'manufacturers_detail' in temp_vod else [],
                    "actors": temp_vod['actors'] if 'actors' in temp_vod else [],
                    "ribbon_logo": "",
                    "episode_total": int(temp_vod['episode_total']) if 'episode_total' in temp_vod else int(1),
                    "title_vie": temp_vod['title_vie'] if 'title_vie' in temp_vod else '',
                    "small_img": str(temp_vod['thumb']) if 'thumb' in temp_vod else '',
                    "overlay_logo": "",
                    "title_origin": temp_vod['title_origin'] if 'title_origin' in temp_vod else '',
                    "type": str(temp_vod['type']) if 'type' in temp_vod else 'general',
                    "standing_img": str(temp_vod['standing_thumb']) if 'standing_thumb' in temp_vod else '',
                    "age_max": int(100),
                    "description": temp_vod['description'] if 'description' in temp_vod else '',
                    "admin_note": "crawl",
                    "tags": temp_vod['tags'] if 'tags' in temp_vod else [],
                    "encode_system": int(0),
                    "big_img": str(temp_vod['banner_thumb']) if 'banner_thumb' in temp_vod else '',
                    "nations_list": temp_vod['nations_list'] if 'nations_list' in temp_vod else [],
                    "nation": str(temp_vod['nation']) if 'nation' in temp_vod else '',
                    "sync_platforms": int(1),
                    "link": [],
                    "logo_img": "",
                    "advertisement": {
                        "enable_ads": int(0)
                    },
                    "sync_geoip": int(1),
                    "uploader": "",
                    "structure_id": temp_vod["list_structure_id"],
                    "pin_top": int(0),
                    "ribbon_payment": "",
                    "dub_index": int(temp_vod['dub_index']) if 'dub_index' in temp_vod else int(-1),
                    "slug": '',  # TODO add or reqrite
                    "anthology": int(0) if 'is_anthology' not in temp_vod or not temp_vod['is_anthology'] else int(1),
                    "available_url": [
                        "mp4"
                    ],
                    "isp": ["fpt", "other", "vnpt", "spt", "viettel"],
                    "ribbon_partner": "",
                    "sub_index": int(temp_vod['sub_index']) if 'sub_index' in temp_vod else int(-1),
                    "like": int(0),
                    "GEOIP_COUNTRY_CODE_availability": ["REST_OF_THE_WORLD", "VN", "LOCAL_TEST"],
                    "imdb_rating": "",
                    "updating_status": int(0),
                    "release": str(temp_vod["movie_release_date"]) if 'movie_release_date' in temp_vod else "",
                    "crawl_source_url": "",
                    "trailer_url": "",
                    "episode_type": "Series" if 'episode_type' in temp_vod and temp_vod[
                                                                                   'episode_type'] == 1 else 'Single',
                    "tags_plot": temp_vod['tags_plot'] if 'tags_plot' in temp_vod else [],
                    "verimatrix": int(0),
                }

                vod_obj['slug'] = slugify(unicode(unidecode(vod_obj['title'])))

                # Remove domain image
                vod_obj["small_img"] = vod_obj["small_img"][vod_obj["small_img"].find("/", 45) + 1:] if vod_obj["small_img"] else ''
                vod_obj["standing_img"] = vod_obj["standing_img"][vod_obj["standing_img"].find("/", 45) + 1:] if vod_obj["standing_img"] else ''
                vod_obj["big_img"] = vod_obj["big_img"][vod_obj["big_img"].find("/", 45) + 1:] if vod_obj["big_img"] else ''
                vod_obj["logo_img"] = vod_obj["logo_img"][vod_obj["logo_img"].find("/", 45) + 1:] if vod_obj["logo_img"] else ''

                # Set priority
                count_s = 1
                if vod_obj["structure_id"]:
                    for s in vod_obj["structure_id"]:
                        vod_obj["priority"][s] = int(count_s)
                        count_s = count_s + 1

                links = []
                # Build episode
                for epi in temp_vod['episodes']:
                    episode = {
                        "standing_img": str(epi['standing_img']) if 'standing_img' in epi else '',
                        "description": "",
                        "hls": "fake.mp4",
                        "mp4": "fake.mp4",
                        "uploader": "",
                        "duration": str(epi['duration']) if 'duration' in epi else '',
                        "timeline_img": "",
                        "img": str(epi['thumb']) if 'thumb' in epi else '',
                        "title": epi['title'] if 'title' in epi else '',
                        "publish": int(1),
                        "end_time": int(0),
                        "streams": []
                    }
                    episode['standing_img'] = episode["standing_img"][episode["standing_img"].find("/", 45) + 1:] if episode["standing_img"] else ''
                    episode['img'] = episode["img"][episode["img"].find("/", 45) + 1:] if episode["img"] else ''
                    streams = []
                    epi_id = epi['_id']
                    for u in epi["url"]:
                        profile_id = u['_id']
                        prorile_name = u['name']
                        episode_detail = get_episode_detail(video_id, epi_id, profile_id)
                        stream = {
                            "url": str(episode_detail['stream_url']),
                            "hls": str(episode_detail['stream_url']),
                            "requirement": [],
                            "type": str(profile_id),
                            "name": str(prorile_name),
                        }
                        streams.append(stream)
                    episode['streams'] = streams
                    links.append(episode)

                vod_obj["link"] = links

                return vod_obj
        else:
            print 'request status:', resp.status_code
    except:
        traceback.print_exc()

    return None


#video_id = "59cdf7975583202639c1842d"
#print get_video_detail(video_id)


def call_crawl_video(video_id, page=1):

    print 'Call get call_crawl_video'
    endpoint_url = current_app.config['CRAWLER_URL'] + 'crawl/video'
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data_send = {
        'video_id': video_id,
        'page': page,
    }

    try:
        response_data = requests.post(url=endpoint_url, data=data_send, headers=headers, timeout=120)
        if response_data.json():
            return response_data.json()
        else:
            print 'Request get crawl fail. No json returned.'
            return {'result': 0,
                    'msg': 'Request get snapshot failed. Either the server is down or connection timeout after 10s.'}
    except:
        traceback.print_exc()
        print 'Request get snapshot failed. Either the server is down or connection timeout after 10s.'
        return {'result': 0,
                'msg': 'Request get snapshot failed. Either the server is down or connection timeout after 10s.!'}


def is_valid_email(email):
    if len(email) > 7:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match == None:
            return False
    return True


def process_paypal_order(order_id):
    try:
        order = Order.find(order_id)
        print("Got Order details for Order[%s]" % (order.id))

    except ResourceNotFound as error:
        print("Order Not Found")


BLOCK_SIZE = 16
KEY_HEX = '2CF92C76DEB98ADC19C5F2138D797D9003D9AE5BCFA223B097894DC47DDE20C2'
IV_HEX = '13192C2C76797D8A8D90B9C5DCDEF2F9'

KEY = None
IV = None


def initKey():
    global KEY
    global IV
    KEY = KEY_HEX.decode("hex")
    IV = IV_HEX.decode("hex")

def enc(data):
    initKey()
    rjn = newRij(KEY, MODE_CBC, IV, blocksize=BLOCK_SIZE)
    output = rjn.encrypt(data)
    result = base64.urlsafe_b64encode(output)
    return result

def dec(data):
    initKey()
    input = base64.urlsafe_b64decode(data)
    rjn = newRij(KEY, MODE_CBC, IV, blocksize=BLOCK_SIZE)
    output = rjn.decrypt(input)
    return output

def generate_key():
    data = str(uuid.uuid4()).replace('-', '1').upper()
    return data

def get_ssmms_link(token):
    output = enc('LW|1.2|'+token[0, 12].upper()+'|' + generate_key())
    return "https://onlinebooking.sand.telangana.gov.in/SPHJILAL/Masters/YUVA.aspx?DFGJ=" + output
