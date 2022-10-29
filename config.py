from app import app
#from flaskext.mysql import MySQL

from flask_mysqldb import MySQL


app.config['MYSQL_USER'] = 'b085c05e849089'
app.config['MYSQL_PASSWORD'] = 'a4f7c93e'
app.config['MYSQL_DB'] = 'migospay'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'

mysql = MySQL(app)

#mysql.init_app(app)
