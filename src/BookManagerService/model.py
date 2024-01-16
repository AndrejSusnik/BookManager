import marshmallow as ma
from config_managment import CustomConfigManager
from typing import Optional
import psycopg2 as ps
import logging
import time

class BookReviewSchema(ma.Schema):
    id = ma.fields.Integer()
    user_id = ma.fields.Integer()
    title = ma.fields.String()
    review = ma.fields.String()
    rating = ma.fields.Integer()
    time_spent = ma.fields.Float()

class BookReviewQuerySchema(ma.Schema):
    id = ma.fields.Integer()
    user_id = ma.fields.Integer()

class BookReviewQueryByUserSchema(ma.Schema):
    id = ma.fields.Integer()
    user_id = ma.fields.Integer()

class BookReviewNotFound(Exception):
    pass

class CouldNotConnectToDatabase(Exception):
    pass

class _BookReview:
    def __init__(self, config_manager: CustomConfigManager):
        self.host = config_manager.get("DB_URL", default="localhost")
        self.db_name = config_manager.get("DB_NAME", default="postgres")
        self.username = config_manager.get("DB_USER", default="postgres")
        self.password = config_manager.get("DB_PASSWORD", default="postgres")

        self.db_max_connection_attempts = config_manager.get("DB_MAX_CONNECTION_ATTEMPTS", default=5)
        self.db_connection_attempt_delay = config_manager.get("DB_CONNECTION_ATTEMPT_DELAY", default=1)

        self.has_error = False
        self.connection: Optional[ps.connection] = None

        self.try_reconnect()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def get_book_reviews(self, args: BookReviewQueryByUserSchema) -> list:
        if self.has_error:
            raise CouldNotConnectToDatabase("Could not connect to database")

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM read_books WHERE user_id = %s;", (args.user_id,))
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def get_book_review(self, args: BookReviewQuerySchema) -> BookReviewSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase("Could not connect to database")

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM read_books WHERE id = %s AND user_id = %s;", (args.id, args.user_id))
        row = cur.fetchone()
        cur.close()
        if row is None:
            raise BookReviewNotFound("Book review not found")
        return row

    def create_book_review(self, book_review: BookReviewSchema) -> BookReviewSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase("Could not connect to database")

        cur = self.connection.cursor()
        cur.execute("INSERT INTO read_books (user_id, title, review, rating, time_spent) VALUES (%s, %s, %s, %s, %s) RETURNING *;", (book_review.user_id, book_review.title, book_review.review, book_review.rating, book_review.time_spent))
        row = cur.fetchone()
        self.connection.commit()
        cur.close()
        return row

    def update_book_review(self, book_review: BookReviewSchema) -> BookReviewSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase("Could not connect to database")

        cur = self.connection.cursor()
        cur.execute("UPDATE read_books SET title = %s, review = %s, rating = %s, time_spent = %s WHERE id = %s AND user_id = %s RETURNING *;", (book_review.title, book_review.review, book_review.rating, book_review.time_spent, book_review.id, book_review.user_id))
        row = cur.fetchone()
        self.connection.commit()
        cur.close()
        if row is None:
            raise BookReviewNotFound("Book review not found")
        return row

    def delete_book_review(self, args: BookReviewQuerySchema) -> BookReviewSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase("Could not connect to database")

        cur = self.connection.cursor()
        cur.execute("DELETE FROM read_books WHERE id = %s AND user_id = %s RETURNING *;", (args.id, args.user_id))
        row = cur.fetchone()
        cur.close()
        if row is None:
            raise BookReviewNotFound("Book review not found")
        return row

    def try_reconnect(self) -> bool:
        max_connection_attempts = self.db_max_connection_attempts
        while max_connection_attempts > 0:
            try:
                logging.info("Connecting to database %s on %s as %s", self.db_name, self.host, self.username)
                self.connection = ps.connect(host=self.host, database=self.db_name, user=self.username, password=self.password)

                return True
            except Exception as e:
                logging.error("Error while connecting to database: %s", str(e))
                max_connection_attempts -= 1
                if max_connection_attempts == 0:
                    self.has_error = True
                time.sleep(self.db_connection_attempt_delay)
        return False

BookReviewDb = _BookReview(CustomConfigManager())
