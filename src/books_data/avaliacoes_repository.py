from .db import Db


class AvaliacoesRepository():

    get_avaliacoes_select = "SELECT * FROM avaliacao_usuarios WHERE title = ?;"
    get_book_title_select = "SELECT title FROM avaliacao_usuarios WHERE Id = ?;"

    def get_book(self, title):
        with Db() as conn:
            cur = conn.connector.cursor()
            cur.execute(self.get_avaliacoes_select, [title])
            result = cur.fetchone()
            return result[0:]

    def get_book_title(self, Id):
        with Db() as conn:
            cur = conn.connector.cursor()
            cur.execute(self.get_book_title_select, [str(Id)])
            result = cur.fetchone()
            return result
