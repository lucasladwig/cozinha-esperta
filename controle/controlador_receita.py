from entidade.item_de_receita import ItemDeReceita
from entidade.receita import Receita
from entidade.insumo import Insumo
from persistencia.receita_dao import ReceitaDAO
from controle.controlador_insumo import ControladorInsumo
from controle.controlador_custos_fixos import ControladorCustosFixos
from limite.tela_gerenciador_receita import TelaGerenciadorReceita
from limite.tela_cadastro_receita import TelaCadastroReceita
from limite.tela_cadastro_item_de_receita import TelaCadastroItemDeReceita


class ControladorReceita:
    """Controlador de Receitas e Itens de Receita."""

    # Constante de classe
    __DADOS_BASE = {
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

    def __init__(self) -> None:
        # self.__controlador_sistema = None
        self.__controlador_insumos = ControladorInsumo()
        self.__controlador_custos_fixos = ControladorCustosFixos()
        self.__dao = ReceitaDAO()
        self.__tela_gerenciador_receita = TelaGerenciadorReceita()
        self.__tela_cadastro_receita = TelaCadastroReceita()
        self.__tela_cadastro_item_receita = TelaCadastroItemDeReceita()

    # GETTERS/SETTERS
    # @property
    # def controlador_sistema(self):
    #     return self.__controlador_sistema

    @property
    def dao(self):
        return self.__dao

    @property
    def tela_gerenciador_receita(self):
        return self.__tela_gerenciador_receita

    @property
    def tela_cadastro_receita(self):
        return self.__tela_cadastro_receita

    @property
    def tela_cadastro_item_receita(self):
        return self.__tela_cadastro_item_receita

    @property
    def controlador_insumos(self):
        return self.__controlador_insumos

    @property
    def controlador_custos_fixos(self):
        return self.__controlador_custos_fixos

   # TELAS
    def abrir_tela(self) -> None:
        while True:
            botao, valores = self.__tela_gerenciador_receita.open(
                self.__listar_receitas())
            match botao:
                case "Nova Receita...":
                    acao, dados_receita = self.tela_cadastro_receita.open(
                        ControladorReceita.__DADOS_BASE)
                    self.incluir_receita(dados_receita)
                case "Editar Receita...":
                    if valores["nome"] == None:
                        self.__tela_gerenciador_receita.mostrar_mensagem(
                            "Nenhuma receita selecionada!", titulo="Erro")
                    else:
                        receita = self.__buscar_receita_por_nome(
                            valores["nome"])
                        dados_receita = self.__tela_cadastro_receita.open(
                            receita)
                        self.alterar_receita(dados_receita, valores["nome"])
                case "Excluir Receita...":
                    if valores["nome"] == None:
                        self.__tela_mensagem.open(
                            "Não foi selecionado nenhuma linha!")
                    else:
                        self.exclui_insumo(valores["nome"])
                case "Voltar":
                    self.__tela_gerenciador_receita.close()
            self.__tela_gerenciador_receita.close()
            self.__tela_gerenciador_receita.init_components()

    # CRUD
    def incluir_receita(self, dados_receita: dict) -> None:
        codigo = dados_receita.get("codigo")
        nome = dados_receita.get("nome")

        if self.__buscar_receita_por_codigo(codigo) is not None or self.__buscar_receita_por_nome(nome) is not None:
            raise ValueError("Receita já existe!")

        custo_fixo_porcao = self.controlador_custos_fixos.enviar_custo_fixo_porcao()

        nova_receita = Receita(codigo, nome, custo_fixo_porcao)
        nova_receita.descricao = dados_receita.get("descricao")
        nova_receita.rendimento_porcoes = dados_receita.get(
            "rendimento_porcoes")
        nova_receita.tempo_preparo = dados_receita.get("tempo_preparo")
        nova_receita.validade = dados_receita.get("validade")
        nova_receita.modo_preparo = dados_receita.get("modo_preparo")
        nova_receita.itens = dados_receita.get("itens")

        self.dao.add(nova_receita)

    def alterar_receita(self, dados_receita: dict) -> None:
        if dados_receita is None:
            dados_receita = self.__DADOS_BASE
        codigo = dados_receita["codigo"]
        nome = dados_receita["nome"]

        if (self.__buscar_receita_por_codigo(codigo) is not None
                or self.__buscar_receita_por_nome(nome) is not None):
            raise ValueError

        nova_receita = Receita(codigo, nome)
        nova_receita.descricao = dados_receita["descricao"]
        nova_receita.rendimento_porcoes = dados_receita["rendimento_porcoes"]
        nova_receita.tempo_preparo = dados_receita["tempo_preparo"]
        nova_receita.validade = dados_receita["validade"]
        nova_receita.modo_preparo = dados_receita["modo_preparo"]
        nova_receita.itens = dados_receita["itens"]

        self.dao.add(nova_receita)

    # MÉTODOS AUXILIARES
    def __buscar_receita_por_codigo(self, codigo: str) -> Receita:
        if isinstance(codigo, str):
            for receita in self.dao.get_all():
                if receita.codigo == codigo:
                    return receita
        else:
            raise TypeError

    def __buscar_receita_por_nome(self, nome: str) -> Receita:
        try:
            if isinstance(nome, str):
                for receita in self.dao.get_all():
                    if receita.nome == nome:
                        return receita
            else:
                raise TypeError
        except TypeError:
            self.tela_gerenciador_receita.mostrar_mensagem(
                "Nome de receita inválido!", titulo="Erro")

    def __listar_receitas(self) -> list:
        receitas = []
        for receita in self.dao.get_all():
            dados_receita = []
            dados_receita.append(receita.codigo)
            dados_receita.append(receita.nome)
            dados_receita.append(receita.descricao)
            receitas.append(dados_receita)
        return receitas

    def __listar_dados_receita(self, nome: str) -> dict:
        receita = self.__buscar_receita_por_nome(nome)
        if receita is None:
            dados_receita = ControladorReceita.__DADOS_BASE
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
