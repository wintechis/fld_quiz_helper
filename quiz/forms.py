from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError, NumberRange, Regexp, DataRequired
from typing import Dict, Any


class ExportSettings(FlaskForm):
    class Meta:
        csrf = False
    no_items            = IntegerField('# Items', )
    chapters            = StringField('Chapters', description="Example: 1-3,5,9") 
    max_per_chapter     = IntegerField('Max per chapter')
    ordered             = BooleanField('Ordered')
    submit              = SubmitField('Generate')

    # def __init__(self, chapter_range: str, len_items: int,  **kwargs):
    #     super().__init__(**kwargs)
    #     ExportSettings.chapters.default = 
    #     # self.no_items.validators = [DataRequired(), NumberRange(min(1, len_items), len_items)]
    #     # self.chapters.validators = [Regexp('([1-9][0-9]?|[1-9][0-9]?\-[1-9][0-9]?)')]
    #     # self.max_per_chapter     = [DataRequired()]
        


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