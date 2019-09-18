from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.secret_key = 'diego'
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Products

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario('diego', 'Diego', '123456')
usuario2 = Usuario('eu', 'Eu', '1234')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2}

#Index
@app.route('/')
def index():
    products = None
    try:
        products = Products.query.all()
        if products == None:
           print("vazio")
        return render_template('lista.html', titulo='Products', products=products)
    except Exception as e:
	    return(str(e))
    return render_template('lista.html', titulo='Products', products=products)

#Novo Usuário
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

#Criar post
@app.route('/criar', methods=['POST'])
def create():
    imagem = request.form['imagem']
    descricao = request.form['descricao']
    valor = request.form['valor']

    try:
        p = Products(imagem, descricao, valor)
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('index'))

    except Exception as e:
        return(str(e)) 

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Senha não está correta!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)