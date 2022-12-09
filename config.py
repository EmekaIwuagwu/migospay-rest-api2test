from app import app
#from flaskext.mysql import MySQL

from flask_mysqldb import MySQL


app.config['MYSQL_USER'] = 'b6cf5c996b7e5e'
app.config['MYSQL_PASSWORD'] = '46d6dbe5'
app.config['MYSQL_DB'] = 'heroku_61e683edf0d1de4'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'

mysql = MySQL(app)

#mysql.init_app(app)
