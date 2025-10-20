import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase_helper import normalize_supabase_url

load_dotenv()

supabase_url = normalize_supabase_url(os.environ.get('SUPABASE_URL'))
supabase_key = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)

def create_tables():
    print("Создание таблиц в базе данных Supabase...")
    
    users_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
"""
    
    deliveries_table_sql = """
CREATE TABLE IF NOT EXISTS deliveries (
    id BIGSERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    courier VARCHAR(255) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_deliveries_created ON deliveries(created_at DESC);
"""
    
    rls_sql = """
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE deliveries ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all operations on users" ON users;
DROP POLICY IF EXISTS "Allow all operations on deliveries" ON deliveries;

CREATE POLICY "Allow all operations on users" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on deliveries" ON deliveries FOR ALL USING (true) WITH CHECK (true);
"""
    
    try:
        print("\n1. Создание таблицы users...")
        result = supabase.rpc('exec_sql', {'query': users_table_sql}).execute()
        print("   ✓ Таблица users создана успешно")
        
        print("\n2. Создание таблицы deliveries...")
        result = supabase.rpc('exec_sql', {'query': deliveries_table_sql}).execute()
        print("   ✓ Таблица deliveries создана успешно")
        
        print("\n3. Настройка политик безопасности...")
        result = supabase.rpc('exec_sql', {'query': rls_sql}).execute()
        print("   ✓ Политики безопасности настроены")
        
        print("\n✓ База данных успешно инициализирована!")
        print("Теперь вы можете зарегистрироваться в приложении!")
        
    except Exception as e:
        print(f"\n✗ Ошибка при создании таблиц: {str(e)}")
        print("\nИспользуйте ручной метод:")
        print("Выполните SQL-запросы из файла init_db.py в SQL Editor вашего проекта Supabase")
        print("(запустите: python init_db.py)")

if __name__ == '__main__':
    create_tables()
