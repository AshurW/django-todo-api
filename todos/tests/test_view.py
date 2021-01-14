from random import randrange

from django.test import TestCase
from django.urls import reverse

from .test_setup import TodoSetup

class TodoSetupHelper():
    TS_CLIENT = None
    INTRUDER_CLIENT = None

    def setUp(self):
        self.TS_CLIENT = TodoSetup()
        self.INTRUDER_CLIENT = TodoSetup()

    def get_all_todolist(self, url):
        return self.TS_CLIENT.do_get(url)
    
    def get_todolist(self, url, list_id):
        formated_url = f'{url}{list_id}/'
        return self.TS_CLIENT.do_get(formated_url)
    
    def create_new_todolist(self, url, payload):
        return self.TS_CLIENT.do_post(url, payload)

    def update_todolist_title(self, url, list_id, payload):
        formated_url = f'{url}{list_id}/'
        return self.TS_CLIENT.do_patch(formated_url, payload)
    
    def delete_todolist(self, url, list_id):
        formated_url = f'{url}{list_id}/'
        return self.TS_CLIENT.do_delete(formated_url)
    
    def create_new_todo(self, url, list_id, payload):
        formated_url = f'{url}{list_id}/todos/'
        return self.TS_CLIENT.do_post(formated_url, payload)

    def update_todo_checked(self, url, list_id, todo_id, payload):
        formated_url = f'{url}{list_id}/todos/{todo_id}/'
        return self.TS_CLIENT.do_patch(formated_url, payload)

    def update_todo(self, url, list_id, todo_id, payload):
        formated_url = f'{url}{list_id}/todos/{todo_id}/'
        return self.TS_CLIENT.do_patch(formated_url, payload)
    
    def delete_todo(self, url, list_id, todo_id):
        formated_url = f'{url}{list_id}/todos/{todo_id}/'
        return self.TS_CLIENT.do_delete(formated_url)

    def ts_create_list(self, url, payload):
        return self.TS_CLIENT.do_post(url, payload)
    
    def intruder_delete_list(self, url, list_id):
        formated_url = f'{url}{list_id}/'
        return self.INTRUDER_CLIENT.do_delete(formated_url)
    
    def register_user(self, url, payload):
        return self.TS_CLIENT.do_post(url, payload)

    def get_all_users(self, url):
        return self.TS_CLIENT.do_get(url)

class TestTodoList(TodoSetupHelper, TestCase):
    TEST_TODOLISTS = []
    URL = None

    def setUp(self):
        TodoSetupHelper.setUp(self)
        self.URL = reverse('todoListsView')
        for x in range(5):
            newTodoListData = {
                'title': f'test todolist{x}',
                'todos': []
            }
            res = self.create_new_todolist(self.URL, newTodoListData)
            self.TEST_TODOLISTS.append(res.data)
    
    def test_create_todolist(self):
        newTodoListData = {
            'title': 'new todolist',
            'todos': []
        }
        res = self.create_new_todolist(self.URL, newTodoListData)
        self.assertEqual(res.status_code, 201)

    def test_get_all_todolists(self):
        res = self.get_all_todolist(self.URL)
        self.assertEqual(len(res), 5)
    
    def test_get_todolist(self):
        todolist = self.TEST_TODOLISTS[randrange(5)]
        list_id = todolist['id']
        res = self.get_todolist(self.URL, list_id)
        self.assertEqual(res['id'], list_id)
    
    def test_update_todolist_title(self):
       todolist = self.TEST_TODOLISTS[randrange(5)]
       list_id = todolist['id']
       newTodoListTitle = {
           'title': 'new title'
       }
       res = self.update_todolist_title(self.URL, list_id, newTodoListTitle)
       self.assertEqual(res.data['title'], newTodoListTitle['title'])
    
    def test_delete_todolist(self):
        todolist = self.TEST_TODOLISTS[randrange(5)]
        list_id = todolist['id']

        res = self.delete_todolist(self.URL, list_id)
        self.assertEqual(res.status_code, 204)

class TestTodo(TodoSetupHelper, TestCase):
    TEST_TODOLIST = None
    URL = None

    def setUp(self):
        TodoSetupHelper.setUp(self)
        newTodoListData = {
            'title': 'new todolist',
            'todos': []
        }
        self.URL = reverse('todoListsView')
        res = self.create_new_todolist(self.URL, newTodoListData)
        self.TEST_TODOLIST = res.data
    
    def test_create_todo_for_todolist(self):
        newTodo = {
            'todo': 'new todo'
        }
        res = self.create_new_todo(self.URL, self.TEST_TODOLIST['id'], newTodo)
        self.assertEqual(res.status_code, 201)

    def test_update_todo_checked(self):
        newTodo = {
            'todo': 'new todo'
        }
        res1 = self.create_new_todo(self.URL, self.TEST_TODOLIST['id'], newTodo)
        todo_id = res1.data['id']
        updateTodoCheck = {
            'checked': not res1.data['checked']
        }

        res2 = self.update_todo_checked(self.URL, self.TEST_TODOLIST['id'], todo_id, updateTodoCheck)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['todoList'], self.TEST_TODOLIST['id'])

    def test_update_todo(self):
        newTodo = {
            'todo': 'new todo'
        }
        res1 = self.create_new_todo(self.URL, self.TEST_TODOLIST['id'], newTodo)
        todo_id = res1.data['id']

        updatedTodo = {
            'todo': 'updated todo'
        }

        res2 = self.update_todo(self.URL, self.TEST_TODOLIST['id'], todo_id, updatedTodo)
        self.assertNotEqual(res1.data['todo'], res2.data['todo'])
    
    def test_delete_todo(self):
        newTodo = {
            'todo': 'new todo'
        }
        res1 = self.create_new_todo(self.URL, self.TEST_TODOLIST['id'], newTodo)
        todo_id = res1.data['id']

        res2 = self.delete_todo(self.URL, self.TEST_TODOLIST['id'], todo_id)
        self.assertEqual(res2.status_code, 204)

class TestTodoListOwner(TodoSetupHelper, TestCase):
    TS_CLIENT_TODOLIST = None
    URL = None

    def setUp(self):
        TodoSetupHelper.setUp(self)
        TSclientTodoList = {
            'title': 'TS todolist',
            'todos': []
        }
        self.URL = reverse('todoListsView')
        res = self.ts_create_list(self.URL, TSclientTodoList)
        self.TS_CLIENT_TODOLIST = res.data

    def test_intruder_try_deleting_todolist(self):
        res = self.intruder_delete_list(self.URL, self.TS_CLIENT_TODOLIST['id'])

        self.assertEqual(res.status_code, 403)

class TestUser(TodoSetupHelper, TestCase):
    USER_LIST = []
    USER = None
    REGISTER_URL = None
    USER_URL = None

    def setUp(self):
        TodoSetupHelper.setUp(self)
        self.REGISTER_URL = reverse('registerUser')
        self.USER_URL = reverse('userListView')
    
    def test_register_user(self):
        newUserData = {
            'username': 'newUser',
            'password': '321ewq321'
        }
        res = self.register_user(self.REGISTER_URL, newUserData)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(newUserData['username'], res.data['username'])

    def test_get_all_users(self):
        for x in range(3):
            newUserData = {
                'username': f'newUser{x}',
                'password': '321ewq321'
            }
            res = self.register_user(self.REGISTER_URL, newUserData)
        
        res2 = self.get_all_users(self.USER_URL)
        self.assertEqual(len(res2), 5)