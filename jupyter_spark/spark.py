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
        if not self.request.uri.startswith(self.prefix):
            raise_error('Request URI did not start with %s' % self.prefix)

        spark_url = self.host + self.request.uri[len(self.prefix):]

        try:
            spark_response = requests.get(spark_url)

            content_type = spark_response.headers['content-type']
            self.set_header('Content-Type', content_type)

            if 'text' in content_type:
                # Replace all the relative links with our proxy links
                soup = BeautifulSoup(spark_response.text, 'html.parser')

                for has_href in ['a', 'link']:
                    for a in soup.find_all(has_href):
                        if 'href' in a.attrs:
                            a['href'] = url_path_join(self.full_url, a['href'])

                for has_src in ['img', 'script']:
                    for a in soup.find_all(has_src):
                        if 'src' in a.attrs:
                            a['src'] = url_path_join(self.full_url, a['src'])

                client_response = str(soup)
            else:
                # Probably binary response, send it directly.
                client_response = spark_response.content

        except requests.exceptions.RequestException:
            client_response = json.dumps({'error': 'SPARK_NOT_RUNNING'})

        self.write(client_response)
        self.flush()
