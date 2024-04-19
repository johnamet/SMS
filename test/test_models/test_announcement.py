#!/usr/bin/python3

import unittest
from datetime import datetime
from models.announcement import Announcement


class TestAnnouncementModel(unittest.TestCase):
    def setUp(self):
        self.announcement = Announcement(
            content="Important announcement!",
            staff_id="12345",
            target="All Staff"
        )

    def test_announcement(self):
        self.assertTrue(self.announcement is not None)

    def test_content(self):
        self.assertEqual(self.announcement.content, "Important announcement!")

    def test_staff_id(self):
        self.assertEqual(self.announcement.staff_id, "12345")

    def test_target(self):
        self.assertEqual(self.announcement.target, "All Staff")

    def test_date(self):
        self.assertTrue(isinstance(self.announcement.date, datetime))
        self.assertTrue(self.announcement.date < datetime.now())

    def test_created_at(self):
        self.assertTrue(self.announcement.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.announcement.updated_at < datetime.now())

    def test_update(self):
        self.announcement.update(content="Updated announcement")
        self.assertEqual(self.announcement.content, "Updated announcement")
        self.assertTrue(self.announcement.updated_at > self.announcement.created_at)


if __name__ == '__main__':
    unittest.main()
