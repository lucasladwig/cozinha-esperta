from entidade.insumo_teste import Insumo


class ItemDeListaDeCompras:
    def __init__(self, insumo: Insumo, quantidade: float) -> None:
        self.__insumo = None
        self.__quantidade = None
        if isinstance(insumo, Insumo):
            self.__insumo = insumo
        if isinstance(quantidade, float):
            self.__quantidade = quantidade

    @property
    def insumo(self) -> Insumo:
        return self.__insumo

    @insumo.setter
    def insumo(self, insumo: Insumo) -> None:
        if isinstance(insumo, Insumo):
            self.__insumo = insumo

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade) -> None:
        if isinstance(quantidade, float):
            self.__quantidade = quantidade
