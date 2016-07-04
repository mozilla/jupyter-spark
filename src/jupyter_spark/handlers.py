import json

import tornado.web
from notebook.base.handlers import IPythonHandler
from tornado import httpclient


class SparkHandler(IPythonHandler):

    def initialize(self, spark):
        self.spark = spark

    @tornado.web.asynchronous
    def get(self):
        """
        Fetch the requested URI from the Spark API, replace the
        URLs in the response content for HTML responses or return
        the verbatim response.
        """
        http = httpclient.AsyncHTTPClient()
        url = self.spark.backend_url(self.request)
        self.spark.log.debug('Fetching from Spark %s', url)
        http.fetch(url, self.handle_response)

    def handle_response(self, response):
        if response.error:
            content_type = 'application/json'
            content = json.dumps({'error': 'SPARK_NOT_RUNNING'})
        else:
            content_type = response.headers['Content-Type']
            if 'text/html' in content_type:
                content = self.spark.replace(response.body)
            else:
                # Probably binary response, send it directly.
                content = response.body
        self.set_header('Content-Type', content_type)
        self.write(content)
        self.finish()
