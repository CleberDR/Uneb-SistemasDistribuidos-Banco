import socket
import json

class BankTerminal:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.account_id = 0
        self.event = {}

    def create_account(self):
        self.event = {
            "operation": "create_account",
        }
        self.send_event()
    
        
    def transfer(self):
        while True:
            amount = input("Insira o valor a ser transferido: ")
            if amount.replace(".", "", 1).isdigit():
                break
            else:
                print("Valor inválido. Insira apenas números.")

        while True:
            destiny_account_id = input("Insira a conta de destino: ")
            if destiny_account_id.replace(".", "", 1).isdigit():
                break
            else:
                print("Identificador inválido. Insira apenas números.")

        return {
            "operation": "transfer",
            "account_id": self.account_id,
            "amount": amount,
            "destiny_account_id": destiny_account_id
        }
    
    def withdraw(self):
        while True:
            amount = input("Insira o valor que deseja sacar: ")
            if amount.replace(".", "", 1).isdigit():
                break
            else:
                print("Valor inválido. Insira apenas números.")

        return {
            "operation": "withdraw",
            "account_id": self.account_id,
            "amount": amount,
        }
    
    def deposit(self):
      while True:
          amount = input("Insira o valor a ser depositado: ")
          if amount.replace(".", "", 1).isdigit():
              break
          else:
              print("Valor inválido. Insira apenas números.")

      return {
          "operation": "deposit",
          "account_id": self.account_id,
          "amount": amount,
      }
    
    def balance(self):
      return {
          "operation": "balance",
          "account_id": self.account_id,
      }
    
    def close(self):
      return {
          "operation": "close",
          "account_id": self.account_id,
      }
    
    def send_event(self):
        self.client.send(json.dumps(self.event).encode())
        response = self.client.recv(1024)
        print(response.decode())

    def run(self):
        try: 
            has_account = input('Você já tem uma conta? S/N: ')
            if has_account.lower() == 'n':
                self.event = self.create_account()
            while True:
                self.account_id = input("Insira o número da sua conta: ")
      
                print('1 - Saque\n2 - Transferência\n3 - Depósito\n4 - Saldo\n5 - Encerrar Conta\n')
                operation = input("Escolha a operação desejada: ")

                if operation == "1":
                    self.event = self.withdraw()
                elif operation == "2":
                    self.event = self.transfer()
                elif operation == "3":
                    self.event = self.deposit()
                elif operation == "4":
                    self.event = self.balance()
                elif operation == "5":
                    self.event = self.close()
                else:
                    print("Operação inválida!")
                    self.client.close()
                    return
                
                self.send_event()

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
        finally:
            self.client.close()