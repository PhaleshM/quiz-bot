
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]
    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Validate if answer is empty
    if not answer.strip():
        return False, "Answer cannot be empty."

    # Store the answer in the session
    session["answers"] = session.get("answers", {})
    session["answers"][current_question_id] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    try:
        if current_question_id==None:
            current_question_id=0
        next_question_id = current_question_id + 1
        next_question=PYTHON_QUESTION_LIST[next_question_id]["question_text"]+"<br>Options:-"
        options=PYTHON_QUESTION_LIST[next_question_id]["options"]
        for x in options:
            next_question=next_question+"<br>"+str(x)
        next_question=next_question[:-1]
        # print(next_question)
        return next_question, next_question_id
    except IndexError:
        # current_question_id is out of range
        return None, None

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = calculate_score(session)
    return f"Your final score is: {score}"


def calculate_score(session):
    '''
    Calculates the score based on the answers stored in the session.
    '''
    answers = session.get("answers", {})
    correct_answers = [question["answer"] for idx, question in enumerate(PYTHON_QUESTION_LIST) if idx in answers and answers[idx] == question["answer"]]
    return len(correct_answers)