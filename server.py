from bottle import get, request, run
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db_con = sqlite3.connect("movies.db")
db_con.row_factory = dict_factory
db_cur = db_con.cursor()

# TODO: Make an API! Put your Bottle callback functions here.

run(host="localhost", port=8080)

db_con.close()
