#!/usr/bin/env python3

import click
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import json
import os

# Charger la configuration depuis config.json
def load_config():
    with open("configbackcli.json", "r") as f:
        return json.load(f)

config = load_config()
engine = create_engine(config['database'], echo=config.get('debug', False))
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Connexion à une base de données distante
@click.group()
def backcli():
    """CLI tool for database managing"""
    pass

@backcli.command()
@click.argument('ip')
@click.option('--port', default=3306, help="Database port")
@click.option('--username', prompt=True, help="Username")
@click.option('--password', prompt=True, hide_input=True, help="Password")
def connect(ip, port, username, password):
    """Connect to a distant database"""
    url = f"mysql+pymysql://{username}:{password}@{ip}:{port}/"
    global engine
    engine = create_engine(url)
    click.echo(f"Successfully connected to {ip}:{port}")

# Création de tables
@backcli.command()
@click.argument('table_name')
@click.option('--columns', prompt=True, help="Columns under column form:type (ex: id:INTEGER, name:VARCHAR(100))")
def create_table(table_name, columns):
    """Create a new table"""
    columns_def = []
    for col in columns.split(","):
        name, col_type = col.split(":")
        if col_type.upper() == "INTEGER":
            columns_def.append(Column(name.strip(), Integer))
        elif col_type.upper().startswith("VARCHAR"):
            size = int(col_type.split("(")[1].split(")")[0])
            columns_def.append(Column(name.strip(), String(size)))
    
    table = Table(table_name, metadata, *columns_def)
    metadata.create_all(engine)
    click.echo(f"Table{table_name} have been created successfully")

# Inserting datas in a table
@backcli.command()
@click.argument('table_name')
@click.option('--values', prompt=True, help="Values in column form=values (ex: id=1, name='John')")
def insert_data(table_name, values):
    """Insert datas in a table"""
    table = Table(table_name, metadata, autoload_with=engine)
    data = {k: v for k, v in [item.split('=') for item in values.split(',')]}
    stmt = table.insert().values(**data)
    session.execute(stmt)
    session.commit()
    click.echo(f"Datas inserted in table {table_name}")

# Mise à jour de données
@backcli.command()
@click.argument('table_name')
@click.option('--set', prompt=True, help="New values (ex: name='Jane Doe')")
@click.option('--where', prompt=True, help="Condition WHERE (ex: id=1)")
def update_data(table_name, set, where):
    """Update datas in a table"""
    table = Table(table_name, metadata, autoload_with=engine)
    set_data = {k: v for k, v in [item.split('=') for item in set.split(',')]}
    where_cond = {k: v for k, v in [item.split('=') for item in where.split(',')]}
    stmt = table.update().values(**set_data).where(table.c.id == where_cond['id'])
    session.execute(stmt)
    session.commit()
    click.echo(f"Updated datas in table {table_name}")

# Suppression de données
@backcli.command()
@click.argument('table_name')
@click.option('--where', prompt=True, help="Condition WHERE (ex: id=1)")
def delete_data(table_name, where):
    """Delete datas in a table"""
    table = Table(table_name, metadata, autoload_with=engine)
    where_cond = {k: v for k, v in [item.split('=') for item in where.split(',')]}
    stmt = table.delete().where(table.c.id == where_cond['id'])
    session.execute(stmt)
    session.commit()
    click.echo(f"Deleted datas in table {table_name}")

# Lister les tables
@backcli.command()
def list_tables():
    """List tables in a database"""
    tables = engine.table_names()
    click.echo(f"Tables : {', '.join(tables)}")

# Afficher les données d'une table
@backcli.command()
@click.argument('table_name')
def show_data(table_name):
    """Display a table's datas"""
    table = Table(table_name, metadata, autoload_with=engine)
    query = session.query(table)
    for row in query:
        click.echo(row)

# Sauvegarde de la base de données
@backcli.command()
def backup():
    """Save the database in a SQL file"""
    os.system(f"mysqldump -u {config['username']} -p{config['password']} --databases {config['database']} > backup.sql")
    click.echo("The database have been saved successfully")

# Restauration de la base de données
@backcli.command()
@click.argument('backup_file')
def restore(backup_file):
    """Restore databse using SQL file"""
    os.system(f"mysql -u {config['username']} -p{config['password']} {config['database']} < {backup_file}")
    click.echo("Database restored with success")

if __name__ == "__main__":
    backcli()
