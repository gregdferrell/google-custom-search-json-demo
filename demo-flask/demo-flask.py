import configparser
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('demo.ini')
google_custom_search_engine_id = config['DEFAULT']['GoogleCustomSearchEngineId']
google_custom_search_api_key = config['DEFAULT']['GoogleCustomSearchApiKey']


@app.route("/", methods=['GET'])
def home():
    # Get search request param and log it
    search_string = request.args.get('searchString', '')
    print(search_string)

    if search_string == '':
        return render_template('home.html', num_results=0)

    # Construct URL and call API
    url = 'https://www.googleapis.com/customsearch/v1?q={}&cx={}&key={}'.format(
        search_string, google_custom_search_engine_id, google_custom_search_api_key)
    response = requests.get(url)

    if response.status_code != 200:
        return render_template('home.html', num_results=0, error_message='Search returned an error.')

    data = response.json()

    # Render search results
    num_results = int(data.get('searchInformation').get('formattedTotalResults'))
    search_time = data.get('searchInformation').get('formattedSearchTime')
    results = data.get('items')
    return render_template('home.html', num_results=num_results, search_time=search_time, results=results)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
