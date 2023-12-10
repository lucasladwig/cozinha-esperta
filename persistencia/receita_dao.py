from persistencia.dao import DAO
from entidade.receita import Receita

class ReceitaDAO(DAO):
    def __init__(self):
        super().__init__('dados/receitas.pkl')

    def add(self, receita: Receita):
        if isinstance(receita, Receita) and isinstance(receita.codigo, str):
            super().add(receita.codigo, receita)

    def get(self, chave: str):
        if isinstance(chave, str):
            return super().get(chave)

    def remove(self, chave: str):
        if isinstance(chave, str):
            return super().remove(chave)
