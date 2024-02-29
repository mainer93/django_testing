import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from http import HTTPStatus
from news.pytest_tests import conftest


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_detail, form_data):
    response = client.post(news_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.FOUND
    assert comments_count == 0


def test_user_can_create_comment(auth_client, news_detail,
                                 form_data, news, author):
    response = auth_client.post(news_detail, data=form_data)
    assertRedirects(response, f'{news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == conftest.COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(auth_client, news_detail):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_client.post(news_detail, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(auth_client, comment_for_args):
    delete_url = reverse(conftest.NEWS_DELETE_URL, args=comment_for_args)
    response = auth_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(reader_client,
                                                  comment_for_args):
    delete_url = reverse(conftest.NEWS_DELETE_URL, args=comment_for_args)
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(auth_client, new_data,
                                 comment_for_args, comment):
    edit_url = reverse(conftest.NEWS_EDIT_URL, args=comment_for_args)

    response = auth_client.post(edit_url, data=new_data)
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == conftest.NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(admin_client, form_data,
                                                comment_for_args, comment):
    edit_url = reverse(conftest.NEWS_EDIT_URL, args=comment_for_args)
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == conftest.COMMENT_TEXT
