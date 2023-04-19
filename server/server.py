import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverAddress = ('localhost', 3342)

server.bind(serverAddress)

server.listen(1)

def openAccount(transaction):
    newAccount = {
      "id": transaction['accountId'],
      "amount": 0,
    }
    return  'Conta Criada'

def transfer(transaction):
    return 'Transferencia Realizada'
  

def withdraw(transaction):
    return 'Saque Realizado'

print('Waiting for a connection...')
client, userId = server.accept()

try:
    print('Connection from', userId)

    while True:
        data = client.recv(1024)
        if data:
            response = ""
            transaction = json.loads(data.decode('utf-8'));
            operation = transaction['operation']

            if operation == "transfer":
                response = transfer(transaction)
            elif operation == "withdraw":
                response = withdraw(transaction)
            elif operation == "openAccount":
                response = openAccount(transaction);
       
            print('Transação recebida:', transaction)
            client.sendall(response.encode())

finally:
    client.close()
    server.close()