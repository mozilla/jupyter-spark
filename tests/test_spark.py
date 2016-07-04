# -*- coding: utf-8 -*-
import pytest
import six
import tornado
import tornado.httpclient
import tornado.testing
import tornado.web
from bs4 import BeautifulSoup
from jupyter_spark.handlers import SparkHandler
from jupyter_spark.spark import BEAUTIFULSOUP_BUILDER, Spark


PROXY_PREFIX = "/proxy/application_1234556789012_3456"
spark = Spark(base_url='http://localhost:8888')


class FakeHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header('Content-Type', self.CONTENT_TYPE)
        self.write(self.RESPONSE)


class FakeReplaceHandler(FakeHandler):
    handler_root = '/backend/replace'
    RESPONSE = six.b('<img src="/image.png" />')
    REPLACED = six.b('<img src="/spark/image.png"/>')
    CONTENT_TYPE = 'text/html'


class FakeVerbatimHandler(FakeHandler):
    handler_root = '/backend/verbatim'
    RESPONSE = six.b('<a href="/">Hello, world!</a>')
    CONTENT_TYPE = 'plain/text'


class SparkHandlerTests(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        port = self.get_http_port()
        base_url = 'http://localhost:%s' % port
        self.spark = Spark(base_url=base_url)
        return tornado.web.Application([
            (spark.proxy_root + '.*', SparkHandler, {'spark': self.spark}),
            (FakeReplaceHandler.handler_root, FakeReplaceHandler),
            (FakeVerbatimHandler.handler_root, FakeVerbatimHandler),
        ])

    def test_http_fetch_error(self):
        response = self.fetch(self.spark.proxy_root)
        self.assertEqual(response.code, 200)
        self.assertIn(six.b('SPARK_NOT_RUNNING'), response.body)

    def test_http_fetch_replace_success(self):
        self.spark.url = self.spark.base_url + FakeReplaceHandler.handler_root
        response = self.fetch(self.spark.proxy_root)
        self.assertEqual(response.code, 200)
        self.assertNotEqual(response.body, FakeReplaceHandler.RESPONSE)
        self.assertEqual(response.body, FakeReplaceHandler.REPLACED)
        self.assertEqual(response.headers['Content-Type'],
                         FakeReplaceHandler.CONTENT_TYPE)

    def test_http_fetch_verbatim_success(self):
        self.spark.url = self.spark.base_url + FakeVerbatimHandler.handler_root
        response = self.fetch(self.spark.proxy_root)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, FakeVerbatimHandler.RESPONSE)
        self.assertEqual(response.headers['Content-Type'],
                         FakeVerbatimHandler.CONTENT_TYPE)

    def test_spark_backend_url(self):
        class FakeRequest(object):
            # http://localhost:8888/spark/api
            uri = self.spark.base_url + self.spark.proxy_root + '/api'
        fake_request = FakeRequest()
        self.assertEqual(self.spark.backend_url(fake_request),
                         self.spark.url + '/api')


@pytest.mark.parametrize('content', [
    '<a href="{prefix}/page/">page</a>',
    '<link rel="stylesheet" href="{prefix}/styles.css" />',
    six.u('<a href="{prefix}/über-uns/">Über uns</a>'),
    # missing href attribute so expected to fail:
    pytest.mark.xfail('<a data-href="{prefix}/page/">page</a>'),
    pytest.mark.xfail('<link rel="stylesheet" data-href="{prefix}/styles.css" />'),
    # fails because the URL path doesn't start with the prefix
    pytest.mark.xfail('<a href="/something/completely/">different</a>'),
])
def test_replace_href_tags(content):
    content = content.format(prefix=PROXY_PREFIX)
    replaced = spark.replace(content)
    assert replaced != content
    soup = BeautifulSoup(replaced, BEAUTIFULSOUP_BUILDER)
    for tag in soup.find_all(['a', 'link']):
        assert tag.attrs['href'].startswith(spark.proxy_root)


@pytest.mark.parametrize('content', [
    '<img src="{prefix}/img.png" />',
    '<script src="{prefix}/script.js" />',
    '<img src="/logo.png" />',
    six.u('<script src="{prefix}/scrüpt.js" />'),
    # missing src attribute so expected to fail:
    pytest.mark.xfail('<img data-src="{prefix}/img.png" />'),
    pytest.mark.xfail('<script data-src="{prefix}/script.js" />'),
])
def test_replace_src_tags(content):
    content = content.format(prefix=PROXY_PREFIX)
    replaced = spark.replace(content)
    assert replaced != content
    soup = BeautifulSoup(replaced, BEAUTIFULSOUP_BUILDER)
    for tag in soup.find_all(['img', 'script']):
        assert tag.attrs['src'].startswith(spark.proxy_root)
