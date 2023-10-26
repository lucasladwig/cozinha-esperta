from persistencia.dao import DAO
from entidade.custos_fixos import CustosFixos


class CustosFixosDAO(DAO):
    def __init__(self):
        super().__init__('dados/custos_fixos.pkl')

    def add(self, custos_fixos: CustosFixos):
        if isinstance(custos_fixos, CustosFixos):
            super().add(len(self.cache)+1, custos_fixos)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def get_last(self):
        """Retorna o último objeto instanciado."""
        return super().get(len(self.cache))

    def update(self, objeto: CustosFixos):
        if (objeto is not None
                and isinstance(objeto, CustosFixos)
                and self.cache[len(self.cache)] is not None):
            self.cache[len(self.cache)] = objeto
            self.__dump()

    def remove(self, chave: int):
        if isinstance(chave, int):
            return super().remove(chave)
