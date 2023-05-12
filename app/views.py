from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from .models import Human, FilmGenre, Film
from .inject_data import populate_db
from . import appbuilder, db, app


class HumanView(ModelView):
    datamodel = SQLAInterface(Human)
    name = "Create Human"


appbuilder.add_view(
    HumanView,
    "My HumanView",
    icon="fa-folder-open-o",
)


class GenreView(ModelView):
    datamodel = SQLAInterface(FilmGenre)
    name = "Create FilmGenre"


appbuilder.add_view(
    GenreView,
    "My GenreView",
    icon="fa-folder-open-o",
)


class FilmView(ModelView):
    datamodel = SQLAInterface(Film)
    name = "Create Film"
    list_columns = [
        "id",
        "label",
        "description",
        "pubdate",
        "imdbid",
        "duration",
        "uri",
    ]


appbuilder.add_view(
    FilmView,
    "My FilmView",
    icon="fa-folder-open-o",
)


# Application wide 404 error handler
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
