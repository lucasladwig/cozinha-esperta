from entidade.item_de_receita import ItemDeReceita
from entidade.receita import Receita
from entidade.insumo import Insumo
from persistencia.receita_dao import ReceitaDAO
from limite.tela_receita import TelaReceita


class ControladorReceita:
    def __init__(self) -> None:
        self.__tela = TelaReceita()
        self.__dao = ReceitaDAO()


    # TELAS
