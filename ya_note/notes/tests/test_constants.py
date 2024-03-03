from django.urls import reverse

TITLE_LOGIC = 'Новый заголовок'
TEXT_LOGIC = 'Новый текст'
SLUG_LOGIC = 'new-slug'
TITLE_NOTE = 'Заголовок'
TEXT_NOTE = 'Текст'
SLUG_NOTE = 'testslug'
AUTHOR_USERNAME = 'Автор'
READER_USERNAME = 'Читатель'
ANONYMOUS_USERNAME = 'Аноним'

HOME_URL = reverse('notes:home')
SIGNUP_URL = reverse('users:signup')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
NOTES_LIST_URL = reverse('notes:list')
NOTES_SUCCESS_URL = reverse('notes:success')
NOTES_ADD_URL = reverse('notes:add')
NOTES_DETAIL_URL = reverse('notes:detail', args=(SLUG_NOTE,))
NOTES_DELETE_URL = reverse('notes:delete', args=(SLUG_NOTE,))
NOTES_EDIT_URL = reverse('notes:edit', args=(SLUG_NOTE,))
