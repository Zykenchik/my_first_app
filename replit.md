# Система управления данными с аутентификацией

## Обзор проекта
Веб-приложение на Flask для управления данными доставок с системой аутентификации пользователей. Использует Supabase в качестве базы данных.

## Технологии
- **Backend**: Flask (Python 3.11)
- **База данных**: Supabase (PostgreSQL)
- **Аутентификация**: Flask-Login + bcrypt
- **Frontend**: Bootstrap 5, HTML/CSS/JavaScript

## Структура базы данных

### Таблица users
- id (BIGSERIAL, PRIMARY KEY)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- password (VARCHAR, хешированный bcrypt)
- created_at (TIMESTAMP)

### Таблица deliveries
- id (BIGSERIAL, PRIMARY KEY)
- address (TEXT)
- courier (VARCHAR)
- recipient (VARCHAR)
- description (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## Функциональность
1. **Аутентификация**: Вход/выход, регистрация пользователей
2. **CRUD операции**: Создание, чтение, обновление, удаление записей доставок
3. **Безопасность**: Хеширование паролей bcrypt, управление сессиями
4. **Интерфейс**: Адаптивный дизайн с Bootstrap, модальные окна для форм

## Файлы проекта
- `main.py` - основное приложение Flask
- `init_db.py` - скрипт инициализации базы данных
- `templates/` - HTML шаблоны (base, login, register, dashboard)
- `.gitignore` - игнорируемые файлы

## Переменные окружения
- `SUPABASE_URL` - URL проекта Supabase
- `SUPABASE_KEY` - API ключ Supabase
- `SESSION_SECRET` - секретный ключ для сессий Flask

## Архитектурные решения
- **URL нормализация**: Создан модуль `supabase_helper.py` для автоматической конвертации PostgreSQL DSN формата в HTTPS URL формат, необходимый для Supabase Python client
- **Безопасность**: Пароли хешируются с использованием bcrypt вместо MD5 для повышенной безопасности
- **Сессии**: Используется Flask-Login для управления пользовательскими сессиями

## Последние изменения
**2025-10-20**: 
- Создана полная структура приложения с аутентификацией и CRUD функционалом для управления доставками
- Исправлена критическая проблема с парсингом Supabase URL (добавлен supabase_helper.py)
- Реализована нормализация PostgreSQL DSN в HTTPS URL для корректной работы Supabase client
