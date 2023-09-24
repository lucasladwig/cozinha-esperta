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
        event, values = self.__window.read()
        return event, values

    # NAVEGAÇÃO
    def tela_opcoes(self):
        self.inicializar_janela()
        event, values = self.__window.read()
        opcao = 0

        # escolha de módulo
        if values['1']:
            opcao = 1
        if values['2']:
            opcao = 2
        if values['3']:
            opcao = 3

        # voltar ou encerrar
        if event in (None, 'Encerrar Sistema'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def inicializar_janela(self):
        layout = [[sg.Table(values=self.modulos, 
                            headings=["Módulo", "Descrição"], 
                            auto_size_columns=True,
                            expand_x=True, 
                            expand_y=True, 
                            key="-MODULOS-", 
                            justification="left", 
                            select_mode="browse", 
                            enable_events=True)],
                  [sg.Button("Excluir Insumo..."), sg.Button(
                      "Editar Insumo..."), sg.Button("Novo Insumo...")],
                  [sg.Button("Voltar")]]

        self.__window = sg.Window('Cozinha Esperta v1.0').layout(layout)
