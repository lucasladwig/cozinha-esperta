import PySimpleGUI as sg


class TelaCadastroInsumo:
    unidades = ["ml", "l", "g", "kg", "un."]

    def __init__(self):
        self.__window = None
        self.init_components([None, None, None])

    def init_components(self, lista):
        layout = [[sg.Text("Nome do insumo:"), sg.InputText(key="it_nome", default_text=lista[0])],
                  [sg.Text("Unidade de medida:"), sg.Combo(self.unidades, auto_size_text=True, readonly=True, key="it_unidade", default_value=lista[1])],
                  [sg.Text("Valor Calórico (por unidade de medida):"), sg.InputText(key="it_caloria", default_text=lista[2])],
                  [sg.Submit("Cancelar"), sg.Cancel("Salvar")]]

        self.__window = sg.Window("Cadastro de insumo").layout(layout)

    def open(self, lista):
        self.init_components(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()