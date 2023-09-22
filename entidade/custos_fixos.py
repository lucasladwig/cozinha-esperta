class CustosFixos:
    """Classe que guarda os itens de custo fixo da cozinha. Só haverá uma instância desta classe no controlador."""

    # CONSTRUTOR
    def __init__(self) -> None:
        self.__custo_agua = 0.0
        self.__custo_aluguel = 0.0
        self.__custo_eletricidade = 0.0
        self.__custo_gas = 0.0
        self.__custo_outros = 0.0
        self.__porcoes_produzidas_mes = 1
        self.__custo_fixo_total = sum(self.__custo_agua,
                                      self.__custo_aluguel,
                                      self.__custo_eletricidade,
                                      self.__custo_gas,
                                      self.__custo_outros)
        self.__custo_fixo_por_porcao = (self.__custo_fixo_total /
                                        self.__porcoes_produzidas_mes)

    # GETTERS / SETTERS
    @property
    def custo_agua(self) -> float:
        return self.__custo_agua

    @custo_agua.setter
    def custo_agua(self, custo_agua) -> None:
        if isinstance(custo_agua, float) and custo_agua >= 0.0:
            self.__custo_agua = custo_agua
            self.__atualiza_custos()

    @property
    def custo_aluguel(self) -> float:
        return self.__custo_aluguel

    @custo_aluguel.setter
    def custo_aluguel(self, custo_aluguel) -> None:
        if isinstance(custo_aluguel, float) and custo_aluguel >= 0.0:
            self.__custo_aluguel = custo_aluguel
            self.__atualiza_custos()

    @property
    def custo_eletricidade(self) -> float:
        return self.__custo_eletricidade

    @custo_eletricidade.setter
    def custo_eletricidade(self, custo_eletricidade) -> None:
        if isinstance(custo_eletricidade, float) and custo_eletricidade >= 0.0:
            self.__custo_eletricidade = custo_eletricidade
            self.__atualiza_custos()

    @property
    def custo_gas(self) -> float:
        return self.__custo_gas

    @custo_gas.setter
    def custo_gas(self, custo_gas) -> None:
        if isinstance(custo_gas, float) and custo_gas >= 0.0:
            self.__custo_gas = custo_gas
            self.__atualiza_custos()

    @property
    def custo_outros(self) -> float:
        return self.__custo_outros

    @custo_outros.setter
    def custo_outros(self, custo_outros) -> None:
        if isinstance(custo_outros, float) and custo_outros >= 0.0:
            self.__custo_outros = custo_outros
            self.__atualiza_custos()

    @property
    def porcoes_produzidas_mes(self) -> int:
        return self.__porcoes_produzidas_mes

    @porcoes_produzidas_mes.setter
    def porcoes_produzidas_mes(self, porcoes_produzidas_mes) -> None:
        if isinstance(porcoes_produzidas_mes, int) and porcoes_produzidas_mes > 0:
            self.__porcoes_produzidas_mes = porcoes_produzidas_mes
            self.__atualiza_custos()

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
    def __atualiza_custos(self) -> None:
        self.custo_fixo_total = sum(self.__custo_agua,
                                    self.__custo_aluguel,
                                    self.__custo_eletricidade,
                                    self.__custo_gas,
                                    self.__custo_outros)
        self.custo_fixo_por_porcao = (self.__custo_fixo_total /
                                      self.__porcoes_produzidas_mes)
