from app import app
#from flaskext.mysql import MySQL

from flask_mysqldb import MySQL


app.config['MYSQL_USER'] = 'bce595e396ecba'
app.config['MYSQL_PASSWORD'] = '14d18fbb'
app.config['MYSQL_DB'] = 'heroku_7880d8ac0ebd47f'
app.config['MYSQL_HOST'] = 'eu-cdbr-west-03.cleardb.net'

mysql = MySQL(app)

#mysql.init_app(app)
