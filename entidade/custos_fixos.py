class CustosFixos:
    """Classe que guarda os custos fixos da cozinha."""

    # Garante que só haja uma instância da classe
    # __instancia = None
    # def __new__(cls):
    #     if cls.__instancia is None:
    #         cls.__instancia = super(CustosFixos, cls).__new__(cls)
    #     return cls.__instancia
    
    # ATRIBUTOS
    def __init__(self, 
                 agua: float, 
                 aluguel: float, 
                 eletricidade: float, 
                 gas: float, 
                 manuntencao: float, 
                 outros: float, 
                 porcoes_produzidas_mes: int) -> None:
        self.__agua = agua
        self.__aluguel = aluguel
        self.__eletricidade = eletricidade
        self.__gas = gas
        self.__manutencao = manuntencao
        self.__outros = outros
        self.__porcoes_produzidas_mes = porcoes_produzidas_mes
        self.__custo_fixo_total = sum([self.__agua,
                                      self.__aluguel,
                                      self.__eletricidade,
                                      self.__gas,
                                      self.__manutencao,
                                      self.__outros])
        self.__custo_fixo_por_porcao = (self.__custo_fixo_total /
                                        self.__porcoes_produzidas_mes)

    # GETTERS / SETTERS
    @property
    def agua(self) -> float:
        return self.__agua

    @agua.setter
    def agua(self, agua) -> None:
        if isinstance(agua, float) and agua >= 0.0:
            self.__agua = agua
            self.__atualizar_custos()

    @property
    def aluguel(self) -> float:
        return self.__aluguel

    @aluguel.setter
    def aluguel(self, aluguel) -> None:
        if isinstance(aluguel, float) and aluguel >= 0.0:
            self.__aluguel = aluguel
            self.__atualizar_custos()

    @property
    def eletricidade(self) -> float:
        return self.__eletricidade

    @eletricidade.setter
    def eletricidade(self, eletricidade) -> None:
        if isinstance(eletricidade, float) and eletricidade >= 0.0:
            self.__eletricidade = eletricidade
            self.__atualizar_custos()

    @property
    def gas(self) -> float:
        return self.__gas

    @gas.setter
    def gas(self, gas) -> None:
        if isinstance(gas, float) and gas >= 0.0:
            self.__gas = gas
            self.__atualizar_custos()

    @property
    def manutencao(self) -> float:
        return self.__manutencao

    @manutencao.setter
    def manutencao(self, manutencao) -> None:
        if isinstance(manutencao, float) and manutencao >= 0.0:
            self.__manutencao = manutencao
            self.__atualizar_custos()

    @property
    def outros(self) -> float:
        return self.__outros

    @outros.setter
    def outros(self, outros) -> None:
        if isinstance(outros, float) and outros >= 0.0:
            self.__outros = outros
            self.__atualizar_custos()

    @property
    def porcoes_produzidas_mes(self) -> int:
        return self.__porcoes_produzidas_mes

    @porcoes_produzidas_mes.setter
    def porcoes_produzidas_mes(self, porcoes_produzidas_mes) -> None:
        if isinstance(porcoes_produzidas_mes, int) and porcoes_produzidas_mes > 0:
            self.__porcoes_produzidas_mes = porcoes_produzidas_mes
            self.__atualizar_custos()

    @property
    def custo_fixo_total(self) -> float:
        return self.__custo_fixo_total

    @custo_fixo_total.setter
    def custo_fixo_total(self, custo_fixo_total) -> None:
        if isinstance(custo_fixo_total, float) and custo_fixo_total >= 0.0:
            self.__custo_fixo_total = custo_fixo_total

    @property
    def custo_fixo_por_porcao(self) -> float:
        return self.__custo_fixo_por_porcao

    @custo_fixo_por_porcao.setter
    def custo_fixo_por_porcao(self, custo_fixo_por_porcao) -> None:
        if isinstance(custo_fixo_por_porcao, float) and custo_fixo_por_porcao >= 0.0:
            self.__custo_fixo_por_porcao = custo_fixo_por_porcao

    # MÉTODOS AUXILIARES
    def __atualizar_custos(self) -> None:
        """Método utilizado para garantir que o valor total dos custos fixos seja atualizado quando qualquer outro item de custo (água, gás, etc.) é alterado."""
        self.__custo_fixo_total = sum([self.__agua,
                                    self.__aluguel,
                                    self.__eletricidade,
                                    self.__gas,
                                    self.__manutencao,
                                    self.__outros])
        self.__custo_fixo_por_porcao = (self.__custo_fixo_total /
                                      self.__porcoes_produzidas_mes)
