from entidade.custos_fixos import CustosFixos
from limite.tela_custos_fixos import TelaCustosFixos
from persistencia.custos_fixos_dao import CustosFixosDAO


class ControladorCustosFixos:
    def __init__(self) -> None:
        self.__custos_fixos = CustosFixosDAO()
        self.__tela_custos_fixos = TelaCustosFixos()
        # self.__controlador_sistema = controlador_sistema
    
    def atualizar_custos_fixos(self, custos: dict) -> None:
        pass
