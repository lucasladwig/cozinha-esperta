import PySimpleGUI as sg


class TelaInsumo:
    def __init__(self):
        self.__window = None
        self.init_components()

    def init_components(self, lista=[]):
        layout = [[sg.Text("Insumos")],
                  [sg.Table(values=lista, headings=["calorias_por_unidade", "custo_unitario", "estoque_atual", "estoque_minimo", "id_insumo", "nome", "unidade"], auto_size_columns=True,
                            expand_x=True, expand_y=True, key="tab_objeto", justification="left", select_mode="browse")],
                  [sg.Button("Excluir Insumo..."), sg.Button("Editar Insumo..."), sg.Button("Novo Insumo...")],
                  [sg.Button("Voltar")]]

        self.__window = sg.Window("Insumos").layout(layout)

    def open(self, lista=[]):
        self.init_components(lista)
        botao, valores = self.__window.read()
        linha = valores["tab_objeto"]
        try:
            valores["id_insumo"] = self.__window.find_element("tab_objeto").get()[
                linha[0]][4]
        except:
            valores["id_insumo"] = None
        return botao, valores

    def close(self):
        self.__window.close()