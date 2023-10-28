from persistencia.dao import DAO
from entidade.producao import Producao


class ProducaoDAO(DAO):
    def __init__(self):
        super().__init__('insumo.pkl')

    def add(self, producao: Producao):
        if isinstance(producao, Producao) and isinstance(producao.nome, str):
            super().add(producao.nome, producao)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
