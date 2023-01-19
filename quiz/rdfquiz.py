from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import ValidationError
import rdflib
from dataclasses import dataclass
from typing import List
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import random

bp = Blueprint('rdfquiz', __name__, url_prefix='/quiz')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return 'hello me'

@bp.route('/<chapter_no>', methods=('GET', 'POST'))
def show_quiz(chapter_no: str):
    form = QuizItemInput()
  
    # load data

    graph = load_data('data.ttl')

    # get query
  
    query = get_query('requests/get_quizitems.rq')

    # add FILTER statement
    if chapter_no.isnumeric():
        query = query.replace('#PLACEHOLDER', f'FILTER(?chapter_no={chapter_no})')
    
    
    rst = graph.query(query)

    session['items'] = []
    for row in rst:
        dct =  {k:v.toPython() if v else None for k,v in row.asdict().items()}

        query = get_query('requests/get_chapters.rq')
        query = query.replace('#PLACEHOLDER', f'FILTER(?no={dct["chapter_no"]})')
        chapter_rst = graph.query(query)
        for crow in chapter_rst:
            cdct =  {k:v.toPython() if v else None for k,v in crow.asdict().items()}

        chapter = Chapter(cdct['label'], cdct['no'])   # ?label ?no 

        quiz_item = QuizItem(dct['statement'], dct['isTrue'], dct['answer'])  # ?statement ?isTrue ?answer ?no ?chapter_no
        
        session['items'].append((chapter, quiz_item))

    
    c,q = random.choice(session['items'])
    session['current'] = (c,q)
    return render_template('rdfquiz.html', form=form, chapter=c, quiz_item=q)

           
   

def load_data(path: str) -> rdflib.Graph:
    g = rdflib.Graph()
    try:
        return g.parse('data.ttl', format='ttl')
    except Exception:
        return g
    

def get_query(path: str):
    try:
        with open(path, mode='r', encoding='utf8') as f:
            return f.read() 
    except Exception:
        return ''

class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
            message = 'Incorrect answer.'
            if field.data != self.answer:
                raise ValidationError(message)


class PopQuiz(FlaskForm):
    class Meta:
        csrf = False
    q1 = RadioField("The answer to question one is False.",
                    choices=[('True', 'True'), ('False', 'False')],
                    validators=[CorrectAnswer('False')]
                    )

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


@dataclass
class QuizItem:
    statement: str
    isTrue: bool
   # goals: List[str]
    answer: str=''

@dataclass
class Chapter:
    title: str
    no: int

@dataclass
class LearningGoal:
    chapter_no: int
    no: int
    description: str