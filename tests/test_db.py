
import unittest
from peewee import *
from app import TimelinePost, app
from playhouse.shortcuts import model_to_dict
from flask import jsonify

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
  def setUp(self):
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)

    self.client = app.test_client(use_cookies=True)

  def tearDown(self):
    test_db.drop_tables(MODELS)
    test_db.close()

  def test_timeline_post(self):
    first_post = TimelinePost.create(name="John Doe", email="john@example.com", content='Hello World, I\'m John!')
    assert first_post.id == 1

    second_post = TimelinePost.create(name="Jane Doe", email='james@example.com', content="Hello world, I\'m Jane!")
    assert second_post.id == 2

    #TODO: get posts and check that they are the same
    response = self.client.get('/api/timeline_post')

    self.assertEqual(response.status_code, 200)

    posts = response.json['timeline_posts'];
    posts.reverse()

    resp_first_post = posts[0]
    resp_second_post = posts[1]

    with app.app_context():
      models_json = jsonify([model_to_dict(first_post), model_to_dict(second_post)]).json
      
      self.assertEqual(models_json[0], resp_first_post)
      self.assertEqual(models_json[1], resp_second_post)