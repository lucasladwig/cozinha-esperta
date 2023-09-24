from limite.tela import Tela
import PySimpleGUI as sg


class TelaSistema(Tela):
    """Tela inicial do sistema."""

    # Nomes e descrições dos módulos
    modulos = [
        ["Insumos", "Gerencie os tipos de insumos com os quais sua cozinha trabalha.", ],
        ["Estoque", "Gerencie estoque e custos dos seus insumos.", ],
        ["Receitas", "Gerencie suas receitas e fichas técnicas.", ],
        ["Produções", "Planeje suas produções.", ],
        ["Listas de Compras", "Gere uma lista de compras com base em uma produção.", ],
        ["Relatórios de Custos", "Veja um relatório de custos de um período.", ],
        ["Custos Fixos", "Insira os custos fixos da sua cozinha para calcular de custos de seus pratos.", ],
        ["Etiquetagem", "Gere um arquivo de texto com as informações essenciais para uma etiqueta.", ],
    ]

    def __init__(self):
        super().__init__()

    # ABRIR/FECHAR
    def abrir_tela(self):
        botao, valores = self.__window.read()
        return botao, valores

    # NAVEGAÇÃO
    def escolher_modulo(self):
        self.inicializar_janela()
        while True:
            event, values = self.__window.read()
            print("event:", event, "values:", values)
            if event == sg.WIN_CLOSED:
                break
            if '+CLICKED+' in event:
                print(f"You clicked row: {event[2][0]} Column: {event[2][1]}")
        self.__window.close()

        # botao, valores = self.__window.read()
        # modulo = valores["-MODULOS-"]
        # try:
        #     valores["Módulo"] = self.__window.find_element("-MODULOS-").get()[
        #         modulo[0]][0]
        # except:
        #     valores["nome"] = None
        
        # return botao, valores

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
