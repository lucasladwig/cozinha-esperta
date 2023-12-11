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
    def init_components(self, custos_atuais: CustosFixos) -> dict:
        """"Gera o layout da janela do gerenciador de custos fixos."""

        # Campos de inserção
        agua = [sg.Push(),
                sg.Text("Água:"),
                sg.Input(key="agua",
                         size=16,
                         default_text=f"{custos_atuais.agua:.2f}",
                         tooltip="Valor da conta de água.")]
        aluguel = [sg.Push(),
                   sg.Text("Aluguel:"),
                   sg.Input(key="aluguel",
                            size=16,
                            default_text=f"{custos_atuais.aluguel:.2f}",
                            tooltip="Valor do aluguel de espaço de cozinha, caso haja.")]
        eletricidade = [sg.Push(),
                        sg.Text("Eletricidade:"),
                        sg.Input(key="eletricidade",
                                 size=16,
                                 default_text=f"{custos_atuais.eletricidade:.2f}",
                                 tooltip="Valor da conta de eletricidade.")]
        gas = [sg.Push(),
               sg.Text("Gás:"),
               sg.Input(key="gas",
                        size=16,
                        default_text=f"{custos_atuais.gas:.2f}",
                        tooltip="Custo com gás de cozinha.")]
        manutencao = [sg.Push(),
                      sg.Text("Manutenção:"),
                      sg.Input(key="manutencao",
                               size=16,
                               default_text=f"{custos_atuais.manutencao:.2f}",
                               tooltip="Custo com manutenção de equipamentos.")]
        outros = [sg.Push(),
                  sg.Text("Outros:"),
                  sg.Input(key="outros",
                           size=16,
                           default_text=f"{custos_atuais.outros:.2f}",
                           tooltip="Custo com produtos de limpeza, embalagens, etc...")]

        frame_custos = [
            [sg.Column([agua, aluguel, eletricidade]),
             sg.Column([gas, manutencao, outros])],
            [sg.Text(
                f"Custo fixo total: R${custos_atuais.custo_fixo_total:.2f}")],
        ]

        layout = [
            [sg.Text("Insira uma estimativa do custo mensal (R$) com os itens abaixo:")],
            [sg.Frame("Custos Fixos:", frame_custos)],
            [sg.Text("Produção mensal estimada (em número porções):"),
             sg.Input(key="producao_mensal",
                      size=14,
                      default_text=f"{custos_atuais.porcoes_produzidas_mes}",
                      tooltip="A soma mensal de todas as porções produzidas de todos os pratos."),
             # sg.Button("Pegar do Último Mês", disabled=True)
             ],
            [sg.Text(
                f"Contribuição dos custos fixos em cada porção: R${custos_atuais.custo_fixo_por_porcao:.2f}")],
            [sg.Push(), sg.Button("Sair"), sg.Button("Atualizar e Salvar")]
        ]

        self.__window = sg.Window("Custos Fixos", layout, resizable=True)

    def open(self, custos: CustosFixos):
        self.init_components(custos)
        botao, valores = self.__window.read()

        agua_novo = float(valores["agua"])
        aluguel_novo = float(valores["aluguel"])
        eletricidade_novo = float(valores["eletricidade"])
        gas_novo = float(valores["gas"])
        manutencao_novo = float(valores["manutencao"])
        outros_novo = float(valores["outros"])
        producao_mensal_novo = int(valores["producao_mensal"])

        lista_custos_novos = [
            agua_novo, aluguel_novo, eletricidade_novo, gas_novo, manutencao_novo, outros_novo]

        # Valida valores inseridos
        if (all([custo <= 0 for custo in lista_custos_novos])
                or producao_mensal_novo < 1):
            raise ValueError

        novos_valores = {
            "agua": agua_novo,
            "aluguel": aluguel_novo,
            "eletricidade": eletricidade_novo,
            "gas": gas_novo,
            "manutencao": manutencao_novo,
            "outros": outros_novo,
            "producao_mensal": producao_mensal_novo
        }

        return botao, novos_valores

    def close(self):
        self.__window.close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)

    # def atualizar_valores_tela(self, custos: CustosFixos):
    #     soma = sum(custos.values())
    #     self.__window['custo_total'].update(soma)
