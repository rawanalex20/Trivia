import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate(questions, request):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    return questions[start:end], start, end


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true'
          )
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PUT,POST,DELETE,OPTIONS'
          )
        return response

    # Endpoint to handle GET requests
    # for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_cat():
        try:
            categories = [cat.type for cat in Category.query.all()]
            return jsonify({
              "success": True,
              "categories": categories
            })
        except:
            abort(422)

    # An endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination
    # at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    @app.route('/questions', methods=['GET'])
    def get_all():
        try:
            questions = Question.query.all()
            paginated_questions, start, end = paginate(questions, request)
            questions_cat = Question.query.distinct(Question.category).all()
            categories = [cat.type for cat in Category.query.all()]
            if len(paginated_questions) == 0:
                abort(404)
            else:
                return jsonify({
                  "success": True,
                  "questions": list(paginated_questions),
                  "total questions": len(questions),
                  "categories": categories
                  })
        except:
            abort(422)

    # DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question,
    # the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)
            else:
                question.delete()
                db.session.commit()
                return jsonify({
                  "success": True
                  })
        except:
            abort(422)

    # POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear
    # and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        print(body.get('category', None))
        question = Question(
          question=body.get('question', None),
          answer=body.get('answer', None),
          category=body.get('category', None),
          difficulty=body.get('difficulty', None)
          )
        try:
            db.session.add(question)
            db.session.commit()
            return jsonify({
              "success": True
              })
        except:
            abort(422)

    # POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    @app.route('/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        data = []
        try:
            questions = Question.query.filter(
              Question.question.like('%' + search_term + '%')).all()
            for question in questions:
                data.append({
                  "id": question.id,
                  "question": question.question,
                  "answer": question.answer,
                  "category": question.category,
                  "difficulty": question.difficulty
                })
            return jsonify({
              "success": True,
              "questions": data,
              "total_questions": len(questions),
              "current_category": None
              })
        except:
            abort(422)

    # GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.

    @app.route('/categories/<int:question_category>', methods=['GET'])
    def get_by_category(question_category):
        data = []
        try:
            question_category = question_category + 1
            questions = Question.query.filter_by(
              category=str(question_category)).all()
            category = Category.query.filter_by(
              id=(question_category))[0].type
            for question in questions:
                data.append({
                  "id": question.id,
                  "question": question.question,
                  "answer": question.answer,
                  "category": question.category,
                  "difficulty": question.difficulty
                })
            return jsonify({
              "success": True,
              "questions": data,
              "total_questions": len(questions),
              "current_category": category
              })
        except:
            abort(422)

    # POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    @app.route('/quizzes', methods=['POST'])
    def play_questions():
        body = request.get_json()
        category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)
        try:
            if category == 0:
                questions = Question.query.all()
                questionstemp = Question.query.all()
            else:
                category = int(category)
                questions = Question.query.filter_by(category=category).all()
                qtemp = Question.query.filter_by(category=category).all()
            for question in qtemp:
                if question.id in previous_questions:
                    questions.remove(question)
            if (len(questions) == 0):
                return jsonify({
                  "success": True
                })
            index = random.randrange(0, len(questions))
            question = questions[index]
            return jsonify({
              "success": True,
              "question": {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "category": question.category,
                "difficulty": question.difficulty
                }
              })
        except:
            abort(422)

    # Error handlers for all expected errors
    # including 404 and 422.

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
          }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
          }), 405

    return app

if __name__ == '__main__':
    app.run()
