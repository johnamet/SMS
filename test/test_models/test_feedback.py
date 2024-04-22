#!/usr/bin/python3
import unittest
from datetime import datetime

from models.feedback import Feedback


class TestFeedbacksModel(unittest.TestCase):
    def setUp(self):
        self.feedback = Feedback(
            content="Great job!",
            user_id=1
        )

    def test_feedback(self):
        self.assertTrue(self.feedback is not None)

    def test_content(self):
        self.assertEqual(self.feedback.content, "Great job!")

    def test_user_id(self):
        self.assertEqual(self.feedback.user_id, 1)

    def test_created_at(self):
        self.assertTrue(self.feedback.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.feedback.updated_at < datetime.now())

    def test_update(self):
        self.feedback.update(content="Good work!")
        self.assertEqual(self.feedback.content, "Good work!")
        self.assertTrue(self.feedback.updated_at > self.feedback.created_at)


if __name__ == '__main__':
    unittest.main()
