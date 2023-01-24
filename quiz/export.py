from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .forms import ExportSettings
from .etc import add_chapters_session, get_items, resolve_chapters
from .selector import DoesNotComputeExeption, generate_LaTeX
from .myDataclasses import Settings
bp = Blueprint('export', __name__, url_prefix='/export')


@bp.get('/')
def index():
    session['items'] = get_items('all')

    form = ExportSettings()
    form.chapters.default = f'{session["chapters"][0]["no"]}-{session["chapters"][-1]["no"]}'
    form.no_items.default = len(session['items'])        
    form.process()
    return render_template('export.html', form=form)


@bp.post('/')
def generate():
    form = ExportSettings()
    if form.validate_on_submit():
        s = Settings(
            no_items=form.no_items.data,
            chapters=resolve_chapters(form.chapters.data),
            max_per_chapter=form.max_per_chapter.data,
            ordered=form.ordered.data
        )
        try:
            session['latex'] = generate_LaTeX(s)
        except DoesNotComputeExeption:
            pass
    return redirect(url_for(f'{__name__.split(".")[-1]}.index'))


@bp.before_request
def ensure_chapters_menu():
    add_chapters_session()
  





