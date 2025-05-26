Описание:
# Weather Web Application

Веб-приложение для получения прогноза погоды по названию города.

## Реализованный функционал

- [x] Основной функционал: ввод города, получение прогноза погоды.
- [x] Данные о погоде выводятся в удобном формате (на сегодня и на 3 дня вперед).
- [x] Написаны тесты (для views и services с использованием `pytest` и `mock`).
- [x] Приложение полностью обернуто в Docker-контейнеры (`web`, `db`).
- [x] Реализовано автодополнение (подсказки) при вводе города с помощью Яндекс.Геосаджеста.
- [x] При повторном посещении сайта предлагается посмотреть погоду в городе, который искали в последний раз (используются сессии Django).
- [x] Сохраняется общая история поиска городов.
- [x] Реализован API-эндпоинт (`/api/stats/`), который показывает статистику поисковых запросов (какой город сколько раз искали), отсортированную по популярности.

## Технологии

- **Backend:** Python, Django, Django REST Framework
- **База данных:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (для API Яндекс.Карт)
- **API погоды:** Яндекс.Погода, Яндекс.Геокодер, Яндекс.Геосаджест
- **Тестирование:** Pytest, pytest-django
- **Контейнеризация:** Docker, Docker Compose
- **Менеджер пакетов:** uv

## Как запустить проект

### Требования

- Docker
- Docker Compose

### Запуск с помощью Docker

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <your-repo-url>
    cd weather_project
    ```

2.  **Создайте файл `.env`:**
    Скопируйте `example.env` (если вы его создали) в `.env` и заполните своими данными:
    ```
    cp example.env .env
    ```
    Или создайте файл `.env` вручную со следующим содержимым:
    ```
    DJANGO_SECRET_KEY='your-django-secret-key'
    YANDEX_API_KEY='your-yandex-api-key-for-weather-and-geocoder'
    # API ключ для JS (если он отличается)
    YANDEX_JS_API_KEY='your-yandex-js-api-key-for-suggest'

    # PostgreSQL settings
    POSTGRES_DB=weather_db
    POSTGRES_USER=weather_user
    POSTGRES_PASSWORD=strongpassword
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```
    **Важно:** Не забудьте также вставить ваш JS API ключ в шаблон `weather/templates/weather/base.html`.

3.  **Сборка и запуск контейнеров:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Применение миграций:**
    После первого запуска контейнеров необходимо применить миграции Django.
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Готово!**
    - Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)
    - API статистики будет доступно по адресу: [http://localhost:8000/api/stats/](http://localhost:8000/api/stats/)

### Запуск тестов

Чтобы запустить тесты, выполните команду в контейнере:
```bash
docker-compose exec web pytest
```