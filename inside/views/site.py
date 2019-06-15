# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, current_app, redirect, request, send_from_directory, safe_join)
from ..utils import sentry_log_activity
import json

site = Blueprint('site', __name__)


@site.route('/')
@site.route('/index.html')
@site.route('/index')
def index():
    projects = current_app.config['PROJECTS']
    page_title = "Source code How to recognize bubble sheet with Android and OpenCV"
    return render_template('index.html', projects=projects, page_title=page_title)


@site.route('/about.html')
@site.route('/about')
def about():
    page_title = "About Source code How to recognize bubble sheet with Android and OpenCV"
    return render_template('about.html', page_title=page_title)


@site.route('/privacy')
def privacy():
    page_title = "Privacy Policy"
    return render_template('privacy.html', page_title=page_title)


@site.route('/contact.html')
@site.route('/contact')
def contact():
    page_title = "Contact Source code How to recognize bubble sheet with Android and OpenCV"
    return render_template('contact.html', page_title=page_title)


@site.route('/project/<string:id>/<string:any>')
def project(id, any):
    print id, any
    projects = current_app.config['PROJECTS']
    for p in projects:
        if p['id'] == id:
            return render_template('single-project.html', page_title=p['title'], project=p)

    # Redirect home
    return redirect('index')


@site.route('/paypal-transaction-complete', methods=['POST'])
def paypal_transaction_complete():
    print "User pay. Order ID"
    paypal_data = json.loads(request.data)
    print paypal_data['order_id'], paypal_data['payer_id'], paypal_data['payer_email']
    data = {
        'request': {
            'data': {
                'order_id': paypal_data['order_id'],
                'payer_id': paypal_data['payer_id'],
                'payer_email': paypal_data['payer_email'],
                'amount': paypal_data['amount']
            }}
    }

    sentry_log_activity('User pay. Order id: ' + paypal_data['order_id'] + '. user email: ' + paypal_data['payer_email'] + '. Amount: ' + str(paypal_data['amount']), data)

    # Redirect home
    return redirect('index')


@site.route('/paypal-webhook', methods=['POST'])
def paypal_webhook():
    print "User pay. Order ID"

    # Redirect home
    return redirect('index')


@site.route('/message', methods=['POST'])
def message():
    data = {
        'request': {
            'data': {
                'name': request.form['name'],
                'email': request.form['email'],
                'message': request.form['message']
            }}
    }
    print "================ Message ==================="
    print data
    sentry_log_activity('User message to contact ' + request.form['email'], data)
    return redirect('index')


@site.route('/single-post.html')
@site.route('/single-post')
def single_post():
    page_title = "About Source code How to recognize bubble sheet with Android and OpenCV"
    return render_template('single-post.html', page_title=page_title)


@site.route('/robots.txt')
@site.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


@site.route('/player-videojs')
def test_player():
    projects = "Test LIVE"
    page_title = "Test LIVE"
    return render_template('player-videojs.html', projects=projects, page_title=page_title)