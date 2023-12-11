import PySimpleGUI as sg


class TelaSistema:
    """Interface de usuário para selecionar a funcionalidade."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None
    
    def definir_layout(self, modulos): 
        """Cria o layout da tela."""
        frame = [
            [sg.Table(values=modulos,
                      headings=["Módulo", "Descrição"],
                      auto_size_columns=True,
                      expand_x=True,
                      expand_y=True,
                      key="modulos",
                      justification="left",
                      select_mode="browse",
                      num_rows=15)],
            [sg.Push(), sg.Button("Abrir Módulo...")]
        ]

        layout = [
            [sg.Text("Seja bem-vindo ao Cozinha Esperta! Escolha o módulo desejado no menu abaixo:")],
            [sg.Frame("Módulos", frame, expand_x=True)],
            [sg.Push(), sg.Button("Encerrar")]
        ]
        return layout

    def abrir_tela(self, modulos: list = []):
        """Inicializa a tela com o layout definido e os campos preenchidos com os dados passados."""
        layout = self.definir_layout(modulos)
        self.__window = sg.Window(
            "Cozinha Esperta v1.0", layout, size=(720, 420), resizable=True)
        botao, valores = self.__window.read()
        
        linha = valores["modulos"]
        if linha:
            valores["modulos"] = self.__window.find_element(
                "modulos").get()[linha[0]][0]
        else:
            valores["modulos"] = None

        return valores["modulos"]

    def fechar_tela(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem: str, titulo: str = ""):
        sg.popup(mensagem, title=titulo)
