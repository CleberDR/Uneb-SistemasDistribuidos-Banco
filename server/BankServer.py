import socket
import json
import threading
from decimal import Decimal

class BankServer:
    def __init__(self, address, port, database):
        self.database = database
        self.database.connect()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((address, port))
        self.server.listen(1)
        print('Bank server listening on {}:{}'.format(address, port))

    def handle_transaction(self, transaction):
      operation = transaction['operation']
      if operation == "create_account":
          return self.create_account()
      
      account_id = transaction['account_id']

      if not self.database.account_exists(account_id):
        return 'Conta inválida'

      if operation == "transfer":
          to_account = transaction['destiny_account_id']
          if not self.database.account_exists(to_account):
            return 'Conta inválida'
          return self.transfer(transaction)
      
      if operation == "withdraw":
          return self.withdraw(transaction)
      
      if operation == "deposit":
          return self.deposit(transaction)
      
      if operation == "balance":
          return self.balance(transaction)
      
      if operation == "close":
          if self.database.account_is_empty(account_id):
              self.database.delete_account(account_id)
              return 'Conta encerrada'
          else:
              return 'Sua conta não pôde ser encerrada, retire todo o saldo'
    
      return 'Operação inválida'

    def deposit(self, transaction):
      account_id = transaction['account_id']
      deposit_amount = Decimal(transaction['amount'])

      account_balance = self.database.get_account_balance(account_id)

      new_balance = account_balance + deposit_amount

      self.database.update_account_balance(account_id, new_balance)

      return f"Depósito realizado. Novo saldo: {new_balance}"   

    def transfer(self, transaction):
        from_account = transaction['account_id']
        to_account = transaction['destiny_account_id']
        transfer_amount = Decimal(transaction['amount'])

        from_account_balance = self.database.get_account_balance(from_account)

        if transfer_amount > from_account_balance:
            return 'Saldo insuficiente'

        new_from_account_balance = from_account_balance - transfer_amount
        new_to_account_balance = self.database.get_account_balance(to_account) + transfer_amount
        self.database.update_account_balance(from_account, new_from_account_balance)
        self.database.update_account_balance(to_account, new_to_account_balance)

        return 'Transferência realizada com sucesso'

    def withdraw(self, transaction):
        account_balance = self.database.get_account_balance(transaction['account_id'])

        transaction_amount = Decimal(transaction['amount'])
        if transaction_amount > account_balance:
            return 'Saldo insuficiente'
        new_balance = account_balance - transaction_amount

        self.database.update_account_balance(transaction['account_id'], new_balance)

        return f"Saque realizado. Novo saldo: {new_balance}"

    def balance(self, transaction):
        account_balance = self.database.get_account_balance(transaction['account_id'])
        print(account_balance)
        return f"Saldo da conta {transaction['account_id']}: {account_balance}"

    def create_account(self):
        account_id = self.database.create_account()
        return f"Conta criada com sucesso: {account_id}"

    def serve_client(self, client):
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    break

                transaction = json.loads(data.decode('utf-8'))
                print('Transação: ', transaction)
                response = self.handle_transaction(transaction)
                client.sendall(response.encode())

        except socket.error as e:
            print('Socket error:', e)

        except ValueError as e:
            print('Invalid transaction:', e)

        except Exception as e:
            print('Error:', e)

        finally:
            client.close()

    def serve(self):
      try:
        while True:
            print('Esperando conexão...')
            client, address = self.server.accept()
            print('Cliente conectado: ', address)

            while True:
                print('Esperando conexão...')
                client, address = self.server.accept()
                print('Cliente conectado: ', address)

                client_thread = threading.Thread(target=self.serve_client, args=(client,))
                client_thread.start()

      except KeyboardInterrupt:
        self.database.disconnect()
        self.server.close()
        print('\nBank server stopped.')