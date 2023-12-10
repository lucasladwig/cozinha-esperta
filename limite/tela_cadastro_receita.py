import PySimpleGUI as sg


class TelaCadastroReceita:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None

    def definir_layout(self, dados_receita: dict, dados_itens_receita: list):
        """Cria o layout da tela."""
        if dados_receita is None:
            dados_receita = {}

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
            [sg.Table(values=dados_itens_receita,
                      headings=["Insumo",
                                "Un.",
                                "Qtd. Bruta",
                                "FC",
                                "Qtd. Limpa",
                                "IC",
                                "Qtd. Pronta",
                                "Calorias",
                                "Custo"],
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
            [sg.Text(
                f"Custo total: R${dados_receita.get('custo_total', 0.0):.2f}", tooltip="Custo total da receita, não incluindo os custos fixos.")],
            [sg.Text(
                f"Custo por Porção: R${dados_receita.get('custo_porcao', 0.0):.2f}", tooltip="Custo por porção, incluindo os custos fixos.")],
            [sg.Text(
                f"Calorias por Porção: {dados_receita.get('calorias_porcao', 0):.0f} kcal", tooltip="Calorias (kcal) por porção")],
            [sg.Push(), sg.Button("Cancelar"), sg.Button("Salvar")]
        ]
        return layout

    def abrir_tela(self, dados_receita: dict, dados_itens_receita: list):
        """Inicializa a tela com o layout definido e os campos preenchidos com os dados passados."""
        layout = self.definir_layout(dados_receita, dados_itens_receita)
        self.__window = sg.Window(
            "Gerenciador de Receitas", layout, resizable=True)
        evento, valores = self.__window.read()

        linha = valores["tabela_itens_receita"]
        if linha:
            nome_insumo_selecionado = self.__window.find_element(
                "tabela_itens_receita").get()[linha[0]][0]
        else:
            nome_insumo_selecionado = None

        nome = valores['nome'].strip()
        codigo = valores['codigo'].strip()
        descricao = valores['descricao'].strip()
        modo_preparo = valores['modo_preparo'].strip()

        if (nome == "" or codigo == "") and evento == "Salvar":
            self.mostrar_mensagem(
                "Nome e código de receita não podem ser vazios!", titulo="Erro")
            self.fechar_tela()
            return evento, None
        
        if evento == "Cancelar":
            return evento, None

        try: 
            rendimento_porcoes = int(valores['rendimento_porcoes'])
            validade = int(valores['validade'])
            tempo_preparo = int(valores['tempo_preparo'])        
        except ValueError:            
            self.mostrar_mensagem(
                "Rendimento, validade e tempo de preparo devem ser números inteiros!", titulo="Erro")
            self.fechar_tela()
            return evento, None
        
        if rendimento_porcoes < 1 or validade < 0 or tempo_preparo < 1:
            self.mostrar_mensagem(
                "Rendimento e tempo de preparo devem ser números inteiros maiores que 0!", titulo="Erro")
            self.fechar_tela()
            return evento, None

        valores_receita = {
            'nome': nome,
            'codigo': codigo,
            'descricao': descricao,
            'modo_preparo': modo_preparo,
            'rendimento_porcoes': rendimento_porcoes,
            'validade': validade,
            'tempo_preparo': tempo_preparo,
            'nome_insumo_selecionado': nome_insumo_selecionado,
        }

        return evento, valores_receita

    def fechar_tela(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)

    def confirmar_exclusao(self):
        layout = [
            [sg.T('Tem certeza que deseja excluir o item selecionado?\nEssa ação NÃO pode ser desfeita!')],
            [sg.Push(), sg.Button("Não", s=10), sg.Button("Sim", s=10)],
        ]

        escolha, _ = sg.Window("Confirmar exclusão",
                               layout, disable_close=True).read(close=True)
        return escolha
