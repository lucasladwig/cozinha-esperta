import PySimpleGUI as sg


class TelaCadastroItemDeReceita:
    """Interface de usuário para gerenciar as receitas."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self):
        self.__window = None

    def definir_layout(self, lista_insumos: list, dados_item: dict):
        """Cria o layout da tela."""
        # Verifica o tipo de quantidade (bruta ou limpa)
        if dados_item["calcula_por_qtd_bruta"]:
            qtd_item = dados_item.get("qtd_bruta")
            eh_bruta = True
            eh_limpa = False
        else:
            qtd_item = dados_item.get("qtd_limpa")
            eh_bruta = False
            eh_limpa = True

        layout = [
            [sg.Text(f"Insumo:"), sg.Combo(lista_insumos, key="nome_insumo" ,default_value=dados_item['nome_insumo'])],
            [sg.Text(f"Quantidade (na unidade do insumo):", key="unidade"),
             sg.Input(key="quantidade",
                      size=5,
                      default_text=f"{qtd_item}",
                      tooltip="Quantidade do item (na unidade do insumo)"),
             sg.Radio("Bruta",
                      "tipo_qtd",
                      key="bruta",
                      default=eh_bruta,
                      size=(10, 1),
                      tooltip="Calcular com base na quantidade bruta"),
             sg.Radio("Limpa",
                      "tipo_qtd",
                      key="limpa",
                      default=eh_limpa,
                      size=(10, 1),
                      tooltip="Calcular com base na quantidade limpa")],
            [sg.Text("Fator de Correção (FC):"),
             sg.Input(key="fator_correcao",
                      size=5,
                      default_text=f"{dados_item.get('fator_correcao')}",
                      tooltip="Fator de correção do item para este preparo")],
            [sg.Text("Índice de Cocção (IC):"),
             sg.Input(key="indice_coccao",
                      size=5,
                      default_text=f"{dados_item.get('indice_coccao')}",
                      tooltip="Índice de cocção do item para este preparo")],
            [sg.Push(), sg.Cancel("Cancelar"), sg.Submit("Salvar")]
        ]
        return layout

    def abrir_tela(self, lista_insumos: dict, dados_item: dict):
        """Inicializa a tela com o layout definido e os campos preenchidos com os dados passados."""
        layout = self.definir_layout(lista_insumos, dados_item)
        self.__window = sg.Window(
            "Inserir/editar item de receita", layout, resizable=True)
        evento, valores = self.__window.read()

        nome_insumo = valores['nome_insumo']
        calcula_por_qtd_bruta = bool(valores['bruta'])

        try:
            quantidade = float(valores['quantidade'])
            fator_correcao = float(valores['fator_correcao'])
            indice_coccao = float(valores['indice_coccao'])

        except ValueError:
            self.mostrar_mensagem(
                "Quantidade, fator de correção e índice de cocção devem ser números decimais!", titulo="Erro")
            self.fechar_tela()
            return None

        if quantidade <= 0 or fator_correcao <= 0 or indice_coccao <= 0:
            self.mostrar_mensagem(
                "Quantidade, fator de correção e índice de cocção devem ser maiores que 0!", titulo="Erro")
            self.fechar_tela()
            return None
        
        elif nome_insumo == "" and evento == "Salvar":
            self.mostrar_mensagem(
                "Insumo não pode ser vazio!", titulo="Erro")
            self.fechar_tela()
            return None

        valores_item = {
            'nome_insumo': nome_insumo,
            'calcula_por_qtd_bruta': calcula_por_qtd_bruta,
            'quantidade': quantidade,
            'fator_correcao': fator_correcao,
            'indice_coccao': indice_coccao,
        }

        if evento == "Salvar":
            return valores_item
        elif evento == "Cancelar":
            return None

    def fechar_tela(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)
