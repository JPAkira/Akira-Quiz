from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
import os
from banco import UsuarioDao

usuario_dao = UsuarioDao(db)

SQL_JOGO_POR_ID = 'SELECT id, resposta, disciplina from questoes where id = %s'

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

class Questao:
    def __init__(self, resposta, disciplina, id=None):
        self.id = id
        self.resposta = resposta
        self.disciplina = disciplina

class QuestaoDao:
    def __init__(self, db):
        self.__db = db

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        if tupla:
            return Questao(tupla[1], tupla[2], id=tupla[0])

questao_dao = QuestaoDao(db)

@app.route('/jogar')
def jogar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    id = session['usuario_logado']
    usuario = usuario_dao.buscar_por_id(id)
    questao = questao_dao.busca_por_id(usuario.questao)
    if questao == None:
        flash('Acabou as questões, você é god')
        return redirect(url_for('index'))
    id = questao.id
    nome_arquivo = recupera_imagem(id)
    return render_template('jogar.html', questao=questao, nome_arquivo=nome_arquivo, usuario=usuario)

@app.route('/chute', methods=['POST',])
def chute():
    resposta = request.form['resposta']
    id = session['usuario_logado']
    usuario = usuario_dao.buscar_por_id(id)
    questao = questao_dao.busca_por_id(usuario.questao)
    if resposta == questao.resposta:
        usuario.questao = int(usuario.questao)
        usuario.pontos = int(usuario.pontos)
        usuario.pontos += 1
        usuario.questao += 1
        usuario_dao.atualizar(usuario)
        return redirect(url_for('jogar'))
    else:
        usuario.questao = int(usuario.questao)
        usuario.pontos = int(usuario.pontos)
        usuario.pontos -= 1
        usuario.questao += 1
        usuario_dao.atualizar(usuario)
        return redirect(url_for('jogar'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
