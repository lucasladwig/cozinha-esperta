from entidade.item_de_receita import ItemDeReceita
from entidade.insumo import Insumo


class Receita():
    """Entidade que representa a receita (ficha técnica), calculando os parâmteros gerais e instanciando itens de receita."""

    # ATRIBUTOS
    def __init__(self, codigo: str, nome: str, custo_fixo: float) -> None:
        self.__codigo = codigo
        self.__nome = nome
        self.__descricao = ""
        self.__rendimento_porcoes = 1   # Atualizar no diagrama de classes
        self.__tempo_preparo = 0        # Atualizar no diagrama de classes
        self.__validade = 0
        self.__modo_preparo = ""        # Atualizar no diagrama de classes
        self.__itens = []
        self.__calorias_porcao = 0
        self.__custo_total = 0.0
        self.__custo_porcao = 0.0
        self.__custo_fixo = custo_fixo

    # GETTERS / SETTERS
    # Identificação
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: str) -> None:
        if isinstance(codigo, str) and len(codigo) <= 10:
            self.__codigo = codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if isinstance(descricao, str):
            self.__descricao = descricao

    # Preparo, Rendimento e Validade
    @property
    def rendimento_porcoes(self) -> int:
        return self.__rendimento_porcoes

    @rendimento_porcoes.setter
    def rendimento_porcoes(self, rendimento_porcoes: int) -> None:
        if isinstance(rendimento_porcoes, int) and rendimento_porcoes > 0:
            self.__rendimento_porcoes = rendimento_porcoes

    @property
    def tempo_preparo(self) -> int:
        return self.__tempo_preparo

    @tempo_preparo.setter
    def tempo_preparo(self, tempo_preparo: int) -> None:
        if isinstance(tempo_preparo, int):
            self.__tempo_preparo = tempo_preparo

    @property
    def validade(self) -> int:
        return self.__validade

    @validade.setter
    def validade(self, validade: int) -> None:
        if isinstance(validade, int):
            self.__validade = validade

    @property
    def modo_preparo(self) -> str:
        return self.__modo_preparo

    @modo_preparo.setter
    def modo_preparo(self, modo_preparo: str) -> None:
        if isinstance(modo_preparo, str):
            self.__modo_preparo = modo_preparo

    # Lista de ingredientes - TALVEZ NÃO PRECISE SETTERS, NÃO PODE SER EDITADO DIRETAMENTE
    @property
    def itens(self) -> list:
        return self.__itens

    @itens.setter 
    def itens(self, itens: list) -> None:
        if isinstance(itens, list):
            self.__itens = itens

    # Calorias e Custos - TALVEZ NÃO PRECISE SETTERS, NÃO PODE SER EDITADO DIRETAMENTE
    @property
    def calorias_porcao(self) -> int:
        return self.__calorias_porcao

    # @calorias_porcao.setter
    # def calorias_porcao(self, calorias_porcao: int) -> None:
    #     if isinstance(calorias_porcao, int):
    #         self.__calorias_porcao = calorias_porcao

    @property
    def custo_total(self) -> float:
        return self.__custo_total

    # @custo_total.setter
    # def custo_total(self, custo_total: float) -> None:
    #     if isinstance(custo_total, float):
    #         self.__custo_total = custo_total

    @property
    def custo_porcao(self) -> float:
        return self.__custo_porcao

    # @custo_porcao.setter
    # def custo_porcao(self, custo_porcao: float) -> None:
    #     if isinstance(custo_porcao, float):
    #         self.__custo_porcao = custo_porcao

    @property
    def custo_fixo(self) -> float:
        return self.__custo_fixo

    # CRUD
    def incluir_item_em_receita(self, insumo_novo: Insumo) -> None:
        if isinstance(insumo_novo, Insumo):
            if self.__buscar_item_por_insumo(insumo_novo) is None:
                self.__itens.append(ItemDeReceita(insumo_novo))
                self.__atualiza_calorias()
                self.__atualiza_custos()
            else:
                raise ValueError
        else:
            raise TypeError

    def excluir_item_de_receita(self, insumo: Insumo) -> None:
        if isinstance(insumo, Insumo):
            item = self.__buscar_item_por_insumo(insumo)
            self.__itens.remove(item)
            self.__atualiza_calorias()
            self.__atualiza_custos()
        else:
            raise TypeError
    
    def alterar_insumo(self, insumo_antigo: Insumo, insumo_novo: Insumo) -> None:
        if isinstance(insumo_novo, Insumo) and isinstance(insumo_antigo, Insumo):
            item = self.__buscar_item_por_insumo(insumo_antigo)
            if item is None or self.__buscar_item_por_insumo(insumo_novo) is not None:
                raise ValueError
            item.insumo = insumo_novo
            self.__atualiza_calorias()
            self.__atualiza_custos()
        else:
            raise TypeError

    def alterar_quantidade(self, insumo: Insumo, quantidade: float) -> None:
        if isinstance(insumo, Insumo) and isinstance(quantidade, float):
            item = self.__buscar_item_por_insumo(insumo)
            if item is None:
                raise ValueError
            if item.calcula_por_qtd_bruta:
                item.qtd_bruta = quantidade
            else:
                item.qtd_limpa = quantidade
            self.__atualiza_calorias()
            self.__atualiza_custos()
        else:
            raise TypeError

    def alterar_fator_correcao(self, insumo: Insumo, fator: float) -> None:
        if isinstance(insumo, Insumo) and isinstance(fator, float):
            item = self.__buscar_item_por_insumo(insumo)
            if item is None:
                raise ValueError
            if fator > 0:
                item.fator_correcao = fator
            else:
                raise ValueError
            self.__atualiza_calorias()
            self.__atualiza_custos()
        else:
            raise TypeError

    def alterar_indice_coccao(self, insumo: Insumo, indice: float) -> None:
        if isinstance(insumo, Insumo) and isinstance(indice, float):
            item = self.__buscar_item_por_insumo(insumo)
            if item is None:
                raise ValueError
            if indice > 0:
                item.indice_coccao = indice
            else:
                raise ValueError
        else:
            raise TypeError

    # MÉTODOS AUXILIARES
    def __buscar_item_por_insumo(self, insumo: Insumo) -> Insumo:
        if isinstance(insumo, Insumo):
            for item in self.__itens:
                if item.insumo == insumo:
                    return item
        else:
            raise TypeError
    
    def __atualiza_custos(self) -> None:
        custo_total = 0
        for item in self.__itens:
            custo_total += item.custo
        
        self.__custo_total = custo_total
        self.__custo_porcao = (custo_total / self.__rendimento_porcoes) + self.__custo_fixo
    
    def __atualiza_calorias(self) -> None:
        calorias_total = 0
        for item in self.__itens:
            calorias_total += item.calorias
        
        self.__calorias_porcao = calorias_total / self.__rendimento_porcoes

    # MÉTODOS PÚBLICOS
    def listar_insumos_e_quantidades(self) -> dict:
        insumos_qtds = {}
        for item in self.__itens:
            insumos_qtds.update({item.insumo: item.qtd_bruta})
        return insumos_qtds

    def listar_dados_itens(self) -> list:
        dados_itens = []
        for item in self.__itens:
            dados_itens.append(item.insumo.nome)
            dados_itens.append(item.insumo.unidade)
            dados_itens.append(item.qtd_bruta)
            dados_itens.append(item.fator_correcao)
            dados_itens.append(item.qtd_limpa)
            dados_itens.append(item.indice_coccao)
            dados_itens.append(item.qtd_pronta)
            dados_itens.append(item.calorias)
            dados_itens.append(item.custo)

        return dados_itens
