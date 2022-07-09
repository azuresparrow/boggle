from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(str(session.get('highscore')), "0")
            self.assertIn(b'<p class="mb-0">High Score: <span id="highscore">', response.data)
            self.assertIn(b"Score:", response.data)
    
    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board']=[["B", "O", "A", "T", "S"],["C", "A", "T", "T", "S"],["B", "O", "A", "T", "S"],["B", "O", "A", "T", "S"],["B", "O", "A", "T", "S"]]
                sess['words']=["cat"]
        response = self.client.get('/guess/boat')
        self.assertIn(b'ok', response.data)
        response = self.client.get('/guess/cat')
        self.assertIn(b'repeat', response.data)
    
    def test_wrong_word(self):
        self.client.get('/')
        response = self.client.get('/guess/impossible')
        self.assertIn(b'not-on-board', response.data)

    def test_bad_word(self):
        self.client.get('/')
        response = self.client.get('/guess/weifojoiawefjioweasd')
        self.assertIn(b'not-word', response.data)

