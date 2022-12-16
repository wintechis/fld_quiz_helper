from typing import List
from loader import QuizItem




def create_LaTeX(items: List[QuizItem]):
    head = r'''
    \newpage
    \begin{question}{0}{Quiz. Decide whether the following statements are \texttt{true} or \texttt{false}. Each correct answer leads to 1 point. Wrong answers will have no affect.}{}{}{}{}{}
        \begin{solution}
            \textbf{Solution:}
        \end{solution}
        
        \begin{quiz}{1}
    '''
    tail = r'''

        \end{quiz}
    \end{question}
    '''
    return head + add_items(items) + tail



def add_items(items: List[QuizItem]) -> str:
    s = ''
    for item in items:
        s += add_quiz_item(item.statement, item.isTrue, item.goals)
    return s

def add_quiz_item(statement: str, is_true: bool, goals: List[str]) -> str:
    return '\t  ' + r'\quizItem' + bracket_str(repr(statement)[1:-1]) + get_bool_letter(is_true) + bracket_goals(goals) + '\n'

def get_bool_letter(is_true: bool) -> str:
    return bracket_str('T' if is_true else 'F')
   
def bracket_str(s: str) -> str:
    return '{%s}' % s

def bracket_goals(goals: List[str]) -> str:
    # LaTeX template requires always five goal arguments
    s = ''
    for i in range(5):
        if i < len(goals):
            s += bracket_str(goals[i])
        else:
            s += r'{}'
    return s


if __name__ == '__main__':
    a = QuizItem('This is the first statement.', True, ['1.1', '2.2'])
    b = QuizItem('This is the second statement.', False, [])
    latex = create_LaTeX([a,b])
    print(latex)
