# import functools
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash
# from quiz.db import get_db
# from quiz.quiz import ChapterInput, LearningGoalInput

# bp = Blueprint('input', __name__, url_prefix='/input')

# @bp.route('/chapter', methods=['GET', 'POST'])
# def edit_chapter():
#     form = ChapterInput(csrf_enabled=False)
#     db = get_db()
#     if request.method == 'POST':
#         no = form.no.data
#         name = form.name.data

#         try:
#             db.execute(
#                 "INSERT INTO chapter (no, name) VALUES (?, ?)",
#                 (no, name),
#             )
#             db.commit()
        
#         except db.IntegrityError:
#             try:
#                 db.execute(
#                     f"UPDATE chapter SET name='{name}' WHERE no={no}"
#                 )
#                 db.commit()
#             except Exception as e:
#                 print(e)

#     chapters = db.execute(
#         'SELECT no, name FROM chapter ORDER BY no'
#     ).fetchall()

#     return render_template('input.html', form=form, data_list=chapters)


# @bp.route('/learning_goal', methods=['GET', 'POST'])
# def edit_lg():
    
#     db = get_db()
#     form = LearningGoalInput(csrf_enabled=False)

#     chapters = db.execute(
#         'SELECT no FROM chapter ORDER BY no'
#     ).fetchall()
#     chapters = list(map(lambda x: x['no'], chapters))
#     form.chapter_no.choices = chapters

#     if request.method == 'POST':

#         chapter_no = form.chapter_no.data
#         no         = form.no.data
#         desc       = form.description.data

       
#         try:
#             db.execute(
#                 "INSERT INTO learning_goal (chapter_no, no, description) VALUES (?, ?, ?)",
#                 (chapter_no,no, desc),
#             )
#             db.commit()
#         except Exception as e:
#             print('hello2',e)
#             try:
#                 db.execute(
#                     f"UPDATE learning_goal SET description='{desc}' WHERE no={no} AND chapter_no = {chapter_no}"
#                     )
#                 db.commit()
#             except Exception as e:
#                 print('hello', e)
            

#     goals = db.execute(
#         'SELECT * FROM learning_goal'
#     ).fetchall()
#     print(goals)

#     return render_template('input.html', form=form, data_list=goals)