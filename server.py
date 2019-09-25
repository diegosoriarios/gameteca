from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.secret_key = 'diego'
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Products, Usuarios

#Index
@app.route('/')
def index():
    products = None
    try:
        products = Products.query.all()
        if products == None:
           print("vazio")
        return render_template('index.html', titulo='Products', products=products)
    except Exception as e:
	    return(str(e))
    return render_template('index.html', titulo='Products', products=products)

#Produtos
@app.route('/produtos')
def produtos():
    products = None
    try:
        products = Products.query.all()
        if products == None:
           print("vazio")
        return render_template('produtos.html', titulo='Products', products=products)
    except Exception as e:
	    return(str(e))
    return render_template('produtos.html', titulo='Products', products=products)

#Novo Usuário
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


#Nova compra
@app.route('/compra/<name>')
def compra(product):
    print(product)
    print('\n AQUI \n')
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('compra')))
    return render_template('compra.html', titulo='Finalizar Compra')

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

#Tela de login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#Tela Acessórios
@app.route('/acessorios')
def acessorios():
    products = None
    try:
        products = Products.query.all()
        if products == None:
           print("vazio")
        return render_template('acessorios.html', titulo='Products', products=products)
    except Exception as e:
	    return(str(e))
    return render_template('acessorios.html', titulo='Products', products=products)

@app.route('/empresa')
def empresa():
    proxima = request.args.get('proxima')
    return render_template('empresa.html', proxima=proxima)

@app.route('/contato')
def contato():
    proxima = request.args.get('proxima')
    return render_template('contato.html', proxima=proxima)

#Checa autenticação
@app.route('/autenticar', methods=['POST'])
def autenticar():

    usuarios = Usuarios.query.all()

    #Procura usuários, se tiver cadastrado loga
    for usuario in usuarios:
        if request.form['email'] == usuario.name:
            if request.form['password'] == usuario.senha:
                session['usuario_logado'] = usuario.name
                flash(usuario.name + ' logou com sucesso!')
                proxima_pagina = request.form['proxima']
                return redirect(proxima_pagina)


    #senão mostra mensagem de erro
    flash('Senha não está correta!')
    return redirect(url_for('login'))

#Logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)