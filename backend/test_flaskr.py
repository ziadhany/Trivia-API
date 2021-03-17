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
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
            'question': 'How many paintings did Van Gogh sell in his lifetime??',
            'answer': 'One',
            'difficulty': 5,
            'category': '3'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['questions']), 10)

    def test_delete_questions(self):

        question_created = Question(category=self.question['category'],
                                    question=self.question['question'],
                                    answer=self.question['answer'],
                                    difficulty=self.question['difficulty'])
        question_created.insert()
        response = self.client().delete('/questions/{}'.format(question_created.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "The Question deleted")

    def test_create_question(self):
        response = self.client().post('/questions', json=self.question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "The Question Created")

    def test_create_question_missing(self):
        response = self.client().post('/questions', json={'question': '', 'answer': '', 'difficulty': 5,
                                                          'category': '3'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['error'], "422")
        self.assertEqual(data['massage'], "Page not found")
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        response = self.client().post('/questions/search', json={'searchTerm': 'did'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    def test_search_questions_empty(self):
        response = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], '422')
        self.assertEqual(data['massage'], 'Page not found')

    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_play_quiz(self):
        response = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science",
                                                                                                    "id": "1"}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_categories_failure(self):
        Category.query.delete()
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], '404')
        self.assertTrue(data['massage'], 'Page not found')
        self.assertEqual(data['success'], False)

    def test_get_question_failure(self):
        Category.query.delete()
        Question.query.delete()
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], '404')
        self.assertTrue(data['massage'], 'Page not found')
        self.assertEqual(data['success'], False)

    def test_delete_question_failure(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], '404')
        self.assertTrue(data['massage'], 'Page not found')
        self.assertEqual(data['success'], False)
    def test_quiz_failure(self):
        response = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': []})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['error'], '500')
        self.assertTrue(data['massage'], 'Internal Server Error')
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()
