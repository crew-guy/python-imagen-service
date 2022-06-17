import time
from aws import s3_client
from slidegen import HandoutSlide
import os
from utils import delete_file

t0 = time.time()

default_combat_obj = {
    "name": "UPSC CSESE Current Affairs Special Combat. 80 characters title should come here.",
    "uid": "3ENJ3I3M",
    "is_enrolled": True,
    "starts_at": "2022-06-26T05:30:00Z",
    "topic_groups": [
        {
            "name": "Mathematics",
            "uid": "AZCAV",
            "title": "Mathematics",
        },
        {
            "name": "Science",
            "uid": "WWTLJ",
            "title": "Science",
        },
        {
            "name": "Physics",
            "uid": "WWTLJ",
            "title": "Science",
        },
        {
            "name": "Science",
            "uid": "WWTLJ",
            "title": "Science",
        },
        {
            "name": "Physics",
            "uid": "WWTLJ",
            "title": "Science",
        },
    ],
    "quiz_details": {
        "available_languages": [],
        "uid": "L6I3JT7KEI",
        "title": "CBSE Class 10 Mega Combat",
        "section": 1,
        "questions": 0,
        "duration": 45,
        "max_question_count": 0
    },
    "is_live": False,
    "state": 10,
}

handout = HandoutSlide('COMBAT', default_combat_obj)
handout_img = handout.get_img()
res_html = handout.get_html()

print(f'{handout_img} generated ! now uploading to s3')
s3_client.upload_file(handout_img, os.getenv('BUCKET_NAME'), f'zamzar/{default_combat_obj["uid"]}/{handout_img}')

print('uploaded to s3 !')

t1=time.time()
total = t1-t0
print(total)