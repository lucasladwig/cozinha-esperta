from entidade.item_lista_de_compras import ItemDeListaDeCompras
from entidade.insumo_teste import Insumo
from limite.tela_lista_de_compras import TelaListaDeCompras
from limite.tela_item_na_lista_de_compras import TelaItemNaListaDeCompras
from limite.tela_mensagem import TelaMensagem


class ControladorListaDeCompras:
    def __init__(self) -> None:
        self.__lista_de_compras = []
        self.__insumo = Insumo
        self.__tela_lista_de_compras = TelaListaDeCompras()
        self.__tela_item_na_lista_de_compras = TelaItemNaListaDeCompras()
        self.__tela_mensagem = TelaMensagem()

    def adicionar_na_lista_de_compras(self, valores):
        if valores == None:
            self.__tela_item_na_lista_de_compras.close()
        else:
            self.__tela_lista_de_compras.close()
            self.__tela_item_na_lista_de_compras.close()
            nome = valores["it_nome"]
            quantidade = float(valores["it_quantidade"])
            item = self.buscar_item_por_nome(nome)
            if item == None:
                for insumo in self.__insumo.lista_insumos(): # Classe de teste
                    if insumo.nome == nome:
                        self.__lista_de_compras.append(ItemDeListaDeCompras(insumo, quantidade))
                        self.__tela_mensagem.open("Item Adicionado com sucesso!")
                        break
            else:
                item.quantidade += quantidade
                self.__tela_mensagem.open(f"Item '{item.insumo.nome}' atualizado com sucesso!")
        
    def editar_na_lista_de_compras(self, valores, nome):
        self.__tela_lista_de_compras.close()
        self.__tela_item_na_lista_de_compras.close()
        item = self.buscar_item_por_nome(nome)
        if valores == None:
            self.__tela_item_na_lista_de_compras.close()
        else:
            if float(valores["it_quantidade"]) != item.quantidade:
                item.quantidade = float(valores["it_quantidade"])

    def verificar_estoque(self):
        lista_de_insumos = self.__insumo.lista_insumos() # Classe teste
        for insumo in lista_de_insumos:
            if insumo.estoque_minimo > insumo.estoque_atual:
                for item in self.__lista_de_compras:
                    if insumo.nome == item.insumo.nome:
                        break
                else:
                    quantidade_a_comprar = insumo.estoque_minimo - insumo.estoque_atual
                    self.__lista_de_compras.append(ItemDeListaDeCompras(insumo, quantidade_a_comprar))

    def buscar_item_por_nome(self, nome):
        for item in self.__lista_de_compras:
            if item.insumo.nome == nome:
                return item
        else:
            return None
    
    def __monta_lista(self):
        self.verificar_estoque()
        lista_insumo = []
        for item in self.__lista_de_compras:
            lista_auxiliar = []
            lista_auxiliar.append(item.insumo.nome)
            lista_auxiliar.append(item.quantidade)
            lista_insumo.append(lista_auxiliar)
        return lista_insumo
    
    def adicionar_producao_a_lista_de_compras(self):
        pass

    def listar_nome_de_insumos(self):
        lista_de_insumos = self.__insumo.lista_insumos() # Classe teste
        lista_de_nomes = []
        for item in lista_de_insumos:
            lista_de_nomes.append(item.nome)
        return lista_de_nomes
    
    def abre_tela(self):
        while True:
            botao, valores = self.__tela_lista_de_compras.open(self.__monta_lista())
            if botao == "Adicionar Item...":
                informacoes = self.__tela_item_na_lista_de_compras.open(self.listar_nome_de_insumos())
                self.adicionar_na_lista_de_compras(informacoes)
            elif botao == "Editar Item...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open("Não foi selecionado nenhuma linha!")
                else:
                    item = self.buscar_item_por_nome(valores["nome"])
                    informacoes = self.__tela_item_na_lista_de_compras.open([item.insumo.nome, item.quantidade])
                    self.editar_na_lista_de_compras(informacoes, valores["nome"])
            elif botao == "Excluir Insumo...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.exclui_insumo(valores["nome"])
            elif botao == "Voltar":
                self.__tela_lista_de_compras.close()
                # self.voltar()
            self.verificar_estoque()
            self.__tela_lista_de_compras.close()
            self.__tela_lista_de_compras.init_components()