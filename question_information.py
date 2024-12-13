"""
Generates additional context/information for a question.
"""

from database import fetch_question, update_column_value
from information import information


def question_information(question_id: int):
    """
    """
    print(f"Question information for {question_id} started.")
    question = fetch_question(question_id)
    if question == {}:
        print("Invalid question id")
        return
    information_text = information(question['question'])
    update_column_value('questions', question_id, 'information', information_text)
    print(f"Question information for {question_id} completed.")
