from flask import render_template, request, redirect, session, flash, url_for
from main import app, db
from banco import UsuarioDao, Usuario
import smtplib
from random import choice

usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    return render_template('index.html')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            if usuario.codigo == '1':
                session['usuario_logado'] = usuario.id
                flash(usuario.nome + ' logou com sucesso!')
                proxima_pagina = request.form['proxima']
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('confirmar'))

    else:
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session['admin_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('login'))

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/cadastro', methods=['POST',])
def cadastro():
    nome = request.form['usuario']
    senha = request.form['senha']
    id = request.form['usuario']
    email = request.form['email']
    cpf = request.form['cpf']

    if len(cpf) != 11:
        flash('CPF INVÁLIDO')
        return redirect(url_for('registrar'))

    char = '0123456789abcdefghijlmnopqrstuwvxz@!QWERTYUIOPASDFGHJKLZXCVBNM'
    passwd = ""
    num_caract = 8
    while len(passwd) != num_caract:
        passwd = passwd + choice(char)
    if len(passwd) == num_caract:
        passwd = passwd

    email_from = "temperoapp1@gmail.com"
    email_to = '{}'.format(email)

    smtp = "smtp.gmail.com"

    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    server.login('akiraquizsuporte@gmail.com', 'tempers153')

    msg = '''
        AkiraQuiz Suporte,

        Seu codigo de verificacao:

        {}


        '''.format(passwd)

    server.sendmail(email_from, email_to, msg)
    server.quit()

    usuario = Usuario(id, nome, senha, questao=0, pontos=0, email=email, cpf=cpf, codigo=passwd)
    usuario_dao.salvar(usuario)
    return redirect(url_for('confirmar',  id=usuario.id))

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')


@app.route('/recuperarsenha', methods=['POST',])
def recuperarsenha():
    email = request.form['email']
    usuario = usuario_dao.buscar_por_email(email)

    email_from = "temperoapp1@gmail.com"
    email_to = '{}'.format(usuario.email)

    smtp = "smtp.gmail.com"

    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    server.login('akiraquizsuporte@gmail.com', 'tempers153')

    char = '0123456789abcdefghijlmnopqrstuwvxz@!QWERTYUIOPASDFGHJKLZXCVBNM'
    passwd = ""
    num_caract = 8
    while len(passwd) != num_caract:
        passwd = passwd + choice(char)
    if len(passwd) == num_caract:
        passwd = passwd

    usuario.senha = passwd

    msg = '''
    AkiraQuiz Suporte,
    
    Foi identificado um pedido de recuperacao de senha
    
    Sua senha  {}
    
    
    
    '''.format(passwd)

    server.sendmail(email_from, email_to, msg)
    server.quit()
    flash('Foi enviado um email para recuperar sua conta')

    usuario = Usuario(usuario.id, usuario.nome, passwd, usuario.questao, usuario.pontos, usuario.email, usuario.cpf)
    usuario_dao.atualizarsenha(usuario)
    return redirect(url_for('login'))

@app.route('/confirmar')
def confirmar():
    return render_template('confirmar.html')

@app.route('/confirmado', methods=['POST',])
def confirmado():
    codigoemail = request.form['senha']
    id = request.form['usuario']

    usuario = usuario_dao.buscar_por_id(id)

    if codigoemail == usuario.codigo:
        codigo = 1
        usuario_dao.confirmar(id, codigo)
    else:
        flash('O codigo que você colocou está incorreto')
        return redirect(url_for('confirmar'))
    return redirect(url_for('login'))





