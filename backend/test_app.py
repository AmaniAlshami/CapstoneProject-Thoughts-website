import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Bolgger, Blog ,Comment ,Visitor , db_drop_and_create_all

Access_token_blogger= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpkY3dtZWozRkZqZU5JNkNFdVlNUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1nY3RoZXVnci51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTU5MDQxMDkxNzA2MDMwMjc3ODYiLCJhdWQiOiJUaG91Z2h0c0FwcCIsImlhdCI6MTYzMTgwMTYwNCwiZXhwIjoxNjMxODg4MDA0LCJhenAiOiIyMExSa29Ybkd1bmFKWUJiTzE2YVVBN0oyRE93Vml3dCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJsb2ciLCJnZXQ6YmxvZ2dlciIsImdldDpibG9ncyIsImdldDpjb21tZW50cyIsInBhdGNoOmJsb2ciLCJwb3N0OmJsb2ciLCJwb3N0OmNvbW1lbnQiXX0.RF1ol56JL1dgb6MSZ-NWKp1cwoIvpRJN_aoRBVvsiDp_GYMyBRdbNw9dzFa61rt81lUMwgmqswoN2avVpQhAXhdbr54ZRWZKbqIqlLn6Y80ML1AsNOK59RYSQckkPapW3xW3gEmcZD2U_-3CJxaJQBiARyiLQlXoTTLtNeGnLiO11SQ03ol5WsApmF3dmggqkn9cUAlhe9E_8Fg7ZHkvy5kM3sqNqxmdt_RrqtwklY4gtbDsTCVOYTvRe9u8fKDZmn2OrQJRQ6i19xsXVIZoQz_2MyonairwsKYAGU1nIauokqwuIRWZfFu9Ph8gNBqvUBqFhvxvfEStOAcw2KBVdg'
Access_token_Visitor= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpkY3dtZWozRkZqZU5JNkNFdVlNUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1nY3RoZXVnci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE0MzRmYjM0NDY3MmMwMDY5NGMyNTQwIiwiYXVkIjoiVGhvdWdodHNBcHAiLCJpYXQiOjE2MzE4MDE1MDcsImV4cCI6MTYzMTg4NzkwNywiYXpwIjoiMjBMUmtvWG5HdW5hSllCYk8xNmFVQTdKMkRPd1Zpd3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpibG9nZ2VyIiwiZ2V0OmJsb2dzIiwiZ2V0OmNvbW1lbnRzIiwicG9zdDpjb21tZW50Il19.Asub6uVpbX9TyHj1G60CB_rlz8Lo3Jt4HYvWdxV3wVl4nahw0SEWHheM0OBsfsDGoU0KaLdJZwvDzr5r_bXDKsxUQsbQxb76z2pGGMXK2LhRDO3MOa-hgOBWT86v0NGpA6YJpXvJqMf18y1H_cg4vy9fD7Qv2SVJpWKGPnizUuXk3bSUeAnBH7nDik8wyAGdy8wob272DxMdcdlJSVSKt4fIm84xALSw7aYgOMajgRvTo5ZNum0JzE6aMyUP06lT-DHE2KaIumtPLCOWEsx6tkLOmv49Sj0XLAb6ZIMU1uUCOnLZzVXv9c5jyaNU66xgimPbhTX40npe7Zx29eb-_Q'

class ThoughtsTestCase(unittest.TestCase):
    """This class represents the Thoughts test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "Thoughts_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /blogs 

    def test_get_blogs(self):
        res = self.client().get('/blogs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['blogs'])



    # GET '/bloggers' 

    def test_get_bloggers(self):
        res = self.client().get('/bloggers')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
   
    
    # GET '/${blogger_id}/blogs'   

    def test_get_blogs_for_one_blogger(self):

        res = self.client().get('/1/blogs')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['blogs'])


    def test_404_sent_requesting_beyond_valid_blogger(self):

        res = self.client().get('/1000/blogs')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    # GET '/blogs/${blog_id}'   

    def test_get_one_blog(self):

        res = self.client().get('/blogs/1')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)


    
    def test_404_sent_requesting_beyond_valid_blog(self):

        res = self.client().get('/blogs/1000')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    # POST '/${blogger_id}/blogs' - create blog

    def test_create_new_blog(self):
        res = self.client().post('/1/blogs',
        json={'title': 'New testing blog',
        'content': 'This is a new blog'},headers={'Authorization': 'Bearer ' + Access_token_blogger})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_405_if_blogs_creation_not_allowed(self):
        res = self.client().post('/blogs', json={'title': 'New testing blog',
        'content': 'This is a new blog'},headers={'Authorization': 'Bearer ' + Access_token_Visitor})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
 

    
     
    # POST '/blogs/${blog_id}' - new comment

    def test_create_new_comment(self):
        res = self.client().post('/blogs/1',
        json={"VisitorName":'John',"Comment":'this new comment'},headers={'Authorization': 'Bearer ' + Access_token_Visitor})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       # self.blog_id = data['blogs']['id']
    
    def test_422_if_visitor_name_does_not_exist(self):
        res = self.client().post('/blogs/1',
        json={"VisitorName":'John22',"Comment":'this new comment'},headers={'Authorization': 'Bearer ' + Access_token_Visitor})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')  



# PATCH  '${blogger_id}/blogs/${blog_id}' 

    def test_edit_blog(self):
        res = self.client().patch('/1/blogs/1',
        json={'title': 'New edit blog',
        'content': 'This is a chaging blog'},headers={'Authorization': 'Bearer ' + Access_token_blogger})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_403_if_blogs_edit_not_allowed(self):
        res = self.client().patch('/1/blogs/1',
        json={'title': 'New edit blog',
        'content': 'This is a chaging blog'}, headers={'Authorization': 'Bearer ' + Access_token_Visitor})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
       


    
    # DELETE '${blogger_id}/blogs/${blog_id}' 


    def test_delete_blog(self):
        res = self.client().delete('/1/blogs/1',headers={'Authorization': 'Bearer ' + Access_token_blogger})
        data = json.loads(res.data)
    
        blog = Blog.query.filter(Blog.id == 1).one_or_none()
      

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(blog, None)
        
    
    def test_404_if_blog_does_not_exist(self):
        res = self.client().delete('/1/blogs/1000',headers={'Authorization': 'Bearer ' + Access_token_blogger})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()