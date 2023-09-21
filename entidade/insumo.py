class Insumo():
    def __init__(self, calorias_por_unidade: int, custo_unitario: float, estoque_atual: float, estoque_minimo: float, id_insumo: int, nome: str, unidade: str) -> None:
        self.__calorias_por_unidade = None
        self.__custo_unitario = None
        self.__estoque_atual = None
        self.__estoque_minimo = None
        self.__id_insumo = None
        self.__nome = None
        self.__unidade = None
        if isinstance(calorias_por_unidade, int):
            self.__calorias_por_unidade = calorias_por_unidade
        if isinstance(custo_unitario, float):
            self.__custo_unitario = custo_unitario
        if isinstance(estoque_atual, float):
            self.__estoque_atual = estoque_atual
        if isinstance(estoque_minimo, float):
            self.__estoque_minimo = estoque_minimo
        if isinstance(id_insumo, int):
            self.__id_insumo = id_insumo
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(unidade, str):
            self.__unidade = unidade

    @property
    def calorias_por_unidade(self) -> int:
        return self.__calorias_por_unidade

    @calorias_por_unidade.setter
    def calorias_por_unidade(self, calorias_por_unidade):
        if isinstance(calorias_por_unidade, int):
            self.__calorias_por_unidade = calorias_por_unidade

    @property
    def custo_unitario(self) -> float:
        return self.__custo_unitario

    @custo_unitario.setter
    def custo_unitario(self, custo_unitario):
        if isinstance(custo_unitario, float):
            self.__custo_unitario = custo_unitario

    @property
    def estoque_atual(self) -> float:
        return self.__estoque_atual

    @estoque_atual.setter
    def estoque_atual(self, estoque_atual):
        if isinstance(estoque_atual, float):
            self.__estoque_atual = estoque_atual

    @property
    def estoque_minimo(self) -> float:
        return self.__estoque_minimo

    @estoque_minimo.setter
    def estoque_minimo(self, estoque_minimo):
        if isinstance(estoque_minimo, float):
            self.__estoque_minimo = estoque_minimo

    @property
    def id_insumo(self) -> int:
        return self.__id_insumo

    @id_insumo.setter
    def id_insumo(self, id_insumo):
        if isinstance(id_insumo, int):
            self.__id_insumo = id_insumo

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def unidade(self) -> str:
        return self.__unidade

    @unidade.setter
    def unidade(self, unidade):
        if isinstance(unidade, str):
            self.__unidade = unidade
