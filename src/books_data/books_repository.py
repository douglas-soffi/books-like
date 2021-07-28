import pandas as pd
from db import Db


class BookRepository():

    get_book_select = "SELECT * FROM books WHERE Id = ?;"
    get_books_select = "SELECT * FROM books;"

    def get_book(self, id):
        with Db() as conn:
            cur = conn.connector.cursor()
            cur.execute(self.get_book_select, (id))
            result = cur.fetchone()
            return result

    def get_books(self, data_frame):
        with Db() as conn:
            cur = conn.connector.cursor()
            cur.execute(self.get_book_select, (id))
            rows = cur.fetchall()
            return rows