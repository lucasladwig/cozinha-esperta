import PySimpleGUI as sg


class TelaFiltroReceitas:
    """Interface de usuário para filtrar as receitas."""

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

        receitas = [
            [sg.Table(values=dados_receitas,
                      headings=["Código", "Nome", "Descrição"],
                      auto_size_columns=True,
                      expand_x=True,
                      expand_y=True,
                      key="lista_receitas",
                      justification="left",
                      select_mode="browse",
                      num_rows=15)],
            [sg.Push(), sg.Button("Ver Receita Selecionada...")]
        ]

        filtros = [
            # Custos
            [sg.Radio("Por custo (R$) da porção: de",
                      "tipo_filtro",
                      key="filtro_custo",
                      default=True,
                      tooltip="Filtrar receitas por custo"),
             sg.Input(key="custo_min",
                      default_text="1.00",
                      size=5,
                      tooltip="Custo mínimo por porção"),
             sg.Text("até"),
             sg.Input(key="custo_max",
                      default_text="5.00",
                      size=5,
                      tooltip="Custo máximo por porção"),
             ],
            # Calorias
            [sg.Radio("Por valor calórico (kcal) da porção: de",
                      "tipo_filtro",
                      key="filtro_calorias",
                      tooltip="Filtrar receitas por valor calórico"),
             sg.Input(key="calorias_min",
                      size=5,
                      default_text="250",
                      tooltip="Valor calórico mínimo por porção"),
             sg.Text("até"),
             sg.Input(key="calorias_max",
                      size=5,
                      default_text="500",
                      tooltip="Valor calórico máximo por porção"),
             ],
            # Estoque
            [sg.Radio("Por estoque suficiente para",
                      "tipo_filtro",
                      key="filtro_estoque",
                      tooltip="Filtrar receitas por estoque"),
             sg.Input(key="num_porcoes",
                      default_text="20",
                      size=5,
                      tooltip="Número de porções a produzir"),
             sg.Text("porções"),
             ],
            [sg.Push(), sg.Button("Limpar Filtros"), sg.Button("Filtrar Receitas")]
        ]

        layout = [
            [sg.Text(
                "Escolha um tipo de filtro para selecionar receitas e insira os valores nos campos:")],
            [sg.Frame("Suas receitas", receitas, expand_x=True)],
            [sg.Frame("Filtros", filtros, expand_x=True)],
            [sg.Push(), sg.Button("Voltar")]
        ]
        return layout

    def abrir_tela(self, dados_receitas: list = []):
        """Inicializa a tela com o layout definido e os campos preenchidos com os dados passados."""
        layout = self.definir_layout(dados_receitas)
        self.__window = sg.Window(
            "Filtrar Receitas", layout, size=(720, 570), resizable=True)
        botao, valores = self.__window.read()

        linha = valores["lista_receitas"]
        if linha:
            valores["codigo"] = self.__window.find_element(
                "lista_receitas").get()[linha[0]][0]
        else:
            valores["codigo"] = None

        if botao == "Filtrar Receitas":
            try:
                custo_min = float(valores['custo_min'])
                custo_max = float(valores['custo_max'])
                calorias_min = int(valores['calorias_min'])
                calorias_max = int(valores['calorias_max'])
                num_porcoes = int(valores['num_porcoes'])

                if custo_min <= 0 or custo_max <= 0 or calorias_min < 1 or calorias_max < 1 or num_porcoes < 1:
                    self.mostrar_mensagem(
                        "Valores inseridos devem ser maiores do que zero!", titulo="Erro")
                    self.fechar_tela()

                if custo_min >= custo_max or calorias_min >= calorias_max:
                    self.mostrar_mensagem(
                        "Valores mínimos não podem ser maiores ou iguais aos valores máximos!", titulo="Erro")
                    self.fechar_tela()

                valores['filtro_custo'] = bool(valores['filtro_custo'])
                valores['filtro_calorias'] = bool(valores['filtro_calorias'])
                valores['filtro_estoque'] = bool(valores['filtro_estoque'])
                valores['custo_min'] = custo_min
                valores['custo_max'] = custo_max
                valores['calorias_min'] = calorias_min
                valores['calorias_max'] = calorias_max
                valores['num_porcoes'] = num_porcoes

            except ValueError:
                self.mostrar_mensagem(
                    "Custos devem ser números decimais, Calorias e Número de Porções devem ser números inteiros!", titulo="Erro")
                self.fechar_tela()
                return botao, None

        return botao, valores

        # if botao in ("Voltar", sg.WIN_CLOSED):
        #     return botao, valores

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
