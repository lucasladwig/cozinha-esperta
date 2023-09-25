from abc import ABC, abstractmethod
from limite.tela import Tela

class Controlador(ABC):
    """Classe 'pai' de todos os controladores. Garante que os métodos comuns a todos os controladores tenham a mesma assinatura e obrigam sua implementação."""

    @abstractmethod
    def __init__(self, tela: Tela, controlador_sistema: 'Controlador') -> None:
        self.__tela = tela
        self.__controlador_sistema = controlador_sistema

    @property
    def tela(self):
        return self.__tela
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    @abstractmethod
    def abrir_tela(self):
        pass

    @abstractmethod
    def voltar(self):
        pass