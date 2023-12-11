import PySimpleGUI as sg


class TelaRelatorioDeCustos:
    def __init__(self):
        self.__window = None
        self.init_components(None, None, None, None)

    def init_components(self, lista, inicio, fim, custo_total):
        layout = [[sg.Text(f"Produções do período de {inicio} a {fim}")],
                  [sg.Table(values=lista, headings=["nome", "custo_total", "data"], auto_size_columns=True,
                            expand_x=True, expand_y=True, key="tab_objeto", justification="left", select_mode="browse")],
                  [sg.Text(f"Custo total do período (R$): {custo_total}")],
                  [sg.Button("Voltar")]]

        self.__window = sg.Window("Relatório de Custos").layout(layout)

    def open(self, lista, inicio, fim, custo_total):
        self.init_components(lista, inicio, fim, custo_total)
        botao, valores = self.__window.read()
        return botao, valores

    def close(self):
        self.__window.close()