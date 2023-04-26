import mysql.connector

class Database:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor(prepared=True)
        self.make_table()
        print('Database listening on {}:{}'.format(self.host, 3306))

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_account(self):
        query = "INSERT INTO accounts (balance) VALUES (%s)"
        values = (0.0,)
        self.execute_query(query, values)
        return self.cursor.lastrowid
    
    def account_exists(self, account_id):
        query = "SELECT COUNT(*) FROM accounts WHERE id = %s"
        values = (account_id,)
        result = self.execute_query(query, values)
        return result[0][0] > 0
    
    def get_account_balance(self, account_id):
        query = "SELECT balance FROM accounts WHERE id = %s"
        values = (account_id,)
        result = self.execute_query(query, values)
        if result:
            return result[0][0]
        else:
            return None

    def update_account_balance(self, account_id, amount):
        query = "UPDATE accounts SET balance = %s WHERE id = %s"
        values = (amount, account_id)
        self.execute_query(query, values)

    def delete_account(self, account_id):
        query = "DELETE FROM accounts WHERE id = %s"
        values = (account_id,)
        self.execute_query(query, values)

    def execute_query(self, query, values=None):
      try:
          self.cursor.execute(query, values)
          if query.startswith("SELECT"):
              return self.cursor.fetchall()
          else:
              self.connection.commit()
              return None

      except mysql.connector.Error as err:
          print('Error: '+ err.msg)

    def account_is_empty(self, account_id):
      balance = self.get_account_balance(account_id)
      return balance == 0

    def make_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, balance DECIMAL(10, 2) NOT NULL DEFAULT '0.00')")