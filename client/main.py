import os
from dotenv import load_dotenv
from BankTerminal import BankTerminal

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

client = BankTerminal(HOST, PORT)
client.run()