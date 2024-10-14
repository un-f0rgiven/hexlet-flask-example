from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
import os


app = Flask(__name__)
app.secret_key = 'my_secret_key'
users_file = 'users.json'


def load_users():
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                return json.loads(f.read())
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading users: {e}")
            return []
    return []

def save_users(users):
    with open(users_file, 'w') as f:
        f.write(json.dumps(users, indent=4))


users = load_users()

@app.route('/')
def index():
    return 'Some text...'


@app.route('/users/', methods=['GET', 'POST'])
def users_index():
    query = request.args.get('query')
    if query:
        filtered_users = [user for user in users if query.lower() in user['name'].lower()]
    else:
        filtered_users = users
        
    messages = get_flashed_messages(with_categories=True)

    return render_template('users/index.html', users=filtered_users, search=query)


@app.route('/users/new', methods=['GET', 'POST'])
def users_post():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            return 'Не заполнены поля', 400
        
        # Генерируем ID (в данном случае просто длина списка + 1)
        user_id = len(users) + 1
        
        # Создаем нового пользователя и добавляем в список
        new_user = {'id': user_id, 'name': name, 'email': email}
        users.append(new_user)

        save_users(users)
        
        # Перенаправляем на страницу списка пользователей
        flash('Новый пользователь успешно добавлен', 'success')
        return redirect(url_for('users_index'))

    # Если GET, отображаем форму
    return render_template('users/new.html')
