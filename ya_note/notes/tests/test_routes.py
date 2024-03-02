from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.tests import test_constants

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            author=cls.author,
            title=test_constants.TITLE_NOTE,
            text=test_constants.TEXT_NOTE,
            slug=test_constants.SLUG_NOTE,
        )

    def test_page_availability(self):
        tests = [
            ('notes:home', None, HTTPStatus.OK, ()),
            ('users:signup', None, HTTPStatus.OK, ()),
            ('users:login', None, HTTPStatus.OK, ()),
            ('users:logout', None, HTTPStatus.OK, ()),
            ('notes:list', self.auth_client, HTTPStatus.OK, ()),
            ('notes:success', self.auth_client, HTTPStatus.OK, ()),
            ('notes:add', self.auth_client, HTTPStatus.OK, ()),
            ('notes:detail', self.auth_client, HTTPStatus.OK,
             (self.note.slug,)),
            ('notes:delete', self.auth_client, HTTPStatus.OK,
             (self.note.slug,)),
            ('notes:edit', self.auth_client, HTTPStatus.OK,
             (self.note.slug,)),
        ]

        for name, client, expected_status, args in tests:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                if client:
                    response = client.get(url)
                else:
                    response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)
