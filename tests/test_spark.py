# -*- coding: utf-8 -*-
import pytest
import requests
import six
import tornado
from bs4 import BeautifulSoup
from httmock import HTTMock, urlmatch
from jupyter_spark.spark import BEAUTIFULSOUP_BUILDER, SparkProxy
from notebook.utils import url_path_join


SPARK_ENDPOINT = '/spark'
SPARK_URL = 'http://localhost:4040'
APP_URL = 'http://localhost:8888'
FULL_URL = url_path_join(APP_URL, SPARK_ENDPOINT)
RESPONSE_CONTENT = '<img src="/image.png" />'


@pytest.fixture
def proxy():
    return SparkProxy(FULL_URL)


@urlmatch(path=r'^/success$')
def successful_response(url, request):
    return {'status_code': 200,
            'content': RESPONSE_CONTENT,
            'headers': {'content-type': 'text/html'}}


def test_successful_response(proxy):
    with HTTMock(successful_response):
        content, content_type = proxy.fetch(FULL_URL + '/success', SPARK_URL)
        assert content_type == 'text/html'
        assert six.u(FULL_URL) in content


def test_request_uri_prefix(proxy):
    with HTTMock(successful_response):
        with pytest.raises(tornado.web.HTTPError) as excinfo:
            proxy.fetch(APP_URL + '/false/prefix', SPARK_URL)
        assert 'Request URI did not start with' in str(excinfo.value)


@urlmatch(path=r'^/wrong$')
def wrong_content_type(url, request):
    return {'status_code': 200,
            'content': RESPONSE_CONTENT,
            'headers': {'content-type': 'special/test'}}


def test_wrong_content_type(proxy):
    with HTTMock(wrong_content_type):
        content, content_type = proxy.fetch(FULL_URL + '/wrong', SPARK_URL)
        assert content_type == 'special/test'
        assert six.u(FULL_URL) not in content  # replacement didn't happen


@urlmatch(path=r'^/exception$')
def requests_exception(url, request):
    raise requests.exceptions.RequestException(500, 'error')


def test_requests_exception(proxy):
    with HTTMock(requests_exception):
        content, content_type = proxy.fetch(FULL_URL + '/exception', SPARK_URL)
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
def test_replace_href_tags(content, proxy):
    replaced = proxy.replace(content)
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
def test_replace_src_tags(content, proxy):
    replaced = proxy.replace(content)
    assert replaced != content
    soup = BeautifulSoup(replaced, BEAUTIFULSOUP_BUILDER)
    for tag in soup.find_all(['img', 'script']):
        assert tag.attrs['src'].startswith(FULL_URL)
