from flask import Flask, request
from os.path import exists
import pandas as pd
import shutil
import requests
import search_engine
import json
from flask_cors import CORS
import bookmark

app = Flask(__name__)
CORS(app)

metadata_file_name = 'metadata.csv'
if not exists(metadata_file_name):
    print(f'Downloading {metadata_file_name}...')
    metadata_file_url = f'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-04-03/{metadata_file_name}'
    response = requests.get(metadata_file_url, stream=True)
    with open(metadata_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print(f'{metadata_file_name} downloaded')
else:
    print(f'Glad the {metadata_file_name} file is already here')

columns_needed = ['title', 'publish_time', 'journal', 'url', 'authors', 'abstract']
metadata_df = pd.read_csv(metadata_file_name, usecols=columns_needed)


@app.route('/search', methods=['GET'])
def search_metadata():
    try:
        search_term=request.args.get('search_term')

        if not search_term or len(search_term) < 3:
            return app.response_class(
                response=json.dumps({'message': 'search_term must be longer than 3 characters'}),
                status=422,
                mimetype='application/json')

        full_search_result_df=search_engine.get_df_search_result(
            metadata_df.copy(), search_term.strip().lower())

        json_response={
            'number_results': len(full_search_result_df.index),
            'papers': json.loads(full_search_result_df[:100].to_json(orient='records'))
        }

        return app.response_class(
            response=json.dumps(json_response),
            status=200,
            mimetype='application/json')
    except Exception as error:
        return app.response_class(
            response=json.dumps({'message': f'Unexpected error: {error}'}),
            status=500,
            mimetype='application/json')


@app.route('/bookmark', methods = ['POST', 'GET'])
def bookmarks():
    try:
        if request.method == 'POST':
            payload = request.get_json()

            if not payload:
                return app.response_class(
                    response=json.dumps({'message': 'empty bookmark payload'}),
                    status=422,
                    mimetype='application/json')

            persist_error = bookmark.persist_bookmark(payload)

            if persist_error:
                return app.response_class(
                    response=json.dumps({'message': persist_error}),
                    status=422,
                    mimetype='application/json')
            
            return 'saved'
        
        bookmarks_list = bookmark.get_bookmarks_list()

        return app.response_class(
            response=json.dumps(bookmarks_list),
            status=200,
            mimetype='application/json')
    except Exception as error:
        return app.response_class(
            response=json.dumps({'message': f'Unexpected error: {error}'}),
            status=500,
            mimetype='application/json')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
