from flask import render_template, session
from main import app, db
from banco import UsuarioDao

usuario_dao = UsuarioDao(db)

@app.route('/perfil')
def perfil():

    id = session['usuario_logado']

    usuario = usuario_dao.buscar_por_id(id)

    return render_template('perfil.html', usuario=usuario)