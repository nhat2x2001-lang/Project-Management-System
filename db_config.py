import os

# MySQL connection settings for the Project Uno application.
# Default is a dedicated, least-privileged user for the app.
# If you have not created the `project_uno` DB user yet, run the SQL
# commands below as a MySQL administrator (for example, as `root`).
# Example SQL to run in the MySQL client:
#
#   CREATE DATABASE IF NOT EXISTS project_uno;
#   CREATE USER 'project_uno'@'127.0.0.1' IDENTIFIED BY 'ProjectUnoPass!23';
#   CREATE USER 'project_uno'@'localhost' IDENTIFIED BY 'ProjectUnoPass!23';
#   GRANT ALL PRIVILEGES ON project_uno.* TO 'project_uno'@'127.0.0.1';
#   GRANT ALL PRIVILEGES ON project_uno.* TO 'project_uno'@'localhost';
#   FLUSH PRIVILEGES;
#
# Replace the password above with a secure secret in production.
# The values below can also be overridden with environment variables:
#   PROJECT_UNO_DB_HOST, PROJECT_UNO_DB_USER, PROJECT_UNO_DB_PASSWORD, PROJECT_UNO_DB_DATABASE

DB_CONFIG = {
    "host": os.environ.get("PROJECT_UNO_DB_HOST", "127.0.0.1"),
    "user": os.environ.get("PROJECT_UNO_DB_USER", "root"),
    "password": os.environ.get("PROJECT_UNO_DB_PASSWORD", "Rey_244456"),
    "database": os.environ.get("PROJECT_UNO_DB_DATABASE", "project_uno")
}
 