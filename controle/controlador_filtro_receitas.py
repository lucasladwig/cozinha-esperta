from limite.tela_filtro_receitas import TelaFiltroReceitas
from entidade.receita import Receita
from entidade.item_de_receita import ItemDeReceita
from entidade.insumo import Insumo

# from controle.controlador_sistema import ControladorSistema


class ControladorFiltroReceitas:
    """Controla os filtros de receita"""

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_filtro_receitas = TelaFiltroReceitas()

    # TELAS

    def abrir_tela(self) -> None:
        """Abre a tela de filtro de receitas"""

        lista_receitas = self.__controlador_sistema.controlador_receitas.listar_dados_todas_receitas()

        while True:
            acao_filtro, valores_filtro = self.__tela_filtro_receitas.abrir_tela(
                lista_receitas)
            self.__tela_filtro_receitas.fechar_tela()

            if acao_filtro == "Filtrar Receitas":
                if valores_filtro is None:
                    continue
                
                if valores_filtro['filtro_custo']:
                    receitas_filtradas = self.filtrar_por_custo(
                        valores_filtro['custo_min'], valores_filtro['custo_max'])
                    
                elif valores_filtro['filtro_calorias']:
                    receitas_filtradas = self.filtrar_por_calorias(
                        valores_filtro['calorias_min'], valores_filtro['calorias_max'])
                    
                elif valores_filtro['filtro_estoque']:
                    receitas_filtradas = self.filtrar_por_estoque(
                        valores_filtro['num_porcoes'])

                lista_receitas = self.__listar_dados_receitas(
                    receitas_filtradas)
            
            elif acao_filtro == "Limpar Filtros":
                lista_receitas = self.__controlador_sistema.controlador_receitas.listar_dados_todas_receitas()

            elif acao_filtro == "Ver Receita Selecionada...":
                if valores_filtro["codigo"] is None:
                    self.__tela_filtro_receitas.mostrar_mensagem(
                        "Nenhuma receita selecionada!", titulo="Erro")
                else:
                    receita_atual = self.__controlador_sistema.controlador_receitas.buscar_receita_por_codigo(
                        valores_filtro["codigo"])
                    self.__controlador_sistema.controlador_receitas.abrir_tela_receita(
                        receita_atual)

            elif acao_filtro == "Voltar":
                self.__tela_filtro_receitas.fechar_tela()
                break

            self.__tela_filtro_receitas.fechar_tela()

    # FILTROS DE RECEITA

    def filtrar_por_custo(self, custo_min: float, custo_max: float) -> list:
        """Retorna as receitas cujo custo por porção estejam dentro da faixa indicada."""
        receitas = self.__buscar_receitas_cadastradas()
        receitas_por_custo = [
            receita for receita in receitas if custo_min <= receita.custo_porcao <= custo_max]

        return receitas_por_custo

    def filtrar_por_calorias(self, calorias_min: int, calorias_max: int) -> list:
        """Retorna as receitas cujo valor calórico por porção estejam dentro da faixa indicada."""
        receitas = self.__buscar_receitas_cadastradas()
        receitas_por_caloria = [
            receita for receita in receitas if calorias_min <= receita.calorias_porcao <= calorias_max]

        return receitas_por_caloria

    def filtrar_por_estoque(self, num_porcoes: int) -> list:
        """Retorna as receitas que sejam possíveis de fabricar com o estoque atual, no número de porções indicado."""
        receitas = self.__buscar_receitas_cadastradas()
        receitas_por_estoque = []

        # Percorre todas as receitas cadastradas
        for receita in receitas:
            # Pressupõe que todos os insumos da receita tem estoque suficiente
            todos_insumos_em_estoque = True

            # Percorre toddos os itens da receita
            for item in receita.itens:
                # Verifica se não há estoque para a número de porções desejado
                if (item.qtd_bruta / receita.rendimento_porcoes) * num_porcoes > item.insumo.estoque_atual:
                    todos_insumos_em_estoque = False
                    break

            # Caso haja estoque para todos itens, adiciona na lista das receitas filtradas
            if todos_insumos_em_estoque:
                receitas_por_estoque.append(receita)

        return receitas_por_estoque

    # MÉTODOS AUXILIARES
    def __buscar_receitas_cadastradas(self) -> list:
        """Busca todas as receitas cadastradas no controlador de receitas."""
        return self.__controlador_sistema.controlador_receitas.receita_dao.get_all()

    def __listar_dados_receitas(self, lista_receitas: list) -> list:
        """Retorna código, nome e descrição de uma receita para serem exibidos em tela (em formato de tabela)."""
        receitas = []
        for receita in lista_receitas:
            dados_receita = []
            dados_receita.append(receita.codigo)
            dados_receita.append(receita.nome)
            dados_receita.append(receita.descricao)
            receitas.append(dados_receita)
        return receitas
