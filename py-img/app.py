from jinja2 import Environment, FileSystemLoader, select_autoescape
import time
from pathlib import Path
from datetime import datetime
from dateutil import parser
from generators import *


t0 = time.time()
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

default_combat_obj = {
    "name": "CBSE Class 10 Mega Combat",
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

template = env.get_template("combat.html")

def return_html(template_name, combat_obj):
    template = env.get_template(template_name)
    combat_date = parser.parse(combat_obj["starts_at"])
    combat_day = combat_date.strftime("%d %b %Y")
    combat_time = combat_date.strftime("%H:%M %p")
    quiz_details = combat_obj["quiz_details"]
    topics = [topic["name"] for topic in combat_obj["topic_groups"]]
    return template.render(combat={
        'name':combat_obj["name"], 
        'time':combat_time, 
        'date':combat_day,
        'topics':topics, 
        'details':[f'{quiz_details["section"]} round', f'{quiz_details["questions"]} questions'], 
        'duration':f'{quiz_details["duration"]} mins', 
        'coupon_code':'ANK2001' 
        })


def create_file():
    modified_template = return_html(template, default_combat_obj) 

    # create an image file
    filename = 'generated'
    result_file = use_htmltoimz(f'{filename}-img.png',modified_template)

    # create pdf using pdfkit
    # result_file = use_pdfkit(f'{filename}-pdfkit.pdf', modified_template)
    

    # create pdf using weasyprint
    # result_file = use_weasyprint(f'{filename}-weasyprint.pdf',modified_template)


    # To create a output HTML for testing
    # create_html(modified_template)

    return result_file

def upload_file_to_s3(filename):
    # Let's use Amazon S3
    client = boto3.client('s3',
    aws_access_key_id='AKIAXVK5ZIQTW6OZUTAQ',
    aws_secret_access_key='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',
    region_name='ap-south-1'
    )
        
    # Upload a new file
    client.upload_file(filename, 'demo-testing-python-imagen', filename)


upload_file_to_s3(create_file())
    
t1=time.time()
total = t1-t0
print(total)