from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/ankit')
def hello_ankit():
    return "<p> Hey ankit</p>"



@app.route('/hello')
@app.route('/hello/<name>')
def hello_name(name=None):
    return render_template('hello.html', name=name)
