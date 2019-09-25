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
            'id': "7",
            'listed': True,
            'title': 'Braille reader and Speech with Android + OpenCV',
            'short_title': 'Braille reader and Speech with Android + OpenCV',
            'price': 165,
            'hit_donate': 3000,
            'total_donate': 473,
            'slug_title': 'source-code-braille-to-speech-with-android-opencv',
            'img': 'project7.png',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/C-afb8nGT7o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>The basic braille alphabet, braille numbers, braille punctuation and special symbols characters are constructed from six dots. These braille dots are positioned like the figure six on a die, in a grid of two parallel vertical lines of three dots each. From the six dots that make up the basic grid, 64 different configurations can be created.</p>'

                           '<p>This project purpose help students build there final project for graduation at school. '
                           'This project also help teachers build their tool to manage they students exams quickly. Or this '
                           'is also the prototype for professional developers to make a crazy recognize braille application.</p> '
                           '<ul>'
                           '<li> Easy to Use: The scanning process is simple and quick and you can process a Braille-sheet in a single scan. Pressing the scan icon starts the process of scanning. After less than thirty seconds the information is presented on the screen and speak up the result. You can continue to scan the next page or start to use the information.</li>'
                           '<li> No Braille Knowledge required: Braille in a small letter/ document or a complete Book can be scanned into the computer just like a normal printed paper is scanned. And you do not need to know Braille to do this.</li>'
                           '<li> Accurate Recognition: The recognition from a good quality Braille document is excellent but even when scanning an old worn-out Braille document; the fault frequency is surprisingly low. By using standard Windows functions your Braille handling system will be complete and effective.</li></ul>'

                           '<p>The clear source code with many comments insight, and overview document help the owner understand easily.</p>'
                           '<p>Highlight features:</p>'
                           '</p><ul>'
                           '<li>Capture braille dots with android camera</li>'
                           '<li>Recognize braille dots and convert to text, number</li>'
                           '<li>Speak the braille text</li>'
                           '</ul>'
                           '<p><strong>You will receive your donation back if it is not working.</strong></p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your email. Just email to <strong>workspace.gold@gmail.com</strong> '
                           'when you need support to setting project, build, run the app.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'June 27, 2019'
                }

            ],
            'donators': [],
            'keywords': 'braille recognition, braille to speech, braille converter, recognize braille alphabet, read braille, extra braille, braille reader, braille scanner, braille to text, braille mobile reader, braille image to text, braille translator, braille application, braille translator camera, braille text speech, blind reader, how to convert braille to text, android text to speech, braille dots, accubraille, blindness reader, blind, brailliant, loss vision reader, dots scan, obr',
        },
        {
            'id': "1",
            'listed': True,
            'title': 'Recognize bubble sheet and input correct answers with Android + OpenCV',
            'short_title': 'Recognize bubble sheet and correct answers',
            'price': 125,
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
                           '<p><strong>You will receive your donation back if it is not working.</strong></p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. Just email to <strong>workspace.gold@gmail.com</strong> '
                           'when you need support to setting project, build, run the app.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'May 09, 2019'
                }

            ],
            'donators': [
            ],
            'keywords': 'vgrade, omr, recognize sheet, sheet scanner, omr scanner, omr scanning, sheet recognize, exam scanner, omr reader, recognize table, recognize bubble, quiz scanner, quiz reader, grading, bubble scanner, omr solution, Optical Mark Recognition, cham trac nghiem, multiple choice, zipgrade cheat, scan ljk, koreksi ljk',
        },
        {
            'id': "2",
            'listed': True,
            'title': 'Recognize bubble sheet with Android and OpenCV from 10 to 100 questions',
            'short_title': 'Recognize from 10 to 100 questions',
            'price': 85,
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
                           '<p><strong>You will receive your donation back if it is not working.</strong></p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. And the source code belong to you, you can do anythings with it. '
                           'Just send email to <strong>workspace.gold@gmail.com</strong> when you need support to setting project, build, run the app.</p>',
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
            ],
            'keywords': 'vgrade, omr, recognize sheet, sheet scanner, omr scanner, omr scanning, sheet recognize, exam scanner, omr reader, recognize table, recognize bubble, quiz scanner, quiz reader, grading, bubble scanner, omr solution, Optical Mark Recognition, cham trac nghiem, multiple choice, zipgrade cheat, scan ljk, koreksi ljk',

        },
        {
            'id': "3",
            'listed': True,
            'title': 'Recognize bubble sheet and manage Students, Classes, Subjects',
            'short_title': 'Recognize bubble sheet and manage students',
            'price': 105,
            'hit_donate': 2000,
            'total_donate': 473,
            'slug_title': 'source-code-recognize-bubble-sheet-with-android-opencv-and-manage-students-classes-subjects',
            'img': 'project2.png',
            'video_embed': '<iframe width="480" height="270" src="https://www.youtube.com/embed/t66OAXI9mkw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p>This project purpose help students build there final project for graduation at school. '
                           'This project also help teachers build their tool to manage they students exams quickly. Or this '
                           'is also the prototype for professional developers to make a crazy recognize exam service.</p> '
                           '<p><strong>You will receive your donation back if it is not working.</strong></p>'
                           '<p>The clear source code with many comments insight, and overview document help the owner understand easily.</p>'
                           '<p>The project is developed using Android, OpenCV and build on Android studio. After make the '
                           'donate, you will receive the source code, template, apk file and overview document via your Paypal email. Just email to <strong>workspace.gold@gmail.com</strong> '
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
            ],
            'keywords': 'vgrade, omr, recognize sheet, sheet scanner, omr scanner, omr scanning, sheet recognize, exam scanner, omr reader, recognize table, recognize bubble, quiz scanner, quiz reader, grading, bubble scanner, omr solution, Optical Mark Recognition, cham trac nghiem, multiple choice, zipgrade cheat, scan ljk, koreksi ljk',
        },
        {
            'id': "4",
            'listed': True,
            'title': 'Rohtang permits auto fill info',
            'short_title': 'Rohtang permits auto fill info version 2.0',
            'price': 55,
            'hit_donate': 100,
            'total_donate': 15,
            'slug_title': 'fastly-rohtang-permit',
            'img': 'project4_2.png',
            'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/blBGvf8G_8g" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'description': '<p><strong>Only pay attention if you need succeed booking on Rohtang. And send an email <strong>workspace.gold@gmail.com</strong> to get demo video if you need.</strong></p>'
                           '<p>Monkey script features:</p>'
                           '<ul>'
                           '<li> work on: Rohtang Pass, Green tax, Special Permit </li>'
                           '<li>auto refresh page until time come. Make sure you first guy go to this site</li>'
                           '<li><strong>auto fill captcha math expression</strong></li>'
                           '<li>auto fill all fields</li>'
                           '<li>auto refresh captcha if can not recognize captcha</li>'
                           '<li>auto submit and click Proceed for payment and go to Payment method input</li>'
                           '</ul>'
                           '<p>After get extension via email, extract it using winrar. After that you just replace demo data by your personal data in file content.js from line 161 to line 179. Then import extension to your chrome and use.</p>'
                           '<p>No need to install any additional software.</p>'
                           '<p>If you need this extension, just make donation and get the extension.</p>',
            'info': [
                {
                    'name': 'Last Update',
                    'value': 'Jun 07, 2019'
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
            ],
            'keywords': 'auto captcha, auto captcha extension, auto fill captcha, chrome captcha auto solver, bypass captchca, Rohtangpermits, Rohtangpermits fast login, Rohtangpermits fastly submit, Rohtangpermits auto fill, fastly rohtang permit, fast rohtang submit, rohtang permit auto, quick rohtange permit, rohtang permit trick, rohtang permit tip, trick quickly rohtang submit, quick rohtang form, rohtang quick submit vehicle, rohtang fast register, captcha solver,Online Permit for Rohtang Pass',
        },
        {
            'id': "5",
            'listed': True,
            'title': 'Rohtang permits auto click Proceed for Payment',
            'short_title': 'Rohtang permits auto click Proceed for Payment',
            'price': 19,
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
            ],
            'keywords': 'auto captcha, auto captcha extension, auto fill captcha, chrome captcha auto solver, bypass captchca, Rohtangpermits, Rohtangpermits fast login, Rohtangpermits fastly submit, Rohtangpermits auto fill, fastly rohtang permit, fast rohtang submit, rohtang permit auto, quick rohtange permit, rohtang permit trick, rohtang permit tip, trick quickly rohtang submit, quick rohtang form, rohtang quick submit vehicle, rohtang fast register, captcha solver,Online Permit for Rohtang Pass',
        },
        {
             'id': "6",
            'listed': True,
            'title': 'SSMMS auto captcha fastly | Online sand booking auto filling info with Tampermonkey script Greasemonkey script',
             'short_title': 'SSMMS auto captcha & auto otp',
            'price': 69,
            'hit_donate': 100,
            'total_donate': 15,
           'slug_title': 'ssmms-auto-captcha-online-sand-booking-auto-fill-info',
             'img': 'project6_2.png',
             'video_embed': '<iframe width="560" height="315" src="https://www.youtube.com/embed/pmD1Lc6LsbU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            'video_embed2': '<iframe width="560" height="315" src="https://www.youtube.com/embed/1BG5NSqVnao" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
           'description': '<p>Monkey script available for almost browsers. </p>'
                          '<p><a href="https://www.dropbox.com/s/2qte27luehy6krv/WS_Auto_Otp_3.0.apk?dl=0" style="color: blue; text-decoration: underline;">Click to DOWNLOAD WS_Auto_OTP ver 3: </a></p>'
                          '<p><a href="https://www.dropbox.com/s/c0rg69dqespww5x/auto_captcha_5.6.js?dl=0" style="color: blue; text-decoration: underline;">Click to DOWNLOAD Auto captcha 5.6</a></>'
                          '<p>Features:</p>'
                           '<ul>'
                           '<li>work on: https://onlinebooking.sand.telangana.gov.in</li>'
                          '<li>auto fill captcha 95% correct</li>'
                          '<li>auto fill username, password</li>'
                          '<li>auto login after 20s</li>'
                          '<li>no limit IPs</li>'
                          '<li>No limit devices</li>'
                          '<li>support to install via teamviewer in case you need</li>'
                          '</ul>'
                            '<p>Make donation for above features and get resource.</p>',
            'info': [
                {
                   'name': 'Last Update',
                    'value': 'Septemper 25, 2019'
               }
        
            ],
            'donators': [
            ],
             'keywords': 'autofill captcha, auto captcha, ssmms, ssmms auto captcha, ssmms auto fill, sand booking, sand in telangana, ssmms tricks, sand booking website, sand online booking, ssmms login quickly, ssmms fastly auto fill captcha, tsmdc online booking, bypass captcha, tmsdc auto captcha, tsmdc quickly login, captcha solver',
        }
    ]

    GPC_PROJECT_ID = os.environ['GCP_PROJECT_ID']
    GPC_LOCATION = os.environ['GCP_LOCATION']
    GPC_QUEUE_ID = os.environ['GCP_QUEUE_ID']
