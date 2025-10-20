import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    conn_string = os.environ.get('SUPABASE_URL')
    
    print("Подключение к базе данных Supabase...")
    
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        print("✓ Подключение установлено")
        
        print("\n1. Создание таблицы users...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """)
        
        print("   ✓ Таблица users создана")
        
        print("\n2. Создание таблицы deliveries...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                id BIGSERIAL PRIMARY KEY,
                address TEXT NOT NULL,
                courier VARCHAR(255) NOT NULL,
                recipient VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_deliveries_created ON deliveries(created_at DESC);
        """)
        
        print("   ✓ Таблица deliveries создана")
        
        print("\n3. Настройка политик безопасности...")
        cur.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY;")
        cur.execute("ALTER TABLE deliveries ENABLE ROW LEVEL SECURITY;")
        
        cur.execute("DROP POLICY IF EXISTS \"Allow all operations on users\" ON users;")
        cur.execute("DROP POLICY IF EXISTS \"Allow all operations on deliveries\" ON deliveries;")
        
        cur.execute("""
            CREATE POLICY "Allow all operations on users" ON users 
            FOR ALL USING (true) WITH CHECK (true);
        """)
        
        cur.execute("""
            CREATE POLICY "Allow all operations on deliveries" ON deliveries 
            FOR ALL USING (true) WITH CHECK (true);
        """)
        
        print("   ✓ Политики безопасности настроены")
        
        conn.commit()
        
        print("\n✓✓✓ База данных успешно инициализирована! ✓✓✓")
        print("Теперь вы можете зарегистрироваться в приложении!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Ошибка при создании таблиц: {str(e)}")
        raise

if __name__ == '__main__':
    setup_database()
