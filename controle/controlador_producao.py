from entidade.producao import Producao
from persistencia.producao_dao import ProducaoDAO
from limite.tela_producao import TelaProducao
from limite.tela_insere_producao import TelaInsereProducao
from limite.tela_edita_producao import TelaEditaProducao
from limite.tela_mensagem import TelaMensagem
from dados.receitas_dict import Receitas

from datetime import datetime, date


class ControladorProducao:
    def __init__(self) -> None:
        self.__producao_dao = ProducaoDAO()
        self.__tela_producao = TelaProducao()
        self.__tela_insere_producao = TelaInsereProducao()
        self.__tela_edita_producao = TelaEditaProducao()
        self.__tela_mensagem = TelaMensagem()

    def edita_producao(self, valores, id):
        # self.__tela_estoque_insumo.close()
        # self.__tela_atualiza_estoque_insumo.close()
        producao = self.busca_producao_por_id(id)
        if valores == None:
            return

        if producao.status == True:
            return self.__tela_mensagem.open("Você não pode alterar uma produção que já foi feita!")

        if valores["it_quantidade"] != str(producao.numero_porcoes):
            try:
                numero_porcoes = int(valores["it_quantidade"])
                if numero_porcoes < 0:
                    raise ValueError
                producao.numero_porcoes = numero_porcoes
            except (ValueError, TypeError):
                self.__tela_mensagem.open("Caractere Invalido!")
                return

        try:
            data_producao = (valores["it_data"])
            data_formatada = datetime.strptime(
                data_producao, "%Y-%m-%d %H:%M:%S")
            data_formatada = data_formatada.date()
        except ValueError:
            try:
                data_producao = (valores["it_data"])
                data_formatada = datetime.strptime(data_producao, "%Y-%m-%d")
            except ValueError:
                return self.__tela_mensagem.open("Erro na Data")

        if data_formatada < datetime.now().date():
            return self.__tela_mensagem.open("A data de produção não pode ser anterior a hoje!")

        if data_formatada != producao.data_producao:
            producao.data_producao = data_formatada.date()

        self.__producao_dao.add(producao=producao)
        self.__tela_mensagem.open("Alteração Concluida!")

    def cria_producao(self, potencial_producao):
        # verificação do objeto receita
        try:
            quantidade_porcoes = int(potencial_producao.get("it_quantidade"))
            if quantidade_porcoes < 1:
                raise ValueError
        except (ValueError, TypeError):
            return self.__tela_mensagem.open("Caractere Invalido!")

        try:
            data_producao = potencial_producao["it_data"]
            data_formatada = datetime.strptime(
                data_producao, "%Y-%m-%d %H:%M:%S")

            if data_formatada.date() < datetime.now().date():
                return self.__tela_mensagem.open("A data de produção não pode ser anterior a hoje!")

        except BaseException:
            return self.__tela_mensagem.open("Erro na Data")

        producao = Producao(receita=potencial_producao["it_receita"],
                            custo_total_producao=potencial_producao["it_receita"]["custo_porcao"],
                            numero_porcoes=quantidade_porcoes,
                            data_producao=data_formatada.date(),
                            status=False)

        self.__producao_dao.add(producao=producao)
        self.__tela_mensagem.open("Produção criada com sucesso!")
        # metodo para pegar os itens utilizados nessa receita

    def busca_producao_por_id(self, id: str):
        for producao in self.__producao_dao.get_all():
            if producao.id == id:
                return producao
        else:
            return None

    def lista_dados_producao(self, id):
        lista_objeto_producao = []
        producao = self.busca_producao_por_id(id)
        lista_objeto_producao.append(producao.receita["nome"].title())
        lista_objeto_producao.append(producao.numero_porcoes)
        lista_objeto_producao.append(producao.data_producao)
        return lista_objeto_producao

    def __monta_lista(self):
        lista_insumo = []
        producoes = self.__producao_dao.get_all()
        try:
            for values in producoes:
                lista_auxiliar = []
                lista_auxiliar.append(values.id)
                lista_auxiliar.append(values.receita['nome'])
                lista_auxiliar.append(values.custo_total_producao)
                lista_auxiliar.append(datetime.strftime(
                    values.data_producao, "%Y-%m-%d"))
                lista_auxiliar.append(values.numero_porcoes)
                lista_auxiliar.append(
                    "Produzido" if values.status else "Não Produzido")
                lista_insumo.append(lista_auxiliar)
            return lista_insumo
        except:
            return lista_insumo

    def __produz(self, id):
        producao = self.busca_producao_por_id(id)
        if producao.status:
            self.__tela_mensagem.open(
                "Receita Já Produzida")
            return
        producao.status = True
        self.__tela_mensagem.open("Alteração Concluida!")
        return producao

        # dispara metodo para efetivar os intens utilizados

    def abre_tela(self):
        while True:
            botao, valores = self.__tela_producao.open(self.__monta_lista())
            self.__tela_producao.close()

            if botao == "Nova Produção":
                receitas = Receitas
                informacoes = self.__tela_insere_producao.open(
                    lista=None, receitas=receitas)
                if informacoes:
                    self.cria_producao(informacoes)

                self.__tela_insere_producao.close()

            elif botao == "Editar Produção":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.__tela_producao.close()
                    receitas = Receitas
                    informacoes = self.__tela_edita_producao.open(
                        self.lista_dados_producao(valores["id"]))
                    self.edita_producao(informacoes, valores["id"])
                    self.__tela_edita_producao.close()

            elif botao == "Produzir":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.__tela_producao.close()
                    producao = self.__produz(valores["id"])
                    self.__producao_dao.add(producao)

            elif botao == "Excluir Produção":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.__tela_producao.close()
                    self.__producao_dao.remove(valores["id"])
                    self.__tela_mensagem.open(
                        "Remoção Concluida!")
                    # metodo para liberar os intens

            elif botao == "Voltar":
                self.__tela_producao.close()
                break

        self.__tela_producao.close()
        self.__tela_producao.init_components()
