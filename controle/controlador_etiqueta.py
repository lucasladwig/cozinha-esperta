from datetime import datetime, timedelta

from limite.tela_mensagem import TelaMensagem
from limite.tela_etiqueta import TelaEtiqueta
from persistencia.producao_dao import ProducaoDAO
from dados.receitas_dict import Receitas


class ControladorEtiqueta:
    # def __init__(self, controlador_sistema) -> None:
    def __init__(self) -> None:
        # self.__controlador_sistema = controlador_sistema
        self.__producao_dao = ProducaoDAO()
        self.__tela_etiqueta = TelaEtiqueta()
        self.__tela_mensagem = TelaMensagem()

    def cria_etiqueta(self, valores, id):
        producao = self.busca_producao_por_id(id)
        if valores == None:
            return self.__tela_mensagem.open("Nenhuma Produção Selecionada!")

        if producao.status == True:
            return self.__tela_mensagem.open("Você não pode alterar uma produção que já foi feita!")

        try:
            data_producao = (valores["it_data_validade"])
            data_formatada = datetime.strptime(
                data_producao, "%Y-%m-%d %H:%M:%S")
            data_formatada = data_formatada.date()
        except ValueError:
            try:
                data_producao = (valores["it_data_validade"])
                data_formatada = datetime.strptime(data_producao, "%Y-%m-%d")
            except ValueError:
                return self.__tela_mensagem.open("Erro na Data")

        if data_formatada < datetime.now().date():
            return self.__tela_mensagem.open("A data de produção não pode ser anterior a hoje!")
        etiqueta = f"{producao.receita['nome']}\n Fabricação: {datetime.strftime(producao.data_producao, '%Y-%m-%d')}\n Validade: {datetime.strftime(data_formatada, '%Y-%m-%d')}"
        self.__salva_etiqueta(etiqueta, producao.receita["nome"], producao.id)
        self.__tela_mensagem.open("Criação de etiqueta Concluida!")

    def busca_producao_por_id(self, id: str):
        for producao in self.__producao_dao.get_all():
            if producao.id == id:
                return producao
        else:
            return None

    def lista_dados_producao(self, id: str):
        lista_objeto_producao = []
        producao = self.busca_producao_por_id(id)
        lista_objeto_producao.append(producao.receita["nome"].title())
        lista_objeto_producao.append(
            producao.data_producao + timedelta(days=15))
        return lista_objeto_producao

    def __monta_lista(self):
        lista_producao = []
        producoes = self.__producao_dao.get_all()
        try:
            for values in producoes:
                if not values.status:
                    continue
                lista_auxiliar = []
                lista_auxiliar.append(values.id)
                lista_auxiliar.append(values.receita['nome'])
                lista_auxiliar.append(values.custo_total_producao)
                lista_auxiliar.append(datetime.strftime(
                    values.data_producao, "%Y-%m-%d"))
                lista_auxiliar.append(values.numero_porcoes)
                lista_auxiliar.append(
                    "Produzido" if values.status else "Não Produzido")
                lista_producao.append(lista_auxiliar)
            return lista_producao
        except:
            return lista_producao

    def __salva_etiqueta(self, etiqueta, nome, id_producao):
        # texto
        dados = etiqueta
        # nome do arquivo
        nome_arquivo = f"{nome}_{id_producao}.txt"
        # diretorio
        diretorio = 'etiquetas'
        # caminho completo
        caminho_completo = f"{diretorio}/{nome_arquivo}"
        # tipo de manipulaçao do arquivo
        modo_abertura = "w"

        with open(caminho_completo, modo_abertura) as arquivo:
            arquivo.write(dados)

    def abre_tela(self):
        while True:
            botao, valores = self.__tela_etiqueta.open(self.__monta_lista())
            self.__tela_etiqueta.close()

            if botao == "Gerar Etiqueta":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    producao = self.lista_dados_producao(valores["id"])
                    informacoes = self.__tela_edita_producao.open(producao)
                    self.cria_etiqueta(informacoes, valores["id"])
                    self.__tela_edita_producao.close()

            elif botao == "Produzir":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    producao = self.__produz(valores["id"])
                    self.__producao_dao.add(producao)

            elif botao == "Excluir Produção":
                if valores["id"] == None:
                    self.__tela_mensagem.open(
                        "Não foi selecionado nenhuma linha!")
                else:
                    self.__producao_dao.remove(valores["id"])
                    self.__tela_mensagem.open(
                        "Remoção Concluida!")
                    # metodo para liberar os intens

            elif botao == "Voltar":
                self.__tela_etiqueta.close()
                break

        self.__tela_producao.close()
        self.__tela_producao.init_components()
