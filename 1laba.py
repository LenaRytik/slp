import requests  # Импортируем библиотеку для работы с HTTP запросами

# URL для взаимодействия с тестовым сервером
api_url = "https://jsonplaceholder.typicode.com/posts"

# Шаг 1: Выполняем GET-запрос для получения списка всех постов
get_response = requests.get(api_url)

# Проверяем статус ответа
if get_response.status_code == 200:
    # Преобразуем данные ответа в формат JSON для дальнейшей работы
    all_posts = get_response.json()
    print("Посты пользователей с чётными идентификаторами (ID):")
    
    # Перебираем посты и выводим только те, у которых ID пользователя чётное
    for post_item in all_posts:
        if post_item['userId'] % 2 == 0:
            print(f"Post ID: {post_item['id']}, Title: {post_item['title']}")
else:
    print(f"Ошибка при выполнении запроса: {get_response.status_code}")

# Шаг 2: Подготавливаем данные для создания нового поста
create_url = "https://jsonplaceholder.typicode.com/posts"

# Данные нового поста
post_data = {
    "title": "Мой тестовый пост",
    "body": "Это содержание моего тестового поста",
    "userId": 2
}

# Отправляем POST-запрос для создания поста
post_response = requests.post(create_url, json=post_data)

# Проверяем успешность запроса и выводим результат
if post_response.status_code == 201:
    new_post_response = post_response.json()
    print("Новый пост успешно создан:")
    print(new_post_response)
else:
    print(f"Ошибка при создании поста: {post_response.status_code}")

# Шаг 3: Обновление созданного поста
# Определяем ID поста для обновления (в реальности берётся из ответа при создании)
created_post_id = 101  # В тестовой среде JSONPlaceholder ID всегда > 100

# URL для обновления поста
update_url = f"https://jsonplaceholder.typicode.com/posts/{created_post_id}"

# Данные для обновления поста
updated_post_data = {
    "title": "Обновлённый заголовок поста",
    "body": "Это обновлённое содержание поста",
    "userId": 2
}

# Выполняем PUT-запрос для обновления поста
update_response = requests.put(update_url, json=updated_post_data)

# Проверяем статус ответа и выводим обновлённые данные поста
if update_response.status_code == 200:
    updated_post = update_response.json()
    print("Пост успешно обновлён:")
    print(updated_post)
else:
    print(f"Ошибка при обновлении поста: {update_response.status_code}")
