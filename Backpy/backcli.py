#!/usr/bin/env python3

import click
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import json
import os

# Charger la configuration depuis config.json
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()
engine = create_engine(config['database'], echo=config.get('debug', False))
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Connexion à une base de données distante
@click.group()
def backcli():
    """Outil CLI pour la gestion de base de données"""
    pass

@backcli.command()
@click.argument('ip')
@click.option('--port', default=3306, help="Port de la base de données")
@click.option('--username', prompt=True, help="Nom d'utilisateur")
@click.option('--password', prompt=True, hide_input=True, help="Mot de passe")
def connect(ip, port, username, password):
    """Se connecter à une base de données distante"""
    url = f"mysql+pymysql://{username}:{password}@{ip}:{port}/"
    global engine
    engine = create_engine(url)
    click.echo(f"Connexion réussie à {ip}:{port}")

# Création de tables
@backcli.command()
@click.argument('table_name')
@click.option('--columns', prompt=True, help="Colonnes sous forme colonne:type (ex: id:INTEGER, name:VARCHAR(100))")
def create_table(table_name, columns):
    """Créer une nouvelle table"""
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
    click.echo(f"Table {table_name} créée avec succès")

# Insertion de données dans une table
@backcli.command()
@click.argument('table_name')
@click.option('--values', prompt=True, help="Valeurs sous forme colonne=valeur (ex: id=1, name='John')")
def insert_data(table_name, values):
    """Insérer des données dans une table"""
    table = Table(table_name, metadata, autoload_with=engine)
    data = {k: v for k, v in [item.split('=') for item in values.split(',')]}
    stmt = table.insert().values(**data)
    session.execute(stmt)
    session.commit()
    click.echo(f"Données insérées dans {table_name}")

# Mise à jour de données
@backcli.command()
@click.argument('table_name')
@click.option('--set', prompt=True, help="Nouvelles valeurs (ex: name='Jane Doe')")
@click.option('--where', prompt=True, help="Condition WHERE (ex: id=1)")
def update_data(table_name, set, where):
    """Mettre à jour des données dans une table"""
    table = Table(table_name, metadata, autoload_with=engine)
    set_data = {k: v for k, v in [item.split('=') for item in set.split(',')]}
    where_cond = {k: v for k, v in [item.split('=') for item in where.split(',')]}
    stmt = table.update().values(**set_data).where(table.c.id == where_cond['id'])
    session.execute(stmt)
    session.commit()
    click.echo(f"Données mises à jour dans {table_name}")

# Suppression de données
@backcli.command()
@click.argument('table_name')
@click.option('--where', prompt=True, help="Condition WHERE (ex: id=1)")
def delete_data(table_name, where):
    """Supprimer des données dans une table"""
    table = Table(table_name, metadata, autoload_with=engine)
    where_cond = {k: v for k, v in [item.split('=') for item in where.split(',')]}
    stmt = table.delete().where(table.c.id == where_cond['id'])
    session.execute(stmt)
    session.commit()
    click.echo(f"Données supprimées dans {table_name}")

# Lister les tables
@backcli.command()
def list_tables():
    """Lister les tables dans la base de données"""
    tables = engine.table_names()
    click.echo(f"Tables : {', '.join(tables)}")

# Afficher les données d'une table
@backcli.command()
@click.argument('table_name')
def show_data(table_name):
    """Afficher les données d'une table"""
    table = Table(table_name, metadata, autoload_with=engine)
    query = session.query(table)
    for row in query:
        click.echo(row)

# Sauvegarde de la base de données
@backcli.command()
def backup():
    """Sauvegarder la base de données dans un fichier SQL"""
    os.system(f"mysqldump -u {config['username']} -p{config['password']} --databases {config['database']} > backup.sql")
    click.echo("Sauvegarde effectuée avec succès")

# Restauration de la base de données
@backcli.command()
@click.argument('backup_file')
def restore(backup_file):
    """Restaurer la base de données à partir d'un fichier SQL"""
    os.system(f"mysql -u {config['username']} -p{config['password']} {config['database']} < {backup_file}")
    click.echo("Base de données restaurée avec succès")

if __name__ == "__main__":
    backcli()
