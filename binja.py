from binaryninja.enums import SymbolType, SymbolBinding
from binaryninja.types import Symbol
from binaryninja.binaryview import BinaryViewType

from .util import get_symbol_name
from .base import Dependency, register_dependency_type

EXPORTABLE_TYPES = {SymbolType.FunctionSymbol, SymbolType.DataSymbol}


@register_dependency_type
class BinaryViewDependency(Dependency):
    @classmethod
    def can_parse(cls, file):
        # Hard to predict, so let's assume we can try for everything
        return True

    def __init__(self, file):
        self.bv = BinaryViewType.get_view_of_file(file, update_analysis=False)

    def is_valid(self):
        return self.bv is not None and self.bv.has_symbols

    def get_exports(self):
        return [
            Symbol(s.type, s.address, s.short_name, full_name=get_symbol_name(self.bv, s), raw_name=s.raw_name, binding=s.binding, namespace=s.namespace, ordinal=s.ordinal)
            for s in self.bv.get_symbols() if s.type in EXPORTABLE_TYPES and s.binding == SymbolBinding.GlobalBinding
        ]