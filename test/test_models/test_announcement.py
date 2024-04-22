#!/usr/bin/python3

import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.announcement import Announcement
from models.basemodel import Base


class TestAnnouncementModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        self.announcement = Announcement(
            content="Important announcement!",
            staff_id="12345",
            target="All Staff"
        )

    def test_announcement(self):
        self.assertTrue(self.announcement is not None)
        announcement = Announcement(content="Just announcement!",
                                    staff_id="12345", target="All Staff")
        self.session.add(announcement)
        self.session.add(self.announcement)
        self.session.commit()
        self.assertIsNotNone(announcement.id)

    def test_query(self):
        announcement = Announcement(content="Just announcement!",
                                    staff_id="12345", target="All Staff")
        self.session.add(announcement)
        self.session.add(self.announcement)
        self.session.commit()
        self.assertIsNotNone(announcement.id)
        query = self.session.query(Announcement)
        self.assertEqual(query.count(), 2)
        by_staff = (query.
                    filter(Announcement.staff_id == "12345").all())
        self.assertEqual(len(by_staff), 2)

        queried_announcement = (query.filter(Announcement.id == self.announcement.id)
                                .first())
        self.assertEqual(queried_announcement, self.announcement)

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
