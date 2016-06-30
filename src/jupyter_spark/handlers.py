from notebook.base.handlers import IPythonHandler


class SparkHandler(IPythonHandler):

    def initialize(self, spark):
        self.spark = spark

    def get(self):
        content, content_type = self.spark.fetch(self.request.uri)
        self.set_header('Content-Type', content_type)
        self.write(content)
