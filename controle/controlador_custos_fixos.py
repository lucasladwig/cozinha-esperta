from entidade.custos_fixos import CustosFixos
from limite.tela_custos_fixos import TelaCustosFixos
from persistencia.custos_fixos_dao import CustosFixosDAO


class ControladorCustosFixos():
    """Controlador de custos fixos."""    

    def __init__(self) -> None:
        self.__tela = TelaCustosFixos()
        self.__dao = CustosFixosDAO()
        self.__controlador_sistema = None

        # Instanciar custos fixos iniciais
        if len(self.dao.cache) == 0:
            custos_iniciais = CustosFixos(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
            self.dao.add(custos_iniciais)
        
    # GETTERS/SETTERS
    @property
    def tela(self):
        return self.__tela

    @property
    def dao(self):
        return self.__dao
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    # TELAS
    def abrir_tela(self):
        custos_atual = self.dao.get_last()
        
        while True:            
            self.tela.inicializar_tela(custos_atual)

    #CRUD
    def atualizar_custos_fixos(self) -> None:
        self.abrir_tela()

        if not novos_custos:
            raise ValueError

        custos_atual.agua = novos_custos["agua"]
        custos_atual.aluguel = novos_custos["aluguel"]
        custos_atual.eletricidade = novos_custos["eletricidade"]
        custos_atual.gas = novos_custos["gas"]
        custos_atual.manutencao = novos_custos["manutencao"]
        custos_atual.outro = novos_custos["outros"]

        self.__dao.add(custos_atual)

    def voltar(self):
        self.__controlador_sistema.abrir_tela()
