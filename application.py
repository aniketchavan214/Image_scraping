from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import logging
from urllib.request import urlopen as uReq
import pymongo
import os
from flask_cors import CORS, cross_origin

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

application = Flask(__name__)

@application.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@application.route("/review", methods=['GET', 'POST'])
def index():
    if request.method== 'POST':
        try:
            # query to search images
            query = input("Enter name ")
            # query = request.form['content'].replace(" ","")
            save_directory = "images/"
            
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            # fake user agent to avoid getting blocked by google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            
            url = f"https://www.google.co.in/search?q={query}&tbm=isch&ved=2ahUKEwjD763JyrWAAxXhxqACHV0GCyoQ2-cCegQIABAA&oq=elo&gs_lcp=CgNpbWcQARgAMgoIABCKBRCxAxBDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDOgQIIxAnOgQIABADOgsIABCABBCxAxCDAToJCAAQGBCABBAKOgcIIxDqAhAnOgUIABCABDoICAAQsQMQgwE6BwgAEIoFEENQlBRYjTRgo0ZoAnAAeAOAAZQBiAGrD5IBBDAuMTWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=gOXFZMOvHOGNg8UP3Yys0AI&bih=923&biw=1920"
            
            response=requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            image_tags = soup.find_all('img')
            del image_tags[0]
            img_data = []
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag['src']
                image_data = requests.get(image_url).content
                mydict = {"index":index,"image":image_data}
                img_data.append(mydict)
                with open(os.path.join(save_directory, f"{query}_{image_tags.index(image_tag)}.jpg"),'wb') as f:
                    f.write(image_data)
                    
            # client = pymongo.MongoClient("mongodb+srv://snshrivas:Snshrivas@cluster0.ln0bt5m.mongodb.net/?retryWrites=true&w=majority")
            #         db = client['image_scrap']
            #         review_col = db['image_scrap_data']
            #         review_col.insert_many(img_data)      
            
            
            return "image loaded"
        except Exception as e:
            logging.info(e)
            return "something is wrong"
        
    else:
        return render_template('index.html')
        
    
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)
            
            