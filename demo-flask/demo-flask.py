import configparser
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('demo.ini')
google_custom_search_engine_id = config['DEFAULT']['GoogleCustomSearchEngineId']
google_custom_search_api_key = config['DEFAULT']['GoogleCustomSearchApiKey']


def get_paging_links(start_index, num_results):
    '''
    Gets a tuple of paging links given the current start index and the number of
    results for the search query.
    :param start_index: the start index of the search request
    :param num_results: the total number of search results
    :return: A tuple containing paging info (boolean, str, str):
        (link_is_current_page, link_text, link_start_index)
    '''
    paging_links = []
    count = 0
    for i in range(1, min(100, num_results), 10):
        count += 1
        paging_links.append((True if start_index == i else False, count, i))
    return paging_links


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
    paging_links = get_paging_links(start_index, num_results)

    return render_template('home.html', search_string=search_string, search_result_message=search_result_message,
                           num_results=num_results, search_time=search_time, results=results, paging_links=paging_links)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
