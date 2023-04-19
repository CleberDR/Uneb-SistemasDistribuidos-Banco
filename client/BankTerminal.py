import socket
import json

class BankTerminal:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.account_id = input("Insira o identificador da sua conta: ")    
    
    def transfer(self):
        amount = input("Insira o valor a ser transferido: ")
        destiny_account_id = input("Insira a conta de destino: ")
        return {
            "operation": "transfer",
            "accountId": self.account_id,
            "amount": amount,
            "destinyAccountId": destiny_account_id
        }
    
    def withdraw(self):
        amount = input("Insira o valor que deseja sacar: ")
        return {
            "operation": "withdraw",
            "accountId": self.account_id,
            "amount": amount,
        }
    
    def run(self):
        try: 
            while True:
                print('Escolha a operação desejada:\n1 - Saque\n2 - Transferência')
                operation = input("Insira a operação: ")

                if operation == "1":
                    event = self.withdraw()
                elif operation == "2":
                    event = self.transfer()
                else:
                    print("Operação invalida!")
                    self.client.close()

                self.client.send(json.dumps(event).encode())

                response = self.client.recv(1024)
                print(response.decode())
        finally:
            self.client.close()
