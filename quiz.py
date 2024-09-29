# import flask
# from flask import Flask, request, jsonify
# from Question import questions  

# quiz_app = Flask(__name__)

# # Endpoint to get all questions
# @quiz_app.route('/api/questions', methods=['GET'])
# def get_question():
#     return jsonify(questions)

# # Endpoint to submit an answer
# @quiz_app.route('/api/submit', methods=['POST'])
# def answer_submit():
#     data = request.json
#     question_id = data.get("id")  # Get the question ID
#     selected_option = data.get("option")  # Get the selected option index (0-based)

#     # Find the question by its ID
#     question = next((q for q in questions if q["id"] == question_id), None)

#     if not question:
#         return jsonify({"message": "Question not found"}), 404

#     # Check if the selected option is correct
#     if question["answer"] == selected_option:
#         return jsonify({"message": "Right!"})
#     else:
#         correct_option = question["answer"]
#         return jsonify({
#             "message": "Wrong!",
#             "correct_answer": question["options"][correct_option]
#         })


# if __name__ == "__main__":
#     quiz_app.run(debug=True)


import flask
from flask import Flask, request, jsonify
from Question import questions
import requests

quiz_app = Flask(__name__)

# API Endpoint to get all questions
@quiz_app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

# API Endpoint to submit an answer
@quiz_app.route('/api/submit', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get("id")  # Get the question ID
    selected_option = data.get("option")  # Get the selected option index (0-based)

    # Find the question by its ID
    question = next((q for q in questions if q["id"] == question_id), None)

    if not question:
        return jsonify({"message": "Question not found"}), 404

    # Check if the selected option is correct
    if question["answer"] == selected_option:
        return jsonify({"message": "Right!"})
    else:
        correct_option = question["answer"]
        return jsonify({
            "message": "Wrong!",
            "correct_answer": question["options"][correct_option]
        })

# CLI Quiz functions
BASE_URL = "http://127.0.0.1:5000"

def get_questions_from_api():
    """
    Fetch all questions from the Flask API.
    """
    try:
        response = requests.get(f"{BASE_URL}/api/questions")
        return response.json()
    except Exception as e:
        print("Error fetching questions:", e)
        return []

def submit_answer_to_api(question_id, selected_option):
    """
    Submit the answer to the Flask API and return the result.
    """
    try:
        data = {
            "id": question_id,
            "option": selected_option
        }
        response = requests.post(f"{BASE_URL}/api/submit", json=data)
        return response.json()
    except Exception as e:
        print("Error submitting the answer:", e)
        return {"message": "Failed to submit the answer"}

def run_quiz():
    """
    Runs the CLI-based quiz by fetching questions and prompting the user for answers.
    """
    questions = get_questions_from_api()

    if not questions:
        print("No questions available!")
        return

    score = 0

    for question in questions:
        print(f"\nQuestion {question['id']}: {question['question']}")
        options = question['options']

        for i, option in enumerate(options):
            print(f"{i}. {option}")

        try:
            selected_option = int(input("Select your option (0, 1, 2, 3): "))
            if selected_option < 0 or selected_option >= len(options):
                print("Invalid option. Please try again.")
                continue

            result = submit_answer_to_api(question['id'], selected_option)
            print(result['message'])

            if result['message'] == "Right!":
                score += 1
            else:
                print(f"The correct answer is: {result['correct_answer']}")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"\nYour final score: {score}/{len(questions)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # If the script is run with 'cli' argument, run the CLI quiz
        run_quiz()
    else:
        # Otherwise, run the Flask app
        quiz_app.run(debug=True)
