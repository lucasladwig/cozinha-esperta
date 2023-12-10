# from controle.controlador_sistema import ControladorSistema
from controle.controlador_insumo import ControladorInsumo
from controle.controlador_estoque_insumo import ControladorEstoqueInsumo
from controle.controlador_receita import ControladorReceita
# from controle.controlador_custos_fixos import ControladorCustosFixos


if __name__ == "__main__":
    ControladorReceita().abrir_tela_gerenciador()
    # ControladorInsumo().abre_tela()
    # ControladorEstoqueInsumo().abre_tela()

# if __name__ == "__main__":
#     ControladorEstoqueInsumo().abre_tela()

# if __name__ == "__main__":
#     ControladorCustosFixos().abrir_tela()
