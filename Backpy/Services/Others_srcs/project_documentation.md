
# **Documentation du Projet**

## **Table des matières :**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Utilisation du CLI](#utilisation-du-cli)
    - [Se connecter à une base de données](#connexion-à-une-base-de-données)
    - [Création de tables](#création-de-tables)
    - [Insertion de données](#insertion-de-données)
    - [Mise à jour et suppression de données](#mise-à-jour-et-suppression-de-données)
    - [Visualisation des données](#visualisation-des-données)
    - [Sauvegarde et restauration](#sauvegarde-et-restauration)
4. [Structure du code](#structure-du-code)
    - [Explication des principaux fichiers](#explication-des-principaux-fichiers)
5. [Configuration](#configuration)
6. [Exécution des tests](#exécution-des-tests)

---

## **1. Introduction :**
Ce projet propose un outil de gestion de base de données via une interface en ligne de commande (CLI) et une application web en **Flask** pour l'interaction avec les utilisateurs. Il permet de créer et manipuler des tables, d'insérer, modifier, et supprimer des données, ainsi que d'exécuter des requêtes SQL brutes. Il inclut également des fonctionnalités de **sauvegarde et de restauration** pour garantir la sécurité des données.

---

## **2. Installation :**
### **Prérequis :**
- **Python 3.8+**
- **pip** installé

### **Étapes d'installation :**
1. Clonez le dépôt Git :
   ```bash
   git clone https://github.com/votre-compte/votre-repo.git
   cd votre-repo
   ```

2. Installez les dépendances Python via pip :
   ```bash
   pip install -r requirements.txt
   ```

3. Assurez-vous que votre base de données est accessible via les informations de configuration dans le fichier `config.json`.

4. Démarrez l'application **Flask** pour tester les routes :
   ```bash
   python app.py
   ```

---

## **3. Utilisation du CLI :**
L'outil **CLI** vous permet de gérer votre base de données directement depuis le terminal. Voici une liste des commandes principales.

### **3.1 Connexion à une base de données :**
Pour se connecter à une base de données distante :
```bash
python cli.py connect <IP> --port=<port> --username=<user> --password
```
Exemple :
```bash
python cli.py connect 192.168.1.100 --port=3306 --username=root --password
```
Cela vous permettra d'établir une connexion à une base de données distante.

### **3.2 Création de tables :**
Vous pouvez créer une nouvelle table en spécifiant son nom et ses colonnes avec leurs types :
```bash
python cli.py create_table <table_name> --columns "<colonne:type, colonne:type>"
```
Exemple :
```bash
python cli.py create_table users --columns "id:INTEGER, name:VARCHAR(100), email:VARCHAR(100)"
```

### **3.3 Insertion de données :**
Pour insérer des données dans une table :
```bash
python cli.py insert_data <table_name> --values "colonne=valeur, colonne=valeur"
```
Exemple :
```bash
python cli.py insert_data users --values "id=1, name='John Doe', email='john@example.com'"
```

### **3.4 Mise à jour et suppression de données :**
- **Mise à jour** :
  ```bash
  python cli.py update_data <table_name> --set "colonne=nouvelle_valeur" --where "colonne=valeur"
  ```
  Exemple :
  ```bash
  python cli.py update_data users --set "name='Jane Doe'" --where "id=1"
  ```

- **Suppression** :
  ```bash
  python cli.py delete_data <table_name> --where "colonne=valeur"
  ```
  Exemple :
  ```bash
  python cli.py delete_data users --where "id=1"
  ```

### **3.5 Visualisation des données :**
- **Lister les tables** :
  ```bash
  python cli.py list_tables
  ```
- **Afficher les données d'une table** :
  ```bash
  python cli.py show_data <table_name>
  ```
  Exemple :
  ```bash
  python cli.py show_data users
  ```

### **3.6 Sauvegarde et restauration :**
- **Sauvegarde de la base de données** :
  ```bash
  python cli.py backup
  ```

- **Restauration à partir d'une sauvegarde** :
  ```bash
  python cli.py restore <backup_file.sql>
  ```

---

## **4. Structure du code :**
### **4.1 Architecture du projet :**
```
example_project/
│
├── app.py                 # Point d'entrée Flask
├── cli.py                 # Outil CLI pour la gestion de la base de données
├── config.json            # Fichier de configuration pour la base de données
├── routes/                # Gestion des routes Flask
│   ├── __init__.py
│   ├── user_routes.py
│   └── static_routes.py
├── services/              # Services pour la base de données et le stockage en cloud
│   ├── __init__.py
│   ├── database_service.py
│   └── cloud_storage_service.py
└── utils/                 # Outils d'utilitaires
    ├── __init__.py
    ├── error_handler.py
    └── input_validator.py
```

### **4.2 Explication des principaux fichiers :**

- **`app.py`** : Point d'entrée de l'application Flask. Gère l'initialisation et l'enregistrement des routes et services.
- **`cli.py`** : Fichier CLI qui contient toutes les commandes pour la gestion de la base de données.
- **`config.json`** : Fichier de configuration avec les informations de la base de données et des accès au cloud.
- **`routes/`** : Dossier contenant les routes Flask, comme les routes utilisateurs ou les routes statiques.
- **`services/`** : Services de gestion de la base de données et du stockage sur le cloud (AWS S3 dans ce cas).
- **`utils/`** : Dossier utilitaires pour la gestion des erreurs et la validation des entrées.

---

## **5. Configuration :**

Le fichier `config.json` est utilisé pour définir les paramètres de la base de données et les informations de configuration AWS pour le stockage cloud.

Exemple de fichier `config.json` :
```json
{
  "database": "sqlite:///example.db",
  "debug": true,
  "aws_access_key": "your_aws_access_key",
  "aws_secret_key": "your_aws_secret_key",
  "bucket_name": "your_bucket_name"
}
```

- **`database`** : Le lien de connexion SQLAlchemy à votre base de données (ex. : `sqlite:///example.db`).
- **`aws_access_key` et `aws_secret_key`** : Informations d'accès pour AWS S3, si vous utilisez le stockage cloud.
- **`bucket_name`** : Nom du bucket S3 pour stocker vos fichiers.

---

## **6. Exécution des tests :**

### **Test des routes Flask :**

Vous pouvez tester l'application Flask avec un outil comme **Postman** ou **curl**.

Exemple de commande **curl** pour tester les routes :
```bash
curl -X GET http://localhost:8080/user/JohnDoe
```

### **Test du CLI :**

Testez chaque fonctionnalité du CLI en exécutant les commandes correspondantes dans votre terminal. Vérifiez les logs pour toute erreur et assurez-vous que les données sont insérées, mises à jour, ou supprimées correctement dans votre base de données.

---

### **Conclusion :**

Ce projet fournit un ensemble complet d'outils pour la gestion de bases de données via un outil en ligne de commande (CLI) et une interface web Flask. La structure modulaire du code rend l'ajout de nouvelles fonctionnalités simple et direct. Vous pouvez facilement le déployer et le personnaliser en fonction de vos besoins.
