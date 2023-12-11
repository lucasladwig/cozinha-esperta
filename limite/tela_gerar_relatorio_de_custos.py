import PySimpleGUI as sg


class TelaGerarRelatorioDeCustos:
    def __init__(self):
        self.__window = None
        self.init_components()

    def init_components(self):
        layout = [[sg.Text('Selecione a data inicial e a data final no formato dd/mm/aaaa:')],
                  [sg.Text("Data inicial:"), sg.CalendarButton("Data", target="-STARTDATE-", pad=(
                (5, 0), (0, 10))), sg.InputText(key="-STARTDATE-", size=(10, 1), pad=((20, 0), (0, 15)))],
                  [sg.Text("Data final:"), sg.CalendarButton("Data", target="-ENDDATE-", pad=(
                (5, 0), (0, 10))), sg.InputText(key="-ENDDATE-", size=(10, 1), pad=((20, 0), (0, 15)))],
                  [sg.Cancel("Cancelar"), sg.Submit("Visualizar")]]

        self.__window = sg.Window("Gerar Relatório de Custos").layout(layout)

    def open(self):
        botao, valores = self.__window.read()
        if botao == "Visualizar":
            return botao, valores
        elif botao == "Cancelar":
            return botao, valores

    def close(self):
        self.__window.close()