"""
Performs post-processing on a Question.
1. Translates the english text for a question and the associated choices to various target languages.
2. Generates additional context/information for a question.
"""

from database import fetch_question, update_column_value, fetch_question_answers
from translate import translate
from information import information


def post_process(question_id: int):
    """
    The function translates the english text for a question and the associated choices to various target languages.

    In addition, it update the question row in the database and sets the translated text. Thus it assumes that proper columns exist.

    Similarly, it generates information for a question and updates the same in the database.
    """
    print(f"Post processing for {question_id} started.")
    question = fetch_question(question_id)
    if question == {}:
        print("Invalid question id")
        return
    if question['question_hindi'] is None:
        print(f"Hindi translation for {question['question']} not available. Performing translation")
        hindi_text = translate(question['question'])
        update_column_value('questions', question_id, 'question_hindi', hindi_text)
    answers = fetch_question_answers(question_id)
    for answer in answers:
        if answer['answer_hindi'] is None:
            print(f"Hindi translation for {answer['answer']} not available. Performing translation")
            hindi_text = translate(answer['answer'])
            update_column_value('answers', answer['id'], 'answer_hindi', hindi_text)
    if question['question_telugu'] is None:
        print(f"Telugu translation for {question['question']} not available. Performing translation")
        telugu_text = translate(question['question'], translate_to='Telugu')
        update_column_value('questions', question_id, 'question_telugu', telugu_text)
    for answer in answers:
        if answer['answer_telugu'] is None:
            print(f"Telugu translation for {answer['answer']} not available. Performing translation")
            telugu_text = translate(answer['answer'], translate_to='Telugu')
            update_column_value('answers', answer['id'], 'answer_telugu', telugu_text)

    if question['information'] is None:
        information_text = information(question['question'])
        update_column_value('questions', question_id, 'information', information_text)
    print(f"Post processing for {question_id} completed.")
