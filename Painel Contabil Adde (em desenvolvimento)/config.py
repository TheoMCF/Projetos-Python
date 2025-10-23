import sqlite3

# conexão com a db
cn = sqlite3.connect(r'database.db', check_same_thread=False)
cr = cn.cursor()