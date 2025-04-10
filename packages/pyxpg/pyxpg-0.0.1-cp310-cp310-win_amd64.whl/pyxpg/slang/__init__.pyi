from collections.abc import Sequence
import enum


class Array(Type):
    @property
    def type(self) -> Type: ...

    @property
    def count(self) -> int: ...

    def __getstate__(self) -> tuple[Type, int]: ...

    def __setstate__(self, arg: tuple[Type, int], /) -> None: ...

class CompilationError(Exception):
    pass

class Field(Type):
    @property
    def name(self) -> str: ...

    @property
    def type(self) -> Type: ...

    @property
    def offset(self) -> int: ...

    def __getstate__(self) -> tuple[str, Type, int]: ...

    def __setstate__(self, arg: tuple[str, Type, int], /) -> None: ...

class Matrix(Type):
    @property
    def base(self) -> ScalarKind: ...

    @property
    def rows(self) -> int: ...

    @property
    def columns(self) -> int: ...

    def __getstate__(self) -> tuple[ScalarKind, int, int]: ...

    def __setstate__(self, arg: tuple[ScalarKind, int, int], /) -> None: ...

class Reflection:
    @property
    def resources(self) -> list[Resource]: ...

    def __getstate__(self) -> list[Resource]: ...

    def __setstate__(self, arg: Sequence[Resource], /) -> None: ...

class Resource:
    @property
    def name(self) -> str: ...

    @property
    def kind(self) -> ResourceKind: ...

    @property
    def shape(self) -> ResourceShape: ...

    @property
    def access(self) -> ResourceAccess: ...

    @property
    def set(self) -> int: ...

    @property
    def binding(self) -> int: ...

    @property
    def type(self) -> Type: ...

    def __getstate__(self) -> tuple[ResourceKind, ResourceShape, ResourceAccess, str, int, int, Type]: ...

    def __setstate__(self, arg: tuple[ResourceKind, ResourceShape, ResourceAccess, str, int, int, Type], /) -> None: ...

class ResourceAccess(enum.Enum):
    SLANG_RESOURCE_ACCESS_NONE = 0

    SLANG_RESOURCE_ACCESS_READ = 1

    SLANG_RESOURCE_ACCESS_READ_WRITE = 2

    SLANG_RESOURCE_ACCESS_RASTER_ORDERED = 3

    SLANG_RESOURCE_ACCESS_APPEND = 4

    SLANG_RESOURCE_ACCESS_CONSUME = 5

    SLANG_RESOURCE_ACCESS_WRITE = 6

    SLANG_RESOURCE_ACCESS_FEEDBACK = 7

    SLANG_RESOURCE_ACCESS_UNKNOWN = 2147483647

class ResourceKind(enum.Enum):
    CONSTANT_BUFFER = 0

    STRUCTURED_BUFFER = 1

class ResourceShape(enum.Enum):
    NONE = 0

    TEXTURE_1D = 1

    TEXTURE_2D = 2

    TEXTURE_3D = 3

    TEXTURE_CUBE = 4

    TEXTURE_BUFFER = 5

    STRUCTURED_BUFFER = 6

    BYTE_ADDRESS_BUFFER = 7

    RESOURCE_UNKNOWN = 8

    ACCELERATION_STRUCTURE = 9

class Scalar(Type):
    @property
    def base(self) -> ScalarKind: ...

    def __getstate__(self) -> ScalarKind: ...

    def __setstate__(self, arg: ScalarKind, /) -> None: ...

class ScalarKind(enum.Enum):
    None = 0

    Void = 1

    Bool = 2

    Int32 = 3

    UInt32 = 4

    Int64 = 5

    UInt64 = 6

    Float16 = 7

    Float32 = 8

    Float64 = 9

    Int8 = 10

    UInt8 = 11

    Int16 = 12

    UInt16 = 13

class Shader:
    @property
    def code(self) -> bytes: ...

    @property
    def reflection(self) -> Reflection: ...

    @property
    def dependencies(self) -> list: ...

    def __getstate__(self) -> tuple[bytes, Reflection, list]: ...

    def __setstate__(self, arg: tuple[bytes, Reflection, list], /) -> None: ...

class Struct(Type):
    @property
    def fields(self) -> list[Field]: ...

    def __getstate__(self) -> list[Field]: ...

    def __setstate__(self, arg: Sequence[Field], /) -> None: ...

class Type:
    def __getstate__(self) -> object: ...

    def __setstate__(self, arg: object, /) -> None: ...

class Vector(Type):
    @property
    def base(self) -> ScalarKind: ...

    @property
    def count(self) -> int: ...

    def __getstate__(self) -> tuple[ScalarKind, int]: ...

    def __setstate__(self, arg: tuple[ScalarKind, int], /) -> None: ...

def compile(arg0: str, arg1: str, /) -> Shader: ...
