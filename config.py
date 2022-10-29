from app import app
#from flaskext.mysql import MySQL

from flask_mysqldb import MySQL


app.config['MYSQL_USER'] = 'bbc7c2522deece'
app.config['MYSQL_PASSWORD'] = '8fdba964'
app.config['MYSQL_DB'] = 'migospay'
app.config['MYSQL_HOST'] = 'eu-cdbr-west-03.cleardb.net'

mysql = MySQL(app)

#mysql.init_app(app)
