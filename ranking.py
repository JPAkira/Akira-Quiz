from flask import render_template, request, redirect, session, flash, url_for
from main import app, db
from banco import UsuarioDao, Usuario

usuario_dao = UsuarioDao(db)

@app.route('/ranking')
def ranking():
    ranking = usuario_dao.buscarranking()
    return render_template('ranking.html', ranking=ranking)