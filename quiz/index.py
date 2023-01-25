from flask import (
    Blueprint, render_template, send_from_directory
)
from .etc import add_chapters_session
import os
bp = Blueprint('index', __name__, url_prefix='/')


@bp.get('/')
def index():
    return render_template('index.html')


@bp.get('/data.ttl')
def download():
    return send_from_directory(os.curdir, 'data.ttl',)


@bp.before_request
def ensure_chapters_menu():
    add_chapters_session()


