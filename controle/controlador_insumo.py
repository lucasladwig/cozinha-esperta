from entidade.insumo import Insumo
from limite.tela_insumo import TelaInsumo
from limite.tela_mensagem import TelaMensagem
from persistencia.insumo_dao import InsumoDAO


class ControladorInsumo:
    lista_inicial = [None, None, None, None, None, None, None]

    def __init__(self) -> None:
        self.__tela_insumo = TelaInsumo()
        self.__insumo_dao = InsumoDAO()
        self.__tela_mensagem = TelaMensagem()

    def cadastra_insumo(self):
        pass

    def edita_insumo(self):
        pass

    def exclui_insumo(self):
        pass

    def busca_insumo_por_id(self, id_insumo: int):
        for insumo in self.__insumo_dao.get_all():
            if insumo.id_insumo == id_insumo:
                return insumo
        else:
            return None

    def lista_dados_insumo(self, id_insumo):
        lista_objeto_insumo = []
        insumo = self.busca_insumo_por_id(id_insumo)
        lista_objeto_insumo.append(insumo.calorias_por_unidade)
        lista_objeto_insumo.append(insumo.custo_unitario)
        lista_objeto_insumo.append(insumo.estoque_atual)
        lista_objeto_insumo.append(insumo.estoque_minimo)
        lista_objeto_insumo.append(insumo.id_insumo)
        lista_objeto_insumo.append(insumo.nome)
        lista_objeto_insumo.append(insumo.unidade)
        return lista_objeto_insumo

    def __monta_lista(self):
        lista_insumo = []
        for values in self.__insumo_dao.get_all():
            lista_auxiliar = []
            lista_auxiliar.append(values.calorias_por_unidade)
            lista_auxiliar.append(values.custo_unitario)
            lista_auxiliar.append(values.estoque_atual)
            lista_auxiliar.append(values.estoque_minimo)
            lista_auxiliar.append(values.id_insumo)
            lista_auxiliar.append(values.nome)
            lista_auxiliar.append(values.unidade)
            lista_insumo.append(lista_auxiliar)
        return lista_insumo

    def abre_tela(self):
        while True:
            botao, valores = self.__tela_insumo.open(self.__monta_lista())
            if botao == "Novo Insumo...":
                informacoes = self.__tela_insumo.open(
                    self.lista_inicial)
                self.cadastra_insumo(informacoes)
            elif botao == "Editar Insumo...":
                if valores["id_insumo"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    informacoes = self.__tela_insumo.open(
                        self.lista_dados_insumo(valores["id_insumo"]))
                    self.edita_insumo(informacoes, valores["id_insumo"])
            elif botao == "Excluir Insumo...":
                if valores["id_insumo"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.exclui_insumo(valores["id_insumo"])
            elif botao == "Voltar":
                self.__tela_insumo.close()
                # self.voltar()
            self.__tela_insumo.close()
            self.__tela_insumo.init_components()