import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase_helper import normalize_supabase_url

load_dotenv()

supabase_url = normalize_supabase_url(os.environ.get('SUPABASE_URL'))
supabase_key = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)

def init_database():
    print("Инициализация базы данных Supabase...")
    print("\nВыполните следующие SQL-запросы в SQL Editor вашего проекта Supabase:")
    print("\n" + "="*80)
    
    users_table = """
-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Добавление индексов для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
"""
    
    deliveries_table = """
-- Создание таблицы доставок
CREATE TABLE IF NOT EXISTS deliveries (
    id BIGSERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    courier VARCHAR(255) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Добавление индекса
CREATE INDEX IF NOT EXISTS idx_deliveries_created ON deliveries(created_at DESC);
"""
    
    rls_policies = """
-- Включение Row Level Security (опционально)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE deliveries ENABLE ROW LEVEL SECURITY;

-- Политики доступа (разрешить все операции для анонимного ключа)
CREATE POLICY "Allow all operations on users" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on deliveries" ON deliveries FOR ALL USING (true) WITH CHECK (true);
"""
    
    print("\n1. Создание таблицы пользователей:")
    print(users_table)
    print("\n2. Создание таблицы доставок:")
    print(deliveries_table)
    print("\n3. Настройка политик безопасности:")
    print(rls_policies)
    print("="*80)
    print("\nИнструкция:")
    print("1. Откройте https://app.supabase.com")
    print("2. Выберите ваш проект")
    print("3. Перейдите в SQL Editor")
    print("4. Скопируйте и выполните каждый SQL-блок выше")
    print("5. После выполнения запустите приложение командой: python main.py")
    print("\nПосле создания таблиц вы сможете зарегистрироваться в системе!")

if __name__ == '__main__':
    init_database()
