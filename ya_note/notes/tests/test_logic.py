from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from notes.tests import test_constants


User = get_user_model()


class TestLogicApp(TestCase):

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
        cls.note = Note.objects.create(
            author=cls.author,
            title=test_constants.TITLE_NOTE,
            text=test_constants.TEXT_NOTE,
            slug=test_constants.SLUG_NOTE,
        )
        cls.form_data = {
            'title': test_constants.TITLE_LOGIC,
            'text': test_constants.TEXT_LOGIC,
            'slug': test_constants.SLUG_LOGIC
        }

    def test_authenticated_user_can_create_note(self):
        url = test_constants.NOTES_ADD_URL
        note_count = Note.objects.count()
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), note_count + 1)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.title, self.note.title)
        self.assertEqual(new_note.text, self.note.text)
        self.assertEqual(new_note.slug, self.note.slug)
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        url = test_constants.NOTES_ADD_URL
        note_count = Note.objects.count()
        response = self.client.post(url, data=self.form_data)
        login_url = test_constants.LOGIN_URL
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), note_count)

    def test_empty_slug(self):
        url = test_constants.NOTES_ADD_URL
        note_count = Note.objects.count()
        self.form_data.pop('slug')
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, test_constants.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), note_count + 1)
        expected_slug = slugify(self.form_data['title'])
        new_note = Note.objects.filter(slug=expected_slug).first()
        self.assertIsNotNone(new_note)
        self.assertEqual(new_note.slug, expected_slug)

    def test_not_unique_slug(self):
        url = test_constants.NOTES_ADD_URL
        note_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(url, data=self.form_data)
        self.assertFormError(response, form='form', field='slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), note_count)

    def test_author_can_edit_note(self):
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.auth_client.post(url, self.form_data)
        self.assertRedirects(response, test_constants.NOTES_SUCCESS_URL)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author, new_note.author)

    def test_other_user_cant_edit_note(self):
        user, status = self.reader_client, HTTPStatus.NOT_FOUND
        url = reverse('notes:edit', args=(self.note.slug,))
        response = user.post(url, self.form_data)
        self.assertEqual(response.status_code, status)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.auth_client.post(url)
        self.assertRedirects(response, test_constants.NOTES_SUCCESS_URL)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_delete_note(self):
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.reader_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
