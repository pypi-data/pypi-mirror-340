from kirin import ir, types, lowering
from kirin.decl import info, statement
from kirin.dialects import ilist

from bloqade.qasm2.types import QubitType

from ._dialect import dialect


@statement(dialect=dialect)
class PauliChannel(ir.Statement):

    traits = frozenset({lowering.FromPythonCall()})

    px: float = info.attribute(types.Float)
    py: float = info.attribute(types.Float)
    pz: float = info.attribute(types.Float)
    qargs: ir.SSAValue = info.argument(ilist.IListType[QubitType])


NumQubits = types.TypeVar("NumQubits")


@statement(dialect=dialect)
class CZPauliChannel(ir.Statement):

    traits = frozenset({lowering.FromPythonCall()})

    paired: bool = info.attribute(types.Bool)
    px_ctrl: float = info.attribute(types.Float)
    py_ctrl: float = info.attribute(types.Float)
    pz_ctrl: float = info.attribute(types.Float)
    px_qarg: float = info.attribute(types.Float)
    py_qarg: float = info.attribute(types.Float)
    pz_qarg: float = info.attribute(types.Float)
    ctrls: ir.SSAValue = info.argument(ilist.IListType[QubitType, NumQubits])
    qargs: ir.SSAValue = info.argument(ilist.IListType[QubitType, NumQubits])


@statement(dialect=dialect)
class AtomLossChannel(ir.Statement):

    traits = frozenset({lowering.FromPythonCall()})

    prob: float = info.attribute(types.Float)
    qargs: ir.SSAValue = info.argument(ilist.IListType[QubitType])
