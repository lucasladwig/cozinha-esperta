import PySimpleGUI as sg


class TelaCadastroReceita:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None

    def init_components(self, dados_receita: dict):
        identificacao = [
            [sg.Push(),
             sg.Text("Nome:"),
             sg.Input(key="nome",
                      size=50,
                      default_text=f"{dados_receita.get('nome')}",
                      tooltip="Nome comercial do prato"),
             sg.Text("Código:"),
             sg.Input(key="codigo",
                      size=10,
                      default_text=f"{dados_receita.get('codigo')}",
                      tooltip="Código alfanumérico até 10 caracteres")],
            [sg.Push(),
             sg.Text("Descrição:"),
             sg.Input(key="descricao",
                      size=(50, 5),
                      default_text=f"{dados_receita.get('descricao')}",
                      tooltip="Descrição comercial (resumida) do prato")]
        ]

        preparo = [
            [sg.Push(),
             sg.Text("Tempo de preparo (min):"),
             sg.Input(key="tempo_preparo",
                      size=5,
                      default_text=f"{dados_receita.get('tempo_preparo')}",
                      tooltip="Tempo total de preparo do prato"),
             sg.Text("Rendimento em porções:"),
             sg.Input(key="rendimento_porcoes",
                      size=5,
                      default_text=f"{dados_receita.get('rendimento_porcoes')}",
                      tooltip="Número de porções que esta receita rende"),
             sg.Text("Validade (dias):"),
             sg.Input(key="validade",
                      size=5,
                      default_text=f"{dados_receita.get('validade')}",
                      tooltip="Validade do prato a partir da data de produção")],
            [sg.Push(),
             sg.Text("Modo de preparo:"),
             sg.Input(key="modo_preparo",
                      size=(100, 5),
                      default_text=f"{dados_receita.get('modo_preparo')}",
                      tooltip="Passo a passo do modo de preparo")]
        ]

        itens = [
            [sg.Table(values=dados_receita.get('itens'),
                      headings=["Insumo", "Un.", "Qtd. Bruta", "FC",
                                "Qtd. Limpa", "IC", "Qtd. Pronta", "Calorias", "Custo"],
                      auto_size_columns=True,
                      expand_x=True,
                      expand_y=True,
                      key="tabela_itens_receita",
                      justification="left",
                      select_mode="browse",
                      num_rows=15)],
            [sg.Push(),
             sg.Button("Excluir Item..."),
             sg.Button("Editar Item..."),
             sg.Button("Adicionar Item...")]
        ]

        layout = [
            [sg.Frame("Identificação", identificacao, expand_x=True)],
            [sg.Frame("Preparo e Validade", preparo, expand_x=True)],
            [sg.Frame("Itens da receita", itens, expand_x=True)],
            [sg.Text(f"Custo total: R${dados_receita.get('custo_total'):.2f}")],
            [sg.Text(f"Custo por Porção: R${dados_receita.get('custo_porcao'):.2f}")],
            [sg.Text(f"Calorias por Porção: {dados_receita.get('custo_porcao'):.2f} kcal")],
            [sg.Push(), sg.Button("Cancelar"), sg.Button("Salvar")]
        ]

        self.__window = sg.Window("Insumos", layout, resizable=True)

    def open(self, dados_receita: dict):
        self.init_components(dados_receita)
        botao, valores = self.__window.read()
        linha = valores["tabela_itens_receita"]
        try:
            valores["nome"] = self.__window.find_element("tabela_itens_receita").get()[
                linha[0]][0]
        except:
            valores["nome"] = None
        return botao, valores

    def close(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)
