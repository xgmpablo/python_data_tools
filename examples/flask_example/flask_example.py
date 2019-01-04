###################################################################################################
from bs4 import BeautifulSoup
import requests
import webbrowser
import urllib
import wget
import os

def create_daughter_directory(dir_name):
    dir_name = dir_name.replace(' ','_')
    cwd = os.getcwd()
    dir_path = os.path.join(cwd,dir_name)
    if not os.path.exists(dir_path): 
        os.makedirs(dir_path)  
    return dir_path

create_daughter_directory('static')
upload_folder = os.path.join(os.getcwd(), 'static')

tag = raw_input("Provide an instagram tag for the photos you want to download: ")
num_images = int( raw_input("List the number of images you want to download: ") )

url = requests.get("https://www.instagram.com/explore/tags/%s/?hl=en" %tag.strip(' '))
soup = BeautifulSoup(url.text)

i = 0
for script in soup.findAll('script'):
    if script.string != None:
        if "window._sharedData = " in script.string:
            images_string = script.string
            chunks = images_string.split(',')
            for chunk in chunks:
                if '"display_url"' in chunk: # or '"src"' in chunk:
                    for string in chunk.split('":'):
                        if "https" in string:
                            image_url =  str(string.split('"')[1])
                            break
                    if i > num_images:
                        break
                    i += 1
                    wget.download(image_url)
                    image_file = image_url.split('?')[0].split('/')[-1]
                    os.rename(image_file, os.path.join(upload_folder,image_file) )

###################################################################################################
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import random
import webbrowser
webbrowser.get('firefox').open('http://127.0.0.1:5000/')



# creates a Flask application, named app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

# a route where we will display a welcome message via an HTML template
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def hello():  
    message = "Hello World"
    all_images = os.listdir( app.config['UPLOAD_FOLDER'] )
    random_image = all_images[random.randint(0,len(all_images)-1)]
    image = os.path.join("static", random_image)
    return render_template('home.html', message=message, image=image)

# a route where we will display a welcome message via an HTML template
@app.route("/about")
def about():  
    return render_template('about.html')

# run the application
if __name__ == "__main__":  
    app.run()
###################################################################################################

