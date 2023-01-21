from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError
import rdflib
from typing import List
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import random
import os
from .myDataclasses import Chapter, QuizItem, LearningGoal
from typing import Dict, Any

bp = Blueprint('rdfquiz', __name__, url_prefix='/quiz')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return 'hello me'

@bp.get('/<chapter_no>')
def show_quiz(chapter_no: str):  
    if session.get('chapter_no') != chapter_no:
        session['chapter_no'] = chapter_no
        session['items'] = get_items(chapter_no)

    item = random.choice(session['items'])
    session['current'] = item
    return render_template('rdfquiz.html', form=PopQuiz(), chapter=item['chapter'], quiz_item=item['quiz'], next=Next())

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
        print(g.is_correct, form.isTrue.data, quiz.isTrue)
        return render_template('rdfquiz.html', form=form, chapter=chapter, quiz_item=quiz,next=Next())
    # add flash
    print('next')         
    return redirect(url_for('rdfquiz.show_quiz', chapter_no=chapter_no), 301)


def get_item_cls(dct: Dict[str, Any]) -> QuizItem:
    return QuizItem(dct['statement'], dct['isTrue'], dct['answer'])

def get_chapter_cls(dct: Dict[str, Any]) -> Chapter:
    return Chapter(dct['label'], dct['no']) 

class PopQuiz(FlaskForm):
    class Meta:
        csrf = False
    isTrue = RadioField(choices=[('True', 'True'), ('False', 'False')], validate_choice=False)

class Next(FlaskForm):
    class Meta:
        csrf = False
    submit = SubmitField('Next')

class ChapterInput(FlaskForm):
    no   = IntegerField('Chapter No.')
    name = StringField('Name')

class LearningGoalInput(FlaskForm):
    id          = IntegerField('ID') #, render_kw={'readonly': True})
    chapter_no  = SelectField('Chapter No.')
    no          = IntegerField('Learning Goal No.')
    description = StringField('Description')

class QuizItemInput(FlaskForm):
    id          = IntegerField('ID')
    chapter_no  = SelectField('Chapter No.')
    #lg_no      = SelectField('Learning Goal No.')   
    no          = IntegerField('Item No.')
    statement   = StringField('statement')
    isTrue      = BooleanField('isTrue')
    answer      = StringField('answer')


def get_items(chapter_no: str):
    # load graph
    graph = load_graph('data.ttl')

    query = get_query('get_quizitems.rq')
    # add FILTER statement
    if chapter_no.isnumeric():
        query = replace_placeholder(query, 'chapter_no', chapter_no)
    rst = graph.query(query)

    lst = []
    for row in rst:
        dct =  {k:v.toPython() if v else None for k,v in row.asdict().items()}
        quiz_item = get_item_cls(dct)
        chapter = get_chapter(graph, dct['chapter_no'])
        lst.append({
            'chapter':chapter,
            'quiz': quiz_item}
            )
    return lst

def get_chapter(graph: rdflib.Graph, chapter_no: int) -> Chapter:
    query = get_query('get_chapters.rq')
    query = replace_placeholder(query, 'no', str(chapter_no))
    rst = graph.query(query)
    for row in  rst:
        dct =  {k:v.toPython() if v else None for k,v in row.asdict().items()}
    return get_chapter_cls(dct)

def replace_placeholder(query: str, var: str, value: str) -> str:
    return  query.replace('#PLACEHOLDER', f'FILTER(?{var}={value})')
           
def load_graph(path: str) -> rdflib.Graph:
    return rdflib.Graph().parse(path, format='ttl')
   
def get_query(path: str):
    path = os.path.join('requests', path)
    with open(path, mode='r', encoding='utf8') as f:
        return f.read() 