import PySimpleGUI as sg


class TelaGerenciadorReceitas:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None

    def definir_layout(self, dados_receitas=None):
        """Cria o layout da tela."""
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
        return layout
        

    def abrir_tela(self, dados_receitas: list = []):
        """Inicializa a tela com o layout definido e os campos preenchidos com os dados passados."""
        layout = self.definir_layout(dados_receitas)
        self.__window = sg.Window(
            "Gerenciador de Receitas", layout, size=(720, 420), resizable=True)
        botao, valores = self.__window.read()
        
        linha = valores["lista_receitas"]
        if linha:
            valores["codigo"] = self.__window.find_element(
                "lista_receitas").get()[linha[0]][0]
        else:
            valores["codigo"] = None

        return botao, valores

    def fechar_tela(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem: str, titulo: str = ""):
        sg.popup(mensagem, title=titulo)

    def confirmar_exclusao(self) -> bool:
        layout = [
            [sg.T('Tem certeza que deseja excluir esta receita?\nEssa ação NÃO pode ser desfeita!')],
            [sg.Push(), sg.Button("Não", s=10), sg.Button("Sim", s=10)],
        ]

        escolha, _ = sg.Window("Confirmar exclusão",
                               layout, disable_close=True).read(close=True)
        return escolha
