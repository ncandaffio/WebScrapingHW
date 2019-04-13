from scrape_mars import scrape
from flask import Flask, render_template, redirect, jsonify
import pymongo

#Initialize Flask
app = Flask(__name__)

#Create the /scrape page
@app.route('/scrape')
def new_scrape():

    # setup mongo connection
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # connect to mongo db and collection
    db = client.mars
    collection = db.site_data

    scrape_data = scrape()

    db.collection.update_one({}, {'$set':scrape_data}, upsert=True)
    return redirect("/")

#Test Main Page
@app.route('/')
def home():
    # setup mongo connection
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars

    data = db.collection.find_one()
    
    return render_template(
        'index.html',news_title=data['news_title'], news_p=data['news_p'], 
        featured_image_url=data['featured_image_url'], mars_weather=data['mars_weather'],
        facts_table=data['facts_table'], hemisphere_image_urls=data['hemisphere_image_urls']
        )
   

if __name__ == "__main__":
    app.run(debug=True)
