#zakladni importy pro flask
from flask import Flask, render_template, request, redirect, url_for  

app = Flask(__name__)


#domovska stranka
@app.route('/')
def home():
    return render_template("indexhome.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run()