import json

import requests
import tornado
from bs4 import BeautifulSoup
from notebook.utils import url_path_join
from traitlets.config import LoggingConfigurable
from traitlets.traitlets import Unicode

# try importing lxml and use it as the BeautifulSoup builder if available
try:
    import lxml  # noqa
except ImportError:
    BEAUTIFULSOUP_BUILDER = 'html.parser'
else:
    BEAUTIFULSOUP_BUILDER = 'lxml'  # pragma: no cover


class Spark(LoggingConfigurable):
    """
    A proxy for requests from the extension frontend to Spark that
    replaces URLs on the fly.
    """
    url = Unicode(
        'http://localhost:4040',
        help='The URL of Spark API',
    ).tag(config=True)

    endpoint = Unicode(
        '/spark',
        help='The URL path under which the Spark API will be proxied',
    )

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super(Spark, self).__init__(*args, **kwargs)
        self.endpoint_url = url_path_join(self.base_url, self.endpoint)
        self.session = requests.Session()

    def fail(self):
        raise tornado.web.HTTPError(
            500,
            'ERROR: Request URI did not start with %s' % self.endpoint_url
        )

    def fetch(self, request_uri):
        """
        Fetch the requested URI from the Spark API, replace the
        URLs in the response content for HTML responses or return
        the verbatim response.
        """
        if not request_uri.startswith(self.endpoint_url):
            self.fail()
        spark_url = self.url + request_uri[len(self.endpoint_url):]
        try:
            response = self.session.get(spark_url)
            content_type = response.headers['content-type']

            if 'text/html' in content_type:
                content = self.replace(response.text)
            else:
                # Probably binary response, send it directly.
                content = response.text

        except requests.exceptions.RequestException:
            content = json.dumps({'error': 'SPARK_NOT_RUNNING'})
            content_type = 'application/json'

        return content, content_type

    def replace(self, content):
        """
        Replace all the relative links with our proxy links
        """
        soup = BeautifulSoup(content, BEAUTIFULSOUP_BUILDER)

        for link in soup.find_all(['a', 'link'], href=True):
            link['href'] = url_path_join(self.endpoint_url, link['href'])

        for image in soup.find_all(['img', 'script'], src=True):
            image['src'] = url_path_join(self.endpoint_url, image['src'])
        return str(soup)
