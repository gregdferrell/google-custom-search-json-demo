import http.server
import requests
from urllib.parse import unquote, parse_qs

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

    GOOGLE_CUSTOM_SEARCH_ENGINE_ID = '' # TODO fill in
    GOOGLE_CUSTOM_SEARCH_API_KEY = '' # TODO fill in

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the form with the messages in it.
        self.wfile.write(form.format('<br>').encode())

    def do_POST(self):
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # Return main page if user didn't enter search terms.
        if "searchString" not in params:
            self.do_GET()
            return

        search_string = params["searchString"][0]

        # TODO Construct URL
        url = 'https://www.googleapis.com/customsearch/v1?q={}&cx={}&key={}'.format(search_string, self.GOOGLE_CUSTOM_SEARCH_ENGINE_ID, self.GOOGLE_CUSTOM_SEARCH_API_KEY)

        # TODO Call API
        results = (
            {'title': 'Search Result 1', 'file_format': 'PDF/Adobe Acrobat', 'link': 'http://www.google.com',
             'preview': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eget interdum nisl, sit amet faucibus ex. Sed id sapien nec metus ultricies molestie. Nulla aliquam sodales metus sit amet vestibulum. Cras dignissim tempus magna, sagittis auctor nulla posuere vel. Phasellus justo est, cursus sit amet pretium non, laoreet in mauris.'},
            {'title': 'Search Result 2', 'file_format': 'Word', 'link': 'http://www.foogle.com',
             'preview': 'Aenean consectetur tortor in lorem eleifend efficitur. Nunc vehicula pretium nisl ut feugiat. Phasellus egestas ligula et nibh auctor rhoncus. Proin sit amet arcu quis lectus eleifend rhoncus. Duis ut vehicula sapien. Proin justo tellus, tempor in quam vel, mattis ullamcorper sem.'},
            {'title': 'Search Result 3', 'file_format': 'PDF/Adobe Acrobat', 'link': 'http://www.doogle.com',
             'preview': 'Vestibulum vel lorem quis eros ullamcorper lacinia in id sapien. Donec dictum mauris hendrerit, molestie justo sed, viverra ex. In fringilla vulputate egestas.'},
            {'title': 'Search Result 4', 'file_format': 'Word', 'link': 'http://www.droogle.com',
             'preview': 'Nulla quis condimentum massa. Pellentesque fermentum in magna eu pharetra. Morbi eu tellus eu lorem maximus gravida. Donec neque odio, efficitur sit amet scelerisque vitae, congue a erat. Vivamus lacus eros, dignissim ac convallis ac, cursus id est. Duis non dapibus nibh, in eleifend mauris. Donec quis feugiat ligula, at condimentum justo. Curabitur ut est augue. Donec malesuada nec metus id facilisis. Aliquam sit amet mauris vulputate, iaculis turpis sit amet, mattis sem.'},
            {'title': 'Search Result 5', 'file_format': 'Word', 'link': 'http://www.schmoogle.com',
             'preview': 'Donec metus massa, dapibus ornare molestie ut, eleifend nec est. Fusce egestas odio feugiat, tincidunt diam non, tempor nunc. Sed a elit a arcu blandit efficitur ac non libero.'}
        )

        # Convert Results to HTML
        h = self.get_html_div_from_search_results(results)

        html = form.format(h)

        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
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
            if 'file_format' in result:
                h = h + file_format.format(result.get('file_format'))
            h = h + preview.format(result.get('preview'))
            h = h + link.format(result.get('link'))
        h = h + '</div>'
        return h


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, GoogleCustomSearchDemo)
    httpd.serve_forever()
