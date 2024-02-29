import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import datetime, timedelta
from news.models import News, Comment


User = get_user_model()

NEWS_COUNT_ON_HOME_PAGE = 10

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
NEWS_HOME = reverse('news:home')

NEWS_DELETE_URL = ('news:delete')
NEWS_EDIT_URL = ('news:edit')
NEWS_HOME_URL = ('news:home')
NEWS_DETAIL_URL = ('news:detail')

CLIENT = Client()
ADMIN = pytest.lazy_fixture('admin_client')
AUTHOR = pytest.lazy_fixture('auth_client')
COMMENT_FOR_ARGS = pytest.lazy_fixture('comment_for_args')

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'
NEWS_TITLE = 'Заголовок'
NEWS_TEXT = 'Текст'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def auth_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title=NEWS_TITLE,
        text=NEWS_TEXT,
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT,
    )
    return comment


@pytest.fixture
def news_list():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Заголовок {index}',
            text=f'Текст {index}',
            date=today - timedelta(days=index),
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_list(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        return comment


@pytest.fixture
def form_data():
    return {
        'text': COMMENT_TEXT,
    }


@pytest.fixture
def new_data():
    return {
        'text': NEW_COMMENT_TEXT,
    }


@pytest.fixture
def comment_for_args(comment):
    return (comment.id,)


@pytest.fixture
def news_for_args(news):
    return (news.id,)


@pytest.fixture
def news_detail(news):
    return reverse(NEWS_DETAIL_URL, args=(news.id,))


@pytest.fixture
def news_home():
    return NEWS_HOME
