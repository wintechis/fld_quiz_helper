import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from quiz.db import get_db

bp = Blueprint('export', __name__, url_prefix='/export')
