import os
from dotenv import load_dotenv
from BankServer import BankServer
from Database import Database

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

DB_HOST= os.getenv('DB_HOST')
DB_PORT= int(os.getenv('DB_PORT'))
DB_USER= os.getenv('DB_USER')
DB_PASS= os.getenv('DB_PASS')
DB_NAME= os.getenv('DB_NAME')

database = Database(DB_HOST, DB_USER, DB_PASS, DB_NAME)
server = BankServer(HOST, PORT, database)
server.serve()