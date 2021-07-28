import pandas as pd
from db import Db


class CriarBanco():
        
    def create_tables(self, create_command):
        with Db() as conn:
            cursor = conn.connector.cursor()
            cursor.execute("DROP TABLE IF EXISTS {};".format(create_command['table_name']))
            cursor.execute(create_command['create_table'])
            print('OK. Tabelas criadas com sucesso.')

    def load_table(self, query, tuples):
        with Db() as conn:
            cursor = conn.connector.cursor()
            cursor.executemany(query, tuples)
            print('OK. Tabelas carregadas com sucesso.')
    
    def load_table_avaliacao_usuarios(self, data_frame):
        with Db() as conn:
            data_frame.to_sql('avaliacao_usuarios', conn.connector)
            print('OK. Tabelas carregadas com sucesso.')

TABLE_CREATE_BOOKS = "books"

CREATE_BOOKS = {
        "table_name": TABLE_CREATE_BOOKS,
        "create_table": "CREATE TABLE {} (" \
              "Id integer PRIMARY KEY," \
              "ISBN integer NULL," \
              "Book_Title text NULL," \
              "Book_Author text NULL," \
              "Year_Of_Publication integer NULL," \
              "Publisher text NULL," \
              "Image text NULL" \
        ")".format(TABLE_CREATE_BOOKS)
        }


df = pd.read_csv("src/books_data/data/BX-Books.csv", sep=';', encoding="latin-1", error_bad_lines= False)
books = df[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]

avaliacao_usuarios = pd.read_csv('src/books_data/data/avaliacao_usuarios.csv')
avaliacao_usuarios['Id'] = avaliacao_usuarios.index

books = books.rename(columns={'Book-Title':'Book_Title',
'Book-Author':'Book_Author', 
'Year-Of-Publication':'Year_Of_Publication',
'Image-URL-L':'Image'
}).reindex()


books = books[books['Book_Title'].isin(avaliacao_usuarios['title'])].reindex()

books.drop_duplicates(subset=['Book_Title'], inplace=True)

books = books.reindex()
books['Id'] = books.index

tuples = [tuple(x) for x in books.to_numpy()]
cols = ','.join(list(books.columns))
INSERT_BOOKS  = "INSERT INTO  %s(%s) VALUES(?,?,?,?,?,?,?)" % (TABLE_CREATE_BOOKS, cols)


CriarBanco = CriarBanco()
CriarBanco.create_tables(CREATE_BOOKS)
CriarBanco.load_table(INSERT_BOOKS, tuples)
CriarBanco.load_table_avaliacao_usuarios(avaliacao_usuarios)