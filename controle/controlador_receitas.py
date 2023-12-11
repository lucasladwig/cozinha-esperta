from entidade.item_de_receita import ItemDeReceita
from entidade.receita import Receita
from entidade.insumo import Insumo
from persistencia.receita_dao import ReceitaDAO
from controle.controlador_insumo import ControladorInsumo
from controle.controlador_custos_fixos import ControladorCustosFixos
from limite.tela_gerenciador_receitas import TelaGerenciadorReceitas
from limite.tela_cadastro_receita import TelaCadastroReceita
from limite.tela_cadastro_item_de_receita import TelaCadastroItemDeReceita


class ControladorReceitas:
    """Controlador de Receitas e Itens de Receita."""

    # Constantes de classe
    __DADOS_NOVA_RECEITA = {
        "codigo": "",
        "nome": "",
        "descricao": "",
        "rendimento_porcoes": 1,
        "tempo_preparo": 1,
        "validade": 0,
        "modo_preparo": "",
        "itens": [],
        "calorias_porcao": 0,
        "custo_total": 0.0,
        "custo_porcao": 0.0,
    }

    __DADOS_NOVO_ITEM_RECEITA = {
        "nome_insumo": None,
        "qtd_bruta": 1.0,
        "qtd_limpa": 1.0,
        "calcula_por_qtd_bruta": True,
        "fator_correcao": 1.0,
        "indice_coccao": 1.0,
    }

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__controlador_insumos = ControladorInsumo()
        self.__controlador_custos_fixos = ControladorCustosFixos()
        self.__receita_dao = ReceitaDAO()
        self.__tela_gerenciador_receitas = TelaGerenciadorReceitas()
        self.__tela_cadastro_receita = TelaCadastroReceita()
        self.__tela_cadastro_item_receita = TelaCadastroItemDeReceita()

        # Disponibiliza a lista de insumos para todos os métodos
        self.__insumos_cadastrados = self.__listar_insumos()

    # GETTERS/SETTERS

    # TELAS
    def abrir_tela_gerenciador(self) -> None:
        """Abre a tela inicial do gerenciador de receitas."""
        while True:
            acao_gerenciador, dados_gerenciador = self.__tela_gerenciador_receitas.abrir_tela(
                self.__listar_dados_todas_receitas())
            self.__tela_gerenciador_receitas.fechar_tela()

            # NOVA RECEITA
            if acao_gerenciador == "Nova Receita...":
                self.abrir_tela_receita(None)

            # EDITAR RECEITA
            elif acao_gerenciador == "Editar Receita...":
                if dados_gerenciador["codigo"] is None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    receita_atual = self.__buscar_receita_por_codigo(
                        dados_gerenciador["codigo"])

                    self.abrir_tela_receita(receita_atual)

            elif acao_gerenciador == "Excluir Receita...":
                if dados_gerenciador["codigo"] is None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    confirma_exclusao = self.__tela_gerenciador_receitas.confirmar_exclusao()
                    if confirma_exclusao == "Sim":
                        self.excluir_receita(dados_gerenciador["codigo"])
                        self.__tela_gerenciador_receitas.mostrar_mensagem(
                            "Receita excluída com sucesso!", titulo="Receita excluída")
                    elif confirma_exclusao == "Não":
                        pass
                #
            elif acao_gerenciador == "Voltar":
                self.__tela_gerenciador_receitas.fechar_tela()
                break

            # Fecha a tela para atualizar com novos valores
            self.__tela_gerenciador_receitas.fechar_tela()

    # Verificar tipo do retorno, se houver
    def abrir_tela_receita(self, receita: Receita):
        """Abre a tela de cadastro/edição de uma receita, carregando seus parâmetros e uma lista dos seus itens."""

        # Abre uma tela de cadastro/edição de receita com os dados passados
        if receita is None:
            dados_receita_atual = ControladorReceitas.__DADOS_NOVA_RECEITA
            itens_da_receita = []
            dados_itens_receita_atual = []
        else:
            dados_receita_atual = self.__listar_dados_uma_receita(receita)
            itens_da_receita = receita.itens
            dados_itens_receita_atual = self.__listar_dados_todos_itens_receita(
                itens_da_receita)

        # Abre tela de cadastro de itens carregando a lista de insumos e parâmetros de um novo item de receita
        while True:
            evento_receita, valores_receita = self.__tela_cadastro_receita.abrir_tela(
                dados_receita_atual, dados_itens_receita_atual)

            # Adicionar item de receita
            if evento_receita == "Adicionar Item...":
                valores_item_novo = self.__tela_cadastro_item_receita.abrir_tela(
                    lista_insumos=self.__insumos_cadastrados,
                    dados_item=ControladorReceitas.__DADOS_NOVO_ITEM_RECEITA
                )
                if valores_item_novo is None:
                    self.__tela_cadastro_item_receita.fechar_tela()

                elif self.__buscar_item_receita_por_nome(itens_da_receita, valores_item_novo['nome_insumo']) is not None:
                    self.__tela_cadastro_item_receita.mostrar_mensagem(
                        "Insumo já incluído na receita!", titulo="Erro")
                    self.__tela_cadastro_item_receita.fechar_tela()

                else:
                    novo_item = self.criar_item_de_receita(
                        valores_item_novo)
                    itens_da_receita.append(novo_item)
                    self.__tela_cadastro_item_receita.fechar_tela()
                    self.__tela_cadastro_receita.fechar_tela()

                    dados_itens_receita_atual = self.__listar_dados_todos_itens_receita(
                        itens_da_receita)

                    dados_receita_atual = valores_receita
                    pass

            # Editar um item de receita
            elif evento_receita == "Editar Item...":
                # Verifica se tem uma linha selecionada
                if valores_receita["nome_insumo_selecionado"] is None:
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhum item selecionado!", titulo="Erro")
                else:
                    item_a_editar = self.__buscar_item_receita_por_nome(
                        itens_da_receita, valores_receita['nome_insumo_selecionado'])

                    # Abre janela de edição de itens carregando a lista de insumos e os valores atuais do item de receita
                    novos_dados_item = self.__tela_cadastro_item_receita.abrir_tela(
                        self.__insumos_cadastrados,
                        self.__listar_dados_um_item_receita(item_a_editar))

                    if novos_dados_item is None:
                        self.__tela_cadastro_item_receita.fechar_tela()
                        pass

                    # Altera item de receita
                    self.alterar_item_de_receita(
                        item_a_editar, novos_dados_item)

                    dados_itens_receita_atual = self.__listar_dados_todos_itens_receita(
                        itens_da_receita)
                    dados_receita_atual = valores_receita

                    self.__tela_cadastro_item_receita.fechar_tela()

            # Excluir um item de receita
            elif evento_receita == "Excluir Item...":
                if valores_receita["nome_insumo_selecionado"] is None:  # verificar
                    self.__tela_gerenciador_receitas.mostrar_mensagem(
                        "Nenhum item selecionado!", titulo="Erro")
                else:
                    nome_insumo = valores_receita["nome_insumo_selecionado"]
                    confirma_exclusao = self.__tela_cadastro_receita.confirmar_exclusao()
                    if confirma_exclusao == "Sim":
                        item_a_excluir = None
                        for item in itens_da_receita:
                            if item.insumo.nome == nome_insumo:
                                item_a_excluir = item
                                break
                        itens_da_receita.remove(item_a_excluir)

                        dados_itens_receita_atual = self.__listar_dados_todos_itens_receita(
                            itens_da_receita)
                        dados_receita_atual = valores_receita
                        self.__tela_cadastro_receita.fechar_tela()
                        # self.__tela_cadastro_item_receita.fechar_tela()

                    else:
                        self.__tela_cadastro_item_receita.fechar_tela()

            else:
                # Salvar nova Receita
                if evento_receita == "Salvar":
                    if valores_receita is None:
                        dados_receita_atual = ControladorReceitas.__DADOS_NOVA_RECEITA
                        itens_da_receita = []
                        dados_itens_receita_atual = []

                        self.__tela_cadastro_receita.fechar_tela()
                        continue

                    elif self.__buscar_receita_por_codigo(valores_receita['codigo']) is not None:
                        self.__tela_cadastro_receita.mostrar_mensagem(
                            "Código de receita já existe!", titulo="Erro")
                        self.__tela_cadastro_receita.fechar_tela()

                    elif receita is None and valores_receita is not None:
                        self.incluir_receita(
                            valores_receita, itens_da_receita)
                        self.__tela_cadastro_receita.mostrar_mensagem(
                            "Receita salva com sucesso!", titulo="Sucesso")
                        self.__tela_cadastro_receita.fechar_tela()
                        break

                    elif receita is not None:
                        self.alterar_receita(
                            receita, valores_receita, itens_da_receita)
                        self.__tela_cadastro_receita.mostrar_mensagem(
                            "Receita salva com sucesso!", titulo="Sucesso")
                        self.__tela_cadastro_receita.fechar_tela()
                        break

                # Cancelar
                elif evento_receita == "Cancelar":
                    self.__tela_cadastro_receita.fechar_tela()
                    break

                self.__tela_cadastro_receita.fechar_tela()
                # break

        return evento_receita, valores_receita

    # CRUD RECEITAS
    def incluir_receita(self, dados_receita: dict, lista_itens: list) -> None:
        """Inclui a nova receita no DAO."""

        # Testa se código inserido já existe
        novo_codigo = dados_receita["codigo"]

        if self.__buscar_receita_por_codigo(novo_codigo) is not None:
            self.__tela_cadastro_receita.mostrar_mensagem(
                "Receita com este código já existe!", titulo="Erro")

        novo_nome = dados_receita["nome"]
        custo_fixo = self.__controlador_custos_fixos.enviar_custo_fixo_porcao()
        novo_descricao = dados_receita["descricao"]
        novo_modo = dados_receita["modo_preparo"]
        novo_rendimento = int(dados_receita["rendimento_porcoes"])
        novo_tempo = int(dados_receita["tempo_preparo"])
        novo_validade = int(dados_receita["validade"])

        nova_receita = Receita(codigo=novo_codigo,
                               nome=novo_nome,
                               custo_fixo=custo_fixo,
                               descricao=novo_descricao,
                               rendimento_porcoes=novo_rendimento,
                               tempo_preparo=novo_tempo,
                               validade=novo_validade,
                               modo_preparo=novo_modo,
                               )

        # INSERÇÃO DE ITENS DE RECEITA - Revisar
        nova_receita.itens = lista_itens

        # Persistir receita
        self.__receita_dao.add(nova_receita)

    def alterar_receita(self, receita: Receita, dados_receita: dict, lista_itens: list) -> None:
        """Altera dados de uma receita."""

        # Busca receita a editar
        receita_a_editar = receita

        # Testa se novo nome já existe
        if dados_receita["nome"] != receita.nome:
            if self.__buscar_receita_por_nome(dados_receita["nome"]) is None:
                receita_a_editar.nome = dados_receita["nome"]
            else:
                self.__tela_cadastro_receita.mostrar_mensagem(
                    f"Receita com este nome já existe!", titulo="Erro")
                return

        # Atualiza parâmetros
        receita_a_editar.descricao = dados_receita["descricao"]
        receita_a_editar.rendimento_porcoes = dados_receita["rendimento_porcoes"]
        receita_a_editar.tempo_preparo = dados_receita["tempo_preparo"]
        receita_a_editar.validade = dados_receita["validade"]
        receita_a_editar.modo_preparo = dados_receita["modo_preparo"]
        receita_a_editar.itens = lista_itens

        # Persistir receita
        self.__receita_dao.add(receita_a_editar)

    def excluir_receita(self, codigo: str) -> None:
        if self.__buscar_receita_por_codigo(codigo) is None:
            raise ValueError("Receita não existe!")
        self.__receita_dao.remove(codigo)

    # CRUD ITENS RECEITAS
    def criar_item_de_receita(self, dados_item_receita: dict) -> ItemDeReceita:
        """Insere um item em uma receita existente."""

        # Instancia novo item
        insumo = self.__controlador_insumos.busca_insumo_por_nome(
            dados_item_receita["nome_insumo"])
        novo_item = ItemDeReceita(insumo)

        novo_item.fator_correcao = dados_item_receita["fator_correcao"]
        novo_item.indice_coccao = dados_item_receita["indice_coccao"]
        novo_item.calcula_por_qtd_bruta = dados_item_receita["calcula_por_qtd_bruta"]

        # Atualiza quantidade
        if novo_item.calcula_por_qtd_bruta:
            novo_item.qtd_bruta = dados_item_receita["quantidade"]
        else:
            novo_item.qtd_limpa = dados_item_receita["quantidade"]

        return novo_item

    def alterar_item_de_receita(self, item_receita: ItemDeReceita, dados_item_receita: dict) -> None:
        """Altera um item em uma receita existente."""
        item_atual = item_receita

        # Verufica se houve mudança do insumo
        if item_atual.insumo.nome != dados_item_receita["nome_insumo"]:
            insumo_novo = self.__controlador_insumos.busca_insumo_por_nome(
                dados_item_receita["nome_insumo"])
            item_atual.insumo = insumo_novo

        item_atual.fator_correcao = dados_item_receita["fator_correcao"]
        item_atual.indice_coccao = dados_item_receita["indice_coccao"]
        item_atual.calcula_por_qtd_bruta = dados_item_receita["calcula_por_qtd_bruta"]

        # Atualiza novo item com os dados inseridos
        if item_atual.calcula_por_qtd_bruta:
            item_atual.qtd_bruta = dados_item_receita["quantidade"]
        else:
            item_atual.qtd_limpa = dados_item_receita["quantidade"]

    # MÉTODOS DE BUSCA

    def __buscar_receita_por_codigo(self, codigo: str) -> Receita:
        if isinstance(codigo, str):
            for receita in self.__receita_dao.get_all():
                if receita.codigo == codigo:
                    return receita

    def __buscar_receita_por_nome(self, nome: str) -> Receita:
        if isinstance(nome, str):
            for receita in self.__receita_dao.get_all():
                if receita.nome == nome:
                    return receita

    def __buscar_item_receita_por_nome(self, lista_itens: list, nome: str) -> ItemDeReceita:
        if isinstance(nome, str):
            for item_receita in lista_itens:
                if item_receita.insumo.nome == nome:
                    return item_receita

    # MÉTODOS DE LISTAGEM DE DADOS PARA TELAS
    def __listar_dados_uma_receita(self, receita: Receita) -> dict:
        """Retorna todos os atributos de uma receita para serem exibidos em tela."""
        if receita is None:
            dados_receita = ControladorReceitas.__DADOS_NOVA_RECEITA
        else:
            dados_receita = {
                "codigo": receita.codigo,
                "nome": receita.nome,
                "descricao": receita.descricao,
                "rendimento_porcoes": receita.rendimento_porcoes,
                "tempo_preparo": receita.tempo_preparo,
                "validade": receita.validade,
                "modo_preparo": receita.modo_preparo,
                "itens": self.__listar_dados_todos_itens_receita(receita.itens),
                "calorias_porcao": receita.calorias_porcao,
                "custo_total": receita.custo_total,
                "custo_porcao": receita.custo_porcao,
            }
        return dados_receita

    def __listar_dados_todas_receitas(self) -> list:
        """Retorna código, nome e descrição de uma receita para serem exibidos em tela (em formato de tabela)."""
        receitas = []
        for receita in self.__receita_dao.get_all():
            dados_receita = []
            dados_receita.append(receita.codigo)
            dados_receita.append(receita.nome)
            dados_receita.append(receita.descricao)
            receitas.append(dados_receita)
        return receitas

    def __listar_dados_um_item_receita(self, item_receita: ItemDeReceita) -> dict:
        """Retorna os atributos editáveis de um item de receita para serem exibidos em tela."""
        if item_receita is None:
            dados_item_receita = ControladorReceitas.__DADOS_NOVO_ITEM_RECEITA
        else:
            dados_item_receita = {
                "nome_insumo": item_receita.insumo.nome,
                "qtd_bruta": item_receita.qtd_bruta,
                "qtd_limpa": item_receita.qtd_limpa,
                "calcula_por_qtd_bruta": item_receita.calcula_por_qtd_bruta,
                "fator_correcao": item_receita.fator_correcao,
                "indice_coccao": item_receita.indice_coccao,
            }
        return dados_item_receita

    def __listar_dados_todos_itens_receita(self, lista_itens: list) -> list:
        """Retorna todos os atributos de todos itens de uma receita para serem exibidos em tela (em formato de tabela)."""
        dados_todos_itens = []
        for item in lista_itens:
            dados_item = []
            dados_item.append(item.insumo.nome)
            dados_item.append(item.insumo.unidade)
            dados_item.append(item.qtd_bruta)
            dados_item.append(item.fator_correcao)
            dados_item.append(item.qtd_limpa)
            dados_item.append(item.indice_coccao)
            dados_item.append(item.qtd_pronta)
            dados_item.append(item.calorias)
            dados_item.append(item.custo)
            dados_todos_itens.append(dados_item)
        return dados_todos_itens

    def __listar_insumos(self) -> list:
        """Retorna um dicionário ordenado dos nomes dos insumos cadastrados e suas unidades."""
        lista_insumos = self.__controlador_insumos.insumo_dao.get_all()
        nomes_insumos = [insumo.nome for insumo in lista_insumos]
        nomes_insumos.sort()

        return nomes_insumos
