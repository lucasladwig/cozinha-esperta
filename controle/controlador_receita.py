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
        "qtd_bruta": 0.0,
        "qtd_limpa": 0.0,
        "calcula_por_qtd_bruta": True,
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
        """Abre todas as telas de receitas."""
        while True:
            acao_gerenciador, dados_gerenciador = self.__tela_gerenciador_receitas.open(
                self.__listar_receitas())

            # Carrega lista de insumos do controlador de insumos
            lista_insumos = self.__listar_insumos()

            # CRIAR NOVA RECEITA
            if acao_gerenciador == "Nova Receita...":
                self.__tela_gerenciador_receitas.close()
                lista_itens = []

                # Abre janela de cadastro de nova receita com dados em branco
                acao_receita, dados_receita = self.__tela_cadastro_receita.open(
                    ControladorReceita.__DADOS_BASE_RECEITA)

                # Adicionar itens de receita
                if acao_receita == "Adicionar Item...":
                    self.__tela_cadastro_receita.close()

                    # Abre janela de cadastro de itens carregando a lista de insumos já cadastrados
                    dados_item = self.__tela_cadastro_item_receita.open(
                        lista_insumos, ControladorReceita.__DADOS_BASE_ITEM_RECEITA)

                    novo_item = self.criar_item_de_receita(dados_item)
                    lista_itens.append(novo_item)

                    self.__tela_cadastro_item_receita.close()

                # Editar um item de receita
                elif acao_receita == "Editar Item...":
                    self.__tela_cadastro_receita.close()

                    # Verifica se tem uma linha selecionada
                    if dados_receita["tabela_itens_receita"] == None:
                        self.__tela_gerenciador_receitas.mostrar_mensagem(
                            "Nenhum item selecionado!", titulo="Erro")
                    else:
                        item_a_editar = None
                        for item in lista_itens:
                            if item.insumo.nome == dados_receita["tabela_itens_receita"][0]:
                                item_a_editar = item
                                break

                        # Abre janela de edição de itens carregando a lista de insumos e os valores atuais do item de receita
                        dados_item = self.__tela_cadastro_item_receita.open(
                            lista_insumos, self.__listar_dados_item_receita(item_a_editar))

                        lista_itens.remove(item_a_editar)
                        novo_item = self.criar_item_de_receita(dados_item)
                        lista_itens.append(novo_item)

                        self.__tela_cadastro_item_receita.close()

                # Excluir um item de receita
                elif acao_receita == " Excluir Item...":
                    if dados_gerenciador["tabela_itens_receita"] == None:
                        self.__tela_gerenciador_receitas.mostrar_mensagem(
                            "Nenhum item selecionado!", titulo="Erro")
                    else:
                        confirma, _ = self.__tela_cadastro_receita.confirmar_exclusao()
                        if confirma:
                            item_a_excluir = None
                            for item in lista_itens:
                                if item.insumo.nome == dados_receita["tabela_itens_receita"][0]:
                                    item_a_excluir = item
                                    break
                            lista_itens.remove(item_a_excluir)
                            self.__tela_cadastro_item_receita.close()

                        else:
                            self.__tela_cadastro_item_receita.close()

                # Salvar nova Receita
                elif acao_receita == "Salvar":
                    self.incluir_receita(dados_receita, lista_itens)

                    self.__tela_cadastro_receita.close()

                # Cancelar
                elif acao_receita in ("Cancelar", "WIN_CLOSE"):
                    self.__tela_cadastro_item_receita.close()

            # EDITAR RECEITA
            elif acao_gerenciador == "Editar Receita...":
                if dados_gerenciador["codigo"] == None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    lista_itens = []
                    receita_atual = self.__buscar_receita_por_codigo(
                        dados_gerenciador["codigo"])
                    dados_receita_atual = self.__listar_dados_receita(receita_atual)
                    dados_itens_receita_atual = receita_atual.listar_dados_itens()
                    
                    acao_receita, dados_receita = self.__tela_cadastro_receita.open(dados_receita_atual, dados_itens_receita_atual)
                    
                    # Adicionar itens de receita
                    if acao_receita == "Adicionar Item...":
                        self.__tela_cadastro_receita.close()

                        # Abre janela de cadastro de itens carregando a lista de insumos já cadastrados
                        dados_item = self.__tela_cadastro_item_receita.open(
                            lista_insumos, ControladorReceita.__DADOS_BASE_ITEM_RECEITA)

                        novo_item = self.criar_item_de_receita(dados_item)
                        receita_atual.incluir_item_em_receita(novo_item)

                        self.__tela_cadastro_item_receita.close()

                    # Editar um item de receita
                    elif acao_receita == "Editar Item...":
                        self.__tela_cadastro_receita.close()

                        # Verifica se tem uma linha selecionada
                        if dados_receita["tabela_itens_receita"] == None:
                            self.__tela_gerenciador_receitas.mostrar_mensagem(
                                "Nenhum item selecionado!", titulo="Erro")
                        else:
                            item_a_editar = receita_atual.buscar_item_por_nome_de_insumo(dados_receita["tabela_itens_receita"][0])

                            # Abre janela de edição de itens carregando a lista de insumos e os valores atuais do item de receita
                            dados_item = self.__tela_cadastro_item_receita.open(
                                lista_insumos, self.__listar_dados_item_receita(item_a_editar))

                            item_a_editar = self.alterar_item_de_receita(item_a_editar, dados_item)

                            self.__tela_cadastro_item_receita.close()

                    # Excluir um item de receita
                    elif acao_receita == "Excluir Item...":
                        if dados_gerenciador["tabela_itens_receita"] == None:
                            self.__tela_gerenciador_receitas.mostrar_mensagem(
                                "Nenhum item selecionado!", titulo="Erro")
                        else:
                            confirma, _ = self.__tela_cadastro_receita.confirmar_exclusao()
                            if confirma:
                                item_a_excluir = receita_atual.buscar_item_por_nome_de_insumo(dados_receita["tabela_itens_receita"][0])
                                receita_atual.excluir_item_de_receita(item_a_excluir)
                                self.__tela_cadastro_item_receita.close()

                            else:
                                self.__tela_cadastro_item_receita.close()

                    # Salvar nova Receita
                    elif acao_receita == "Salvar":
                        self.alterar_receita(dados_receita)

                        self.__tela_cadastro_receita.close()

                    # Cancelar
                    elif acao_receita in ("Cancelar", "WIN_CLOSE"):
                        self.__tela_cadastro_item_receita.close()
                        
                        self.alterar_receita(dados_receita)

            elif acao_gerenciador == "Excluir Receita...":
                if dados_gerenciador["codigo"] == None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    self.excluir_receita(dados_gerenciador["codigo"])

            #

            elif acao_gerenciador == "Voltar":
                self.__tela_gerenciador_receitas.close()
                break

            # Atualiza tela com novos valores
            self.__tela_gerenciador_receitas.close()
            self.__tela_gerenciador_receitas.init_components()

    # CRUD
    def incluir_receita(self, dados_receita: dict, lista_itens: list) -> None:
        """Inclui a nova receita no DAO."""

        # Testa se código inserido já existe
        codigo = dados_receita.get("codigo")
        nome = dados_receita.get("nome")

        if self.__buscar_receita_por_codigo(codigo) is not None:
            self.__tela_cadastro_receita.mostrar_mensagem(
                f"Receita com este código já existe!", titulo="Erro")

        # Atualiza a nova receita com dados inseridos
        custo_fixo = self.__controlador_custos_fixos.enviar_custo_fixo_porcao()
        nova_receita = Receita(codigo, nome, custo_fixo)
        nova_receita.codigo = codigo
        nova_receita.nome = nome

        # Atualiza outros campos da receita (com valores padrão caso não sejam inseridos)
        nova_receita.descricao = dados_receita.get(
            "descricao", "Inserir descrição!")
        nova_receita.rendimento_porcoes = dados_receita.get(
            "rendimento_porcoes", 1)
        nova_receita.tempo_preparo = dados_receita.get("tempo_preparo", 0)
        nova_receita.validade = dados_receita.get("validade", 0)
        nova_receita.modo_preparo = dados_receita.get(
            "modo_preparo", "Inserir modo de preparo!")

        # INSERÇÃO DE ITENS DE RECEITA - Revisar
        nova_receita.itens = lista_itens

        # Persistir receita
        self.__dao.add(nova_receita)

    def criar_item_de_receita(self, dados_item_receita: dict) -> None:
        """Insere um item em uma receita existente."""

        # Instancia novo item
        insumo = self.__controlador_insumos.busca_insumo_por_nome(
            dados_item_receita["nome_insumo"])
        novo_item = ItemDeReceita(insumo)

        # Atualiza novo item com os dados inseridos
        if dados_item_receita["bruta"]:
            novo_item.qtd_bruta = dados_item_receita["qtd"]
        elif dados_item_receita["limpa"]:
            novo_item.qtd_limpa = dados_item_receita["qtd"]

        novo_item.fator_correcao = dados_item_receita["fator_correcao"]
        novo_item.indice_coccao = dados_item_receita["indice_coccao"]

        return novo_item

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
            
            # Persistir receita
            self.__dao.add(receita)

    def alterar_item_de_receita(self, item_receita: ItemDeReceita, dados_item_receita: dict) -> None:
        """Altera um item em uma receita existente."""
        item_atual = item_receita

        # Verufica se houve mudança do insumo
        if item_atual.insumo.nome != dados_item_receita["nome_insumo"]:
            insumo_novo = self.__controlador_insumos.busca_insumo_por_nome(
            dados_item_receita["nome_insumo"])
            item_atual.insumo = insumo_novo

        # Atualiza novo item com os dados inseridos
        if dados_item_receita["bruta"]:
            item_atual.qtd_bruta = dados_item_receita["qtd"]
        elif dados_item_receita["limpa"]:
            item_atual.qtd_limpa = dados_item_receita["qtd"]

        item_atual.fator_correcao = dados_item_receita["fator_correcao"]
        item_atual.indice_coccao = dados_item_receita["indice_coccao"]

        return item_atual

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

    # def __listar_itens_de_receitas(self, receita: Receita) -> list:
    #     itens = []
    #     for item in receita.itens:
    #         dados_item = []
    #         dados_item.append(item.insumo.nome)
    #         dados_item.append(item.insumo.unidade)
    #         dados_item.append(item.qtd_bruta)
    #         dados_item.append(item.fator_correcao)
    #         dados_item.append(item.qtd_limpa)
    #         dados_item.append(item.indice_coccao)
    #         dados_item.append(item.qtd_pronta)
    #         dados_item.append(item.calorias)
    #         dados_item.append(item.custo)
    #         itens.append(dados_item)
    #     return itens

    def __listar_dados_item_receita(self, item_receita: ItemDeReceita) -> dict:
        if item_receita is None:
            dados_item_receita = ControladorReceita.__DADOS_BASE_ITEM_RECEITA
        else:
            dados_item_receita = {
                "insumo": item_receita.insumo.nome,
                "qtd_bruta": item_receita.qtd_bruta,
                "qtd_limpa": item_receita.qtd_limpa,
                "calcula_por_qtd_bruta": item_receita.calcula_por_qtd_bruta,
                "fator_correcao": item_receita.fator_correcao,
                "indice_coccao": item_receita.indice_coccao,
            }
        return dados_item_receita

    def __listar_insumos(self) -> list:
        """Retorna uma lista ordenada dos nomes dos insumos cadastrados."""
        lista_insumos = self.__controlador_insumos.listar_insumos()
        nomes_insumos = []

        for insumo in lista_insumos:
            nomes_insumos.append(insumo.nome)

        return sorted(nomes_insumos)
