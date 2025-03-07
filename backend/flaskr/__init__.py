import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#pagination of any request for questions returned
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Headers", "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        category_id = request.args.get("category_id", None, type=int)
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        if category_id:
            category = {
                category.id : category.type for category in categories if category.id==category_id}
            if len(category) == 0:
                abort(404)
            else:
                return jsonify({
                    "success" : True,
                    "category" : category
                })
        else:
            category_dict = {category.id : category.type for category in categories}

            return jsonify({
                "success" : True,
                "categories" : category_dict
            })
        


    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        categories = retrieve_categories().get_json().get("categories")

        return jsonify({
            "success" : True,
            "questions" : questions,
            "total_questions" : len(selection),
            "categories" : categories,
            "current_category" : None
        })
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def purge_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()

            return jsonify({
                "success" : True,
                "deleted_question" : question_id,
                "total_questions_now" : len(Question.query.all())
            })
        
        except:
            abort(404)

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        if new_question==None or new_answer==None or new_category==None or new_difficulty==None:
            abort(422)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)

            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success" : True,
                "question" : new_question,
                "answer" : new_answer,
                "category" : new_category,
                "difficulty" : new_difficulty
            })
        except:
            abort(422)

    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()

        searchTerm = body.get('searchTerm', None)

        if searchTerm:
            selection = Question.query.filter(Question.question.ilike(
                '%{}%'.format(searchTerm))).all()
            if len(selection) == 0 :
                abort(404)
        else:
            error(400)
        
        current_questions = paginate_questions(request, selection)
        current_category = list(set([question.category for question in selection]))
        categories = Category.query.all()
        category_dict = {}
        for category in categories:
            if category.id in current_category:
                category_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category_dict
        })



    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @DONE:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):

        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()

            selection = Question.query.filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success" : True,
                "questions" : current_questions,
                "total_questions" : len(selection),
                "current_category" : category.type
                })
        except:
            abort(404)

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            category = body.get('quiz_category')
            category_id = category['id']

        
            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                Question.category == category_id).all()
            
            if questions :
                random_question = random.choice(questions).format()
            else:
                random_question = False

            return jsonify({
                'success': True,
                'question': random_question
            })
        except:
            abort(404)

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success" : False, 
            "error" : 400, 
            "message" : "bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success" : False, 
            "error" : 404, 
            "message" : "resource not found"
            }), 404
    
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success" : False, 
            "error" : 405, 
            "message" : "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success" : False, 
            "error" : 422, 
            "message" : "unprocessable"
            }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success" : False, 
            "error" : 500,
            "message" : "internal server error" 
        }), 500

    
    return app

