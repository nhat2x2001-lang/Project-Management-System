import os
import logging
import mysql.connector
from mysql.connector import Error

from db_config import DB_CONFIG

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Database connection manager for the project_uno MySQL database."""

    def __init__(self, config=None):
        if config is None:
            config = DB_CONFIG

        self.host = config.get("host", "127.0.0.1")
        if self.host == "localhost":
            self.host = "127.0.0.1"
        self.user = config.get("user", "project_uno")
        self.password = config.get("password", "your_password")
        self.database = config.get("database", "project_uno")
        self.connection = None
        self._ensure_database_exists()
        self.connect()
        self._setup_schema()

    def _connection_info(self):
        return f"host={self.host}, user={self.user}, database={self.database}"

    def _get_host_candidates(self):
        hosts = [self.host]
        if self.host == "127.0.0.1":
            hosts.append("localhost")
        elif self.host == "localhost":
            hosts.insert(0, "127.0.0.1")
        return hosts

    def _privilege_instruction(self):
        return (
            "CREATE USER 'project_uno'@'127.0.0.1' IDENTIFIED BY 'YourPassword';\n"
            "CREATE USER 'project_uno'@'localhost' IDENTIFIED BY 'YourPassword';\n"
            "GRANT ALL PRIVILEGES ON project_uno.* TO 'project_uno'@'127.0.0.1';\n"
            "GRANT ALL PRIVILEGES ON project_uno.* TO 'project_uno'@'localhost';\n"
            "FLUSH PRIVILEGES;"
        )

    def _ensure_database_exists(self):
        """Create the database if it does not exist yet."""
        temp_connection = None
        cursor = None
        attempted_passwords = [self.password]
        if self.password == "your_password":
            attempted_passwords.extend(["", None])

        logger.debug("Ensuring database exists: %s", self._connection_info())
        last_exc = None
        for host_value in self._get_host_candidates():
            for password_value in attempted_passwords:
                try:
                    temp_connection = mysql.connector.connect(
                        host=host_value,
                        user=self.user,
                        password=password_value,
                    )
                    cursor = temp_connection.cursor()
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                    temp_connection.commit()
                    if host_value != self.host:
                        logger.info("Database creation succeeded using fallback host %s", host_value)
                    return
                except Error as exc:
                    last_exc = exc
                    if getattr(exc, 'errno', None) == 1045:
                        logger.error(
                            "Access denied for %s@%s while creating database.",
                            self.user,
                            host_value,
                            exc_info=True,
                        )
                    else:
                        logger.exception(
                            "Database creation failed for host=%s, user=%s", host_value, self.user
                        )
                finally:
                    if cursor is not None:
                        cursor.close()
                    if temp_connection is not None and temp_connection.is_connected():
                        temp_connection.close()

        if getattr(last_exc, "errno", None) == 1045:
            raise RuntimeError(
                f"Access denied for user '{self.user}' when creating or accessing database {self.database}. "
                f"Verify that the MySQL user exists and that the password in db_config.py is correct. "
                f"If needed, create the user and grant permissions with:\n{self._privilege_instruction()}\n"
                f"Last error: {last_exc}"
            ) from last_exc

        raise RuntimeError(
            f"Unable to create or access database with {self._connection_info()}. "
            f"Verify MySQL credentials and permissions. Last error: {last_exc}"
        ) from last_exc

    def connect(self):
        """Open a MySQL connection using the configured credentials."""
        attempted_passwords = [self.password]
        if self.password == "your_password":
            attempted_passwords.extend(["", None])

        logger.debug("Connecting to MySQL: %s", self._connection_info())
        last_exc = None
        for host_value in self._get_host_candidates():
            for password_value in attempted_passwords:
                try:
                    self.connection = mysql.connector.connect(
                        host=host_value,
                        user=self.user,
                        password=password_value,
                        database=self.database,
                        autocommit=False,
                    )
                    if host_value != self.host:
                        logger.info("Connected using fallback host %s", host_value)
                    return
                except Error as exc:
                    last_exc = exc
                    if getattr(exc, 'errno', None) == 1045:
                        logger.error(
                            "Access denied for %s@%s during connection.",
                            self.user,
                            host_value,
                            exc_info=True,
                        )
                    else:
                        logger.exception("Connection attempt failed for host=%s, user=%s", host_value, self.user)

        if getattr(last_exc, "errno", None) == 1045:
            raise RuntimeError(
                f"Access denied for user '{self.user}' when connecting to database {self.database}. "
                f"Verify the password in db_config.py and that the MySQL user exists for both '127.0.0.1' and 'localhost'. "
                f"If needed, create the user and grant permissions with:\n{self._privilege_instruction()}\n"
                f"Last error: {last_exc}"
            ) from last_exc

        raise RuntimeError(
            f"Database connection failed for {self._connection_info()}. "
            f"Verify credentials, that the user exists, and that the user has access to the database. Last error: {last_exc}"
        ) from last_exc

    def _setup_schema(self):
        """Create the required tables if they are missing."""
        table_statements = [
            """
            CREATE TABLE IF NOT EXISTS Task (
                TaskID INT AUTO_INCREMENT PRIMARY KEY,
                WBS_Code VARCHAR(50),
                Task_Description VARCHAR(255),
                Duration INT,
                Start DATE,
                Finish DATE,
                Predecessors VARCHAR(100)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Materials (
                MaterialID INT AUTO_INCREMENT PRIMARY KEY,
                Materials VARCHAR(255),
                Quantity INT,
                Unit VARCHAR(50),
                Cost DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Workers (
                WorkerID VARCHAR(20) PRIMARY KEY,
                WorkerName VARCHAR(255),
                Position VARCHAR(100)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS MaterialAssignmentCost (
                ForemanID INT AUTO_INCREMENT PRIMARY KEY,
                Task_Description VARCHAR(255),
                Materials VARCHAR(255),
                Quantity INT,
                Unit VARCHAR(50),
                UnitPrice DECIMAL(10,2),
                BudgetCost DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS MaterialsUsage (
                UsageID INT AUTO_INCREMENT PRIMARY KEY,
                TaskID INT,
                MaterialID INT,
                Materials VARCHAR(255),
                Quantity INT,
                Unit VARCHAR(50),
                Cost DECIMAL(10,2),
                FOREIGN KEY (TaskID) REFERENCES task(TaskID) ON DELETE CASCADE,
                FOREIGN KEY (MaterialID) REFERENCES materials(MaterialID) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS TaskAssignments (
                AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
                TaskID INT,
                WorkerID VARCHAR(20),
                AssignedDate DATE DEFAULT (CURRENT_DATE),
                FOREIGN KEY (TaskID) REFERENCES task(TaskID) ON DELETE CASCADE,
                FOREIGN KEY (WorkerID) REFERENCES workers(WorkerID) ON DELETE CASCADE
            )
            """
        ]

        for statement in table_statements:
            self.execute_query(statement)

    def get_cursor(self):
        """Return an active cursor. Reconnect automatically if needed."""
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None, many=False):
        """Execute a single SQL query or a list of parameterized queries."""
        cursor = self.get_cursor()
        try:
            if many and isinstance(params, list):
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Database operation failed: {exc}") from exc
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Fetch all rows from a SELECT query."""
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as exc:
            raise RuntimeError(f"Database fetch failed: {exc}") from exc
        finally:
            cursor.close()

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
