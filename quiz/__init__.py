import os

from flask import Flask
from flask_session import Session
from flask_bootstrap import Bootstrap


from . import export
from . import rdfquiz
from . import index



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_PERMANENT = False,
        SESSION_TYPE = 'filesystem',
    )
    
    Session(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

 
    app.register_blueprint(rdfquiz.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(export.bp)
  

    return app


