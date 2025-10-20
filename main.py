import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            return User(user_data['id'], user_data['username'], user_data['email'])
    except Exception as e:
        print(f"Error loading user: {e}")
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = supabase.table('users').select('*').eq('username', username).execute()
            
            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                
                if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                    user = User(user_data['id'], user_data['username'], user_data['email'])
                    login_user(user)
                    flash('Вход выполнен успешно!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Неверное имя пользователя или пароль', 'danger')
            else:
                flash('Неверное имя пользователя или пароль', 'danger')
        except Exception as e:
            flash(f'Ошибка входа: {str(e)}', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')
        
        try:
            existing = supabase.table('users').select('*').eq('username', username).execute()
            if existing.data and len(existing.data) > 0:
                flash('Пользователь с таким именем уже существует', 'danger')
                return render_template('register.html')
            
            existing_email = supabase.table('users').select('*').eq('email', email).execute()
            if existing_email.data and len(existing_email.data) > 0:
                flash('Пользователь с такой почтой уже существует', 'danger')
                return render_template('register.html')
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            response = supabase.table('users').insert({
                'username': username,
                'email': email,
                'password': hashed_password
            }).execute()
            
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Ошибка регистрации: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        response = supabase.table('deliveries').select('*').order('id').execute()
        deliveries = response.data if response.data else []
    except Exception as e:
        flash(f'Ошибка загрузки данных: {str(e)}', 'danger')
        deliveries = []
    
    return render_template('dashboard.html', deliveries=deliveries)

@app.route('/delivery/add', methods=['POST'])
@login_required
def add_delivery():
    try:
        data = {
            'address': request.form.get('address'),
            'courier': request.form.get('courier'),
            'recipient': request.form.get('recipient'),
            'description': request.form.get('description')
        }
        
        supabase.table('deliveries').insert(data).execute()
        flash('Запись добавлена успешно', 'success')
    except Exception as e:
        flash(f'Ошибка добавления: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/delivery/update/<int:id>', methods=['POST'])
@login_required
def update_delivery(id):
    try:
        data = {
            'address': request.form.get('address'),
            'courier': request.form.get('courier'),
            'recipient': request.form.get('recipient'),
            'description': request.form.get('description')
        }
        
        supabase.table('deliveries').update(data).eq('id', id).execute()
        flash('Запись обновлена успешно', 'success')
    except Exception as e:
        flash(f'Ошибка обновления: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/delivery/delete/<int:id>', methods=['POST'])
@login_required
def delete_delivery(id):
    try:
        supabase.table('deliveries').delete().eq('id', id).execute()
        flash('Запись удалена успешно', 'success')
    except Exception as e:
        flash(f'Ошибка удаления: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
