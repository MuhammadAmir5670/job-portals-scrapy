from flask import Flask
from dotenv import load_dotenv


from scraper.blueprint import scraping_blueprint

load_dotenv()

app = Flask(__name__)

app.register_blueprint(scraping_blueprint)
