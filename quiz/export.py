from flask import (
    Blueprint, flash, render_template, request, session
)
from .forms import ExportSettings
from .etc import add_chapters_session, get_items, resolve_chapters
from .selector import DoesNotComputeExeption, TooFewItemsException, generate_LaTeX
from .myDataclasses import Settings
bp = Blueprint('export', __name__, url_prefix='/export')


@bp.route('/', methods=['GET', 'POST'])
def generate():
    if not session.get('items'):
        session['items'] = get_items('all')
    form = ExportSettings(len(session['items']))
    if request.method == 'POST':
        add_defaults(form)
        #form.add_defaults(session["chapters"][0]["no"],session["chapters"][-1]["no"])
        if form.validate_on_submit():
            s = Settings(
                no_items=form.no_items.data,
                chapters=resolve_chapters(form.chapters.data),
                max_per_chapter=form.max_per_chapter.data,
                ordered=form.ordered.data
            )
            session['latex'] = ''
            try:
                session['latex'] = generate_LaTeX(s)
            #except DoesNotComputeExeption:
            #    flash(f'"# Items" must be greater than "Chapters" times "Max per chapter": {form.no_items.data} > {len(resolve_chapters(form.chapters.data))} x {form.max_per_chapter.data}')
            except (TooFewItemsException, DoesNotComputeExeption) as e:
                flash(e.message)

    return render_template('export.html', form=form)


def add_defaults(form: ExportSettings) -> None:
    if not form.chapters.data:
        form.chapters.data = f'{session["chapters"][0]["no"]}-{session["chapters"][-1]["no"]}'


@bp.before_request
def ensure_chapters_menu():
    add_chapters_session()
  





