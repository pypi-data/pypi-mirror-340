from collections.abc import Callable, Sequence
import enum
from typing import Annotated

from numpy.typing import ArrayLike

from . import imgui as imgui, slang as slang


class Action(enum.Enum):
    NONE = 4294967295

    RELEASE = 0

    PRESS = 1

    REPEAT = 2

class AllocType(enum.Enum):
    HOST = 0

    HOST_WRITE_COMBINING = 1

    DEVICE_MAPPED_WITH_FALLBACK = 2

    DEVICE_MAPPED = 3

    DEVICE = 4

    DEVICE_DEDICATED = 5

class Attachment:
    def __init__(self, format: Format, blend_enable: bool = False, src_color_blend_factor: BlendFactor = BlendFactor.VK_BLEND_FACTOR_ZERO, dst_color_blend_factor: BlendFactor = BlendFactor.VK_BLEND_FACTOR_ZERO, color_blend_op: BlendOp = BlendOp.OP_ADD, src_alpha_blend_factor: BlendFactor = BlendFactor.VK_BLEND_FACTOR_ZERO, dst_alpha_blend_factor: BlendFactor = BlendFactor.VK_BLEND_FACTOR_ZERO, alpha_blend_op: BlendOp = BlendOp.OP_ADD, color_write_mask: int = 15) -> None: ...

class BlendFactor(enum.Enum):
    VK_BLEND_FACTOR_ZERO = 0

    VK_BLEND_FACTOR_ONE = 1

    VK_BLEND_FACTOR_SRC_COLOR = 2

    VK_BLEND_FACTOR_ONE_MINUS_SRC_COLOR = 3

    VK_BLEND_FACTOR_DST_COLOR = 4

    VK_BLEND_FACTOR_ONE_MINUS_DST_COLOR = 5

    VK_BLEND_FACTOR_SRC_ALPHA = 6

    VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA = 7

    VK_BLEND_FACTOR_DST_ALPHA = 8

    VK_BLEND_FACTOR_ONE_MINUS_DST_ALPHA = 9

    VK_BLEND_FACTOR_CONSTANT_COLOR = 10

    VK_BLEND_FACTOR_ONE_MINUS_CONSTANT_COLOR = 11

    VK_BLEND_FACTOR_CONSTANT_ALPHA = 12

    VK_BLEND_FACTOR_ONE_MINUS_CONSTANT_ALPHA = 13

    VK_BLEND_FACTOR_SRC_ALPHA_SATURATE = 14

    VK_BLEND_FACTOR_SRC1_COLOR = 15

    VK_BLEND_FACTOR_ONE_MINUS_SRC1_COLOR = 16

    VK_BLEND_FACTOR_SRC1_ALPHA = 17

    VK_BLEND_FACTOR_ONE_MINUS_SRC1_ALPHA = 18

class BlendOp(enum.Enum):
    OP_ADD = 0

    OP_SUBTRACT = 1

    OP_REVERSE_SUBTRACT = 2

    OP_MIN = 3

    OP_MAX = 4

    OP_ZERO = 1000148000

    OP_SRC = 1000148001

    OP_DST = 1000148002

    OP_SRC_OVER = 1000148003

    OP_DST_OVER = 1000148004

    OP_SRC_IN = 1000148005

    OP_DST_IN = 1000148006

    OP_SRC_OUT = 1000148007

    OP_DST_OUT = 1000148008

    OP_SRC_ATOP = 1000148009

    OP_DST_ATOP = 1000148010

    OP_XOR = 1000148011

    OP_MULTIPLY = 1000148012

    OP_SCREEN = 1000148013

    OP_OVERLAY = 1000148014

    OP_DARKEN = 1000148015

    OP_LIGHTEN = 1000148016

    OP_COLORDODGE = 1000148017

    OP_COLORBURN = 1000148018

    OP_HARDLIGHT = 1000148019

    OP_SOFTLIGHT = 1000148020

    OP_DIFFERENCE = 1000148021

    OP_EXCLUSION = 1000148022

    OP_INVERT = 1000148023

    OP_INVERT_RGB = 1000148024

    OP_LINEARDODGE = 1000148025

    OP_LINEARBURN = 1000148026

    OP_VIVIDLIGHT = 1000148027

    OP_LINEARLIGHT = 1000148028

    OP_PINLIGHT = 1000148029

    OP_HARDMIX = 1000148030

    OP_HSL_HUE = 1000148031

    OP_HSL_SATURATION = 1000148032

    OP_HSL_COLOR = 1000148033

    OP_HSL_LUMINOSITY = 1000148034

    OP_PLUS = 1000148035

    OP_PLUS_CLAMPED = 1000148036

    OP_PLUS_CLAMPED_ALPHA = 1000148037

    OP_PLUS_DARKER = 1000148038

    OP_MINUS = 1000148039

    OP_MINUS_CLAMPED = 1000148040

    OP_CONTRAST = 1000148041

    OP_INVERT_OVG = 1000148042

    OP_RED = 1000148043

    OP_GREEN = 1000148044

    OP_BLUE = 1000148045

class Buffer(GfxObject):
    def __init__(self, ctx: Context, size: int, usage_flags: int, alloc_type: AllocType) -> None: ...

    def destroy(self) -> None: ...

    @staticmethod
    def from_data(arg0: Context, arg1: bytes, arg2: int, arg3: AllocType, /) -> Buffer: ...

    @property
    def view(self) -> Annotated[ArrayLike, dict(dtype='uint8', shape=(None))]: ...

class BufferUsageFlags(enum.IntFlag):
    TRANSFER_SRC = 1

    TRANSFER_DST = 2

    UNIFORM = 16

    STORAGE = 32

    INDEX = 64

    VERTEX = 128

    INDIRECT = 256

    ACCELERATION_STRUCTURE_INPUT = 524288

    ACCELERATION_STRUCTURE_STORAGE = 1048576

class ColorComponentFlags(enum.IntFlag):
    R = 1

    G = 2

    B = 4

    A = 8

class CommandBuffer(GfxObject):
    def __enter__(self) -> CommandBuffer: ...

    def __exit__(self, exc_type: object | None, exc_val: object | None, exc_tb: object | None) -> None: ...

    def begin(self) -> None: ...

    def end(self) -> None: ...

    def use_image(self, image: Image, usage: ImageUsage) -> None: ...

    def begin_rendering(self, viewport: Sequence[int], color_attachments: Sequence[RenderingAttachment], depth: DepthAttachment | None = None) -> None: ...

    def end_rendering(self) -> None: ...

    def rendering(self, viewport: Sequence[int], color_attachments: Sequence[RenderingAttachment], depth: DepthAttachment | None = None) -> RenderingManager: ...

    def bind_pipeline_state(self, pipeline: GraphicsPipeline, descriptor_sets: Sequence[DescriptorSet] = [], push_constants: bytes | None = None, vertex_buffers: Sequence[Buffer] = [], index_buffer: Buffer | None = None, viewport: Sequence[int] = [0.0, 0.0, 0.0, 0.0], scissors: Sequence[int] = [0.0, 0.0, 0.0, 0.0]) -> None: ...

    def draw_indexed(self, num_indices: int, num_instances: int = 1, first_index: int = 0, vertex_offset: int = 0, first_instanc: int = 0) -> None: ...

class CompareOp(enum.Enum):
    NEVER = 0

    LESS = 1

    EQUAL = 2

    LESS_OR_EQUAL = 3

    GREATER = 4

    NOT_EQUAL = 5

    GREATER_OR_EQUAL = 6

    ALWAYS = 7

class Context:
    def __init__(self, version: tuple[int, int] = (1, 1), device_features: DeviceFeatures = DeviceFeatures.SYNCHRONIZATION_2|DYNAMIC_RENDERING|PRESENTATION, preferred_frames_in_flight: int = 2, enable_validation_layer: bool = False, enable_gpu_based_validation: bool = False, enable_synchronization_validation: bool = False) -> None: ...

class Depth:
    def __init__(self, format: Format = Format.UNDEFINED, test: bool = False, write: bool = False, op: CompareOp = CompareOp.LESS) -> None: ...

class DepthAttachment:
    def __init__(self, image: Image, load_op: LoadOp, store_op: StoreOp, clear: float = 0.0) -> None: ...

class DescriptorBindingFlags(enum.IntFlag):
    UPDATE_AFTER_BIND = 1

    UPDATE_UNUSED_WHILE_PENDING = 2

    PARTIALLY_BOUND = 4

    VARIABLE_DESCRIPTOR_COUNT = 8

class DescriptorSet:
    def __init__(self, ctx: Context, entries: Sequence[DescriptorSetEntry], flags: DescriptorBindingFlags = DescriptorBindingFlags.0) -> None: ...

    def write_buffer(self, buffer: Buffer, type: DescriptorType, binding: int, element: int) -> None: ...

class DescriptorSetEntry:
    def __init__(self, count: int, type: DescriptorType) -> None: ...

class DescriptorType(enum.Enum):
    SAMPLER = 0

    COMBINED_IMAGE_SAMPLER = 1

    SAMPLED_IMAGE = 2

    STORAGE_IMAGE = 3

    UNIFORM_TEXEL_BUFFER = 4

    STORAGE_TEXEL_BUFFER = 5

    UNIFORM_BUFFER = 6

    STORAGE_BUFFER = 7

    UNIFORM_BUFFER_DYNAMIC = 8

    STORAGE_BUFFER_DYNAMIC = 9

    INPUT_ATTACHMENT = 10

    INLINE_UNIFORM_BLOCK = 1000138000

    ACCELERATION_STRUCTURE = 1000150000

    SAMPLE_WEIGHT_IMAGE = 1000440000

    BLOCK_MATCH_IMAGE = 1000440001

    MUTABLE = 1000351000

class DeviceFeatures(enum.IntFlag):
    NONE = 0

    PRESENTATION = 1

    DYNAMIC_RENDERING = 2

    SYNCHRONIZATION_2 = 4

    DESCRIPTOR_INDEXING = 8

    SCALAR_BLOCK_LAYOUT = 16

    RAY_QUERY = 32

    RAY_PIPELINE = 64

    EXTERNAL_RESOURCES = 128

class ExternalBuffer(Buffer):
    def __init__(self, ctx: Context, size: int, usage_flags: int, alloc_type: AllocType) -> None: ...

    def destroy(self) -> None: ...

    @property
    def handle(self) -> int: ...

class ExternalSemaphore(Semaphore):
    def __init__(self, ctx: Context) -> None: ...

    def destroy(self) -> None: ...

    @property
    def handle(self) -> int: ...

class Format(enum.Enum):
    UNDEFINED = 0

    R4G4_UNORM_PACK8 = 1

    R4G4B4A4_UNORM_PACK16 = 2

    B4G4R4A4_UNORM_PACK16 = 3

    R5G6B5_UNORM_PACK16 = 4

    B5G6R5_UNORM_PACK16 = 5

    R5G5B5A1_UNORM_PACK16 = 6

    B5G5R5A1_UNORM_PACK16 = 7

    A1R5G5B5_UNORM_PACK16 = 8

    R8_UNORM = 9

    R8_SNORM = 10

    R8_USCALED = 11

    R8_SSCALED = 12

    R8_UINT = 13

    R8_SINT = 14

    R8_SRGB = 15

    R8G8_UNORM = 16

    R8G8_SNORM = 17

    R8G8_USCALED = 18

    R8G8_SSCALED = 19

    R8G8_UINT = 20

    R8G8_SINT = 21

    R8G8_SRGB = 22

    R8G8B8_UNORM = 23

    R8G8B8_SNORM = 24

    R8G8B8_USCALED = 25

    R8G8B8_SSCALED = 26

    R8G8B8_UINT = 27

    R8G8B8_SINT = 28

    R8G8B8_SRGB = 29

    B8G8R8_UNORM = 30

    B8G8R8_SNORM = 31

    B8G8R8_USCALED = 32

    B8G8R8_SSCALED = 33

    B8G8R8_UINT = 34

    B8G8R8_SINT = 35

    B8G8R8_SRGB = 36

    R8G8B8A8_UNORM = 37

    R8G8B8A8_SNORM = 38

    R8G8B8A8_USCALED = 39

    R8G8B8A8_SSCALED = 40

    R8G8B8A8_UINT = 41

    R8G8B8A8_SINT = 42

    R8G8B8A8_SRGB = 43

    B8G8R8A8_UNORM = 44

    B8G8R8A8_SNORM = 45

    B8G8R8A8_USCALED = 46

    B8G8R8A8_SSCALED = 47

    B8G8R8A8_UINT = 48

    B8G8R8A8_SINT = 49

    B8G8R8A8_SRGB = 50

    A8B8G8R8_UNORM_PACK32 = 51

    A8B8G8R8_SNORM_PACK32 = 52

    A8B8G8R8_USCALED_PACK32 = 53

    A8B8G8R8_SSCALED_PACK32 = 54

    A8B8G8R8_UINT_PACK32 = 55

    A8B8G8R8_SINT_PACK32 = 56

    A8B8G8R8_SRGB_PACK32 = 57

    A2R10G10B10_UNORM_PACK32 = 58

    A2R10G10B10_SNORM_PACK32 = 59

    A2R10G10B10_USCALED_PACK32 = 60

    A2R10G10B10_SSCALED_PACK32 = 61

    A2R10G10B10_UINT_PACK32 = 62

    A2R10G10B10_SINT_PACK32 = 63

    A2B10G10R10_UNORM_PACK32 = 64

    A2B10G10R10_SNORM_PACK32 = 65

    A2B10G10R10_USCALED_PACK32 = 66

    A2B10G10R10_SSCALED_PACK32 = 67

    A2B10G10R10_UINT_PACK32 = 68

    A2B10G10R10_SINT_PACK32 = 69

    R16_UNORM = 70

    R16_SNORM = 71

    R16_USCALED = 72

    R16_SSCALED = 73

    R16_UINT = 74

    R16_SINT = 75

    R16_SFLOAT = 76

    R16G16_UNORM = 77

    R16G16_SNORM = 78

    R16G16_USCALED = 79

    R16G16_SSCALED = 80

    R16G16_UINT = 81

    R16G16_SINT = 82

    R16G16_SFLOAT = 83

    R16G16B16_UNORM = 84

    R16G16B16_SNORM = 85

    R16G16B16_USCALED = 86

    R16G16B16_SSCALED = 87

    R16G16B16_UINT = 88

    R16G16B16_SINT = 89

    R16G16B16_SFLOAT = 90

    R16G16B16A16_UNORM = 91

    R16G16B16A16_SNORM = 92

    R16G16B16A16_USCALED = 93

    R16G16B16A16_SSCALED = 94

    R16G16B16A16_UINT = 95

    R16G16B16A16_SINT = 96

    R16G16B16A16_SFLOAT = 97

    R32_UINT = 98

    R32_SINT = 99

    R32_SFLOAT = 100

    R32G32_UINT = 101

    R32G32_SINT = 102

    R32G32_SFLOAT = 103

    R32G32B32_UINT = 104

    R32G32B32_SINT = 105

    R32G32B32_SFLOAT = 106

    R32G32B32A32_UINT = 107

    R32G32B32A32_SINT = 108

    R32G32B32A32_SFLOAT = 109

    R64_UINT = 110

    R64_SINT = 111

    R64_SFLOAT = 112

    R64G64_UINT = 113

    R64G64_SINT = 114

    R64G64_SFLOAT = 115

    R64G64B64_UINT = 116

    R64G64B64_SINT = 117

    R64G64B64_SFLOAT = 118

    R64G64B64A64_UINT = 119

    R64G64B64A64_SINT = 120

    R64G64B64A64_SFLOAT = 121

    B10G11R11_UFLOAT_PACK32 = 122

    E5B9G9R9_UFLOAT_PACK32 = 123

    D16_UNORM = 124

    X8_D24_UNORM_PACK32 = 125

    D32_SFLOAT = 126

    S8_UINT = 127

    D16_UNORM_S8_UINT = 128

    D24_UNORM_S8_UINT = 129

    D32_SFLOAT_S8_UINT = 130

    BC1_RGB_UNORM_BLOCK = 131

    BC1_RGB_SRGB_BLOCK = 132

    BC1_RGBA_UNORM_BLOCK = 133

    BC1_RGBA_SRGB_BLOCK = 134

    BC2_UNORM_BLOCK = 135

    BC2_SRGB_BLOCK = 136

    BC3_UNORM_BLOCK = 137

    BC3_SRGB_BLOCK = 138

    BC4_UNORM_BLOCK = 139

    BC4_SNORM_BLOCK = 140

    BC5_UNORM_BLOCK = 141

    BC5_SNORM_BLOCK = 142

    BC6H_UFLOAT_BLOCK = 143

    BC6H_SFLOAT_BLOCK = 144

    BC7_UNORM_BLOCK = 145

    BC7_SRGB_BLOCK = 146

    ETC2_R8G8B8_UNORM_BLOCK = 147

    ETC2_R8G8B8_SRGB_BLOCK = 148

    ETC2_R8G8B8A1_UNORM_BLOCK = 149

    ETC2_R8G8B8A1_SRGB_BLOCK = 150

    ETC2_R8G8B8A8_UNORM_BLOCK = 151

    ETC2_R8G8B8A8_SRGB_BLOCK = 152

    EAC_R11_UNORM_BLOCK = 153

    EAC_R11_SNORM_BLOCK = 154

    EAC_R11G11_UNORM_BLOCK = 155

    EAC_R11G11_SNORM_BLOCK = 156

    ASTC_4x4_UNORM_BLOCK = 157

    ASTC_4x4_SRGB_BLOCK = 158

    ASTC_5x4_UNORM_BLOCK = 159

    ASTC_5x4_SRGB_BLOCK = 160

    ASTC_5x5_UNORM_BLOCK = 161

    ASTC_5x5_SRGB_BLOCK = 162

    ASTC_6x5_UNORM_BLOCK = 163

    ASTC_6x5_SRGB_BLOCK = 164

    ASTC_6x6_UNORM_BLOCK = 165

    ASTC_6x6_SRGB_BLOCK = 166

    ASTC_8x5_UNORM_BLOCK = 167

    ASTC_8x5_SRGB_BLOCK = 168

    ASTC_8x6_UNORM_BLOCK = 169

    ASTC_8x6_SRGB_BLOCK = 170

    ASTC_8x8_UNORM_BLOCK = 171

    ASTC_8x8_SRGB_BLOCK = 172

    ASTC_10x5_UNORM_BLOCK = 173

    ASTC_10x5_SRGB_BLOCK = 174

    ASTC_10x6_UNORM_BLOCK = 175

    ASTC_10x6_SRGB_BLOCK = 176

    ASTC_10x8_UNORM_BLOCK = 177

    ASTC_10x8_SRGB_BLOCK = 178

    ASTC_10x10_UNORM_BLOCK = 179

    ASTC_10x10_SRGB_BLOCK = 180

    ASTC_12x10_UNORM_BLOCK = 181

    ASTC_12x10_SRGB_BLOCK = 182

    ASTC_12x12_UNORM_BLOCK = 183

    ASTC_12x12_SRGB_BLOCK = 184

    G8B8G8R8_422_UNORM = 1000156000

    B8G8R8G8_422_UNORM = 1000156001

    G8_B8_R8_3PLANE_420_UNORM = 1000156002

    G8_B8R8_2PLANE_420_UNORM = 1000156003

    G8_B8_R8_3PLANE_422_UNORM = 1000156004

    G8_B8R8_2PLANE_422_UNORM = 1000156005

    G8_B8_R8_3PLANE_444_UNORM = 1000156006

    R10X6_UNORM_PACK16 = 1000156007

    R10X6G10X6_UNORM_2PACK16 = 1000156008

    R10X6G10X6B10X6A10X6_UNORM_4PACK16 = 1000156009

    G10X6B10X6G10X6R10X6_422_UNORM_4PACK16 = 1000156010

    B10X6G10X6R10X6G10X6_422_UNORM_4PACK16 = 1000156011

    G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16 = 1000156012

    G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16 = 1000156013

    G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16 = 1000156014

    G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 = 1000156015

    G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16 = 1000156016

    R12X4_UNORM_PACK16 = 1000156017

    R12X4G12X4_UNORM_2PACK16 = 1000156018

    R12X4G12X4B12X4A12X4_UNORM_4PACK16 = 1000156019

    G12X4B12X4G12X4R12X4_422_UNORM_4PACK16 = 1000156020

    B12X4G12X4R12X4G12X4_422_UNORM_4PACK16 = 1000156021

    G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16 = 1000156022

    G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16 = 1000156023

    G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16 = 1000156024

    G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16 = 1000156025

    G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16 = 1000156026

    G16B16G16R16_422_UNORM = 1000156027

    B16G16R16G16_422_UNORM = 1000156028

    G16_B16_R16_3PLANE_420_UNORM = 1000156029

    G16_B16R16_2PLANE_420_UNORM = 1000156030

    G16_B16_R16_3PLANE_422_UNORM = 1000156031

    G16_B16R16_2PLANE_422_UNORM = 1000156032

    G16_B16_R16_3PLANE_444_UNORM = 1000156033

    G8_B8R8_2PLANE_444_UNORM = 1000330000

    G10X6_B10X6R10X6_2PLANE_444_UNORM_3PACK16 = 1000330001

    G12X4_B12X4R12X4_2PLANE_444_UNORM_3PACK16 = 1000330002

    G16_B16R16_2PLANE_444_UNORM = 1000330003

    A4R4G4B4_UNORM_PACK16 = 1000340000

    A4B4G4R4_UNORM_PACK16 = 1000340001

    ASTC_4x4_SFLOAT_BLOCK = 1000066000

    ASTC_5x4_SFLOAT_BLOCK = 1000066001

    ASTC_5x5_SFLOAT_BLOCK = 1000066002

    ASTC_6x5_SFLOAT_BLOCK = 1000066003

    ASTC_6x6_SFLOAT_BLOCK = 1000066004

    ASTC_8x5_SFLOAT_BLOCK = 1000066005

    ASTC_8x6_SFLOAT_BLOCK = 1000066006

    ASTC_8x8_SFLOAT_BLOCK = 1000066007

    ASTC_10x5_SFLOAT_BLOCK = 1000066008

    ASTC_10x6_SFLOAT_BLOCK = 1000066009

    ASTC_10x8_SFLOAT_BLOCK = 1000066010

    ASTC_10x10_SFLOAT_BLOCK = 1000066011

    ASTC_12x10_SFLOAT_BLOCK = 1000066012

    ASTC_12x12_SFLOAT_BLOCK = 1000066013

    PVRTC1_2BPP_UNORM_BLOCK_IMG = 1000054000

    PVRTC1_4BPP_UNORM_BLOCK_IMG = 1000054001

    PVRTC2_2BPP_UNORM_BLOCK_IMG = 1000054002

    PVRTC2_4BPP_UNORM_BLOCK_IMG = 1000054003

    PVRTC1_2BPP_SRGB_BLOCK_IMG = 1000054004

    PVRTC1_4BPP_SRGB_BLOCK_IMG = 1000054005

    PVRTC2_2BPP_SRGB_BLOCK_IMG = 1000054006

    PVRTC2_4BPP_SRGB_BLOCK_IMG = 1000054007

    R16G16_SFIXED5_NV = 1000464000

    A1B5G5R5_UNORM_PACK16_KHR = 1000470000

    A8_UNORM_KHR = 1000470001

    ASTC_4x4_SFLOAT_BLOCK_EXT = 1000066000

    ASTC_5x4_SFLOAT_BLOCK_EXT = 1000066001

    ASTC_5x5_SFLOAT_BLOCK_EXT = 1000066002

    ASTC_6x5_SFLOAT_BLOCK_EXT = 1000066003

    ASTC_6x6_SFLOAT_BLOCK_EXT = 1000066004

    ASTC_8x5_SFLOAT_BLOCK_EXT = 1000066005

    ASTC_8x6_SFLOAT_BLOCK_EXT = 1000066006

    ASTC_8x8_SFLOAT_BLOCK_EXT = 1000066007

    ASTC_10x5_SFLOAT_BLOCK_EXT = 1000066008

    ASTC_10x6_SFLOAT_BLOCK_EXT = 1000066009

    ASTC_10x8_SFLOAT_BLOCK_EXT = 1000066010

    ASTC_10x10_SFLOAT_BLOCK_EXT = 1000066011

    ASTC_12x10_SFLOAT_BLOCK_EXT = 1000066012

    ASTC_12x12_SFLOAT_BLOCK_EXT = 1000066013

    G8B8G8R8_422_UNORM_KHR = 1000156000

    B8G8R8G8_422_UNORM_KHR = 1000156001

    G8_B8_R8_3PLANE_420_UNORM_KHR = 1000156002

    G8_B8R8_2PLANE_420_UNORM_KHR = 1000156003

    G8_B8_R8_3PLANE_422_UNORM_KHR = 1000156004

    G8_B8R8_2PLANE_422_UNORM_KHR = 1000156005

    G8_B8_R8_3PLANE_444_UNORM_KHR = 1000156006

    R10X6_UNORM_PACK16_KHR = 1000156007

    R10X6G10X6_UNORM_2PACK16_KHR = 1000156008

    R10X6G10X6B10X6A10X6_UNORM_4PACK16_KHR = 1000156009

    G10X6B10X6G10X6R10X6_422_UNORM_4PACK16_KHR = 1000156010

    B10X6G10X6R10X6G10X6_422_UNORM_4PACK16_KHR = 1000156011

    G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16_KHR = 1000156012

    G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16_KHR = 1000156013

    G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16_KHR = 1000156014

    G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16_KHR = 1000156015

    G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16_KHR = 1000156016

    R12X4_UNORM_PACK16_KHR = 1000156017

    R12X4G12X4_UNORM_2PACK16_KHR = 1000156018

    R12X4G12X4B12X4A12X4_UNORM_4PACK16_KHR = 1000156019

    G12X4B12X4G12X4R12X4_422_UNORM_4PACK16_KHR = 1000156020

    B12X4G12X4R12X4G12X4_422_UNORM_4PACK16_KHR = 1000156021

    G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16_KHR = 1000156022

    G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16_KHR = 1000156023

    G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16_KHR = 1000156024

    G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16_KHR = 1000156025

    G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16_KHR = 1000156026

    G16B16G16R16_422_UNORM_KHR = 1000156027

    B16G16R16G16_422_UNORM_KHR = 1000156028

    G16_B16_R16_3PLANE_420_UNORM_KHR = 1000156029

    G16_B16R16_2PLANE_420_UNORM_KHR = 1000156030

    G16_B16_R16_3PLANE_422_UNORM_KHR = 1000156031

    G16_B16R16_2PLANE_422_UNORM_KHR = 1000156032

    G16_B16_R16_3PLANE_444_UNORM_KHR = 1000156033

    G8_B8R8_2PLANE_444_UNORM_EXT = 1000330000

    G10X6_B10X6R10X6_2PLANE_444_UNORM_3PACK16_EXT = 1000330001

    G12X4_B12X4R12X4_2PLANE_444_UNORM_3PACK16_EXT = 1000330002

    G16_B16R16_2PLANE_444_UNORM_EXT = 1000330003

    A4R4G4B4_UNORM_PACK16_EXT = 1000340000

    A4B4G4R4_UNORM_PACK16_EXT = 1000340001

    R16G16_S10_5_NV = 1000464000

class Frame:
    @property
    def command_buffer(self) -> CommandBuffer: ...

    @property
    def image(self) -> Image: ...

class GfxObject:
    pass

class GraphicsPipeline:
    def __init__(self, ctx: Context, stages: Sequence[PipelineStage] = [], vertex_bindings: Sequence[VertexBinding] = [], vertex_attributes: Sequence[VertexAttribute] = [], input_assembly: InputAssembly = ..., push_constants_ranges: Sequence[PushConstantsRange] = [], descriptor_sets: Sequence[DescriptorSet] = [], samples: int = 1, attachments: Sequence[Attachment] = [], depth: Depth = ...) -> None: ...

    def destroy(self) -> None: ...

class Gui:
    def __init__(self, window: Window) -> None: ...

    def begin_frame(self) -> None: ...

    def end_frame(self) -> None: ...

    def render(self, frame: CommandBuffer) -> None: ...

    def frame(self) -> GuiFrame: ...

class GuiFrame:
    def __enter__(self) -> None: ...

    def __exit__(self, exc_type: object | None, exc_val: object | None, exc_tb: object | None) -> None: ...

class Image(GfxObject):
    def __init__(self, ctx: Context, width: int, height: int, format: Format, usage_flags: int, alloc_type: AllocType, samples: int = 1) -> None: ...

    def destroy(self) -> None: ...

class ImageUsage(enum.Enum):
    NONE = 0

    IMAGE = 1

    IMAGE_READ_ONLY = 2

    IMAGE_WRITE_ONLY = 3

    COLOR_ATTACHMENT = 4

    COLOR_ATTACHMENT_WRITE_ONLY = 5

    DEPTH_STENCIL_ATTACHMENT = 6

    DEPTH_STENCIL_ATTACHMENT_READ_ONLY = 7

    DEPTH_STENCIL_ATTACHMENT_WRITE_ONLY = 8

    PRESENT = 9

class ImageUsageFlags(enum.IntFlag):
    TRANSFER_SRC = 1

    TRANSFER_DST = 2

    SAMPLED = 4

    STORAGE = 8

    COLOR_ATTACHMENT = 16

    DEPTH_STENCIL_ATTACHMENT = 32

class InputAssembly:
    def __init__(self, primitive_topology: PrimitiveTopology = PrimitiveTopology.TRIANGLE_LIST, primitive_restart_enable: bool = False) -> None: ...

class Key(enum.Enum):
    ESCAPE = 256

    SPACE = 32

    PERIOD = 46

    COMMA = 44

class LoadOp(enum.Enum):
    LOAD = 0

    CLEAR = 1

    DONT_CARE = 2

class Modifiers(enum.IntFlag):
    SHIFT = 1

    CTRL = 2

    ALT = 4

    SUPER = 8

class MouseButton(enum.Enum):
    NONE = 4294967295

    LEFT = 0

    RIGHT = 1

    MIDDLE = 2

class PipelineStage:
    def __init__(self, shader: Shader, stage: Stage, entry: str = 'main') -> None: ...

class PipelineStageFlags(enum.IntFlag):
    TOP_OF_PIPE = 1

    DRAW_INDIRECT = 2

    VERTEX_INPUT = 4

    VERTEX_SHADER = 8

    TESSELLATION_CONTROL_SHADER = 16

    TESSELLATION_EVALUATION_SHADER = 32

    GEOMETRY_SHADER = 64

    FRAGMENT_SHADER = 128

    EARLY_FRAGMENT_TESTS = 256

    LATE_FRAGMENT_TESTS = 512

    COLOR_ATTACHMENT_OUTPUT = 1024

    COMPUTE_SHADER = 2048

    TRANSFER = 4096

    BOTTOM_OF_PIPE = 8192

    HOST = 16384

    ALL_GRAPHICS = 32768

    ALL_COMMANDS = 65536

    TRANSFORM_FEEDBACK = 16777216

    CONDITIONAL_RENDERING = 262144

    ACCELERATION_STRUCTURE_BUILD = 33554432

    RAY_TRACING_SHADER = 2097152

    FRAGMENT_DENSITY_PROCESS = 8388608

    FRAGMENT_SHADING_RATE_ATTACHMENT = 4194304

    TASK_SHADER = 524288

    MESH_SHADER = 1048576

class PrimitiveTopology(enum.Enum):
    POINT_LIST = 0

    LINE_LIST = 1

    LINE_STRIP = 2

    TRIANGLE_LIST = 3

    TRIANGLE_STRIP = 4

    TRIANGLE_FAN = 5

    LINE_LIST_WITH_ADJACENCY = 6

    LINE_STRIP_WITH_ADJACENCY = 7

    TRIANGLE_LIST_WITH_ADJACENCY = 8

    TRIANGLE_STRIP_WITH_ADJACENCY = 9

    PATCH_LIST = 10

class PushConstantsRange:
    def __init__(self, size: int, offset: int = 0, stages: Stage = Stage.1073741824|536870912|268435456|134217728|67108864|33554432|16777216|8388608|4194304|2097152|1048576|524288|262144|131072|65536|32768|16384|CALLABLE|INTERSECTION|MISS|CLOSEST_HIT|ANY_HIT|RAYGEN|MESH_EXT|TASK_EXT|COMPUTE|FRAGMENT|GEOMETRY|TESSELLATION_EVALUATION|TESSELLATION_CONTROL|VERTEX) -> None: ...

class RenderingAttachment:
    def __init__(self, image: Image, load_op: LoadOp, store_op: StoreOp, clear: Sequence[float] = [0.0, 0.0, 0.0, 0.0], resolve_image: Image | None = None, resolve_mode: ResolveMode = ResolveMode.NONE) -> None: ...

class RenderingManager:
    def __enter__(self) -> None: ...

    def __exit__(self, exc_type: object | None, exc_val: object | None, exc_tb: object | None) -> None: ...

class ResolveMode(enum.Enum):
    NONE = 0

    SAMPLE_ZERO = 1

    AVERAGE = 2

    MIN = 4

    MAX = 8

class Semaphore(GfxObject):
    def __init__(self, ctx: Context) -> None: ...

    def destroy(self) -> None: ...

class Shader:
    def __init__(self, ctx: Context, code: bytes) -> None: ...

    def destroy(self) -> None: ...

class Stage(enum.IntFlag):
    VERTEX = 1

    TESSELLATION_CONTROL = 2

    TESSELLATION_EVALUATION = 4

    GEOMETRY = 8

    FRAGMENT = 16

    COMPUTE = 32

    RAYGEN = 256

    ANY_HIT = 512

    CLOSEST_HIT = 1024

    MISS = 2048

    INTERSECTION = 4096

    CALLABLE = 8192

    TASK_EXT = 64

    MESH_EXT = 128

class StoreOp(enum.Enum):
    STORE = 0

    DONT_CARE = 1

    NONE = 1000301000

class SwapchainStatus(enum.Enum):
    READY = 0

    RESIZED = 1

    MINIMIZED = 2

class VertexAttribute:
    def __init__(self, location: int, binding: int, format: Format, offset: int = 0) -> None: ...

class VertexBinding:
    def __init__(self, binding: int, stride: int, input_rate: VertexInputRate = VertexInputRate.VERTEX) -> None: ...

class VertexInputRate(enum.Enum):
    VERTEX = 0

    INSTANCE = 1

class Window:
    def __init__(self, ctx: Context, title: str, width: int, height: int) -> None: ...

    def should_close(self) -> bool: ...

    def set_callbacks(self, draw: Callable[[], None], mouse_move_event: Callable[[tuple[int, int]], None] | None = None, mouse_button_event: Callable[[tuple[int, int], MouseButton, Action, Modifiers], None] | None = None, mouse_scroll_event: Callable[[tuple[int, int], tuple[int, int]], None] | None = None, key_event: Callable[[Key, Action, Modifiers], None] | None = None) -> None: ...

    def reset_callbacks(self) -> None: ...

    def update_swapchain(self) -> SwapchainStatus: ...

    def begin_frame(self) -> Frame: ...

    def end_frame(self, frame: Frame, additional_wait_semaphores: Sequence[tuple[Semaphore, PipelineStageFlags]] = [], additional_signal_semaphores: Sequence[Semaphore] = []) -> None: ...

    def frame(self, additional_wait_semaphores: Sequence[tuple[Semaphore, PipelineStageFlags]] = [], additional_signal_semaphores: Sequence[Semaphore] = []) -> WindowFrame: ...

    @property
    def swapchain_format(self) -> Format: ...

    @property
    def fb_width(self) -> int: ...

    @property
    def fb_height(self) -> int: ...

    @property
    def num_frames(self) -> int: ...

class WindowFrame:
    def __enter__(self) -> Frame: ...

    def __exit__(self, exc_type: object | None, exc_val: object | None, exc_tb: object | None) -> None: ...

def process_events(wait: bool) -> None: ...

def wait_idle(arg: Context, /) -> None: ...
