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
            [sg.Text("Seja bem-vindo ao Cozinha Esperta! Escolha o módulo deejado no menu abaixo:")],
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
            valores["modulo"] = self.__window.find_element(
                "modulos").get()[linha[0]][0]
        else:
            valores["modulo"] = None

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





from limite.tela import Tela
import PySimpleGUI as sg


class TelaSistema(Tela):
    """Tela inicial do sistema."""

    modulos = [
        ["Insumos", "Gerencie os tipos de insumos com os quais sua cozinha trabalha.", ],
        ["Estoque", "Gerencie estoque e custos dos seus insumos.", ],
        ["Receitas", "Gerencie suas receitas e fichas técnicas.", ],
        ["Produções", "Planeje suas produções.", ],
        ["Lista de Compras", "Gere uma lista de compras com base em uma produção.", ],
        ["Relatórios de Custos", "Veja um relatório de custos de um período.", ],
        ["Custos Fixos", "Insira os custos fixos da sua cozinha para calcular de custos de seus pratos.", ],
        ["Etiquetagem", "Gere um arquivo de texto com as informações essenciais para uma etiqueta.", ],
    ]

    def __init__(self):
        super().__init__()

    def inicializar_tela(self):
        self.definir_layout()
        botao, valores = self.__window.read()
        opcao = "Voltar"

        match valores["-MODULOS-"]:
            case [0]:
                opcao = "Insumos"
                print("Insumos")
            case [1]:
                opcao = "Estoque"
                print("Estoque")
            case [2]:
                opcao = "Receitas"
                print("Receitas")
            case [3]:
                opcao = "Producoes"
                print("Producoes")
            case [4]:
                opcao = "Lista de Compras"
                print("Lista de compras")
            case [5]:
                opcao = "Relatorios de Custos"
                print("Relatorios de custos")
            case [6]:
                opcao = "Custos Fixos"
                print("Custos fixos")
            case [7]:
                opcao = "Etiquetagem"
                print("Etiquetas")
        
        if botao == "Encerrar":
            opcao = "Voltar"

        self.__window.close()
        return opcao

    def definir_layout(self):
        frame_modulos = [[sg.Table(values=self.modulos,
                                   headings=["Módulo", "Descrição"],
                                   num_rows=len(self.modulos),
                                   max_col_width=55,
                                   auto_size_columns=True,
                                   expand_x=True,
                                   key="-MODULOS-",
                                   justification="left",
                                   hide_vertical_scroll=True,
                                   select_mode="browse")],
                         [sg.Push(), sg.Button("Abrir Módulo")]]

        layout = [
            [sg.Text(
                "Seja bem-vindo ao Cozinha Esperta! Escolha o módulo desejado no menu abaixo:")],
            [sg.Frame("Módulos:", frame_modulos, expand_x=True)],
            [sg.Push(), sg.Button("Encerrar", pad=((0, 5), (20, 10)))]
        ]

        self.__window = sg.Window(
            "Cozinha Esperta v1.0", layout, resizable=True)
