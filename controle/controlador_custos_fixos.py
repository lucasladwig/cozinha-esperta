from entidade.custos_fixos import CustosFixos
from limite.tela_custos_fixos import TelaCustosFixos
from persistencia.custos_fixos_dao import CustosFixosDAO


class ControladorCustosFixos():
    """Controlador de custos fixos."""

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
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
    def abrir_tela(self) -> None:
        while True:
            try:
                # custos_atuais = self.dao.get_last()
                custos_atuais = self.dao.get()
                botao, novos_custos = self.tela.open(custos_atuais)
                if botao == "Atualizar e Salvar":
                    custos_atualizados = self.atualizar_custos_fixos(novos_custos)
                    self.tela.close()
                    self.tela.open(custos_atualizados)
                elif botao == "Sair":
                    break
                    # self.tela.close()

                self.tela.close()
                # self.tela.init_components()
            except ValueError:
                self.tela.close()
                self.tela.mostrar_mensagem("Por favor, insira valores numéricos para os custos!",
                                           titulo="Erro ao atualizar custos")

    # CRUD
    def atualizar_custos_fixos(self, novos_custos: dict) -> CustosFixos:
        if novos_custos is None:
            raise ValueError

        # custos_atual = self.dao.get_last()
        custos_atual = self.dao.get()

        custos_atual.agua = novos_custos["agua"]
        custos_atual.aluguel = novos_custos["aluguel"]
        custos_atual.eletricidade = novos_custos["eletricidade"]
        custos_atual.gas = novos_custos["gas"]
        custos_atual.manutencao = novos_custos["manutencao"]
        custos_atual.outros = novos_custos["outros"]
        custos_atual.porcoes_produzidas_mes = novos_custos["producao_mensal"]

        self.dao.add(custos_atual)

        return custos_atual

    # MÉTODOS PÚBLICOS
    def enviar_custo_fixo_porcao(self) -> float:
        return self.dao.get_last().custo_fixo_por_porcao