# appsilon-movie-list


## Highlights

- This is a OA project for Appsilon.
- Flask/Flask-appbuilder
- SQLite
- fetch film data from wikidata
- simple UI
- CURD opperations


## Setup

```bash
# clone this repo
git clone git@github.com:paupaulchen/appsilon-movie-list.git

# install requirements (recommend using virtual environment)
pip install -r requirements.txt

# flask app env variale
export FLASK_APP=app

# Create an admin user
flask fab create-admin

# inject film data to sqlite
flask inject-data

# run dev server
flask run
```

## Usage

- open browser at `http://127.0.0.1:5000`
- login using admin account created earlier
- navigate to 'My FilmView' on top menu to see movie lists
- support sort, search, and edit


