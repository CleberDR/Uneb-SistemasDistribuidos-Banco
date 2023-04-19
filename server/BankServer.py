import socket
import json

class BankServer:
    def __init__(self, address, port, database):
        self.database = database
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((address, port))
        self.server.listen(1)
        print('Bank server listening on {}:{}'.format(address, port))

    def handle_transaction(self, transaction):
        operation = transaction['operation']
        if operation == "openAccount":
            return self.open_account(transaction)
        elif operation == "transfer":
            return self.transfer(transaction)
        elif operation == "withdraw":
            return self.withdraw(transaction)
        else:
            return 'Operação inválida'

    def open_account(self, transaction):
        new_account = {
            "id": transaction['accountId'],
            "amount": 0,
        }
        return 'Conta criada'

    def transfer(self, transaction):
        return 'Transferência realizada'

    def withdraw(self, transaction):
        return 'Saque realizado'

    def serve(self):
        try:
            while True:
                print('Waiting for a connection...')
                client, address = self.server.accept()
                print('Connection from', address)

                data = client.recv(1024)
                if data:
                    transaction = json.loads(data.decode('utf-8'))
                    response = self.handle_transaction(transaction)
                    client.sendall(response.encode())

                client.close()

        except KeyboardInterrupt:
            self.server.close()
            print('\nBank server stopped.')