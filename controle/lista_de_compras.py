from entidade.item_lista_de_compras import ItemDeListaDeCompras
from entidade.insumo_teste import Insumo
from limite.tela_lista_de_compras import TelaListaDeCompras
from limite.tela_item_na_lista_de_compras import TelaItemNaListaDeCompras
from limite.tela_mensagem import TelaMensagem


class ListaDeCompras:
    def __init__(self) -> None:
        self.__lista_de_compras = []
        self.__insumo = Insumo()
        self.__tela_lista_de_compras = TelaListaDeCompras()
        self.__tela_item_na_lista_de_compras = TelaItemNaListaDeCompras()
        self.__tela_mensagem = TelaMensagem()

    def cadastra_insumo(self, valores):
        if valores == None:
            self.__tela_item_na_lista_de_compras.close()
        else:
            self.__tela_lista_de_compras.close()
            self.__tela_item_na_lista_de_compras.close()
            nome = valores["it_nome"]
            quantidade = valores["it_quantidade"]
            if self.buscar_item_por_nome(nome) == None:
                self.__lista_de_compras.append(ItemDeListaDeCompras(nome, quantidade))
                self.__tela_mensagem.open("Item Adicionado com sucesso!")
            else:
                self.__tela_mensagem.open(
                    f"Já existe um item na lista de compras com o nome de {nome}!")

    def verifica_estoque(self):
        lista_de_insumos = self.__insumo.lista_insumos()
        for item in lista_de_insumos:
            if item.estoque_minimo > item.estoque_atual:
                quantidade_a_comprar = item.estoque_minimo - item.estoque_atual
                self.__lista_de_compras.append(ItemDeListaDeCompras(item, quantidade_a_comprar))
    
    def buscar_item_por_nome(self, nome):
        for item in self.listar_insumos():
            if item.nome == nome:
                return item
        else:
            return None
    
    def __monta_lista(self):
        return self.__lista_de_compras
    
    def adicionar_producao_a_lista_de_compras(self):
        pass

    def listar_insumos(self):
        lista_de_insumos = self.__insumo.lista_insumos()
        lista_de_nomes = []
        for item in lista_de_insumos:
            lista_de_nomes.append(item.nome)
        return lista_de_nomes
    
    def abre_tela(self):
        while True:
            botao, valores = self.__tela_lista_de_compras.open(self.__monta_lista())
            if botao == "Adicionar Item...":
                informacoes = self.__tela_item_na_lista_de_compras.open(self.listar_insumos())
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