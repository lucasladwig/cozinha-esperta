from limite.tela import Tela
import PySimpleGUI as sg


class TelaCustosFixos(Tela):
    def __init__(self) -> None:
        super().__init__()

    def inicializar_janela(self):
        """"Gera o layout da janela do gerenciador de custos fixos."""

        # Campos de inserção
        agua = [sg.Push(),
                sg.Text("Água:"),
                sg.Input(key="agua", size=16)]
        aluguel = [sg.Push(),
                   sg.Text("Aluguel:"),
                   sg.Input(key="aluguel", size=16)]
        eletricidade = [sg.Push(),
                        sg.Text("Eletricidade:"),
                        sg.Input(key="eletricidade", size=16)]
        gas = [sg.Push(),
               sg.Text("Gás:"),
               sg.Input(key="gas", size=16)]
        manutencao = [sg.Push(),
                      sg.Text("Manutenção:"),
                      sg.Input(key="gas", size=16)]
        outros = [sg.Push(),
                  sg.Text("Outros:"),
                  sg.Input(key="custo_outros", size=16)]

        frame_custos = [[sg.Column([agua, aluguel, eletricidade]),
                        sg.Column([gas, manutencao, outros])]]

        layout = [
            [sg.Text("Insira uma estimativa do custo mensal (R$) com os itens abaixo:")],
            [sg.Frame("Custos Fixos:", frame_custos)],
            [sg.Text("Produção mensal total (porções):"),
             sg.Input(key="producao_mensal", size=14),
             sg.Button("Pegar do último mês")],
            [sg.Text("Contribuição do custos fixos por porção:"),
             sg.Text(key="custo_fixo_por_porcao")],
            [sg.Push(), sg.Button("Cancelar"), sg.Button("Salvar")]
        ]
        self.__window = sg.Window("Custos Fixos").layout(layout)

    def abrir_tela(self, lista):
        self.inicializar_janela(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None
