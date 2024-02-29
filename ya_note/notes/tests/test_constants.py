from django.urls import reverse

TITLE_LOGIC = 'Новый заголовок'
TEXT_LOGIC = 'Новый текст'
SLUG_LOGIC = 'new-slug'
TITLE_NOTE = 'Заголовок'
TEXT_NOTE = 'Текст'
SLUG_NOTE = 'testslug'
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
LOGIN_URL = reverse('users:login')
NOTES_SUCCESS_URL = reverse('notes:success')
