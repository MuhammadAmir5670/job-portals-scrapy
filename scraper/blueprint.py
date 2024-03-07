from flask import Blueprint, request

import threading
import pandas as pd
import os

from . import PORTALS

scraping_blueprint = Blueprint('scraping', __name__)


@scraping_blueprint.route('/run-scraper/<string:source>', methods=['GET'])
def run_scraper(source):
    data = dict(request.args)

    thread = threading.Thread(
        target=PORTALS[source],
        args=(data['link'], data['job_type']),
        name="ScarperThread"
    )
    thread.start()

    return {'message': 'Scraper started successfully'}


@scraping_blueprint.route('/process-csv', methods=['GET'])
def process_csv():
    dfs = []
    folder_path = './data/'
    csv_files = [file for file in os.listdir(
        folder_path) if file.endswith('.csv')]
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(csv_file_path)
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    data = combined_df.to_dict(orient='records')

    return data
