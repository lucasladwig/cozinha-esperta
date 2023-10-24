import PySimpleGUI as sg


class TelaItemNaListaDeCompras:
    def __init__(self):
        self.__window = None
        self.init_components([None, None, None])

    def init_components(self, lista):
        if isinstance(lista[1], float):
            quantidade = lista[1]
            lista = [lista[0]]
        else:
            quantidade = None
        layout = [[sg.Text("Nome:"), sg.Combo(lista, auto_size_text=False, readonly=True, key="it_nome", default_value=lista[0])],
                  [sg.Text("Quantidade:"), sg.InputText(quantidade, key="it_quantidade")],
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