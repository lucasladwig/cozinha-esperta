import PySimpleGUI as sg


class TelaGerenciadorReceita:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None
        self.valores_teste = [["AB-123", "Escondidinho de Camarão",
                               "Lorem ipsumo dolor amnt it cuorsa clader umni"]]

    def init_components(self, dados_receitas=None):
        if dados_receitas is None:
            dados_receitas = []

        frame = [
            [sg.Table(values=dados_receitas,
                      headings=["Código", "Nome", "Descrição"],
                      auto_size_columns=True,
                      expand_x=True,
                      expand_y=True,
                      key="lista_receitas",
                      justification="left",
                      select_mode="browse",
                      num_rows=15)],
            [sg.Push(), sg.Button("Excluir Receita..."), sg.Button(
                "Editar Receita..."), sg.Button("Nova Receita...")]
        ]

        layout = [
            [sg.Text("Selecione uma receita para editar ou excluir (ou crie uma nova):")],
            [sg.Frame("Suas receitas", frame, expand_x=True)],
            [sg.Push(), sg.Button("Voltar")]
        ]

        self.__window = sg.Window("Insumos", layout, resizable=True)

    def open(self, dados_receitas=[]):
        self.init_components(dados_receitas)
        botao, valores = self.__window.read()
        linha = valores["lista_receitas"]
        if linha:
            valores["nome"] = self.__window.find_element("lista_receitas").get()[linha[0]][0]
        else:
            valores["nome"] = None
        # try:
        #     valores["nome"] = self.__window.find_element("lista_receitas").get()[
        #         linha[0]][0]
        # except:
        #     valores["nome"] = None
        return botao, valores

    def close(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)
