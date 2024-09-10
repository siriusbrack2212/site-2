from flask import Flask, render_template, request, redirect, url_for, session
import requests
from flask import Flask, render_template, redirect, url_for, session
from home_logic import get_home_data
from client_logic import get_client_data

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# Configurações do Airtable
AIRTABLE_PAT = 'pateTdFbPd08gJnSE.bfaefe12522de2cba6fc5f540ba50f0ae287fe1ecc00c1d664f212d4cd6b249a'
AIRTABLE_BASE_ID = 'appz3pTYMUiZFlyVk'
AIRTABLE_TABLE_NAME = 'Restaurants'
AIRTABLE_ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

def get_user_from_airtable(username):
    headers = {
        'Authorization': f'Bearer {AIRTABLE_PAT}',
        'Content-Type': 'application/json'
    }
    params = {
        'filterByFormula': f'{{Username}}="{username}"'
    }
    response = requests.get(AIRTABLE_ENDPOINT, headers=headers, params=params)
    data = response.json()
    records = data.get('records', [])
    if records:
        return records[0]['fields']
    return None

@app.route('/')
def home():
    if 'username' in session:
        # Chama a função get_home_data para obter os dados da página home
        home_data = get_home_data()

        return render_template(
            'home.html', 
            username=session['username'], 
            message=home_data['message'], 
            tasks=home_data['tasks'], 
            restaurants=home_data['restaurants']
        )

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_from_airtable(username)
        if user and user.get('Password') == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials. Please try again.'

    return render_template('login.html')


@app.route('/generate_link')
def generate_link_route():
    link = generate_link()
    if link:
        return redirect(url_for('client_page'))  # Redireciona para a nova página dos clientes
    else:
        return "O limite de geração de links foi atingido."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)