import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_PASSWORD, DB_USER

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = DB_USER
        self.database_pass = DB_PASSWORD
        self.database_url =  'localhost:5432'
        self.database_name = DB_NAME
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_pass, self.database_url, self.database_name)

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
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_404_for_unavailable_questions_pages(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_by_categories(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_delete_question(self):
        res = self.client().delete("/questions/9")
        question = Question.query.filter(Question.id == 9).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist_on_delete(self):
        
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question(self):
        res = self.client().post("/questions", json={
            "question": "Is 'Hello World!' mostly the first program to learn?",
            "answer": "Yes, it is commonly the first program to learn",
            "difficulty": 1,
            "category": 1
        })
        self.assertEqual(res.status_code, 200)

    def test_add_question_without_required_input(self):

        question = {
         'question': 'Is this an incomplete request?',
        }
    
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)  

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "earn"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_search_questions_with_no_result(self):
        
        res = self.client().post('/questions/search',json={'searchTerm': 'trippy'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_quiz(self):
        new_quizz = {
            "previous_questions": [10],
            "quiz_category": {
                "type": "Sports",
                "id": "6"}}
        res = self.client().post('/quizzes', json=new_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)



    def test_create_quiz_fails(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
