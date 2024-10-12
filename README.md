
# **Project Documentation**

## **Table of Contents:**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [CLI Usage](#cli-usage)
    - [Connecting to a Database](#connecting-to-a-database)
    - [Creating Tables](#creating-tables)
    - [Inserting Data](#inserting-data)
    - [Updating and Deleting Data](#updating-and-deleting-data)
    - [Viewing Data](#viewing-data)
    - [Backup and Restore](#backup-and-restore)
4. [Code Structure](#code-structure)
    - [Main Files Explanation](#main-files-explanation)
5. [Configuration](#configuration)
6. [Running Tests](#running-tests)

---

## **1. Introduction:**
This project provides a database management tool via a command-line interface (CLI) and a **Flask** web application for user interaction. It allows creating and managing tables, inserting, updating, and deleting data, as well as executing raw SQL queries. It also includes **backup and restore** features to ensure data security.

---

## **2. Installation:**
### **Prerequisites:**
- **Python 3.8+**

- **pip** installed

- SQLAlchemy

- Flask

- PyMySQL

- Boto3

- Click

- Python-dotenv

-  Alembic

### **Installation Steps:**
1. Clone the Git repository:
   ```bash
   git clone https://github.com/LoukaNoves/Backpy.git
   cd your-repo
   ```

2. Install the Python dependencies using pip:
   ```bash
   pip install -r bckclirqrmnts.cmd
   ```

3. Ensure your database is accessible using the configuration information in the `configbackcli.json` file.

4. Start the **Flask** application to test the routes:
   ```bash
   python app.py
   ```

---

## **3. CLI Usage:**
The **CLI** tool allows you to manage your database directly from the terminal. Below is a list of the main commands.

### **3.1 Connecting to a Database:**
To connect to a remote database:
```bash
python backcli.py connect <IP> --port=<port> --username=<user> --password
```
Example:
```bash
python backcli.py connect 192.168.1.100 --port=3306 --username=root --password
```
This will establish a connection to a remote database.

### **3.2 Creating Tables:**
You can create a new table by specifying its name and its columns with their types:
```bash
python backcli.py create_table <table_name> --columns "<column:type, column:type>"
```
Example:
```bash
python backcli.py create_table users --columns "id:INTEGER, name:VARCHAR(100), email:VARCHAR(100)"
```

### **3.3 Inserting Data:**
To insert data into a table:
```bash
python backcli.py insert_data <table_name> --values "column=value, column=value"
```
Example:
```bash
python backcli.py insert_data users --values "id=1, name='John Doe', email='john@example.com'"
```

### **3.4 Updating and Deleting Data:**
- **Updating**:
  ```bash
  python backcli.py update_data <table_name> --set "column=new_value" --where "column=value"
  ```
  Example:
  ```bash
  python backcli.py update_data users --set "name='Jane Doe'" --where "id=1"
  ```

- **Deleting**:
  ```bash
  python backcli.py delete_data <table_name> --where "column=value"
  ```
  Example:
  ```bash
  python backcli.py delete_data users --where "id=1"
  ```

### **3.5 Viewing Data:**
- **Listing tables**:
  ```bash
  python backcli.py list_tables
  ```
- **Displaying data from a table**:
  ```bash
  python backcli.py show_data <table_name>
  ```
  Example:
  ```bash
  python backcli.py show_data users
  ```

### **3.6 Backup and Restore:**
- **Backing up the database**:
  ```bash
  python backcli.py backup
  ```

- **Restoring from a backup**:
  ```bash
  python backcli.py restore <backup_file.sql>
  ```

---

## **4. Code Structure:**
### **4.1 Project Architecture:**
```
example_project/
│
├── app.py                 # Flask entry point
├── backcli.py                 # CLI tool for database management
├── configbackcli.json            # Database configuration file
├── routes/                # Flask routes management
│   ├── __init__.py
│   ├── user_routes.py
│   └── static_routes.py
├── services/              # Services for database and cloud storage
│   ├── __init__.py
│   ├── database_service.py
│   └── cloud_storage_service.py
└── utils/                 # Utility tools
    ├── __init__.py
    ├── error_handler.py
    └── input_validator.py
```

### **4.2 Main Files Explanation:**

- **`app.py`**: Flask application entry point. Handles initialization and registration of routes and services.
- **`backcli.py`**: CLI file that contains all the commands for database management.
- **`configbackcli.json`**: Configuration file with database and cloud access information.
- **`routes/`**: Folder containing Flask routes, such as user routes or static routes.
- **`services/`**: Database management services and cloud storage (AWS S3 in this case).
- **`utils/`**: Utility folder for error handling and input validation.

---

## **5. Configuration:**

The `configbackcli.json` file is used to define the database parameters and AWS configuration information for cloud storage.

Example `configbackcli.json` file:
```json
{
  "database": "sqlite:///example.db",
  "debug": true,
  "aws_access_key": "your_aws_access_key",
  "aws_secret_key": "your_aws_secret_key",
  "bucket_name": "your_bucket_name"
}
```

- **`database`**: The SQLAlchemy connection string to your database (e.g., `sqlite:///example.db`).
- **`aws_access_key` and `aws_secret_key`**: Access information for AWS S3 if you are using cloud storage.
- **`bucket_name`**: S3 bucket name for storing your files.

---

## **6. Running Tests:**

### **Testing Flask Routes:**

You can test the Flask application using a tool like **Postman** or **curl**.

Example **curl** command to test routes:
```bash
curl -X GET http://localhost:8080/user/JohnDoe
```

### **Testing the CLI:**

Test each CLI functionality by running the corresponding commands in your terminal. Check the logs for any errors and ensure that data is being inserted, updated, or deleted correctly in your database.

---

### **Conclusion:**

This project provides a comprehensive set of tools for database management through a command-line interface (CLI) and a Flask web interface. The modular code structure makes adding new features simple and straightforward. You can easily deploy and customize it according to your needs.
