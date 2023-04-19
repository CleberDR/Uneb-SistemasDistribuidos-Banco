import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3342))

accountId = input("Insira o identificador da sua conta: ")

def openAccount():
    return {
        "operation": "openAccount",
        "accountId": accountId,
    }

def transfer():
    amount = input("Insira a quantidade a ser transferida: ")
    destinyAccountId = input("Insira a conta de destino: ")
    return {
        "operation": "transfer",
        "accountId": accountId,
        "amount": amount,
        "destinyAccountId": destinyAccountId
    }

def withdraw():
    amount = input("Insira a quantidade a ser transferida: ")
    return {
        "operation": "withdraw",
        "accountId": accountId,
        "amount": amount,
    }

try: 
    while True:
        operation = input("Insira a operação: ")

        if operation == "transfer":
          message = transfer()
        elif operation == "withdraw":
          message = withdraw()
        elif operation == "openAccount":
          message = openAccount();
        else:
          print("Operação invalida!")
          client.close()

        client.send(json.dumps(message).encode())

        response = client.recv(1024)
        print(response.decode())
finally:
    client.close()

