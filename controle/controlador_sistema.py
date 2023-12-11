from controle.controlador_insumo import ControladorInsumo
from controle.controlador_estoque_insumo import ControladorEstoqueInsumo
from controle.controlador_receitas import ControladorReceitas
from controle.controlador_filtro_receitas import ControladorFiltroReceitas
from controle.controlador_custos_fixos import ControladorCustosFixos
from controle.controlador_producao import ControladorProducao
from controle.controlador_lista_de_compras import ControladorListaDeCompras
from controle.controlador_etiqueta import ControladorEtiqueta
from controle.controlador_relatorio_de_custos import ControladorRelatorioDeCustos


from limite.tela_sistema import TelaSistema


class ControladorSistema():
    """Controlador do sistema, gerencia o acesso a todos os módulos do sistema."""

    __MODULOS = [
        ["Insumos", "Gerencie os tipos de insumos com os quais sua cozinha trabalha.", ],
        ["Estoque", "Gerencie estoque e custos dos seus insumos.", ],
        ["Receitas", "Gerencie suas receitas e fichas técnicas.", ],
        ["Produções", "Planeje suas produções.", ],
        ["Lista de Compras", "Gere uma lista de compras com base em uma produção.", ],
        ["Relatórios de Custos", "Veja um relatório de custos de um período.", ],
        ["Custos Fixos", "Insira os custos fixos da sua cozinha para calcular de custos de seus pratos.", ],
        ["Etiquetas", "Gere um arquivo de texto com as informações essenciais para uma etiqueta.", ],
        ["Filtrar Receitas", "Filtre receitas cadastradas a partir de custo, calorias ou estoque.", ],
    ]

    def __init__(self) -> None:
        self.__controlador_insumo = ControladorInsumo(self)
        self.__controlador_estoque_insumo = ControladorEstoqueInsumo(self)
        self.__controlador_receitas = ControladorReceitas(self)
        self.__controlador_producao = ControladorProducao(self)
        self.__controlador_lista_compras = ControladorListaDeCompras(self)
        self.__controlador_custos_fixos = ControladorCustosFixos(self)
        self.__controlador_filtro_receitas = ControladorFiltroReceitas(self)
        self.__controlador_etiqueta = ControladorEtiqueta(self)
        self.__controlador_relatorio_de_custos = ControladorRelatorioDeCustos(self)

        self.__tela_sistema = TelaSistema()

    @property
    def controlador_insumo(self):
        return self.__controlador_insumo

    @property
    def controlador_estoque_insumo(self):
        return self.__controlador_estoque_insumo

    @property
    def controlador_receitas(self):
        return self.__controlador_receitas

    @property
    def controlador_filtro_receitas(self):
        return self.__controlador_filtro_receitas

    @property
    def controlador_producao(self):
        return self.__controlador_producao

    @property
    def controlador_lista_compras(self):
        return self.__controlador_lista_compras

    @property
    def controlador_custos_fixos(self):
        return self.__controlador_custos_fixos

    @property
    def controlador_relatorio_de_custos(self):
       return self.__controlador_relatorio_de_custos

    @property
    def controlador_etiquetas(self):
       return self.__controlador_etiquetas

    def abrir_tela(self):
        modulos = {
            "Insumos": self.controlador_insumo.abre_tela,
            "Estoque": self.controlador_estoque_insumo.abre_tela,
            "Receitas": self.controlador_receitas.abrir_tela_gerenciador,
            "Producoes": self.controlador_producao.abre_tela,
            "Lista de Compras": self.controlador_lista_compras.abre_tela,
            "Relatórios de Custos": self.controlador_relatorio_de_custos.abrir_tela,
            "Custos Fixos": self.controlador_custos_fixos.abrir_tela,
            "Etiquetas": self.__controlador_etiqueta.abre_tela,
            "Filtrar Receitas": self.controlador_filtro_receitas.abrir_tela,
            "Sair": self.sair
        }

        while True:
            modulo_escolhido = self.__tela_sistema.abrir_tela(ControladorSistema.__MODULOS)
            modulos[modulo_escolhido]()

    def inicializar_sistema(self):
        self.abrir_tela()

    def sair(self):
        exit(0)
