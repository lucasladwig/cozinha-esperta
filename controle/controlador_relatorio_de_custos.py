from datetime import datetime
from persistencia.producao_dao import ProducaoDAO
from limite.tela_relatorio_de_custos import TelaRelatorioDeCustos
from limite.tela_gerar_relatorio_de_custos import TelaGerarRelatorioDeCustos
from limite.tela_mensagem import TelaMensagem

class ControladorRelatorioDeCustos:
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__producao_dao = ProducaoDAO()
        self.__tela_relatorio_de_custos = TelaRelatorioDeCustos()
        self.__tela_gerar_relatorio_de_custos = TelaGerarRelatorioDeCustos()
        self.__tela_mensagem = TelaMensagem()

    def buscar_periodo(self, dataInicio, dataFim):
        lista_producao = []
        producoes = self.__producao_dao.get_all()
        for values in producoes:
            data = datetime.strftime(values.data_producao, "%Y-%m-%d")
            if data >= dataInicio and data <= dataFim:
                lista_auxiliar = []
                lista_auxiliar.append(values.receita['nome'])
                lista_auxiliar.append(values.custo_total_producao)
                lista_auxiliar.append(data)
                lista_producao.append(lista_auxiliar)
        return lista_producao

    def abrir_tela(self):
        while True:
            botao, valores = self.__tela_gerar_relatorio_de_custos.open()
            if botao == "Visualizar":
                inicio = valores['-STARTDATE-'].split(' ')[0]
                fim = valores['-ENDDATE-'].split(' ')[0]
                lista_producao = self.buscar_periodo(inicio, fim)
                if len(lista_producao) == 0:
                    self.__tela_mensagem.open("Não há produções neste intervalo de datas!")
                    self.__tela_gerar_relatorio_de_custos.close()
                else:
                    custo_total = 0
                    for itens in lista_producao:
                        custo_total += itens[1]
                    self.__tela_relatorio_de_custos.open(lista_producao, inicio, fim, custo_total)
                    self.__tela_relatorio_de_custos.close()
                    self.__tela_gerar_relatorio_de_custos.close()
            elif botao == "Cancelar":
                self.__tela_gerar_relatorio_de_custos.close()
            return