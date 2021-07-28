
import numpy as np
from pandas import DataFrame
from flask import Flask, jsonify
import pickle
from src.books_data.avaliacoes_repository import AvaliacoesRepository

AvaliacoesRepository = AvaliacoesRepository()
## carregando o modelo para o código
with open("src\\books_api\\model.sav","rb") as f:
    #Carrega o arquivo model.pickle em modo read binary
    modelo_carregado = pickle.load(f)

app = Flask(__name__)

@app.route("/")
class MainClass():

    @app.route("/api/v1/get-suggestions/<title>", methods=['GET'])
    def get_suggestions(title): 
        avaliacoes = list(AvaliacoesRepository.get_book(title))
        book_pivot = DataFrame([avaliacoes[2:-1]])
        distances, suggestions = modelo_carregado.kneighbors(book_pivot.iloc[0, :].values.reshape(1, -1))
        
        suggestion_books = list()
        for index in suggestions[0]:
            suggestion_book = AvaliacoesRepository.get_book_title(index)
            suggestion_books.append(suggestion_book[0])
        
        return {"suggestion_books" : suggestion_books}

    if __name__ == "__main__":
        debug = True # com essa opção como True, ao salvar, o "site" recarrega automaticamente.
        app.run(debug=debug)