import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from news.pytest_tests import conftest


def get_test_parameters():
    return [
        (conftest.NEWS_HOME, conftest.CLIENT, HTTPStatus.OK),
        (conftest.SIGNUP_URL, conftest.CLIENT, HTTPStatus.OK),
        (conftest.LOGIN_URL, conftest.CLIENT, HTTPStatus.OK),
        (conftest.LOGOUT_URL, conftest.CLIENT, HTTPStatus.OK),
        (conftest.NEWS_EDIT_URL, conftest.ADMIN, HTTPStatus.NOT_FOUND),
        (conftest.NEWS_EDIT_URL, conftest.AUTHOR, HTTPStatus.OK),
        (conftest.NEWS_DELETE_URL, conftest.ADMIN, HTTPStatus.NOT_FOUND),
        (conftest.NEWS_DELETE_URL, conftest.AUTHOR, HTTPStatus.OK),
    ]


@pytest.mark.parametrize(
    'url, client, expected_status',
    get_test_parameters(),
)
def test_pages_availability_for_different_users(url, client, expected_status,
                                                comment_for_args):
    if url in (conftest.NEWS_EDIT_URL, conftest.NEWS_DELETE_URL):
        url = reverse(url, args=comment_for_args)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        (conftest.NEWS_EDIT_URL, conftest.COMMENT_FOR_ARGS),
        (conftest.NEWS_DELETE_URL, conftest.COMMENT_FOR_ARGS),
    )
)
def test_edit_delete_comment_redirect_for_anonymous(client, name, args):
    login_url = conftest.LOGIN_URL
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
