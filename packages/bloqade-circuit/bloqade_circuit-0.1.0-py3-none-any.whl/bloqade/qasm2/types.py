from kirin import types

from bloqade.types import Qubit as Qubit, QubitType as QubitType


class Bit:
    """Runtime representation of a bit.

    Note:
        This is the base class of more specific bit types, such as
        a reference to a piece of classical register in some quantum register
        dialects.
    """

    pass


class QReg:
    """Runtime representation of a quantum register."""

    def __getitem__(self, index) -> Qubit:
        raise NotImplementedError("cannot call __getitem__ outside of a kernel")


class CReg:
    """Runtime representation of a classical register."""

    def __getitem__(self, index) -> Bit:
        raise NotImplementedError("cannot call __getitem__ outside of a kernel")


BitType = types.PyClass(Bit)
"""Kirin type for a classical bit."""

QRegType = types.PyClass(QReg)
"""Kirin type for a quantum register."""

CRegType = types.PyClass(CReg)
"""Kirin type for a classical register."""
