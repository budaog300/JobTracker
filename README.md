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
  "summary": "Вакансия в целом подходит кандидату"  
}
```

---

## 🏗️ Архитектура

Проект построен по принципу **Layered Architecture**:

```
API (роуты)
↓
Service (бизнес-логика)
↓
Repository (работа с БД)
↓
PostgreSQL
```

---

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
git clone https://github.com/your-username/job-tracker.git
cd job-tracker
```

### 2. Создать `.env`

```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/jobtracker
SECRET_KEY=your_secret_key
```

### 3. Запуск через Docker

```bash
docker-compose up --build
```

---

## 🔗 API эндпоинты

### 🔐 Auth

* `POST /auth/register` — регистрация
* `POST /auth/login` — авторизация
* `GET /auth/me` — текущий пользователь

---

### 💼 Vacancies

* `GET /vacancies` — список вакансий
* `POST /vacancies` — создать вакансию
* `GET /vacancies/{id}` — получить вакансию
* `PUT /vacancies/{id}` — обновить
* `DELETE /vacancies/{id}` — удалить

---

### 🏢 Companies

* `POST /companies`
* `GET /companies`
* `GET /companies/{id}`
* `PUT /companies/{id}`
* `DELETE /companies/{id}`

---

### 📝 Notes

* `POST /vacancies/{id}/notes`
* `GET /vacancies/{id}/notes`

---

### 🤖 AI

* `POST /vacancies/{id}/analyze` — анализ вакансии

---

## 📊 Модель данных

* **User** — пользователь системы
* **Company** — компания (привязана к пользователю)
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

---
