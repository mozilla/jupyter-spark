import json

import requests
import tornado

from bs4 import BeautifulSoup
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler


def raise_error(msg):
    raise tornado.web.HTTPError(500, 'ERROR: ' + msg)


class SparkHandler(IPythonHandler):

    def initialize(self, host, url, prefix):
        self.host = host
        self.url = url
        self.prefix = prefix
        self.full_url = url_path_join(self.url, self.prefix)

    def get(self):
        if not self.request.uri.startswith(self.full_url):
            raise_error('Request URI did not start with %s' % self.full_url)

        spark_url = self.host + self.request.uri[len(self.full_url):]

        try:
            spark_response = requests.get(spark_url)

            content_type = spark_response.headers['content-type']
            self.set_header('Content-Type', content_type)

            if 'text/html' in content_type:
                # Replace all the relative links with our proxy links
                soup = BeautifulSoup(spark_response.text, 'html.parser')

                for link in soup.find_all(['a', 'link'], href=True):
                    link['href'] = url_path_join(self.full_url, link['href'])

                for image in soup.find_all(['img', 'script'], src=True):
                    image['src'] = url_path_join(self.full_url, image['src'])

                client_response = str(soup)
            else:
                # Probably binary response, send it directly.
                client_response = spark_response.content

        except requests.exceptions.RequestException:
            client_response = json.dumps({'error': 'SPARK_NOT_RUNNING'})

        self.write(client_response)
        self.flush()
