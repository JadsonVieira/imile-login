from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = 'uma_chave_muito_secreta_e_complexa'

usuarios = {
    "admin": "98066972",
    "thiago.palos@imile.me": '123456',
    "hugo.fernandes@imile.me": '123456',
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logado'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'HEAD'])  # ✅ Suporte para HEAD
def index():
    if session.get('logado'):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario in usuarios and usuarios[usuario] == senha:
        session['logado'] = True
        session['usuario'] = usuario
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', erro='Usuário ou senha inválidos')

@app.route('/dashboard', methods=['GET', 'HEAD'])  # ✅ Suporte para HEAD
@login_required
def dashboard():
    usuario = session.get('usuario')
    return render_template('dashboard.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
