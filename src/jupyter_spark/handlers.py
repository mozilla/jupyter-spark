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
        spark_url = self.get_argument("spark_url", None)
        if spark_url is not None:
            url = self.spark.backend_url(spark_url, self.request.path)
            http.fetch(url, self.handle_response)
        else:
            content_type = 'application/json'
            content = json.dumps({'error': 'SPARK_URL_MISSING'})
            self.set_header('Content-Type', content_type)
            self.write(content)
            self.finish()

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
