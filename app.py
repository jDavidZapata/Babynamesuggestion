import os
from flask import Flask, flash, redirect, render_template, request, session, abort, redirect, url_for, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


app = Flask(__name__)

#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
app.secret_key = b'_3#y2L"F4Q8z\n\xec]/'

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#print(os.environ['APP_SETTINGS'])


db.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, password VARCHAR NOT NULL, email VARCHAR unique)")
db.execute("CREATE TABLE IF NOT EXISTS names (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, user_id INTEGER REFERENCES users(id))")
db.commit()


'''
db.execute("INSERT INTO users (name, password, email) VALUES ('dave', 'dave', 'd@d')")
db.commit()

db.execute("INSERT INTO names (name, user_id) VALUES ('cataleyah, 1)",
db.commit()
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    names = {}
    names = db.execute(    
            'SELECT name, count(*) FROM names GROUP BY name ORDER BY count(*) DESC'
        ).fetchall()
    print(names)

    user_id = 1

    '''
    user_id = session.get('user_id')
        
    if ('user_id' in session):

        g.user = db.execute(    
            'SELECT * FROM users WHERE id = :id', {"id": user_id,}
        ).fetchone()
        #return render_template("index.html")
    '''

    if request.method == "POST":
        # get name that the user has entered
        name = (request.form['name']).capitalize()
                    
        db.execute("INSERT INTO names (name, user_id) VALUES (:name, :user_id)",
            {"name": name, "user_id": user_id})
        db.commit()
                    
        """Store the user id in a new session and return to the index"""

        names = db.execute('SELECT name FROM names').fetchall()
                    
        return redirect(url_for('index', errors=errors, names=names))
            
    return render_template('index.html', errors=errors, names=names)
       
@app.route('/<name>', methods=['GET', 'POST'])
def search(name):
    errors = []
    
    if request.method == "POST":
        name = (request.form['name']).lower()
        # list of links to stick name into
        print(name)
    
    return render_template('search.html', errors=errors, name=name)
    



if __name__ == '__main__':
    app.run()