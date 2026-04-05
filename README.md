# 🚀 Job Tracker API

**Job Tracker API** — backend-сервис для управления откликами на вакансии с AI-анализом их соответствия кандидату.

Проект позволяет пользователю отслеживать свои отклики, управлять статусами вакансий и получать рекомендации по улучшению навыков с помощью AI.

---

## 🔥 Основные возможности

* 📌 Управление вакансиями (CRUD)
* 🏢 Работа с компаниями
* 📝 Заметки к вакансиям
* 🔐 Аутентификация (JWT)
* 🤖 AI-анализ вакансий:

  * оценка соответствия кандидату
  * выявление сильных и слабых сторон
  * рекомендации по развитию навыков

---

## 🧠 AI-функциональность

Система анализирует вакансии на основе профиля пользователя:

* навыки
* уровень (junior/middle)
* описание профиля
* пользовательские предпочтения

### 📊 Пример ответа AI

```json
{
  "score": 0.72,
  "summary": "Здесь развернутый ответ ии-консультанта"  
}
```

## 🛠️ Технологии

* Python 3.11+
* FastAPI
* SQLAlchemy (async)
* PostgreSQL
* Alembic
* Docker / Docker Compose

---

## 📦 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/budaog300/JobTracker.git
```

### 2. Создать ⚙️ Переменные окружения

Создайте файл `.env` (или несколько файлов: `.env.db`, `.env.auth`, `.env.ai`) в корне проекта.

### 🗄️ База данных (`.env.db`)

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost # название контейнера с базой db
DB_PORT=5432
DB_NAME=job_tracker_db
```

---

### 🔐 Аутентификация (`.env.auth`)

```env
ACCESS_SECRET_KEY=your_access_secret
REFRESH_SECRET_KEY=your_refresh_secret
ALGORITHM=HS256
```

---

### 🤖 AI (`.env.ai`)

```env
OPENAI_API_KEY=your_api_key
BASE_URL=https://api.vsegpt.ru/v1
```

---

### 3. Запуск через Docker

```bash
docker-compose --env-file .env.db up -d --build
```

---

## 🔗 API эндпоинты

### 🔐 Auth

* `POST /auth/register` — регистрация
* `POST /auth/login` — авторизация
* `POST /auth/logout` — авторизация
* `POST /auth/refresh` — авторизация
* `GET /auth/profile` — текущий пользователь

---

### 💼 Vacancies

* `GET /vacancies` — список вакансий
* `POST /vacancies` — создать вакансию
* `GET /vacancies/{vacancy_id}` — получить вакансию
* `PATCH /vacancies/{vacancy_id}` — обновить
* `DELETE /vacancies/{vacancy_id}` — удалить

---

### 🏢 Companies

* `POST /companies`
* `GET /companies`
* `GET /companies/{vacancy_id}`
* `PATCH /companies/{vacancy_id}`
* `DELETE /companies/{vacancy_id}`

---

### 📝 Notes

* `POST /vacancies/{vacancy_id}/notes`
* `GET /vacancies/{vacancy_id}/notes`

---

### 🤖 AI

* `POST /vacancies/{vacancy_id}/analyze` — анализ вакансии

---

## 📊 Модель данных

* **User** — пользователь системы
* **Company** — компания
* **Vacancy** — вакансия
* **Note** — заметки
* **AiAnalysis** — результат AI-анализа

## 🚀 Возможности для развития

* добавление Redis (кэширование AI)
* история изменения статусов
* сравнение вакансий
* рекомендации лучших вакансий
* интеграция с внешними API (hh, LinkedIn)

---

## 👨‍💻 Автор

Backend-разработчик Python с опытом разработки API и интеграции AI-решений.
TG: @holly_molly42

---
