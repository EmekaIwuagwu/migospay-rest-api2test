from app import app
#from flaskext.mysql import MySQL

from flask_mysqldb import MySQL


app.config['MYSQL_USER'] = 'b0c05c7f88b25e'
app.config['MYSQL_PASSWORD'] = '05eb472c'
app.config['MYSQL_DB'] = 'heroku_a25ce4620e787f6'
app.config['MYSQL_HOST'] = 'eu-cdbr-west-03.cleardb.net'

mysql = MySQL(app)

#mysql.init_app(app)
