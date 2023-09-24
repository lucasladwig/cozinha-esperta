import PySimpleGUI as sg


class TelaAtualizaEstoqueInsumo:

    def __init__(self):
        self.__window = None
        self.init_components([None, None, None])

    def init_components(self, lista):
        layout = [
            [sg.Text(f"{lista[0]}")],
            [sg.Text("Custo Unitario:"), sg.InputText(
                key="it_custo_unitario", default_text=lista[1])],
            [sg.Text("Estoque Atual:"), sg.InputText(
                key="it_estoque_atual", default_text=lista[2])],
            [sg.Text("Estoque Mínimo:"), sg.InputText(
                key="it_estoque_minimo", default_text=lista[3])]
            [sg.Submit("Cancelar"), sg.Cancel("Salvar")]
        ]

        self.__window = sg.Window("Atualiza Estoque Insumo").layout(layout)

    def open(self, lista):
        self.init_components(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()
