from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import random
import webbrowser
webbrowser.get('firefox').open('http://127.0.0.1:5000/')

# creates a Flask application, named app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'static')

# a route where we will display a welcome message via an HTML template
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def hello():  
    return render_template('home.html')

# run the application
if __name__ == "__main__":  
    app.run()
