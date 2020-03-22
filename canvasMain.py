import time
import datetime
from canvasapi import Canvas
from canvasapi.requester import Requester
import json
import requests
import asyncio


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


def send_news_update(course, loop):
    discussions = course.get_discussion_topics()

    contents = []

    index = 0
    for discussion in discussions:
        if discussion.pinned:
            entry_time = int(discussion.last_reply_at_date.strftime("%Y%m%d%H%M%S"))

            if entry_time >= (int(datetime.date.today().strftime("%Y%m%d%H%M%S")) - 100):
                discussion_name = '**' + str(discussion.title) + '**' + '\n'
                author = 'Posted by ' + dict(discussion.author).get("display_name") + '\n'
                entry = 'Update in Discussion \n%s' % discussion.url

                contents.append(str(discussion_name + author + entry))
            index += 1

    for content in contents:
        header = {
            "content": "@CanvasUpdatePings\n%s" % content,
            "allowed_mentions": {
                "parse": ["roles"]
            }
        }
        print('Posting %s' % content)
        requests.post(canvas_news_url, json=header)

    time.sleep(3600)

    loop.call_later(1, send_news_update, course, loop)


def send_discussion_update(course, loop):
    discussions = course.get_discussion_topics()

    contents = []

    index = 0
    for discussion in discussions:
        entry_time = int(discussion.last_reply_at_date.strftime("%Y%m%d%H%M%S"))
        if entry_time >= (int(datetime.date.today().strftime("%Y%m%d%H%M%S")) - 100):
            discussion_name = '**' + str(discussion.title) + '**' + '\n'
            author = 'Posted by ' + dict(discussion.author).get("display_name") + '\n'
            entry = 'Update in Discussion \n%s' % discussion.url

            contents.append(str(discussion_name + author + entry))
        index += 1

    for content in contents:
        header = {
            "content": "@CanvasUpdatePings\n%s" % content,
            "allowed_mentions": {
                "parse": ["roles"]
            }
        }
        print('Posting %s' % content)
        requests.post(canvas_discussions_url, json=header)

    time.sleep(3600)

    loop.call_later(1, send_discussion_update, course, loop)

def start():
    loop = asyncio.get_event_loop()

    loop.call_soon(send_news_update, umtymp_course, loop)
    loop.call_soon(send_discussion_update, umtymp_course, loop)

    loop.run_forever()

if __name__ == "__main__":
    start()