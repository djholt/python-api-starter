from bottle import get, hook, post, request, response, run
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db_con = sqlite3.connect("movies.db")
db_con.row_factory = dict_factory
db_cur = db_con.cursor()

@get("/api/movies", method=['GET', 'OPTIONS'])
def get_movies():
    if request.method == 'OPTIONS':
        return {}
    search = request.query.search
    if search:
        db_cur.execute("SELECT id, name FROM movies WHERE name LIKE ?", ["%"+search+"%"])
    else:
        db_cur.execute("SELECT id, name FROM movies")
    movies = db_cur.fetchall()
    return { "movies": movies }

@get("/api/movies/<movie_id>")
def get_movie(movie_id):
    db_cur.execute("SELECT * FROM movies WHERE id = ?", [movie_id])
    movie = db_cur.fetchone()
    return movie

@post("/api/movies")
def create_movie():
    movie = request.json
    db_cur.execute("INSERT INTO movies (name, rating, release_date, poster_url) VALUES (?, ?, ?, ?)", [movie["name"], movie["rating"], movie["release_date"], movie["poster_url"]])
    db_con.commit()
    return "success"

@hook('after_request')
def set_headers():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

run(host="localhost", port=8080)

db_con.close()
