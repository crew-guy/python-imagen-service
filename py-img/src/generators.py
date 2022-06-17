import pdfkit
from weasyprint import HTML, CSS
from html2image import Html2Image
from memory_profiler import profile

PATH_TO_CSS_FILE = '/Users/ankitravikumars/Desktop/python-imagen-service/py-img/static/styles/combat.css'

@profile()
def use_pdfkit(filename, html):
    options = {
    "enable-local-file-access": None,
    'page-height': 405,
    'page-width': 720,
    'margin-top': '0.0in',
    'margin-right': '0.0in',
    'margin-bottom': '0.0in',
    'margin-left': '0.0in'
    }
    pdfkit.from_string(html, filename, options=options)
    return filename

@profile()
def use_weasyprint(filename,html):
    """Generate a PDF file from a string of HTML."""
    htmldoc = HTML(string=html, base_url="")
    htmldoc.write_pdf(target=filename,stylesheets=[CSS(PATH_TO_CSS_FILE)])
    return filename

@profile()
def use_htmltoimz(filename, html):
    hti = Html2Image()
    hti.screenshot(html_str=html, css_file=PATH_TO_CSS_FILE, save_as=filename)
    return filename

# Write to a generated HTML file
def create_html(html):
    file = open("templates/generated.html", "w") 
    file.write(html) 
    file.close() 
