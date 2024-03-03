from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.pytest_tests import conftest


def get_test_parameters():
    return [
        (conftest.NEWS_HOME, Client(), HTTPStatus.OK),
        (conftest.SIGNUP_URL, Client(), HTTPStatus.OK),
        (conftest.LOGIN_URL, Client(), HTTPStatus.OK),
        (conftest.LOGOUT_URL, Client(), HTTPStatus.OK),
        (conftest.DELETE_URL, conftest.AUTHOR, HTTPStatus.OK),
        (conftest.DELETE_URL, conftest.ADMIN, HTTPStatus.NOT_FOUND),
        (conftest.EDIT_URL, conftest.AUTHOR, HTTPStatus.OK),
        (conftest.EDIT_URL, conftest.ADMIN, HTTPStatus.NOT_FOUND),
    ]


@pytest.mark.parametrize(
    'url, client, expected_status',
    get_test_parameters(),
)
@pytest.mark.django_db
def test_pages_availability_for_different_users(url, client, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        conftest.NEWS_EDIT_URL,
        conftest.NEWS_DELETE_URL,
    )
)
def test_edit_delete_comment_redirect_for_anonymous(client, name, comment):
    login_url = conftest.LOGIN_URL
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
