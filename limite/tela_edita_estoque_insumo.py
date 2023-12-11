import PySimpleGUI as sg


class TelaAtualizaEstoqueInsumo:

    def __init__(self):
        self.__window = None
        self.init_components([None, None, None, None, None])

    def init_components(self, lista):
        layout = [
            [sg.Text(f"{lista[0]}", pad=((100, 0), (0, 0)))],
            [sg.Text(f"Custo por {lista[4]} em R$:"), sg.InputText(
                key="it_custo_unitario", default_text=lista[1], size=(10, 1), pad=((5, 0), (2, 10)))],
            [sg.Text("Estoque Atual:"), sg.InputText(
                key="it_estoque_atual", default_text=lista[2], size=(10, 1), pad=((45, 0), (0, 10))), sg.Text(lista[4])],
            [sg.Text("Estoque Mínimo:"), sg.InputText(
                key="it_estoque_minimo", default_text=lista[3], size=(10, 1), pad=((33, 0), (0, 15))), sg.Text(lista[4])],
            [sg.Submit("Cancelar"), sg.Cancel("Salvar", pad=((30, 0), (0, 0)))]
        ]
        window_size = (350, 150)
        # self.__window = sg.Window("Atualiza Estoque Insumo").layout(layout)
        self.__window = sg.Window(
            "Atualiza Estoque Insumo", layout, size=window_size)

    def open(self, lista):
        self.init_components(lista)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()
