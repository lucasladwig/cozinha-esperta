from entidade.insumo import Insumo
from limite.tela_insumo import TelaInsumo
from limite.tela_cadastro_insumo import TelaCadastroInsumo
from limite.tela_mensagem import TelaMensagem
from persistencia.insumo_dao import InsumoDAO


class ControladorInsumo:
    lista_inicial = [None, None, None]

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_insumo = TelaInsumo()
        self.__tela_cadastro_insumo = TelaCadastroInsumo()
        self.__insumo_dao = InsumoDAO()
        self.__tela_mensagem = TelaMensagem()

    # GETTERS / SETTERS
    @property
    def insumo_dao(self):
        return self.__insumo_dao

    # CRUD Insumos
    def cadastra_insumo(self, valores):
        if valores == None:
            self.__tela_cadastro_insumo.close()
        else:
            self.__tela_insumo.close()
            self.__tela_cadastro_insumo.close()
            nome = valores["it_nome"]
            unidade = valores["it_unidade"]
            try:
                caloria = int(valores["it_caloria"])
                if self.busca_insumo_por_nome(nome) == None:
                    self.__insumo_dao.add(Insumo(caloria, None, None, None, nome, unidade))
                    self.__tela_mensagem.open("Insumo cadastrado com sucesso!")
                else:
                    self.__tela_mensagem.open(
                        f"Já existe um insumo cadastrado com o nome '{nome}'!")
            except:
                self.__tela_mensagem.open("Valor inválido para caloria!")
            

    def edita_insumo(self, valores, nome):
        self.__tela_insumo.close()
        self.__tela_cadastro_insumo.close()
        insumo = self.busca_insumo_por_nome(nome)
        if valores == None:
            self.__tela_cadastro_insumo.close()
        else:
            try:
                caloria = int(valores["it_caloria"])
                if caloria != insumo.calorias_por_unidade:
                    insumo.calorias_por_unidade = caloria
                if valores["it_unidade"] != insumo.unidade:
                    insumo.unidade = valores["it_unidade"]
                if valores["it_nome"] != insumo.nome:
                    if self.busca_insumo_por_nome(valores["it_nome"]) == None:
                        insumo.nome = valores["it_nome"]
                    else:
                        self.__tela_mensagem.open(
                            f"Já existe um insumo cadastrado com o nome '{valores['it_nome']}'!")
            except:
                self.__tela_mensagem.open("Valor inválido para caloria!")
            

    def exclui_insumo(self, nome):
        self.__insumo_dao.remove(nome)

    def busca_insumo_por_nome(self, nome_busca: str):
        for insumo in self.__insumo_dao.get_all():
            if insumo.nome == nome_busca:
                return insumo
        else:
            return None

    def lista_dados_insumo(self, nome):
        lista_objeto_insumo = []
        insumo = self.busca_insumo_por_nome(nome)
        lista_objeto_insumo.append(insumo.nome)
        lista_objeto_insumo.append(insumo.unidade)
        lista_objeto_insumo.append(insumo.calorias_por_unidade)
        return lista_objeto_insumo

    def __monta_lista(self):
        lista_insumo = []
        for values in self.__insumo_dao.get_all():
            lista_auxiliar = []
            lista_auxiliar.append(values.nome)
            lista_auxiliar.append(values.unidade)
            lista_auxiliar.append(values.calorias_por_unidade)
            lista_insumo.append(lista_auxiliar)
        return lista_insumo

    def abre_tela(self):
        while True:
            botao, valores = self.__tela_insumo.open(self.__monta_lista())
            if botao == "Novo Insumo...":
                informacoes = self.__tela_cadastro_insumo.open(self.lista_inicial)
                self.cadastra_insumo(informacoes)
            elif botao == "Editar Insumo...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open("Não foi selecionado nenhuma linha!")
                else:
                    informacoes = self.__tela_cadastro_insumo.open(
                        self.lista_dados_insumo(valores["nome"]))
                    self.edita_insumo(informacoes, valores["nome"])
            elif botao == "Excluir Insumo...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.exclui_insumo(valores["nome"])
            elif botao == "Voltar":
                self.__tela_insumo.close()
                # self.voltar()
            self.__tela_insumo.close()
            self.__tela_insumo.init_components()