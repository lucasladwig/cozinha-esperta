from entidade.item_de_receita import ItemDeReceita
from entidade.insumo import Insumo


class Receita():
    """Entidade que representa a receita (ficha técnica), calculando os parâmteros gerais e instanciando itens de receita."""

    # ATRIBUTOS
    def __init__(self,
                 codigo: str = "",
                 nome: str = "",
                 descricao: str = "",
                 rendimento_porcoes: int = 1,
                 tempo_preparo: int = 1,
                 validade: int = 1,
                 modo_preparo: str = "",
                 custo_fixo: float = 0.0,
                 ) -> None:

        self.__codigo = codigo
        self.__nome = nome
        self.__descricao = descricao
        self.__rendimento_porcoes = rendimento_porcoes
        self.__tempo_preparo = tempo_preparo
        self.__validade = validade
        self.__modo_preparo = modo_preparo
        self.__custo_fixo = custo_fixo

        # Lista de itens de receita
        self.__itens = []

        # Atributos calculados
        self.__calorias_porcao = 0
        self.__custo_total = 0.0
        self.__custo_porcao = 0.0

    # GETTERS / SETTERS
    # Identificação
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: str) -> None:
        if isinstance(codigo, str) and 0 < len(codigo) <= 10:
            self.__codigo = codigo
        else:
            raise ValueError("Insira um código de até 10 caracteres!")

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
        if isinstance(rendimento_porcoes, int):
            if rendimento_porcoes > 0:
                self.__rendimento_porcoes = rendimento_porcoes
            else:
                raise ValueError(
                    "Rendimento deve ser valor inteiro maior que zero!")
        else:
            raise TypeError("Rendimento deve ser um número inteiro!")

    @property
    def tempo_preparo(self) -> int:
        return self.__tempo_preparo

    @tempo_preparo.setter
    def tempo_preparo(self, tempo_preparo: int) -> None:
        if isinstance(tempo_preparo, int):
            if tempo_preparo > 0:
                self.__tempo_preparo = tempo_preparo
            else:
                raise ValueError(
                    "Tempo de preparo deve ser valor inteiro maior que zero!")
        else:
            raise TypeError("Tempo de preparo deve ser um número inteiro!")

    @property
    def validade(self) -> int:
        return self.__validade

    @validade.setter
    def validade(self, validade: int) -> None:
        if isinstance(validade, int):
            if validade >= 0:
                self.__validade = validade
            else:
                raise ValueError(
                    "Validade deve ser valor inteiro maior que zero!")
        else:
            raise TypeError("Validade deve ser um número inteiro!")

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
            self.__atualizar_calorias()
            self.__atualizar_custos()

    # Calorias e Custos - TALVEZ NÃO PRECISE SETTERS, NÃO DEVE SER EDITADO DIRETAMENTE
    @property
    def calorias_porcao(self) -> int:
        return self.__calorias_porcao

    @calorias_porcao.setter
    def calorias_porcao(self, calorias_porcao: int) -> None:
        if isinstance(calorias_porcao, int):
            self.__calorias_porcao = calorias_porcao

    @property
    def custo_total(self) -> float:
        return self.__custo_total

    @custo_total.setter
    def custo_total(self, custo_total: float) -> None:
        if isinstance(custo_total, float):
            self.__custo_total = custo_total

    @property
    def custo_porcao(self) -> float:
        return self.__custo_porcao

    @custo_porcao.setter
    def custo_porcao(self, custo_porcao: float) -> None:
        if isinstance(custo_porcao, float):
            self.__custo_porcao = custo_porcao

    @property
    def custo_fixo(self) -> float:
        return self.__custo_fixo

    # CRUD
    def adicionar_item_de_receita(self, item_novo: ItemDeReceita) -> None:
        if isinstance(item_novo, ItemDeReceita):
            if self.__buscar_item_por_insumo(item_novo.insumo) is None:
                self.__itens.append(item_novo)
                self.__atualizar_calorias()
                self.__atualizar_custos()
            else:
                raise ValueError("Insumo já existe na receita!")
        else:
            raise TypeError("Parâmetro não é do tipo item de receita!")

    def substituir_item_de_receita(self, item_novo: ItemDeReceita, item_antigo: ItemDeReceita) -> None:
        if isinstance(item_novo, ItemDeReceita) and isinstance(item_antigo, ItemDeReceita):
            if self.__buscar_item_por_insumo(item_novo.insumo) is None:
                self.__itens.remove(item_antigo)
                self.__itens.append(item_novo)
                self.__atualizar_calorias()
                self.__atualizar_custos()

        else:
            raise TypeError("Entidade não é do tipo item de receita!")

    def excluir_item_de_receita(self, item: ItemDeReceita) -> None:
        if isinstance(item, ItemDeReceita):
            self.__itens.remove(item)
            self.__atualizar_calorias()
            self.__atualizar_custos()
        else:
            raise TypeError("Parâmetro não é do tipo insumo!")

    # MÉTODOS DE BUSCA
    def __buscar_item_por_insumo(self, insumo: Insumo) -> Insumo:
        if isinstance(insumo, Insumo):
            for item in self.__itens:
                if item.insumo == insumo:
                    return item
        else:
            raise TypeError("Parâmetro não é do tipo insumo!")

    # Talvez desnecessário
    def buscar_item_por_nome_de_insumo(self, nome: str) -> Insumo:
        if isinstance(nome, str):
            for item in self.__itens:
                if item.insumo.nome == nome:
                    return item
        else:
            raise TypeError("Parâmetro não é do tipo string!")

    # MÉTODOS DE ATUALIZAÇÃO DE PARÂMETROS
    def __atualizar_custos(self) -> None:
        custo_total = 0
        for item in self.__itens:
            custo_total += item.custo

        self.__custo_total = round(custo_total, 2)
        self.__custo_porcao = round(
            (custo_total / self.__rendimento_porcoes) + self.__custo_fixo, 2)

    def __atualizar_calorias(self) -> None:
        calorias_total = 0
        for item in self.__itens:
            calorias_total += item.calorias

        self.__calorias_porcao = round(
            calorias_total / self.__rendimento_porcoes, 0)
