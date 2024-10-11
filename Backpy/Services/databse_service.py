from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def backup_database():
    with db.engine.connext() as coon :
        conn.execute("CREATE DATABASE IF NOT EXISTS backup_db")
        conn.execute("USE backup_db")
        conn.execute("SET FOREIGN_KEY_CHECKS=0")
        conn.execute("SELECT * INTO OUTFILE '/tmp/backup_db.sql' FROM example_db")
        conn.execute("SET FOREIGN_KEY_CHECKS=1")