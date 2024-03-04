from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from notes.tests import test_constants

User = get_user_model()


class TestContent(TestCase):

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
        cls.note = Note.objects.create(
            author=cls.author,
            title=test_constants.TITLE_NOTE,
            text=test_constants.TEXT_NOTE,
            slug=test_constants.SLUG_NOTE,
        )

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_for_different_users(self):
        def assert_note_in(object_list):
            self.assertIn(self.note, object_list)

        def assert_note_not_in(object_list):
            self.assertNotIn(self.note, object_list)

        users_statuses = (
            (self.author, assert_note_in),
            (self.reader, assert_note_not_in),
        )

        for user, assert_function in users_statuses:
            with self.subTest(user=user):
                url = test_constants.NOTES_LIST_URL
                self.auth_client.force_login(user)
                response = self.auth_client.get(url)
                object_list = response.context['object_list']
                assert_function(object_list)
