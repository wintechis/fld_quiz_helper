from typing import List
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
import random


from .etc import add_chapters_session, get_items, get_chapter_cls, get_item_cls, resolve_chapters
from .forms import PopQuiz

bp = Blueprint('rdfquiz', __name__, url_prefix='/quiz')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('quiz.html')

@bp.get('/<chapter_no>')
def show_quiz(chapter_no: str):
    if session.get('chapter_no') != chapter_no:
        session['chapter_no'] = chapter_no
        session['items'] = get_items(resolve_chapters(chapter_no))

    item = random.choice(session['items'])
    session['current'] = item
    return render_template('rdfquiz.html', form=PopQuiz(), chapter=item['chapter'], quiz_item=item['quiz'])

@bp.post('/<chapter_no>')
def evaluate_quiz(chapter_no:str):
    form = PopQuiz()
    item = session.get('current')
    if session.get('chapter_no') == chapter_no and item and form.validate_on_submit():
        chapter = get_chapter_cls(item['chapter'])
        quiz = get_item_cls(item['quiz'])
        val = True if form.isTrue.data == 'True' else False
        g.is_correct = True if val ==  bool(quiz.isTrue) else False
        g.answered = 'correct' if g.is_correct else 'wrong'
        return render_template('rdfquiz.html', form=form, chapter=chapter, quiz_item=quiz)

    return redirect(url_for(f'{__name__.split(".")[-1]}.show_quiz', chapter_no=chapter_no), 301)


@bp.before_request
def ensure_chapters_menu():
    add_chapters_session()





           
