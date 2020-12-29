from flask import Flask
from flask_mysql_connector import MySQL


app = Flask(__name__)

app.config.from_pyfile('config.py')
db = MySQL(app)

from index import *
from jogar import *
from ranking import *
from erros import *
from perfil import *

'''
db = MySQL(app)
'''
if __name__ == '__main__':
    app.run(debug=True)