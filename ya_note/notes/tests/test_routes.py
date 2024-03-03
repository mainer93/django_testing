from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note
from notes.tests import test_constants

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username=test_constants.AUTHOR_USERNAME
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.reader = User.objects.create(
            username=test_constants.READER_USERNAME
        )
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.anonymous = User.objects.create(
            username=test_constants.ANONYMOUS_USERNAME
        )
        cls.anonymous_client = Client()
        cls.note = Note.objects.create(
            author=cls.author,
            title=test_constants.TITLE_NOTE,
            text=test_constants.TEXT_NOTE,
            slug=test_constants.SLUG_NOTE,
        )

    def test_page_availability(self):
        tests = [
            (test_constants.HOME_URL, self.anonymous_client, HTTPStatus.OK),
            (test_constants.SIGNUP_URL, self.anonymous_client, HTTPStatus.OK),
            (test_constants.LOGIN_URL, self.anonymous_client, HTTPStatus.OK),
            (test_constants.LOGOUT_URL, self.anonymous_client, HTTPStatus.OK),
            (test_constants.NOTES_LIST_URL, self.reader_client,
             HTTPStatus.OK),
            (test_constants.NOTES_SUCCESS_URL, self.reader_client,
             HTTPStatus.OK),
            (test_constants.NOTES_ADD_URL, self.reader_client,
             HTTPStatus.OK),
            (test_constants.NOTES_DETAIL_URL, self.auth_client,
             HTTPStatus.OK),
            (test_constants.NOTES_DELETE_URL, self.auth_client,
             HTTPStatus.OK),
            (test_constants.NOTES_EDIT_URL, self.auth_client,
             HTTPStatus.OK),
            (test_constants.NOTES_DETAIL_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (test_constants.NOTES_DELETE_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (test_constants.NOTES_EDIT_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
        ]

        for url, client, expected_status in tests:
            with self.subTest(url=url, client=client,
                              expected_status=expected_status):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)
