from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'b5bd14e1d764b3'
app.config['MYSQL_DATABASE_PASSWORD'] = '92ab938d'
app.config['MYSQL_DATABASE_DB'] = 'heroku_6e943b69a8f614b'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-06.cleardb.net'
mysql.init_app(app)