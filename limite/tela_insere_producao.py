import PySimpleGUI as sg


class TelaInsereProducao:

    def __init__(self):
        self.__window = None
        self.init_components([None, None, None], None)

    def init_components(self, lista, receitas):
        if receitas:  # condicional necessaria para primeira inicialização da tela
            receitas = [receita.nome for receita in receitas]

        layout = [
            [sg.Text(f"Receita a Produzir:"), sg.Combo(
                receitas, default_value=lista[0], key="it_receita", size=(15, 1), pad=((5, 0), (2, 10)))],
            [sg.Text("Quantidade (porções)"), sg.InputText(
                key="it_quantidade", default_text=lista[1], size=(10, 1), pad=((45, 0), (0, 10)))],
            [sg.Text("Data da Produção:"), sg.CalendarButton("Data", target="it_data", pad=(
                (5, 0), (0, 10))), sg.InputText(key="it_data", default_text=lista[2], size=(10, 1), pad=((20, 0), (0, 15)))],
            [sg.Submit("Cancelar"), sg.Cancel("Salvar", pad=((30, 0), (0, 0)))]
        ]
        window_size = (350, 150)
        # self.__window = sg.Window("Atualiza Estoque Insumo").layout(layout)
        self.__window = sg.Window(
            "Inserir Produção", layout, size=window_size)

    def open(self, lista, receitas=None):
        if not lista:
            lista = [None, None, None]

        self.init_components(lista, receitas)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            receita_escolhida = [
                receita for receita in receitas if receita.nome == valores["it_receita"]]
            if not receita_escolhida:
                return None
            valores["it_receita"] = receita_escolhida[0]
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()