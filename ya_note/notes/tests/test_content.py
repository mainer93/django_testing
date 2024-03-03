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
        users_statuses = (
            (self.author, True),
            (self.reader, False),
        )
        url = test_constants.NOTES_LIST_URL
        for user, status in users_statuses:
            with self.subTest(user=user, status=status):
                self.auth_client.force_login(user)
                response = self.auth_client.get(url)
                object_list = response.context['object_list']
                if status:
                    self.assertIn(self.note, object_list)
                else:
                    self.assertNotIn(self.note, object_list)
