import time
from entidade.insumo import Insumo
from persistencia.insumo_dao import InsumoDAO
from limite.tela_estoque_insumo import TelaEstoqueInsumo
from limite.tela_edita_estoque_insumo import TelaAtualizaEstoqueInsumo
from limite.tela_mensagem import TelaMensagem


class ControladorEstoqueInsumo:
    def __init__(self) -> None:
        self.__insumo_dao = InsumoDAO()
        self.__tela_estoque_insumo = TelaEstoqueInsumo()
        self.__tela_atualiza_estoque_insumo = TelaAtualizaEstoqueInsumo()
        self.__tela_mensagem = TelaMensagem()

    def edita_insumo(self, valores, nome):
        self.__tela_estoque_insumo.close()
        self.__tela_atualiza_estoque_insumo.close()
        insumo = self.busca_insumo_por_nome(nome)
        if valores == None:
            self.__tela_atualiza_estoque_insumo.close()
        else:
            if valores["it_custo_unitario"] != insumo.custo_unitario:
                try:
                    custo_unitario = float(valores["it_custo_unitario"])
                    insumo.custo_unitario = custo_unitario
                except (ValueError, TypeError):
                    self.__tela_mensagem.open("Caractere Invalido!")
                    return

            if valores["it_estoque_atual"] != insumo.estoque_atual:
                try:
                    estoque_atual = float(valores["it_estoque_atual"])
                    insumo.estoque_atual = estoque_atual
                except (ValueError, TypeError):
                    self.__tela_mensagem.open("Caractere Invalido!")
                    return

            if valores["it_estoque_minimo"] != insumo.estoque_minimo:
                try:
                    estoque_minimo = float(valores["it_estoque_minimo"])
                    insumo.estoque_minimo = estoque_minimo
                except (ValueError, TypeError):
                    self.__tela_mensagem.open("Caractere Invalido!")
                    return
            self.__insumo_dao.add(insumo=insumo)

    def busca_insumo_por_nome(self, nome_busca: str):
        for insumo in self.__insumo_dao.get_all():
            if insumo.nome == nome_busca:
                return insumo
        else:
            return None

    def lista_dados_insumo(self, nome):
        lista_objeto_insumo = []
        insumo = self.busca_insumo_por_nome(nome)
        lista_objeto_insumo.append(insumo.nome.upper())
        lista_objeto_insumo.append(insumo.custo_unitario)
        lista_objeto_insumo.append(insumo.estoque_atual)
        lista_objeto_insumo.append(insumo.estoque_minimo)
        lista_objeto_insumo.append(insumo.unidade)
        return lista_objeto_insumo

    def __monta_lista(self):
        lista_insumo = []
        for values in self.__insumo_dao.get_all():
            lista_auxiliar = []
            lista_auxiliar.append(values.nome)
            lista_auxiliar.append(values.custo_unitario)
            lista_auxiliar.append(values.estoque_atual)
            lista_auxiliar.append(values.estoque_minimo)
            lista_auxiliar.append(values.unidade)
            lista_insumo.append(lista_auxiliar)
        return lista_insumo

    def abre_tela(self):
        while True:
            botao, valores = self.__tela_estoque_insumo.open(
                self.__monta_lista())
            if botao == "Editar Estoque Insumo":
                if valores["nome"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.__tela_estoque_insumo.close()
                    informacoes = self.__tela_atualiza_estoque_insumo.open(
                        self.lista_dados_insumo(valores["nome"]))
                    self.edita_insumo(informacoes, valores["nome"])

            elif botao == "Voltar":
                self.__tela_estoque_insumo.close()
                break

                # self.voltar()
        self.__tela_estoque_insumo.close()
        self.__tela_estoque_insumo.init_components()
        # novo insumo
        # edita insumo
        # excluir insumo
