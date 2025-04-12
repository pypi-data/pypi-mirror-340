import mysql.connector
from mysql.connector import Error
import time

class AzureSQLConnection:
    """
    A class to manage a connection to an Azure MySQL Database.

    This class provides methods to establish a connection to an Azure MySQL Database and manage the connection lifecycle,
    including automatic retries for connection attempts.

    Attributes:
        server (str): The server name or IP address of the Azure MySQL Database.
        database (str): The name of the database to connect to.
        user (str): The username for authentication.
        password (str): The password for authentication.
        port (int): The port number for the connection (default is 3306).
        db_connection: The database connection object (initially None).
    """

    def __init__(self, server, user, database, password, port=3306):
        """
        Initializes the AzureSQLConnection with the specified parameters.

        Parameters:
            server (str): The server name or IP address of the Azure MySQL Database.
            user (str): The username for the database connection.
            database (str): The name of the database.
            password (str): The password for the database user.
            port (int, optional): The port for the connection. Defaults to 3306.
        """
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db_connection = None

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establishes a connection to the Azure MySQL Database with retry logic.

        This method attempts to connect to the database up to a specified number of retries. If the connection is
        successful, it returns the connection object; otherwise, it raises an error.

        Parameters:
            max_retries (int, optional): Maximum number of connection attempts. Defaults to 5.
            retry_delay (int, optional): Delay in seconds between retries. Defaults to 5.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection: A connection object to the Azure MySQL Database if successful.

        Raises:
            ConnectionError: If the connection fails after the maximum number of retries.
        """
        if self.db_connection and self.db_connection.is_connected():
            return self.db_connection

        retries = 0
        while retries < max_retries:
            try:
                self.db_connection = mysql.connector.connect(
                    host=self.server,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                if self.db_connection.is_connected():
                    print("Connection to Azure MySQL successful")
                    return self.db_connection

            except Error as e:
                retries += 1
                print(f"Connection failed: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(retry_delay)

        raise ConnectionError(f"Failed to connect to the database after {max_retries} retries.")

    def close_connection(self):
        """
        Closes the database connection if it is open.

        This method ensures that the connection is properly closed and sets the connection object to None.
        """
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            self.db_connection = None
            print("🔌 MySQL connection closed.")
