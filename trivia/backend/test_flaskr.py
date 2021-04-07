import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    
    # Questions 
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total questions"])
        self.assertTrue(len(data["questions"]))

    # Errors in questions 
    def test_404_fail_get_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    # Categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["categories"]))

    # Adding a question
    def test_create_question(self):
        res = self.client().post('/questions', json={'question': "Who built the pyramids?", 'answer': 'pharoahs', 'catogories': 3, 'difficulty': 3})
        data = json.loads(self.data)
        pass

    # Error adding a question
    def test_422_fail_create_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(self.data)
         
        self.assertEqual(self.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'unprocessable'])

    def test_400_fail_create_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(self.data)
         
        self.assertEqual(self.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'bad request'])

    # Searching present questions
    def test_search_questions(self):
        res = self.client().post('/search', json={'searchTerm': 'What'})
        data = json.loads(self.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Error searching questions
    def test_400_bad_request_search(self):
        res = self.client().post('/search')
        data = json.loads(self.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'bad request'])

    # Deleting a question
    def test_delete(self):
        res = self.client().delete('/questions/21')
        data = json.loads(self.data)
        question = Question.query.filter_by(id=21).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertTrue(data['success'])

    # Errors deleting a question
    def test_404_delete_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(self.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'resource not found'])

    # Quizzes
    def test_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(self.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    # Errors in quizzes

    # Questions based on category
    def test_questions_in_category(self):
        res = self.client()('/categories/2')
        data = json.loads(self.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])








# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()