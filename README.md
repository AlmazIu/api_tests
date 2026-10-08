# RealWorld API Tests

Автотесты REST API приложения [RealWorld](https://github.com/gothinkster/realworld) (клон Medium: пользователи, статьи, комментарии) на **Python + pytest + requests**.

Ожидаемое поведение берётся из [спецификации RealWorld API](https://github.com/gothinkster/realworld/tree/main/specs/api) (`openapi.yml` и Hurl-сценарии).

## Что покрыто

| Модуль | Проверки |
|---|---|
| Авторизация | регистрация, логин, текущий пользователь; неверный пароль, запрос без токена, пустые поля (параметризация), дубликат email |
| Профиль | обновление `bio`, проверка сохранения повторным запросом, обновление без токена |
| Статьи | создание, получение по slug, удаление с проверкой 404, запрет удаления чужой статьи (403 + статья не удалена) |

Тестовые данные уникальны для каждого запуска (`uuid`), созданные статьи удаляются фикстурами после теста.

## Стек

- Python 3.14+
- pytest — фикстуры, параметризация
- requests — HTTP-клиент
- [uv](https://docs.astral.sh/uv/) — зависимости и виртуальное окружение

## Запуск

### 1. Поднять бэкенд

Используется реализация [realworld-django-ninja](https://github.com/c4ffein/realworld-django-ninja) в Docker:

```bash
git clone https://github.com/c4ffein/realworld-django-ninja.git
cd realworld-django-ninja
docker compose up
```

API будет доступен на `http://localhost:8000/api`, Swagger — на `http://localhost:8000/docs`.

### 2. Запустить тесты

```bash
uv run pytest -v
```

Другой адрес API задаётся переменной окружения `API_URL`:

```bash
API_URL=https://api.realworld.show/api uv run pytest -v
```

## Структура

```
tests/
├── conftest.py      # фикстуры: пользователи, статья с удалением после теста
├── test_auth.py     # регистрация и логин
├── test_user.py     # обновление профиля
└── test_articles.py # CRUD статей и права доступа
```

## Планы

- [ ] API-клиент вместо прямых вызовов requests
- [ ] Комментарии, избранное, подписки
- [ ] Валидация схем ответов (pydantic)
- [ ] Allure-отчёт
- [ ] Запуск в GitHub Actions
