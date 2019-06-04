# -*- coding: utf-8 -*-

import os

APP_NAME = 'inside'


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # os.urandom(24)
    SECRET_KEY = 'secret key'


class DefaultConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_ECHO = True
    DEBUG_LOG = '/var/log/workspace.debug.log'

    ACCEPT_LANGUAGES = ['vi_VN', 'en_US']
    BABEL_DEFAULT_LOCALE = 'vi_VN'

    MONGODB_HOST = os.environ['MONGODB_HOST']
    MONGODB_PORT = int(os.environ['MONGODB_PORT'])
    MONGODB_DATABASE = os.environ['MONGODB_DATABASE']

    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']

    PROJECTS = [
        {
            'id': "1",
            'title': 'Recognize bubble sheet and input correct answers with Android + OpenCV',
            'short_title': 'Recognize bubble sheet and correct answers',
            'price': 60,
            'hit_donate': 3000,
            'total_donate': 473,
            'slug_title': 'source-code-recognize-bubble-sheet-with-android-opencv',
            'img': 'project3.png',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/SHHYEzJpedo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>This project purpose help students build there final project for graduation at school. '
                           'This project also help teachers build their tool to manage they students exams quickly. Or this '
                           'is also the prototype for professional developers to make a crazy recognize exam service.</p> '
                           '<p>The clear source code with many comments insight, and overview document help the owner understand easily.</p>'
                           '<p>Highlight features:</p>'
                           '</p><ul>'
                           '<li>Input correct answers</li>'
                           '<li>Recognize template 10 to 100 answers</li>'
                           '<li>Show result correct/number of questions, show score</li>'
                           '</ul>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. Just email to workspace.gold@gmail.com '
                           'when you need support to setting project, build, run the app.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'May 09, 2019'
                }

            ],
            'donators': [
            ]
        },
        {
            'id': "2",
            'title': 'Recognize bubble sheet with Android and OpenCV from 10 to 100 questions',
            'short_title': 'Recognize from 10 to 100 questions',
            'price': 45,
            'hit_donate': 2000,
            'total_donate': 523,
            'slug_title': 'source-code-recognize-bubble-sheet-with-android-and-opencv-from-10-to-100-questions',
            'img': 'project1.png',
            'video_embed': '<iframe width="480" height="270" src="https://www.youtube.com/embed/82FlPaQ92OU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>This page for you to purchase source code Recognize bubble sheet using Android and OpenCV. You need this source code if you are:<p>'
                           '<blockquote><p>Students need a this source code for your school project. I promise you will save time so much, because some students used this project for this purpose.</p>'
                           '<p>Teachers need this app to make your life become easy. You can implement more fetures base on this project.</p>'
                           '<p>Professional developers use this source to make a recognize exam service.</p>'
                           '<p>Or someone just need this source code to make crazy thing.</p></blockquote>'
                           '<p>The clear source code with many comments insight, and overview document help the owner understand easily.</p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. And the source code belong to you, you can do anythings with it. '
                           'Just send email to workspace.gold@gmail.com when you need support to setting project, build, run the app.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'Mar 01, 2019'
                }
                # ,
                # {
                #     'name': 'Visitor',
                #     'value': '2800+'
                # },
                # {
                #     'name': 'Donators',
                #     'value': 16
                # }

            ],
            'donators': [
                {
                    'name': 'Olvera Placido Rafael',
                    'country': 'Estado de Mexico',
                    'value': 125
                },
                {
                    'name': 'James Flamarion Silva',
                    'country': 'Brazil',
                    'value': 100
                },
                {
                    'name': 'Schley Camoren',
                    'country': 'United States',
                    'value': 100
                },
                {
                    'name': 'Dutta Prosenjit',
                    'country': 'United States',
                    'value': 90
                }
            ]

        },
        {
            'id': "3",
            'title': 'Recognize bubble sheet and manage Students, Classes, Subjects',
            'short_title': 'Recognize bubble sheet and manage students',
            'price': 55,
            'hit_donate': 2000,
            'total_donate': 473,
            'slug_title': 'source-code-recognize-bubble-sheet-with-android-opencv-and-manage-students-classes-subjects',
            'img': 'project2.png',
            'video_embed': '<iframe width="480" height="270" src="https://www.youtube.com/embed/t66OAXI9mkw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>This project purpose help students build there final project for graduation at school. '
                           'This project also help teachers build their tool to manage they students exams quickly. Or this '
                           'is also the prototype for professional developers to make a crazy recognize exam service.</p> '
                           '<p>The clear source code with many comments insight, and overview document help the owner understand easily.</p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. Just email to workspace.gold@gmail.com '
                           'when you need support to setting project, build, run the app.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'Feb 25, 2019'
                }
                # ,
                # {
                #     'name': 'Visitor',
                #     'value': '1600+'
                # },
                # {
                #     'name': 'Donators',
                #     'value': 12
                # }

            ],
            'donators': [
                {
                    'name': 'Almeida Alan',
                    'country': 'Brazil',
                    'value': 150
                },
                {
                    'name': 'Bantillo Charmel',
                    'country': 'Indonesia',
                    'value': 120
                },
                {
                    'name': 'Karabulut Deniz',
                    'country': 'Turkey',
                    'value': 90
                },
                {
                    'name': 'Enkhsaikhan Tuguldur',
                    'country': 'Mongolia',
                    'value': 70
                }
            ]
        },
        {
            'id': "4",
            'title': '100% workinng Rohtang permits auto fill info',
            'short_title': '100% workinng Rohtang permits auto fill info',
            'price': 20,
            'hit_donate': 100,
            'total_donate': 15,
            'slug_title': 'fastly-rohtang-permit',
            'img': 'project4.png',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/38LbaBDXJAM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p><strong>Only pay attention if you need succeed booking on Rohtang.</strong></p>' 
                            '<p>Chrome extension features:</p>'
                           '<ul>'
                           '<li> work on: Rohtang Pass, Green tax, Special Permit </li>'
                           '<li>auto refresh page until time come. Make sure you first guy go to this site</li>'
                           '<li>auto fill captcha</li>'
                           '<li>auto fill all fields</li>'
                           '<li>auto refresh captcha if can not recognize captcha</li>'
                           '<li>auto submit and click Proceed for payment and go to Payment method input</li>'
                           '</ul>'
                           '<p>After get extension, extract it using winrar. After that you just replace demo data by your personal data in file content.js from line 161 to line 179. Then import extension to your chrome and use.</p>'
                           '<p>No need to install any additional software.</p>'
                           '<p>Limit maximum 2 session at the same time.</p>'
                           '<p>If you need this extension, just make donation and get the extension.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'May 26, 2019'
                }
                # ,
                # {
                #     'name': 'Visitor',
                #     'value': '1600+'
                # },
                # {
                #     'name': 'Donators',
                #     'value': 7
                # }

            ],
            'donators': [
            ]
        },
        {
            'id': "5",
            'title': 'Rohtang permits auto click Proceed for Payment',
            'short_title': 'Rohtang permits auto click Proceed for Payment',
            'price': 9,
            'hit_donate': 100,
            'total_donate': 15,
            'slug_title': 'fastly-rohtang-permit-auto-click-proceed-for-payment',
            'img': 'project4.png',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/K9FsVujC6ZM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>Chrome extension features:</p>'
                           '<ul>'
                           '<li> work on: Rohtang Pass, Green tax, Special Permit </li>'
                           '<li>auto click Proceed for payment and go to Payment method input</li>'
                           '</ul>'
                           '<p>No need to install any additional software.</p>'
                           '<p>One order limited maximum 3 permits at same time. One strong PC can make at least 12 permit per day.</p>'
                           '<p>If you need above features, just make donation and get the extension.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'May 28, 2019'
                }
                # ,
                # {
                #     'name': 'Visitor',
                #     'value': '1600+'
                # },
                # {
                #     'name': 'Donators',
                #     'value': 7
                # }

            ],
            'donators': [
            ]
        },
        {
            'id': "6",
            'title': 'SSMMS Online sand booking auto fill info',
            'short_title': 'SSMMS Online sand booking auto fill info',
            'price': 15,
            'hit_donate': 100,
            'total_donate': 15,
            'slug_title': 'ssmms-online-sand-booking-auto-fill-info',
            'img': 'project6.jpg',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/wA9piBYGG4Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>Chrome extension features:</p>'
                           '<ul>'
                           '<li>work on: https://onlinebooking.sand.telangana.gov.in</li>'
                           '<li>auto fill captcha</li>'
                           '<li>auto fill username, password</li>'
                           '<li>auto login after 20s</li>'
                           '<li>lifetime usage until that site changed without control</li>'
                           '<li>support to install via teamviewer in case you need</li>'
                           '</ul>'
                           '<p>No need to install any additional software.</p>'
                           '<p>Limit maximum 2 PCs.</p>'
                           '<p>If you need above features, just make donation and get the extension.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'May 31, 2019'
                }

            ],
            'donators': [
            ]
        }
    ]

    GPC_PROJECT_ID = os.environ['GCP_PROJECT_ID']
    GPC_LOCATION = os.environ['GCP_LOCATION']
    GPC_QUEUE_ID = os.environ['GCP_QUEUE_ID']
