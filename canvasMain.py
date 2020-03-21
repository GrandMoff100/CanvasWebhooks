import time

import canvasapi
from canvasapi import Canvas
from canvasapi.requester import Requester
import json
import requests
import asyncio

logging = 0

if logging:
    import logging
    import sys

    logger = logging.getLogger("canvasapi")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

with open("user_creds.json") as u:
    user_credentials = json.load(u)

# Initialize Needed Values
token = user_credentials.get("token")
url = user_credentials.get("base_url")
umtymp_id = user_credentials.get("umtymp_id")

# Initialize Needed Objects
request_client = Requester(url, token)
canvas = Canvas(url, token)
umtymp_course = canvas.get_course(umtymp_id)

# Test Executing WebHook
with open("webhooks.json") as w:
    webhooks = json.load(w)

canvas_discussions_url = webhooks.get("canvas_discussions_url")
canvas_news_url = webhooks.get("canvas_news_url")

global_discussions = umtymp_course.get_discussion_topics()


def send_news_update(course, loop):
    discussions = course.get_discussion_topics()

    contents = []

    index = 0
    for discussion in global_discussions:
        if discussion.pinned:
            if discussion == discussions[index]:
                discussions.pop(index)
            else:
                print(discussion.author)
                discussion_name = '**' + str(discussion.title) + '**' + '\n'
                author = 'Posted by ' + dict(discussion.author).get("display_name") + '\n'

                entry = 'Update in Discussion \n%s' % discussion.url

                contents.append(str(discussion_name + author + entry))
            index += 1

    print(contents)

    for content in contents:

        header = {
            "content": "@everyone\n%s" % content,
            "allowed_mentions": {
                "parse": ["everyone"]
            }
        }

        if content != "":
            requests.post(canvas_news_url, json=header)
        time.sleep(60)

    loop.call_later(1, course, loop)


def send_discussion_update(course, loop):
    discussions = course.get_discussion_topics()

    contents = []

    index = 0
    for discussion in global_discussions:
        if discussion == discussions[index]:
            discussions.pop(index)
        else:
            discussion_name = '**' + str(discussion.title) + '**' + '\n'
            author = 'Posted by ' + dict(discussion.author).get("display_name") + '\n'
            entry = 'Update in Discussion \n%s' % discussion.url
            contents.append(str(discussion_name + author + entry))
        index += 1

    print(contents)

    for content in contents:

        header = {
            "content": "@here\n%s" % content,
            "allowed_mentions": {
                "parse": ["here"]
            }
        }

        if input('Send? %s:' % content) != "":

            requests.post(canvas_news_url, json=header)

        time.sleep(60)

    loop.call_later(1, course, loop)


loop = asyncio.get_event_loop()

loop.call_soon(send_news_update, umtymp_course, loop)
loop.call_soon(send_discussion_update, umtymp_course, loop)

loop.run_forever()
