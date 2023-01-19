from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('rdfquiz', __name__, url_prefix='/edit')


@bp.route('/chapters', methods=('GET', 'POST'))
def edit_chapters():
    pass



@bp.route('/goals', methods=('GET', 'POST'))
def edit_goals():
    pass


@bp.route('/goals', methods=('GET', 'POST'))
def edit_goals():
    pass
