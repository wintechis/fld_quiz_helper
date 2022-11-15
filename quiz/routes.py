import os
from flask import Flask, render_template, redirect, url_for, flash
from .quiz import PopQuiz
from dataclasses import dataclass
from . import db
    

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='this is a secret key',
        DATABASE=os.path.join(app.instance_path, 'quiz.sqlite'),
    )
print(app.instance_path)
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass




@dataclass
class QuizItem:
    chapter_id: int
    chapter_name: str
    question: str
    answer: bool
    explanation: str
    lg_no: int
    lg_desc: str



@app.get('/')
def overview():
    form = PopQuiz() 
    return render_template('quiz.html', form=form, is_correct='', explanation='', details=details)

@app.post('/')
def wtf_quiz_post():
    explanation = 'Dummy'
    form = PopQuiz() 
    is_correct='right' if form.validate_on_submit() else 'wrong'
    return render_template('quiz.html', form=form, is_correct=is_correct, explanation=explanation, details=details)



@app.get('/quiz/max<int:val>')
def quiz2max(val: int):
    form = PopQuiz() 
    return render_template('quiz.html', form=form, is_correct='', explanation='', details=details)


@app.get('/quiz/min<int:val>')
def quiz_from_min(val: int):
    form = PopQuiz() 
    return render_template('quiz.html', form=form, is_correct='', explanation='', details=details)

@app.get('/quiz/<int:val>')
def quiz_chapter(val: int):
    form = PopQuiz() 
    return render_template('quiz.html', form=form, is_correct='', explanation='', details=details)

@app.route('/passed')
def  passed(): 
    return render_template('passed.html')



if __name__ == '__main__': 
    app.run(debug=True)