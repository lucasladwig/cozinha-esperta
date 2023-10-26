from controle.controlador import Controlador
from controle.controlador_insumo import ControladorInsumo
from controle.controlador_estoque_insumo import ControladorEstoqueInsumo
from controle.controlador_custos_fixos import ControladorCustosFixos
from limite.tela_sistema import TelaSistema


class ControladorSistema(Controlador):
    """Controlador do sistema, gerencia o acesso a todos os módulos do sistema."""

    def __init__(self) -> None:
        super().__init__(tela=TelaSistema(), controlador_sistema=None)
        self.__controlador_insumo = ControladorInsumo()
        self.__controlador_estoque_insumo = ControladorEstoqueInsumo()
        # self.__controlador_receitas = ControladorReceitas()
        # self.__controlador_producoes = ControladorProducoes()
        # self.__controlador_lista_compras = ControladorListaCompras()
        # self.__controlador_relatorios_custos = ControladorRelatoriosCustos()
        self.__controlador_custos_fixos = ControladorCustosFixos(self)
        # self.__controlador_etiquetas = ControladorEtiquetas()

    @property
    def controlador_insumo(self):
        return self.__controlador_insumo

    @property
    def controlador_estoque_insumo(self):
        return self.__controlador_estoque_insumo

    # @property
    # def controlador_receitas(self):
    #    return self.__controlador_receitas

    # @property
    # def controlador_producoes(self):
    #    return self.__controlador_producoes

    # @property
    # def controlador_lista_compras(self):
    #    return self.__controlador_lista_compras

    # @property
    # def controlador_relatorios_custos(self):
    #    return self.__controlador_relatorios_custos

    @property
    def controlador_custos_fixos(self):
        return self.__controlador_custos_fixos

    # @property
    # def controlador_etiquetas(self):
    #    return self.__controlador_etiquetas

    def abrir_tela(self):
        modulos = {
            "Insumos": self.controlador_insumos.abrir_tela,
            "Estoque": self.controlador_estoque_insumo.abrir_tela,
            "Receitas": self.controlador_receitas.abrir_tela,
            "Producoes": self.controlador_producoes.abrir_tela,
            "Lista de Compras": self.controlador_lista_compras.abrir_tela,
            "Relatorios de Custos": self.controlador_relatorios_custos.abrir_tela,
            "Custos Fixos": self.controlador_custos_fixos.abrir_tela,
            "Etiquetagem": self.controlador_etiqueteas.abrir_tela,
            "Voltar": self.voltar
        }

        while True:
            modulos[self.tela.inicializar_tela()]()

    def inicializar_sistema(self):
        self.abrir_tela()

    def voltar(self):
        exit(0)
