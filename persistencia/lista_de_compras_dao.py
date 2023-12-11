from persistencia.dao import DAO
from entidade.item_lista_de_compras import ItemDeListaDeCompras


class ListaDeComprasDAO(DAO):
    def __init__(self):
        super().__init__('lista_de_compras.pkl')

    def add(self, item: ItemDeListaDeCompras):
        if isinstance(item, ItemDeListaDeCompras) and isinstance(item.insumo.nome, str):
            super().add(item.insumo.nome, item)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
