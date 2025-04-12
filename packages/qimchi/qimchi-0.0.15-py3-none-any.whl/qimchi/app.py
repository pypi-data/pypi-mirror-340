"""
Author: Spandan Anupam
Affiliation: Forschungszentrum Jülich GmbH

"""

from dash import Dash
from starlette.applications import Starlette
from starlette.middleware.wsgi import WSGIMiddleware


external_scripts = []
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css",
]

app = Dash(
    __name__,
    assets_folder="./assets",
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    use_pages=True,
    title="Qimchi",
    update_title=None,
    suppress_callback_exceptions=True,
)

"""
Entry point for running the Starlette app with Dash.

"""
server = app.server

asgi_app = Starlette()
asgi_app.mount("/", WSGIMiddleware(server))
