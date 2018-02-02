import configparser
import http.server
from urllib.parse import parse_qs

import requests

form = '''<!DOCTYPE html>
<html>
    <head>
        <title>Google Custom Search Demo</title>    
    </head>
    <body>
        <div class="search-form" style="padding: 8px 8px 8px;">
            <form method="POST">
                <label>Search:
                    <input name="searchString">
                </label>
                <br><br>
                <button type="submit">Search!</button>
            </form>
        </div>
        {}
    </body>
</html>
'''


class GoogleCustomSearchDemo(http.server.BaseHTTPRequestHandler):
    config = configparser.ConfigParser()
    config.read('demo.ini')
    google_custom_search_engine_id = config['DEFAULT'][
        'GoogleCustomSearchEngineId']
    google_custom_search_api_key = config['DEFAULT']['GoogleCustomSearchApiKey']

    def do_GET(self, error_message=''):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the form with the messages in it.

        self.wfile.write(form.format('<br>{}'.format(error_message)).encode())

    def do_POST(self):
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # Return main page if user didn't enter search terms.
        if "searchString" not in params:
            self.do_GET('The search field is required.')
            return

        search_string = params["searchString"][0]

        # Construct URL and call API
        url = 'https://www.googleapis.com/customsearch/v1?q={}&cx={}&key={}'.format(
            search_string, self.google_custom_search_engine_id,
            self.google_custom_search_api_key)
        response = requests.get(url)
        if response.status_code != 200:
            self.do_GET('Search returned an error.')
            return

        data = response.json()

        # Convert Results to HTML
        num_results = data.get('searchInformation').get('formattedTotalResults')
        search_time = data.get('searchInformation').get('formattedSearchTime')
        h = '<p>About {} results ({} seconds)</p><hr />'.format(num_results,
                                                                search_time)
        if int(num_results) > 0:
            h = h + self.get_html_div_from_search_results(data.get('items'))
        html = form.format(h)

        # Send a 200 OK response.
        self.send_response(200)

        # Send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        self.wfile.write(html.encode())
        return

    def get_html_div_from_search_results(self, results):
        h = '<div id="search-results" style="padding: 8px 8px 8px;">'
        title = '<a href="{}">{}</a>'
        file_format = '<p>File Format: {}</p>'
        preview = '<p>{}</p>'
        link = '<p>{}</p>'
        for result in results:
            h = h + '<br>'
            h = h + title.format(result.get('link'), result.get('title'))
            if 'fileFormat' in result:
                h = h + file_format.format(result.get('fileFormat'))
            h = h + preview.format(result.get('htmlSnippet'))
            h = h + link.format(result.get('htmlFormattedUrl'))
        h = h + '</div>'
        return h


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, GoogleCustomSearchDemo)
    httpd.serve_forever()
