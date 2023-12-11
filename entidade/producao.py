from datetime import date
import random


class Producao:
    def __init__(self, receita, custo_total_producao: float, data_producao: date, numero_porcoes: int, status: str) -> None:
        self.__id = str(random.randint(1, 1000000))
        self.__receita = receita
        self.__custo_total_producao = custo_total_producao
        self.__data_producao = data_producao
        self.__numero_porcoes = numero_porcoes
        self.__status = status

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def receita(self):
        return self.__receita

    @receita.setter
    def receita(self, receita):
        self.__receita = receita

    @property
    def custo_total_producao(self):
        return self.__custo_total_producao

    @custo_total_producao.setter
    def custo_total_producao(self, ctp):
        self.__custo_total_producao = ctp

    @property
    def data_producao(self):
        return self.__data_producao

    @data_producao.setter
    def data_producao(self, dp):
        self.__data_producao = dp

    @property
    def numero_porcoes(self):
        return self.__numero_porcoes

    @numero_porcoes.setter
    def numero_porcoes(self, np):
        self.__numero_porcoes = np

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status
