from abc import ABC, abstractmethod
import PySimpleGUI as sg


class Tela(ABC):

    # INICIALIZAÇÃO
    @abstractmethod
    def __init__(self):
        self.__window = None
        self.inicializar_janela()

        # Tema padrão
        sg.theme("DarkGrey9")
        sg.set_options(font=("Tahoma", 14))

    # CAPTURA ENTRADAS DO USUARIO


    # LAYOUT TELA
    @abstractmethod
    def inicializar_janela(self):
        pass

    # NAVEGAÇÃO
    @abstractmethod
    def abrir_tela(self):
        pass

    def fechar_tela(self):
        self.__window.Close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)