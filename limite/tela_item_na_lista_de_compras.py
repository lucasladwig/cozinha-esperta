import PySimpleGUI as sg


class TelaItemNaListaDeCompras:
    def __init__(self):
        self.__window = None
        self.init_components([None, None, None])

    def init_components(self, lista):
        layout = [[sg.Text("Nome do insumo:"), sg.InputText(key="it_nome", default_text=lista[0])],
                  [sg.Text("Quantidade:"), sg.Combo(self.unidades, auto_size_text=True, readonly=True, key="it_quantidade", default_value=lista[1])],
                  [sg.Submit("Cancelar"), sg.Cancel("Salvar")]]

        self.__window = sg.Window("Inserir/Editar Item na Lista de Compras").layout(layout)

    def open(self, lista):
        self.init_components(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()