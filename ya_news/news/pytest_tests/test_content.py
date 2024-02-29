import pytest

from news.forms import CommentForm
from news.pytest_tests import conftest


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_count(client, news_home):
    url = news_home
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == conftest.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_home):
    url = news_home
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('comments_list')
def test_comments_order(client, news_detail):
    response = client.get(news_detail)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_detail):
    url = news_detail
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(news_detail, auth_client):
    url = news_detail
    response = auth_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
