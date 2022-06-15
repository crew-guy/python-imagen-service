from jinja2 import Environment, FileSystemLoader, select_autoescape
from memory_profiler import profile
import time
from pathlib import Path
import pdfkit
from weasyprint import HTML
from html2image import Html2Image
hti = Html2Image()

t0 = time.time()
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

template = env.get_template("combat.html")

def return_html(template_name):
    template = env.get_template(template_name)
    return template.render(combat={
        'name':'Fundamentals of JEE - Physics, Chemistry & Mathematics', 
        'time':'2pm', 
        'date':'12/12/2019',
        'topic':'Chemical Bonding', 
        'details':['1 round', '54 questions'], 
        'duration':'60mins', 
        'coupon_code':'ANK2001' 
        })

modified_template = return_html(template) 

@profile()
def use_pdfkit(html):
    print(html)
    pdfkit.from_string(html, 'pdfkit.pdf')

@profile()
def use_weasyprint(html):
    """Generate a PDF file from a string of HTML."""
    htmldoc = HTML(string=html, base_url="")
    print(html)
    pdf = htmldoc.write_pdf()
    Path('weasyprint.pdf').write_bytes(pdf)

@profile()
def use_htmltoimz(html):
    """Generate a PDF file from a string of HTML."""
    hti.screenshot(html_str=html, save_as='html2img.png')

# use_pdfkit(modified_template)
# use_weasyprint(modified_template)
# use_htmltoimz(modified_template)
# Path('generated.html').write_bytes(modified_template)
t1=time.time()
total = t1-t0
print(total)


# Write to a generated HTML file
file = open("templates/generated.html", "w") 
file.write(modified_template) 
file.close() 