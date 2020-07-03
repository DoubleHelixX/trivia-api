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
        self.database_name = "trivia"
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format('postgres', '1','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'How much wood can a wood chuck chuck?',
            'answer': 'depends on his dentist bill',
            "category" : "3", 
            'difficulty': 5
        }
        self.new_category = {
            'type' : "Animals"
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        #res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # # @TODO: Write tests for search - at minimum two - that check a response when there are results and when there are none
   
   
   
   # # @TODO: Implement functions on init - app py file.
   
    #Test for updating databases
    """ def test_update_category_type(self):
        res = self.client().patch('/categories/5', json={'type': "Laughables"})
        data = json.loads(res.data)
        category = Category.query.filter(Category.type == "Laughables").one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Category.format()['type'], "Laughables")
    
     def test_update_question_fields(self):
        res = self.client().patch('/questions/5', json={'question': 'Is an egg a egg?', 'answer':'yes' , 'category':'4', 'difficulty':9})
        data = json.loads(res.data)
        category = Question.query.filter(Question.question == "Is an egg a egg?").one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(category.format()['question'], "Is an egg a egg?")
        self.assertEqual(Category.format()['answer'], "yes")
        self.assertEqual(Category.format()['category'], "4")
        self.assertEqual(Category.format()['difficulty'], 9)
        
    def test_400_for_failed_update_questions(self):
        res = self.client().patch('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        
    def test_400_for_failed_update_categories(self):
        res = self.client().patch('/categories/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') """
        
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/5')
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 5)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(question, None)
        
    def test_422_if_question_to_delete_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json={"difficulty":[1,2,3]})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_405_if_question_creation_method_not_allowed(self):
        res = self.client().post('/questions/1000', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    def test_create_new_category(self):
        res = self.client().post('/categories', json=self.new_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        
    def test_422_if_category_creation_fails(self):
        res = self.client().post('/categories', json={'empty':0})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #NOT WORKING - RETURNS 404 FOR SOME REASON
    def test_405_if_categories_creation_method_not_allowed(self):
        res = self.client().post('/categories/10000', json=self.new_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_get_question_search_with_results(self):
        res = self.client().get('/questions/search', json={'search': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_get_questions_search_without_results(self):
        res = self.client().get('/questions/search', json={'search': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()