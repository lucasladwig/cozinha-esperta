from persistencia.dao import DAO
from entidade.custos_fixos import CustosFixos


class CustosFixosDAO(DAO):
    def __init__(self):
        super().__init__('custos_fixos.pkl')

    def add(self, custos_fixos: CustosFixos):
        if isinstance(custos_fixos, CustosFixos) and len(self.__cache) == 0:
            super().add(1, custos_fixos)

    def get(self, chave: int):
        if isinstance(chave, int):
            return super().get(chave)

    def update(self, chave, objeto: object):
        if (objeto is not None 
                and isinstance(objeto, CustosFixos)
                and self.__cache[chave] != None):
            self.__cache[chave] = objeto
            self.__dump()

    def remove(self, chave: int):
        if isinstance(chave, int):
            return super().remove(chave)
