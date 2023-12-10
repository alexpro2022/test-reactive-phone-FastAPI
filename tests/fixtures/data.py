# Messages
POST_NOT_FOUND_MSG = 'Пост(ы) не найден(ы).'
POST_ALREADY_EXISTS_MSG = 'Пост с таким заголовком уже существует.'
NO_PERMISSION_MSG = 'У вас нет прав доступа к данному посту.'
NO_SELF_LIKE_DISLIKE_MSG = 'Запрещено ставить LIKE/DISLIKE собственным постам.'

# Users
AUTH_USER = {'email': 'testuser@example.com', 'password': 'testpass'}
AUTHOR = {'email': 'author@example.com', 'password': 'author'}

# Endpoints
ENDPOINT = 'post'
MY_POSTS_ENDPOINT = f'{ENDPOINT}/my_posts'
LIKE_ENDPOINT = f'{ENDPOINT}/like'
DISLIKE_ENDPOINT = f'{ENDPOINT}/dislike'
ID = 1

# Payloads
POST_PAYLOAD = {'title': 'POST New post title.', 'content': 'POST New post content.'}
PUT_PAYLOAD = {'title': 'update for title.', 'content': 'update for content.'}
