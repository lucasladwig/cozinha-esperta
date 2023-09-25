from entidade.custos_fixos import CustosFixos
import PySimpleGUI as sg


class TelaCustosFixos:
    """Interface de usuário para manipular os custos fixos."""

    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))

    # INICIALIZAÇÃO
    def __init__(self) -> None:
        self.__window = None

    # PEGAR DADOS
    def init_components(self, custos_atual: CustosFixos) -> dict:
        """"Gera o layout da janela do gerenciador de custos fixos."""

        # Campos de inserção
        agua = [sg.Push(),
                sg.Text("Água:"),
                sg.Input(key="agua",
                         size=16,
                         default_text=f"{custos_atual.agua:.2f}",
                         tooltip="Valor da conta de água.")]
        aluguel = [sg.Push(),
                   sg.Text("Aluguel:"),
                   sg.Input(key="aluguel",
                            size=16,
                            default_text=f"{custos_atual.aluguel:.2f}",
                            tooltip="Valor do aluguel de espaço de cozinha, caso haja.")]
        eletricidade = [sg.Push(),
                        sg.Text("Eletricidade:"),
                        sg.Input(key="eletricidade",
                                 size=16,
                                 default_text=f"{custos_atual.eletricidade:.2f}",
                                 tooltip="Valor da conta de eletricidade.")]
        gas = [sg.Push(),
               sg.Text("Gás:"),
               sg.Input(key="gas",
                        size=16,
                        default_text=f"{custos_atual.gas:.2f}",
                        tooltip="Custo com gás de cozinha.")]
        manutencao = [sg.Push(),
                      sg.Text("Manutenção:"),
                      sg.Input(key="manutencao",
                               size=16,
                               default_text=f"{custos_atual.manutencao:.2f}",
                               tooltip="Custo com manutenção de equipamentos.")]
        outros = [sg.Push(),
                  sg.Text("Outros:"),
                  sg.Input(key="outros",
                           size=16,
                           default_text=f"{custos_atual.outros:.2f}",
                           tooltip="Custo com produtos de limpeza, embalagens, etc...")]

        frame_custos = [
            [sg.Column([agua, aluguel, eletricidade]),
             sg.Column([gas, manutencao, outros])],
            [sg.Push(), sg.Button("Atualizar Custos Fixos")],
            [sg.Text(f"Custo fixo total: R$"), sg.Text(key="custo_total")],
        ]

        layout = [
            [sg.Text("Insira uma estimativa do custo mensal (R$) com os itens abaixo:")],
            [sg.Frame("Custos Fixos:", frame_custos)],
            [sg.Text("Produção mensal total (porções):"),
             sg.Input(key="producao_mensal", size=14, default_text=""),
             sg.Button("Pegar do último mês")],
            [sg.Text("Contribuição do custos fixos por porção:"),
             sg.Text(key="custo_porcao")],
            [sg.Push(), sg.Button("Cancelar"), sg.Button("Salvar")]
        ]
        try:
            self.__window = sg.Window("Custos Fixos", layout, resizable=True)

            botao, valores = self.__window.Read()

            agua_novo = float(valores["agua"])
            aluguel_novo = float(valores["aluguel"])
            eletricidade_novo = float(valores["eletricidade"])
            gas_novo = float(valores["gas"])
            manutencao_novo = float(valores["manutencao"])
            outros_novo = float(valores["outros"])
            producao_mensal_novo = int(valores["producao_mensal"])

            lista_custos_novos = [
                agua_novo, aluguel_novo, eletricidade_novo, gas_novo, manutencao_novo, outros_novo]

            if (all([custo <= 0 for custo in lista_custos_novos])
                    or producao_mensal_novo < 1):
                raise ValueError

            self.__window.close()

            return {
                "agua": agua_novo,
                "aluguel": aluguel_novo,
                "eletricidade": eletricidade_novo,
                "gas": gas_novo,
                "manutencao": manutencao_novo,
                "outros": outros_novo
            }

        except ValueError:
            self.mostrar_mensagem(
                "Por favor, insira valores numéricos para os custos!",
                titulo="Erro ao atualizar custos")

    def inicializar_tela(self, custos_fixos: CustosFixos):
        self.init_components(custos_fixos)
        botao, valores = self.__window.read()

        # Atualizar custo total na tela            
        if botao == "Atualizar Custos Fixos":
            soma = sum(valores.values())
            self.__window['custo_total'].update(soma)


        if botao in ("Salvar", "Calcular"):
            return valores
        elif botao == "Cancelar":
            return None

    # MOSTRAR MENSAGENS

    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)
