from bottle import get, post, request, response, run
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db_con = sqlite3.connect("movies.db")
db_con.row_factory = dict_factory
db_cur = db_con.cursor()

@get("/api/movies")
def get_movies():
    set_headers()
    search = request.query.search
    if search:
        db_cur.execute("SELECT id, name FROM movies WHERE name LIKE ?", ["%"+search+"%"])
    else:
        db_cur.execute("SELECT id, name FROM movies")
    movies = db_cur.fetchall()
    return { "movies": movies }

@get("/api/movies/<movie_id>")
def get_movie(movie_id):
    set_headers()
    db_cur.execute("SELECT * FROM movies WHERE id = ?", [movie_id])
    movie = db_cur.fetchone()
    return movie

@post("/api/movies")
def create_movie():
    set_headers()
    movie = request.forms
    db_cur.execute("INSERT INTO movies (name, rating, release_date, poster_url) VALUES (?, ?, ?, ?)", [movie["name"], movie["rating"], movie["release_date"], movie["poster_url"]])
    db_con.commit()
    return "success"

def set_headers():
    response.set_header("Access-Control-Allow-Origin", "*")

run(host="localhost", port=8080)

db_con.close()
