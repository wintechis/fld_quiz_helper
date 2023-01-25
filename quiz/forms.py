from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError, NumberRange, Regexp, Optional, InputRequired



class ExportSettings(FlaskForm):
    class Meta:
        csrf = False
    no_items            = IntegerField('# Items')
    chapters            = StringField('Chapters') 
    max_per_chapter     = IntegerField('Max per chapter')
    ordered             = BooleanField('Ordered', )
    submit              = SubmitField('Generate')

    def __init__(self, len_items, **kw):
        super().__init__(**kw)
        self.add_validators(len_items)

    def add_validators(self, len_items):
        self.no_items.render_kw = {'min':min(1, len_items ), 'max':len_items}
        self.no_items.validators = [InputRequired()]
        self.max_per_chapter.validators = [InputRequired()]



class PopQuiz(FlaskForm):
    class Meta:
        csrf = False
    isTrue = RadioField(choices=[('True', 'True'), ('False', 'False')], validate_choice=False)




#TODO Add Edit Forms for Dataset
# class ChapterInput(FlaskForm):
#     no   = IntegerField('Chapter No.')
#     name = StringField('Name')

# class LearningGoalInput(FlaskForm):
#     id          = IntegerField('ID') #, render_kw={'readonly': True})
#     chapter_no  = SelectField('Chapter No.')
#     no          = IntegerField('Learning Goal No.')
#     description = StringField('Description')

# class QuizItemInput(FlaskForm):
#     id          = IntegerField('ID')
#     chapter_no  = SelectField('Chapter No.')
#     #lg_no      = SelectField('Learning Goal No.')   
#     no          = IntegerField('Item No.')
#     statement   = StringField('statement')
#     isTrue      = BooleanField('isTrue')
#     answer      = StringField('answer')