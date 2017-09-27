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
    search_start = request.args.get('searchStart', '1')
    print('search string: ' + search_string)
    print('search start: ' + search_start)

    if search_string == '':
        return render_template('home.html', search_string='', search_result_message='', num_results=0)

    # Construct URL and call API
    url = 'https://www.googleapis.com/customsearch/v1?q={}&start={}&cx={}&key={}'.format(
        search_string, search_start, google_custom_search_engine_id, google_custom_search_api_key)
    response = requests.get(url)

    if response.status_code != 200:
        search_result_message = 'Search returned an error: {} {}'.format(response.status_code, response.reason)
        return render_template('home.html', search_string=search_string, search_result_message=search_result_message,
                               num_results=0)

    # Render search results
    data = response.json()
    num_results = int(data.get('searchInformation').get('totalResults'))
    search_time = data.get('searchInformation').get('formattedSearchTime')
    results = data.get('items')
    search_result_message = 'No results found ({} seconds)'.format(
        search_time) if num_results == 0 else 'About {} results ({} seconds)'.format(num_results, search_time)
    start_index = data.get('queries').get('request')[0].get('startIndex')

    return render_template('home.html', search_string=search_string, search_result_message=search_result_message,
                           num_results=num_results, search_start=search_start, search_time=search_time, results=results)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
