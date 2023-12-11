from entidade.item_lista_de_compras import ItemDeListaDeCompras
from entidade.insumo_teste import Insumo
from limite.tela_lista_de_compras import TelaListaDeCompras
from limite.tela_item_na_lista_de_compras import TelaItemNaListaDeCompras
from limite.tela_mensagem import TelaMensagem
from persistencia.lista_de_compras_dao import ListaDeComprasDAO


class ControladorListaDeCompras:
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__lista_de_compras_dao = ListaDeComprasDAO()
        self.__insumo = Insumo
        self.__tela_lista_de_compras = TelaListaDeCompras()
        self.__tela_item_na_lista_de_compras = TelaItemNaListaDeCompras()
        self.__tela_mensagem = TelaMensagem()

    def adicionar_na_lista_de_compras(self, valores: dict) -> None:
        if valores == None:
            self.__tela_item_na_lista_de_compras.close()
        else:
            self.__tela_item_na_lista_de_compras.close()
            nome = valores["it_nome"]
            try:
                quantidade = float(valores["it_quantidade"])
            except:
                self.__tela_mensagem.open("Insira um numero válido!")
                return
            item = self.buscar_item_por_nome(nome)
            if item == None:
                for insumo in self.__insumo.lista_insumos():  # Classe de teste
                    if insumo.nome == nome:
                        self.__lista_de_compras_dao.add(
                            ItemDeListaDeCompras(insumo, quantidade))
                        self.__tela_mensagem.open(
                            "Item Adicionado com sucesso!")
                        break
            else:
                item.quantidade += quantidade
                self.__tela_mensagem.open(
                    f"Item '{item.insumo.nome}' atualizado com sucesso!")

    def editar_na_lista_de_compras(self, valores: dict, nome: str) -> None:
        self.__tela_item_na_lista_de_compras.close()
        item = self.buscar_item_por_nome(nome)
        if valores == None:
            self.__tela_item_na_lista_de_compras.close()
        else:
            try:
                if float(valores["it_quantidade"]) != item.quantidade:
                    item.quantidade = float(valores["it_quantidade"])
                    self.__tela_mensagem.open(
                        f"Item '{item.insumo.nome}' atualizado com sucesso!")
            except:
                self.__tela_mensagem.open("Insira um numero válido!")
                return

    def buscar_item_por_nome(self, nome_busca: str) -> Insumo:
        for item in self.__lista_de_compras_dao.get_all():
            if item.insumo.nome == nome_busca:
                return item
        else:
            return None

    def __monta_lista(self) -> list:
        lista_item = []
        for values in self.__lista_de_compras_dao.get_all():
            lista_auxiliar = []
            lista_auxiliar.append(values.insumo.nome)
            lista_auxiliar.append(values.quantidade)
            lista_item.append(lista_auxiliar)
        return lista_item

    def adicionar_producao_a_lista_de_compras(self):
        pass

    def listar_nome_de_insumos(self) -> list:
        lista_de_insumos = self.__insumo.lista_insumos()  # Classe teste
        lista_de_nomes = []
        for item in lista_de_insumos:
            lista_de_nomes.append(item.nome)
        return lista_de_nomes

    def excluir_na_lista_de_compras(self, nome: str) -> None:
        self.__lista_de_compras_dao.remove(nome)

    def abre_tela(self) -> None:
        while True:
            botao, valores = self.__tela_lista_de_compras.open(
                self.__monta_lista())
            if botao == "Adicionar Item...":
                informacoes = self.__tela_item_na_lista_de_compras.open(
                    self.listar_nome_de_insumos())
                self.adicionar_na_lista_de_compras(informacoes)
            elif botao == "Editar Item...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    item = self.buscar_item_por_nome(valores["nome"])
                    informacoes = self.__tela_item_na_lista_de_compras.open(
                        [item.insumo.nome, item.quantidade])
                    self.editar_na_lista_de_compras(
                        informacoes, valores["nome"])
            elif botao == "Excluir Item da Lista...":
                if valores["nome"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.excluir_na_lista_de_compras(valores["nome"])
            elif botao == "Voltar":
                self.__tela_lista_de_compras.close()
                break
            self.__tela_lista_de_compras.close()
            self.__tela_lista_de_compras.init_components()
