import json
import sqlite3
from datetime import datetime
from uuid import uuid4
import time


class ContentManager:
    def __init__(self):
        self.conn = sqlite3.connect("default.db", check_same_thread=False)
        self.c = self.conn.cursor()

        self.validate_tables()

    @staticmethod
    def generate_id():
        return str(uuid4()).replace("-", "")

    @staticmethod
    def convert_row_json(row):
        np = dict()
        np["id"] = row[0]
        np["heading"] = row[1]
        np["short"] = row[2]
        np["date"] = datetime.utcfromtimestamp(int(row[3])).strftime("%A %d %B, %Y")
        np["intro"] = row[4]
        np["image"] = row[5]
        np["content"] = row[6]

        return np

    @staticmethod
    def validate_post_data(pd):
        """ Validate post data coming into the DB has the correct fields """

        valid = {"heading": "", "short": "", "date": int(time.time()), "intro": "",
                 "image": "", "content": ""}

        for key in valid:
            if key in pd.keys():
                pass
            else:
                pd[key] = valid[key]

        return pd

    def validate_tables(self):
        create_posts = """
CREATE TABLE IF NOT EXISTS TBLPosts (
PID TEXT PRIMARY KEY,
Heading TEXT,
Short Text,
Date INT,
Intro TEXT,
Image TEXT,
Content TEXT
);
"""
        self.c.execute(create_posts)
        self.conn.commit()

    def get_posts(self):
        """ Returns a list of formatted dictionaries for Jinja templating to load """

        raw_posts = self.c.execute("SELECT * FROM TBLPosts").fetchall()
        clean_posts = []

        for p in raw_posts:  # convert each row into a dict with post data
            np = self.convert_row_json(p)
            clean_posts.append(np)

        return clean_posts

    def get_post(self, pid):
        """ Return Post Data by its ID """

        raw_post = self.c.execute("SELECT * FROM TBLPosts WHERE PID = (?);", (pid,)).fetchone()
        if raw_post:
            post_data = self.convert_row_json(raw_post)
            return post_data
        else:
            return None

    def add_post(self, post_data):
        """
        Add a post to the DB from JSON format
        :param post_data: Dictionary containing post information
        """

        pd = self.validate_post_data(post_data)
        id = self.generate_id()

        self.c.execute("""
INSERT INTO TBLPosts VALUES ((?), (?), (?), (?), (?), (?), (?));
        """, (id, pd["heading"], pd["short"], pd["date"], pd["intro"], pd["image"], pd["content"],))
        self.conn.commit()

        return id
