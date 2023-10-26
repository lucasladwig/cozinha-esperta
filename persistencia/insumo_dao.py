from persistencia.dao import DAO
from entidade.insumo import Insumo


class InsumoDAO(DAO):
    def __init__(self):
        super().__init__('insumo.pkl')

    def add(self, insumo: Insumo):
        if isinstance(insumo, Insumo) and isinstance(insumo.nome, str):
            super().add(insumo.nome, insumo)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)