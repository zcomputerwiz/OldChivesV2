<<<<<<< HEAD:chives/types/blockchain_format/sized_bytes.py
from chives.util.byte_types import make_sized_bytes

bytes4 = make_sized_bytes(4)
bytes8 = make_sized_bytes(8)
bytes32 = make_sized_bytes(32)
bytes48 = make_sized_bytes(48)
bytes96 = make_sized_bytes(96)
bytes100 = make_sized_bytes(100)
bytes480 = make_sized_bytes(480)
=======
from chives.util.byte_types import SizedBytes


class bytes4(SizedBytes):
    _size = 4


class bytes8(SizedBytes):
    _size = 8


class bytes32(SizedBytes):
    _size = 32


class bytes48(SizedBytes):
    _size = 48


class bytes96(SizedBytes):
    _size = 96


class bytes100(SizedBytes):
    _size = 100


class bytes480(SizedBytes):
    _size = 480
>>>>>>> upstream/main:chives/types/blockchain_format/sized_bytes.py
