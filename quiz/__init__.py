import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#from . import db
#from . import quiz
from . import export
from . import input
from . import rdfquiz
from . import index
from datetime import timedelta


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_PERMANENT = True,
        SESSION_TYPE = 'filesystem',
        PERMANENT_SESSION_LIFETIME= timedelta(hours=1),
        SESSION_FILE_THRESHOLD = 1000 
    #    DATABASE=os.path.join(app.instance_path, 'quiz.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

   

    # db.init_app(app)
    # app.register_blueprint(quiz.bp)
    # app.register_blueprint(input.bp)
    app.register_blueprint(rdfquiz.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(export.bp)
  

    return app


