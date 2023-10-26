from abc import ABC, abstractmethod
import PySimpleGUI as sg


class Tela(ABC):
    # TEMA PADRÃO
    sg.theme("DarkGrey9")
    sg.set_options(font=("Tahoma", 14))
    
    # INICIALIZAÇÃO
    @abstractmethod
    def __init__(self):
        self.__window = None
        self.inicializar_tela()

    # LAYOUT TELA
    @abstractmethod
    def definir_layout(self):
        pass

    # NAVEGAÇÃO
    @abstractmethod
    def inicializar_tela(self):
        pass

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, mensagem, titulo=""):
        sg.popup(mensagem, title=titulo)