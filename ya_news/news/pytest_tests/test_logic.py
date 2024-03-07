from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests import conftest


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    expected_count = Comment.objects.count()
    url = reverse(conftest.NEWS_DETAIL_URL, args=(news.id,))
    response = client.post(url, data={'text': conftest.COMMENT_TEXT})
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.FOUND
    assert expected_count == comments_count


def test_user_can_create_comment(auth_client, news, comment):
    comments_before = set(Comment.objects.all())
    url = reverse(conftest.NEWS_DETAIL_URL, args=(news.id,))
    response = auth_client.post(url, data={'text': conftest.COMMENT_TEXT})
    assertRedirects(response, f'{url}#comments')
    comments_after = (set(Comment.objects.all()) - comments_before)
    assert len(comments_after) == 1
    new_comment = comments_after.pop()
    assert new_comment.text == conftest.COMMENT_TEXT
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author


def test_user_cant_use_bad_words(auth_client, news):
    expected_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse(conftest.NEWS_DETAIL_URL, args=(news.id,))
    response = auth_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_author_can_delete_comment(auth_client, comment):
    delete_url = reverse(conftest.NEWS_DELETE_URL, args=(comment.id,))
    response = auth_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cant_delete_comment_of_another_user(reader_client, comment):
    delete_url = reverse(conftest.NEWS_DELETE_URL, args=(comment.id,))
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(id=comment.id).exists()


def test_author_can_edit_comment(auth_client, comment):
    expected_count = Comment.objects.count()
    edit_url = reverse(conftest.NEWS_EDIT_URL, args=(comment.id,))
    response = auth_client.post(edit_url,
                                data={'text': conftest.NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.FOUND
    new_comment = Comment.objects.get(id=comment.id)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count
    assert new_comment.text == conftest.NEW_COMMENT_TEXT
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(admin_client, comment):
    expected_count = Comment.objects.count()
    edit_url = reverse(conftest.NEWS_EDIT_URL, args=(comment.id,))
    response = admin_client.post(edit_url,
                                 data={'text': conftest.NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    new_comment = Comment.objects.get(id=comment.id)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count
    assert new_comment.text == comment.text
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author
