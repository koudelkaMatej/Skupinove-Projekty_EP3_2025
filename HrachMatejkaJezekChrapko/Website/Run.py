#zakladni importy pro flask
from flask import Flask, render_template, request, redirect, url_for  

app = Flask(__name__)


#domovska stranka
@app.route('/')
def home():
    return render_template("indexhome.html")

if __name__ == '__main__':
    app.run()