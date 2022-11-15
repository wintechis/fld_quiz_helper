from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import ValidationError
from random import randrange
import json


import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from quiz.db import get_db

bp = Blueprint('quiz', __name__, url_prefix='/quiz')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    error = None

    try:
        db.execute(
            "INSERT INTO chapter (no, name) VALUES (?, ?)",
            (1, 'Hypertext, the Internet and the Web'),
        )
        db.commit()
    except db.IntegrityError as e:
        error = str(e)
  
    if error:
        return error
    else:
        return 'okay'



@bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM chapter WHERE no = ?', (1,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'

    if error:
        return 'nope'
    else:
        return json.dumps(dict(user))

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
    lg_no       = SelectField('Learning Goal No.')   
    no          = IntegerField('Item No.')
    question    = StringField('Question')
    answer      = BooleanField('IsTrue')
    explanation = StringField('Explanation')


# render_kw = {'disabled': 'disabled'}