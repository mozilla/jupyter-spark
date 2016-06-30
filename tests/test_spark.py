# -*- coding: utf-8 -*-
import pytest
import requests
import six
import tornado
from bs4 import BeautifulSoup
from httmock import HTTMock, urlmatch
from jupyter_spark.spark import BEAUTIFULSOUP_BUILDER, Spark
from notebook.utils import url_path_join


SPARK_ENDPOINT = '/spark'
SPARK_URL = 'http://localhost:4040'
BASE_URL = 'http://localhost:8888'
FULL_URL = url_path_join(BASE_URL, SPARK_ENDPOINT)
RESPONSE_CONTENT = '<img src="/image.png" />'


@pytest.fixture
def spark():
    return Spark(base_url=BASE_URL)


@urlmatch(path=r'^/success$')
def successful_response(url, request):
    return {'status_code': 200,
            'content': RESPONSE_CONTENT,
            'headers': {'content-type': 'text/html'}}


def test_successful_response(spark):
    with HTTMock(successful_response):
        content, content_type = spark.fetch(FULL_URL + '/success')
        assert content_type == 'text/html'
        assert six.u(FULL_URL) in content


def test_request_uri_prefix(spark):
    with HTTMock(successful_response):
        with pytest.raises(tornado.web.HTTPError) as excinfo:
            spark.fetch(BASE_URL + '/false/prefix')
        assert 'Request URI did not start with' in str(excinfo.value)


@urlmatch(path=r'^/wrong$')
def wrong_content_type(url, request):
    return {'status_code': 200,
            'content': RESPONSE_CONTENT,
            'headers': {'content-type': 'special/test'}}


def test_wrong_content_type(spark):
    with HTTMock(wrong_content_type):
        content, content_type = spark.fetch(FULL_URL + '/wrong')
        assert content_type == 'special/test'
        assert six.u(FULL_URL) not in content  # replacement didn't happen


@urlmatch(path=r'^/exception$')
def requests_exception(url, request):
    raise requests.exceptions.RequestException(500, 'error')


def test_requests_exception(spark):
    with HTTMock(requests_exception):
        content, content_type = spark.fetch(FULL_URL + '/exception')
        assert content_type == 'application/json'
        assert 'SPARK_NOT_RUNNING' in content


@pytest.mark.parametrize('content', [
    '<a href="/page/">page</a>',
    '<link rel="stylesheet" href="/styles.css" />',
    six.u('<a href="/über-uns/">Über uns</a>'),
    # missing href attribute so expected to fail:
    pytest.mark.xfail('<a>page</a>'),
    pytest.mark.xfail('<link rel="stylesheet" data-href="/styles.css" />'),
])
def test_replace_href_tags(content, spark):
    replaced = spark.replace(content)
    assert replaced != content
    soup = BeautifulSoup(replaced, BEAUTIFULSOUP_BUILDER)
    for tag in soup.find_all(['a', 'link']):
        assert tag.attrs['href'].startswith(FULL_URL)


@pytest.mark.parametrize('content', [
    '<img src="/img.png" />',
    '<script src="/script.js" />',
    six.u('<script src="/scrüpt.js" />'),
    # missing src attribute so expected to fail:
    pytest.mark.xfail('<img data-src="/img.png" />'),
    pytest.mark.xfail('<script data-src="/script.js" />'),
])
def test_replace_src_tags(content, spark):
    replaced = spark.replace(content)
    assert replaced != content
    soup = BeautifulSoup(replaced, BEAUTIFULSOUP_BUILDER)
    for tag in soup.find_all(['img', 'script']):
        assert tag.attrs['src'].startswith(FULL_URL)
