from controle.controlador import Controlador
# from controle.controlador_insumos import ControladorInsumos
# from controle.controlador_estoque import ControladorEstoque
# from controle.controlador_custos_fixos import ControladorCustosFixos
from limite.tela_sistema import TelaSistema


class ControladorSistema(Controlador):
    """Controlador do sistema, gerencia o acesso a todos os módulos do sistema."""

    def __init__(self) -> None:
        super().__init__(TelaSistema(), None)
        # self.__controlador_insumos = ControladorInsumos(self)
        # self.__controlador_estoque = ControladorEstoque(self)
        # self.__controlador_custos_fixos = ControladorCustosFixos(self)

    # @property
    # def controlador_insumos(self):
    #    return self.__controlador_insumos

    # @property
    # def controlador_estoque(self):
    #    return self.__controlador_estoque

    # @property
    # def controlador_custos_fixos(self):
    #     isinstance()
    #     return self.__controlador_custos_fixos

    def abrir_tela(self):
        modulos = { # 1: self.abrir_modulo_insumos,
                    # 2: self.abrir_modulo_estoque,
                    # 3: self.abrir_modulo_custos_fixos,
                    0: self.retornar }

        while True:
            modulos[self.tela.tela_opcoes()]()

    def inicializar_sistema(self):
        self.abrir_tela()

    def abrir_modulo_insumos(self):
        self.controlador_insumos.abrir_tela()

    def abrir_modulo_estoque(self):
        self.controlador_estoque.abrir_tela()

    def abrir_modulo_custos_fixos(self):
        self.controlador_custos_fixos.abrir_tela()

    def retornar(self):
        exit(0)
