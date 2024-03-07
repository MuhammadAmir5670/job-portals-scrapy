from flask import Flask

from scraper.blueprint import scraping_blueprint

app = Flask(__name__)

app.register_blueprint(scraping_blueprint)
