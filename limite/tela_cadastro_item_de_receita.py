import PySimpleGUI as sg


class TelaCadastroItemDeReceita:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None

    def init_components(self, lista_insumos: list):
        layout = [
            [sg.Text("Insumo:"), sg.Combo(lista_insumos, key="nome_insumo")],
            [sg.Text("Quantidade:"),
             sg.Input(key="qtd",
                      size=5,
                      default_text="0",
                      tooltip="Quantidade do item (na unidade do insumo)"),
             sg.Radio("Bruta", 
                      "tipo_qtd", 
                      key="bruta",
                      default=True,
                      size=(10, 1),
                      tooltip="Calcular com base na quantidade bruta"),
             sg.Radio("Limpa", 
                      "tipo_qtd", 
                      key="limpa",
                      size=(10, 1),
                      tooltip="Calcular com base na quantidade limpa")],
            [sg.Text("Fator de Correção (FC):"),
             sg.Input(key="fator_correcao",
                      size=5,
                      default_text="1.0",
                      tooltip="Fator de correção do item para este preparo")],
            [sg.Text("Índice de Cocção (IC):"),
             sg.Input(key="indice_coccao",
                      size=5,
                      default_text="1.0",
                      tooltip="Índice de cocção do item para este preparo")],
            [sg.Push(), sg.Submit("Cancelar"), sg.Cancel("Salvar")]
        ]

        self.__window = sg.Window(
            "Inserir/editar item de receita", layout, resizable=True)

    def open(self, lista_insumos):
        self.init_components(lista_insumos)
        botao, valores = self.__window.read()
        if botao == "Salvar":
            return valores
        elif botao == "Cancelar":
            return None

    def close(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)
