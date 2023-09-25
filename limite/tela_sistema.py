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

    def abrir_tela(self):
        self.inicializar_janela()
        botao, valores = self.__window.read()
        opcao = "Voltar"

        if botao == "Abrir Módulo":
            match valores["-MODULOS-"]:
                case [0]:
                    opcao = "Insumos"
                case [1]:
                    opcao = "Estoque"
                case [2]:
                    opcao = "Receitas"
                case [3]:
                    opcao = "Producoes"
                case [4]:
                    opcao = "Lista de Compras"
                case [5]:
                    opcao = "Relatorios de Custos"
                case [6]:
                    opcao = "Custos Fixos"
                case [7]:
                    opcao = "Etiquetagem"
        elif botao in ("Encerrar", None):
            opcao = "Voltar"

        self.fechar_tela()
        return opcao

    def inicializar_janela(self):
        frame_modulos = [[sg.Table(values=self.modulos,
                                   headings=["Módulo", "Descrição"],
                                   num_rows=len(self.modulos),
                                   max_col_width=55,
                                   auto_size_columns=True,
                                   expand_x=True,
                                   key="-MODULOS-",
                                   justification="left",
                                   hide_vertical_scroll=True,
                                   enable_events=True,
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
