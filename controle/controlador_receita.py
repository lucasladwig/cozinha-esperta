from entidade.item_de_receita import ItemDeReceita
from entidade.receita import Receita
from entidade.insumo import Insumo
from persistencia.receita_dao import ReceitaDAO
from controle.controlador_insumo import ControladorInsumo
from controle.controlador_custos_fixos import ControladorCustosFixos
from limite.tela_gerenciador_receitas import TelaGerenciadorReceitas
from limite.tela_cadastro_receita import TelaCadastroReceita
from limite.tela_cadastro_item_de_receita import TelaCadastroItemDeReceita


class ControladorReceita:
    """Controlador de Receitas e Itens de Receita."""

    # Constantes de classe
    __DADOS_BASE_RECEITA = {
        "codigo": "",
        "nome": "",
        "descricao": "",
        "rendimento_porcoes": 0,
        "tempo_preparo": 0,
        "validade": 0,
        "modo_preparo": "",
        "itens": [],
        "calorias_porcao": 0,
        "custo_total": 0.0,
        "custo_porcao": 0.0,
    }

    __DADOS_BASE_ITEM_RECEITA = {
        "insumo": None,
        "qtd": 0.0,
        "fator_correcao": 1.0,
        "indice_coccao": 1.0,
    }

    def __init__(self) -> None:
        # self.__controlador_sistema = None
        self.__controlador_insumos = ControladorInsumo()
        self.__controlador_custos_fixos = ControladorCustosFixos()
        self.__dao = ReceitaDAO()
        self.__tela_gerenciador_receitas = TelaGerenciadorReceitas()
        self.__tela_cadastro_receita = TelaCadastroReceita()
        self.__tela_cadastro_item_receita = TelaCadastroItemDeReceita()

    # GETTERS/SETTERS

   # TELAS
    def abrir_tela(self) -> None:
        """Abre tela do gerenciador de receitas."""
        while True:
            acao_gerenciador, valores_gerenciador = self.__tela_gerenciador_receitas.open(
                self.__listar_receitas())
            
            # Criar nova receita
            if acao_gerenciador == "Nova Receita...":
                acao_receita, dados_receita = self.__tela_cadastro_receita.open(
                    ControladorReceita.__DADOS_BASE_RECEITA)
                if acao_receita == "Adicionar Item...":
                    dados_insumos = self.__listar_insumos()
                    dados_item = self.__tela_cadastro_item_receita.open(
                        dados_insumos)
                    
                    
                elif acao_receita == "Editar Item...":
                    dados_insumos = self.__listar_insumos()
                    dados_item = self.__tela_cadastro_item_receita.open(
                        dados_insumos)
                self.incluir_receita(dados_receita)
            
            # Editar receita
            elif acao_gerenciador == "Editar Receita...":
                if valores_gerenciador["codigo"] == None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    receita = self.__buscar_receita_por_codigo(
                        valores_gerenciador["codigo"])
                    dados_receita = self.abrir_tela_cadastro_receita(
                        self.__listar_dados_receita(receita))
                    self.alterar_receita(dados_receita)
            elif acao_gerenciador == "Excluir Receita...":
                if valores_gerenciador["codigo"] == None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    self.excluir_receita(valores_gerenciador["codigo"])
            elif acao_gerenciador == "Voltar":
                self.__tela_gerenciador_receitas.close()
                break

            # Atualiza tela com novos valores
            self.__tela_gerenciador_receitas.close()
            self.__tela_gerenciador_receitas.init_components()


    # CRUD
    def incluir_receita(self, dados_receita: dict) -> None:
        """Inclui uma nova receita."""
        # Testa se código inserido já existe
        codigo = dados_receita.get("codigo")
        if self.__buscar_receita_por_codigo(codigo) is not None:
            raise ValueError("Receita já existe!")

        # Instancia nova receita com dados isneridos
        nome = dados_receita.get("nome")
        custo_fixo_porcao = self.__controlador_custos_fixos.enviar_custo_fixo_porcao()
        nova_receita = Receita(codigo, nome, custo_fixo_porcao)

        # INSERÇÃO DE ITENS DE RECEITA - Revisar
        nova_receita.itens = dados_receita.get("itens")

        # Atualiza outros campos da receita (com valores padrão caso não sejam inseridos)
        nova_receita.descricao = dados_receita.get(
            "descricao", "Inserir descrição!")
        nova_receita.rendimento_porcoes = dados_receita.get(
            "rendimento_porcoes", 1)
        nova_receita.tempo_preparo = dados_receita.get("tempo_preparo", 0)
        nova_receita.validade = dados_receita.get("validade", 0)
        nova_receita.modo_preparo = dados_receita.get(
            "modo_preparo", "Inserir modo de preparo!")

        # Persistir receita
        self.__dao.add(nova_receita)

    def alterar_receita(self, dados_receita: dict) -> None:
        """Altera dados de uma receita."""
        if dados_receita is None:
            self.__tela_cadastro_receita.close()
        else:
            # Busca receita a editar
            receita = self.__buscar_receita_por_codigo(dados_receita["codigo"])

            # Testa se novo nome já existe
            if dados_receita["nome"] != receita.nome:
                if self.__buscar_receita_por_nome(dados_receita["nome"]) is None:
                    receita.nome = dados_receita["nome"]
                else:
                    self.__tela_cadastro_receita.mostrar_mensagem(
                        f"Receita com este nome já existe!", titulo="Erro")

            # Atualiza parâmetros
            receita.descricao = dados_receita["descricao"]
            receita.rendimento_porcoes = dados_receita["rendimento_porcoes"]
            receita.tempo_preparo = dados_receita["tempo_preparo"]
            receita.validade = dados_receita["validade"]
            receita.modo_preparo = dados_receita["modo_preparo"]
            receita.itens = dados_receita["itens"]  # rever

            # Persistir receita
            self.__dao.add(receita)

    def excluir_receita(self, codigo: str) -> None:
        if self.__buscar_receita_por_codigo(codigo) is None:
            raise ValueError("Receita não existe!")
        self.__dao.remove(codigo)

    # MÉTODOS AUXILIARES
    def __buscar_receita_por_codigo(self, codigo: str) -> Receita:
        if isinstance(codigo, str):
            for receita in self.__dao.get_all():
                if receita.codigo == codigo:
                    return receita

    def __buscar_receita_por_nome(self, nome: str) -> Receita:
        if isinstance(nome, str):
            for receita in self.__dao.get_all():
                if receita.nome == nome:
                    return receita

    def __listar_receitas(self) -> list:
        receitas = []
        for receita in self.__dao.get_all():
            dados_receita = []
            dados_receita.append(receita.codigo)
            dados_receita.append(receita.nome)
            dados_receita.append(receita.descricao)
            receitas.append(dados_receita)
        return receitas

    def __listar_dados_receita(self, receita: Receita) -> dict:
        if receita is None:
            dados_receita = ControladorReceita.__DADOS_BASE_RECEITA
        else:
            dados_receita = {
                "codigo": receita.codigo,
                "nome": receita.nome,
                "descricao": receita.descricao,
                "rendimento_porcoes": receita.rendimento_porcoes,
                "tempo_preparo": receita.tempo_preparo,
                "validade": receita.validade,
                "modo_preparo": receita.modo_preparo,
                "itens": receita.listar_dados_itens(),
                "calorias_porcao": receita.calorias_porcao,
                "custo_total": receita.custo_total,
                "custo_porcao": receita.custo_porcao,
            }
        return dados_receita

    def __listar_dados_item_receita(self, item_receita: ItemDeReceita) -> dict:
        if item_receita is None:
            dados_item_receita = ControladorReceita.__DADOS_BASE_ITEM_RECEITA
        else:
            dados_item_receita = {
                "insumo": item_receita.insumo,
                "qtd": 0.0,
                "fator_correcao": 1.0,
                "indice_coccao": 1.0,
            }
        return dados_item_receita

    def __listar_insumos(self) -> list:
        """Retorna uma lista ordenada dos nomes dos insumos cadastrados."""
        lista_insumos = self.__controlador_insumos.listar_insumos()
        nomes_insumos = []

        for insumo in lista_insumos:
            nomes_insumos.append(insumo.nome)

        return sorted(nomes_insumos)
