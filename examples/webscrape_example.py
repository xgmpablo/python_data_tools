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

#url = requests.get('https://www.instagram.com/explore/tags/wildlifephotography/?hl=en')

tag = raw_input("Provide an instagram tag for the photos you want to download:")
url = requests.get("https://www.instagram.com/explore/tags/%s/?hl=en" %tag.strip(' '))
soup = BeautifulSoup(url.text)

dir_path = create_daughter_directory(tag) 
for script in soup.findAll('script'):
    if "window._sharedData = " in script.string:
        images_string = script.string
        chunks = images_string.split(',')
        for chunk in chunks:
            if '"display_url"' in chunk: # or '"src"' in chunk:
                for string in chunk.split('":'):
                    if "https" in string:
                        image_url =  str(string.split('"')[1])
                        break
                wget.download(image_url)
                image_file = image_url.split('?')[0].split('/')[-1]
                os.rename(image_file, os.path.join(dir_path,image_file) )


