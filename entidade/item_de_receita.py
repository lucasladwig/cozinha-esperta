from entidade.insumo import Insumo


class ItemDeReceita():
    """[REVER DESCRIÇÃO] Instancia as informações de um insumo na receita."""

    # ATRIBUTOS
    def __init__(self, insumo: Insumo) -> None:
        self.__insumo = insumo
        self.__fator_correcao = 1.0
        self.__indice_coccao = 1.0
        self.__calcula_por_qtd_bruta = True # Atualizar no diagrama de classe
        self.__qtd_bruta = 0.0              # Atualizar no diagrama de classe
        self.__qtd_limpa = 0.0              # Atualizar no diagrama de classe
        self.__qtd_pronta = 0.0             # Atualizar no diagrama de classe
        self.__calorias = 0
        self.__custo = 0.0

    # GETTERS / SETTERS
    # Ingrediente
    @property
    def insumo(self) -> float:
        return self.__insumo

    @insumo.setter
    def insumo(self, insumo: Insumo) -> None:
        if isinstance(insumo, Insumo):
            self.__insumo = insumo
            self.__atualizar_custo()
            self.__atualizar_calorias()

    # Fatores para cálculo
    @property
    def fator_correcao(self) -> float:
        return self.__fator_correcao

    @fator_correcao.setter
    def fator_correcao(self, fator_correcao: float) -> None:
        if isinstance(fator_correcao, float) and fator_correcao > 0:
            self.__fator_correcao = fator_correcao
            if self.__calcula_por_qtd_bruta:
                self.__atualizar_qtd_limpa()
            else:
                self.__atualizar_qtd_bruta()
            self.__atualizar_qtd_pronta()
            self.__atualizar_custo()
            self.__atualizar_calorias()

    @property
    def indice_coccao(self) -> float:
        return self.__indice_coccao

    @indice_coccao.setter
    def indice_coccao(self, indice_coccao: float) -> None:
        if isinstance(indice_coccao, float) and indice_coccao > 0:
            self.__indice_coccao = indice_coccao
            self.__atualizar_qtd_pronta()

    @property
    def calcula_por_qtd_bruta(self) -> bool:
        return self.__calcula_por_qtd_bruta

    @calcula_por_qtd_bruta.setter
    def calcula_por_qtd_bruta(self, calcula_por_qtd_bruta: bool) -> None:
        if isinstance(calcula_por_qtd_bruta, bool):
            self.__calcula_por_qtd_bruta = calcula_por_qtd_bruta

    # Quantidades
    @property
    def qtd_bruta(self) -> float:
        return self.__qtd_bruta

    @qtd_bruta.setter
    def qtd_bruta(self, qtd_bruta: float) -> None:
        if isinstance(qtd_bruta, float) and qtd_bruta > 0:
            self.__qtd_bruta = qtd_bruta
            self.__atualizar_qtd_limpa()
            self.__atualizar_qtd_pronta()
            self.__atualizar_custo()
            self.__atualizar_calorias()

    @property
    def qtd_limpa(self) -> float:
        return self.__qtd_limpa

    @qtd_limpa.setter
    def qtd_limpa(self, qtd_limpa: float) -> None:
        if isinstance(qtd_limpa, float) and qtd_limpa > 0:
            self.__qtd_limpa = qtd_limpa
            self.__atualizar_qtd_pronta()
            self.__atualizar_calorias()

    @property
    def qtd_pronta(self) -> float:
        return self.__qtd_pronta

    @qtd_pronta.setter
    def qtd_pronta(self, qtd_pronta: float) -> None:
        if isinstance(qtd_pronta, float) and qtd_pronta > 0:
            self.__qtd_pronta = qtd_pronta

    # Custos e calorias - TALVEZ NÃO PRECISE SETTERS, NÃO PODE SER EDITADO DIRETAMENTE
    @property
    def calorias(self) -> float:
        return self.__calorias

    # @calorias.setter
    # def calorias(self, calorias: float) -> None:
    #     if isinstance(calorias, float) and calorias >= 0:
    #         self.__calorias = calorias

    @property
    def custo(self) -> float:
        return self.__custo

    # @custo.setter
    # def custo(self, custo: float) -> None:
    #     if isinstance(custo, float) and custo >= 0:
    #         self.__custo = custo

    # MÉTODOS AUXILIARES
    def __atualizar_qtd_bruta(self) -> None:
        self.__qtd_bruta = round(self.__qtd_limpa * self.__fator_correcao, 2)

    def __atualizar_qtd_limpa(self) -> None:
        self.__qtd_limpa = round(self.__qtd_bruta / self.__fator_correcao, 2)

    def __atualizar_qtd_pronta(self) -> None:
        self.__qtd_pronta = round(self.__qtd_limpa * self.__indice_coccao, 2)

    def __atualizar_custo(self) -> None:
        self.__custo = round(self.__qtd_bruta * self.__insumo.custo_unitario, 2)

    def __atualizar_calorias(self) -> None:
        self.__calorias = round(self.__qtd_limpa * self.__insumo.calorias_por_unidade, 2)
