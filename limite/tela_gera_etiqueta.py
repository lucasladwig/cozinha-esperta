import PySimpleGUI as sg


class TelaGeraEtiqueta:

    def __init__(self):
        self.__window = None
        self.init_components([None, None, None])

    def init_components(self, lista):

        layout = [
            [sg.Text(f"{lista[0]}", pad=((100, 0), (0, 0)))],
            [sg.Text("Data de Validade:"), sg.CalendarButton("Data", target="it_data", pad=((5, 0), (0, 10))), sg.InputText(key="it_data_validade", default_text=lista[1], size=(10, 1), pad=((20, 0), (0, 15)))],
            [sg.Submit("Cancelar"), sg.Cancel("Salvar", pad=((30, 0), (0, 0)))]
        ]
        window_size = (350, 150)
        # self.__window = sg.Window("Atualiza Estoque Insumo").layout(layout)
        self.__window = sg.Window(
            "Editar Produção", layout, size=window_size)

    def open(self, lista):
        if not lista:
            lista = [None, None, None]

        self.init_components(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None
