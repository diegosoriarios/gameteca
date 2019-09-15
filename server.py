from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.secret_key = 'diego'

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://postgres:postgres@localhost/redesII'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#from models import Games
from models.Games import Games

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

jogo1 = Jogo('Super Mario', 'Plataforma', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Ação', 'PS2')
lista = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    try:
        jogos = Games.query.all()
        for jogo in jogos:
            print(jogo)
        to_return = jsonify([e.serialize() for e in jogos])
        return render_template('lista.html', titulo='Jogos', jogos=to_return)
    except Exception as e:
	    return(str(e))
    #return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def create():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    try:
        jogo = Games(
            name=name,
            categoria=categoria,
            console=console
        )
        db.session.add(jogo)
        db.session.commit()

        return redirect(url_for('index'))
    except Exception as e:
        return(str(e)) 

    #jogo = Jogo(nome, categoria, console)
    #lista.append(jogo)
    #return redirect(url_for('index'))


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