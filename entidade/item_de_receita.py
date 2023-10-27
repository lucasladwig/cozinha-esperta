from entidade.insumo import Insumo


class ItemDeReceita():
    """[REVER DESCRIÇÃO] Instancia as informações de um insumo na receita."""

    # ATRIBUTOS
    def __init__(self,
                 insumo: Insumo,
                 fator_correcao: float,
                 indice_coccao: float,
                 qtd_bruta: float,
                 qtd_limpa: float,
                 qtd_pronta: float,
                 calorias: float,
                 custo: float) -> None:
        self.__insumo = insumo
        self.__unidade = self.__insumo.unidade  # Atualizar no diagrama de classe
        self.__fator_correcao = fator_correcao
        self.__indice_coccao = indice_coccao
        self.__qtd_bruta = qtd_bruta            # Atualizar no diagrama de classe
        self.__qtd_limpa = qtd_limpa            # Atualizar no diagrama de classe
        self.__qtd_pronta = qtd_pronta          # Atualizar no diagrama de classe
        self.__calorias = calorias
        self.__custo = custo

    # GETTERS / SETTERS
    @property
    def insumo(self) -> float:
        return self.__insumo

    @insumo.setter
    def insumo(self, insumo: Insumo) -> None:
        if isinstance(insumo, Insumo):
            self.__insumo = insumo

    @property
    def fator_correcao(self) -> float:
        return self.__fator_correcao

    @fator_correcao.setter
    def fator_correcao(self, fator_correcao: float) -> None:
        if isinstance(fator_correcao, float):
            self.__fator_correcao = fator_correcao

    @property
    def indice_coccao(self) -> float:
        return self.__indice_coccao

    @indice_coccao.setter
    def indice_coccao(self, indice_coccao: float) -> None:
        if isinstance(indice_coccao, float):
            self.__indice_coccao = indice_coccao

    @property
    def qtd_bruta(self) -> float:
        return self.__qtd_bruta

    @qtd_bruta.setter
    def qtd_bruta(self, qtd_bruta: float) -> None:
        if isinstance(qtd_bruta, float):
            self.__qtd_bruta = qtd_bruta

    @property
    def qtd_limpa(self) -> float:
        return self.__qtd_limpa

    @qtd_limpa.setter
    def qtd_limpa(self, qtd_limpa: float) -> None:
        if isinstance(qtd_limpa, float):
            self.__qtd_limpa = qtd_limpa

    @property
    def qtd_pronta(self) -> float:
        return self.__qtd_pronta

    @qtd_pronta.setter
    def qtd_pronta(self, qtd_pronta: float) -> None:
        if isinstance(qtd_pronta, float):
            self.__qtd_pronta = qtd_pronta

    @property
    def calorias(self) -> float:
        return self.__calorias

    @calorias.setter
    def calorias(self, calorias: float) -> None:
        if isinstance(calorias, float):
            self.__calorias = calorias

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float) -> None:
        if isinstance(custo, float):
            self.__custo = custo

    # MÉTODOS AUXILIARES
    def __atualizar_custos_calorias(self) -> float:
        self.__custo = self.__qtd_bruta * self.__insumo.custo_unitario
        self.__calorias = self.__qtd_limpa * self.__insumo.caloria_por_unidade

    def __atualizar_qtd_bruta_por_qtd_limpa(self) -> float:
        self.__qtd_bruta = self.__qtd_limpa * self.__fator_correcao
    
    def __atualizar_qtd_limpa_por_qtd_bruta(self) -> float:
        self.__qtd_limpa = self.__qtd_bruta / self.__fator_correcao
    
    def __atualizar_qtd_pronta(self) -> float:
        self.__qtd_pronta = self.__qtd_limpa * self.__indice_coccao
