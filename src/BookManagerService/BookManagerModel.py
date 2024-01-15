from BookManagerDb import BookManagerDb
import psycopg2
import logging

class BookReview:
    def __init__(self, book_id=None, user_id=None, review=None, rating=None) -> None:
        self.book_id = book_id
        self.user_id = user_id
        self.review = review
        self.rating = rating

    def create(self, db: BookManagerDb):
        try:
            db.cur.execute("INSERT INTO book_reviews (book_id, user_id, review, rating) VALUES (%s, %s, %s, %s)", (self.book_id, self.user_id, self.review, self.rating))
            db.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            db.conn.rollback()
            raise error

class BookRevews(list):
    def __init__(self) -> None:
        pass