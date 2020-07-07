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
            "question": "How much wood can a wood chuck chuck?",
            "answer": "depends on his dentist bill",
            "category" : "3", 
            "difficulty": 5
        }
        self.new_category = {
            "type" : "Animals"
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
    # * ----- TESTING  GET/PAGINATION ON QUESTION ROUTE ----- *
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(type(data['currentCategory']) is str)
    
    def test_404_sent_requesting_beyond_valid_page_questions(self):
        #res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource or url not found')
    
    # * ----- END OF TESTING PAGINATION ON QUESTION ROUTE ----- *
    
    
    # * ----- TESTING GET/PAGINATION ON CATEGORIES ROUTE ----- *
    
    def test_200_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
        
    def test_405_get_categories_wrong_method(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    ## ! OPTIONAL PAGINATION - ONLY WORKS IF CATEGORIES REQUIRED PAGINATION 
    """ 
    def test_404_sent_requesting_beyond_valid_page_categories(self):
        #res = self.client().get('/questions?page=1000', json={'type': "lawls"})
        res = self.client().get('/categories?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource or url not found') 
        """
    
    # * ----- END OF TESTING PAGINATION ON CATEGORIES ROUTE ----- *
    
    
    # ! ----- OPTIONAL - TESTING UPDATE CATEGORY ROUTE - INCOMPLETE FUNCTIONALITY ----- *
    """ 
    # @TODO: Implement below functions on the init - app py file.
    def test_update_category_type(self):
        res = self.client().patch('/categories/5', json={'type': "Laughables"})
        data = json.loads(res.data)
        category = Category.query.filter(Category.type == "Laughables").one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Category.format()['type'], "Laughables")
    
    def test_400_for_failed_update_categories(self):
        res = self.client().patch('/categories/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
     """
    # ! ----- OPTIONAL - END OF TESTING UPDATE CATEGORY ROUTE  ----- *
    
    
    # ! ----- OPTIONAL - TESTING UPDATE QUESTION ROUTE - INCOMPLETE FUNCTIONALITY----- *
    """ 
    # @TODO: Implement below functions on the init - app py file.
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
     """
    # ! ----- OPTIONAL - END OF TESTING UPDATE QUESTION ROUTE ----- *
        
        
    # * ----- TESTING DELETE QUESTION ROUTE ----- *

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)
        
    def test_422_if_question_to_delete_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_405_delete_question_wrong_method(self):
        res = self.client().post('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    # * ----- END OF TESTING DELETE QUESTION ROUTE ----- *
    
    
    # * ----- TESTING CREATE QUESTION ROUTE ----- *
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['question'])
        self.assertTrue(data['total_questions'])
        
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json={"difficulty":[1,2,3]})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
        #Optional 405 testing
    def test_405_if_question_creation_method_not_allowed(self):
        res = self.client().patch('/questions/45', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    
    # * ----- END OF TESTING CREATE QUESTION ROUTE ----- *
    
    
    # ! ----- OPTIOANL -TESTING CREATE CATEGORY ROUTE - INCOMPLETE FUNCTIONALITY ----- *
    
    """  
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
    
        #optional 405 test
    ## ! NOT WORKING - RETURNS 404 FOR SOME REASON
    def test_405_if_category_creation_method_not_allowed(self):
        res = self.client().post('/categories/1000', json=self.new_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed') 
    """
    
    # ! ----- END OF TESTING CREATE CATEGORY ROUTE ----- *
    
    
    # * ----- TESTING SEARCH QUESTION ROUTE ----- *
    def test_200_get_question_search_with_results(self):
        res = self.client().post('/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_200_get_questions_search_without_results(self):
        res = self.client().post('/questions/search', json={"searchTerm": "WaterBallons"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        
    def test_422_get_questions_search_without_JSON_body(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_405_search_questions_method_not_allowed(self):
        res = self.client().patch('/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    # * ----- END OF TESTING SEARCH QUESTION ROUTE ----- *


    # * ----- TESTING GET QUESTION BASED CATEGORY ROUTE ----- *
    
    def test_200_get_category_based_question(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 3)

    def test_404_sent_requesting_beyond_valid_page_category_based_questions(self):
        #res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        res = self.client().get('/categories/5/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource or url not found')
        
    def test_422_invalid_category_based_question(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_405_get_category_based_question_method_not_allowed(self):
        res = self.client().patch('/categories/5/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    # * ----- END OF TESTING SEARCH QUESTION BASED CATEGORY ROUTE ----- *
    

    # * ----- TESTING GET QUESTION QUIZ ROUTE ----- *
    
    def test_200_get_quiz_questions_specific_category(self):
        res = self.client().post('/questions/quiz', json = {"quiz_category": {"type": "Entertainment", "id" : 5}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
        self.assertEqual(len(data['previous_questions']),1)
        self.assertEqual(data['total_questions'], 3)
        
    def test_200_get_quiz_questions_specific_category_with_previous_questions(self):
        res = self.client().post('/questions/quiz', json = {'previous_questions':[4], "quiz_category": {"type": "Entertainment", "id" : 5}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
        self.assertEqual(len(data['previous_questions']),2)
        self.assertEqual(data['total_questions'],2)
        
    def test_200_get_quiz_questions_all_categories(self):
        res = self.client().post('/questions/quiz', json={"quiz_category": {"type": "click", "id" : 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
        self.assertEqual(len(data['previous_questions']),1)
        self.assertTrue(data['total_questions'])
        
    def test_422_invalid_category_based_question(self):
        res = self.client().post('/questions/quiz', json={"quiz_category": {"type": "History", "id" : 1000}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_405_quiz_questions_method_not_allowed(self):
        res = self.client().patch('/questions/quiz', json = {'previous_questions':[4], "quiz_category": {"type": "Entertainment", "id" : 5}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    ## ! OPTIOANL PAGINATION TEST FOR CATEGORIES ONLY WORKS WITH GET METHOD BUT FRONEND IS USING POST
    """ 
    def test_404_sent_requesting_beyond_valid_page_quiz_questions_specific_category(self):
        #res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        res = self.client().get('/questions/quiz?page=1000', json={"quiz_category": {"type": "History", "id" : 3}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource or url not found') 
    """

        ## ! ONLY WORKS WITH GET METHOD BUT FRONEND IS USING POST
    """ 
    def test_404_sent_requesting_beyond_valid_page_quiz_questions_all_categories(self):
        #res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        res = self.client().post('/questions/quiz?page=1000', json={"quiz_category": {"type": "click", "id" : 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource or url not found') 
    """
        
    # * ----- END OFTESTING GET QUESTION QUIZ ROUTE ----- *


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()