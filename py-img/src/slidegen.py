from re import template
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from dateutil import parser
from generators import use_htmltoimz, use_pdfkit, use_weasyprint
import uuid

PATH_TO_TEMPLATES_FOLDER = '/Users/ankitravikumars/Desktop/python-imagen-service/py-img/templates/'

env = Environment(
    loader=FileSystemLoader(PATH_TO_TEMPLATES_FOLDER),
    autoescape=select_autoescape()
)

class HandoutSlide(object):
    def __init__(self, handout_type, handout_data):
        self.handout_type=handout_type
        self.handout_data=handout_data

    def inject_context_in_html(self):
        template_filename = ''
        context = {}
        template_name = self.handout_type
        if template_name == 'COMMUNITY':
            template_filename = env.get_template("combat.html")
        elif template_name == 'COMBAT':
            template_filename = env.get_template("combat.html")
            combat_data = self.handout_data
            combat_date = parser.parse(combat_data["starts_at"])
            combat_day = combat_date.strftime("%d %b %Y")
            combat_time = combat_date.strftime("%H:%M %p")
            quiz_details = combat_data["quiz_details"]
            topics = [topic["name"] for topic in combat_data["topic_groups"]]
            context ={
                'name':combat_data["name"], 
                'time':combat_time, 
                'date':combat_day,
                'topics':topics, 
                'details':[f'{quiz_details["section"]} round', f'{quiz_details["questions"]} questions'], 
                'duration':f'{quiz_details["duration"]} mins', 
                'coupon_code':'ANK2001' 
                }
        
        template = env.get_template(template_filename)
        
        print(context)
        return template.render(context=context)
    
    def get_img(self):
        result_html = self.inject_context_in_html() 
        result_file = use_htmltoimz(f'{uuid.uuid1()}.png',result_html)
        return result_file

    # def get_pdf_using_pdfkit(self):
    #     result_html = self.inject_context_in_html()
    #     result_file = use_pdfkit('generated-pdfkit.pdf', result_html)
    #     return result_file

    # def get_pdf_using_weasyprint(self):
    #     result_html = self.inject_context_in_html()
    #     result_file = use_weasyprint('generated-weasyprint.pdf',result_html)
    #     return result_file
    
    def get_html(self):
        return self.inject_context_in_html() 


