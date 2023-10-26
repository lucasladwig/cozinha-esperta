import PySimpleGUI as sg


class TelaMensagem:
    def __init__(self):
        self.__window = None
        self.init_components()

    def init_components(self, mensagem=""):
        layout = [[sg.Text(mensagem)],
                  [sg.Button("Ok", size=5)]]

        self.__window = sg.Window(
            "Aviso", element_justification="c").layout(layout)

    def open(self, mensagem):
        self.init_components(mensagem)
        botao, valores = self.__window.read()
        if botao == "Ok":
            pass
        self.close()

    def close(self):
        self.__window.close()
