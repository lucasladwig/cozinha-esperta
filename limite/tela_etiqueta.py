import PySimpleGUI as sg


class TelaEtiqueta:
    def __init__(self):
        self.__window = None
        self.init_components()

    def init_components(self, lista=[]):
        layout = [[sg.Table(values=lista, headings=["Id ", "Receita", "Custo Total de Produção", "Data de Produção", "Numero de Porções", "Status"], auto_size_columns=True, expand_x=True, expand_y=True, key="tab_objeto", justification="left", select_mode="browse")],
                  [sg.Button("Gerar Etiqueta")],
                  [sg.Button("Voltar")]]
        self.__window = sg.Window("Gerenciador de Etiquetas").layout(layout)

    def open(self, lista=[]): 
        self.init_components(lista)
        botao, valores = self.__window.read()
        linha = valores["tab_objeto"]
        if botao == sg.WINDOW_CLOSED:
            return 'Voltar', None
        try:
            valores["id"] = self.__window.find_element("tab_objeto").get()[
                linha[0]][0]
        except:
            valores["id"] = None
        return botao, valores

    def close(self):
        self.__window.close()
