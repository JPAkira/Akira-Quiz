

SQL_USUARIO_POR_ID = 'SELECT id, nome, senha, questao, pontos, email, cpf, codigo from usuario where id = %s'
SQL_USUARIO_POR_EMAIL = 'SELECT id, nome, senha, questao, pontos, email, cpf, codigo from usuario where email = %s'
SQL_CRIA_USUARIO = 'INSERT into usuario (id, nome, senha, questao, pontos, email, cpf, codigo) value (%s, %s, %s, %s, %s, %s, %s, %s)'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET questao=%s, pontos=%s where id = %s'
SQL_ATUALIZASENHA_USUARIO = 'UPDATE usuario SET nome=%s, senha=%s, questao=%s, pontos=%s, email=%s, cpf=%s, codigo=%s where id = %s'
SQL_BUSCA_USUARIOS = 'SELECT id, nome, senha, questao, pontos, email, cpf, codigo from usuario WHERE pontos >= 0 ORDER BY pontos DESC'
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'
SQL_CONFIRMAR_USUARIO = 'UPDATE usuario SET codigo=%s where id = %s'


class Usuario:
    def __init__(self, id, nome, senha, questao, pontos, email, cpf, codigo):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.questao = questao
        self.pontos = pontos
        self.email = email
        self.cpf = cpf
        self.codigo = codigo

def traduz_usuarios(usuarios):
    def cria_usuario_com_tupla(tupla):
        return Usuario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7])

    return list(map(cria_usuario_com_tupla, usuarios))

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7])

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def buscar_por_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_EMAIL, (email,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha, usuario.questao, usuario.pontos, usuario.email, usuario.cpf, usuario.codigo))
        self.__db.connection.commit()
        return usuario

    def atualizar(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.questao, usuario.pontos, usuario.id))
        self.__db.connection.commit()
        return usuario

    def atualizarsenha(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ATUALIZASENHA_USUARIO, (usuario.nome, usuario.senha, usuario.questao, usuario.pontos, usuario.email, usuario.cpf, usuario.id))
        self.__db.connection.commit()
        return usuario

    def buscarranking(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduz_usuarios(cursor.fetchall())
        return usuarios

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_USUARIO, (id,))
        self.__db.connection.commit()

    def confirmar(self, id, codigo):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CONFIRMAR_USUARIO, (codigo, id))
        self.__db.connection.commit()
        return id