import re
from copy import copy
from typing import Optional, Final, Self

from jcx.m.number import real_2d, Real1_2D, Real
from pydantic import BaseModel

from jvi.geo import is_normalized
from jvi.geo.point2d import Points, Point


class Size(BaseModel):
    """二维尺寸"""

    width: float = 0
    height: float = 0

    @classmethod
    def new(cls, width: float, height: float) -> Self:
        """长方形-构造函数"""
        return cls(width=width, height=height)

    @classmethod
    def zero(cls) -> Self:
        """长方形-构造函数"""
        return cls()

    def size(self) -> Self:
        """实现ISize2D"""
        return self

    def __bool__(self) -> bool:
        """判定是否存在非零属性"""
        return self != Size()

    def brief(self) -> str:
        """获取简要描述"""
        return "{}x{}".format(self.width, self.height)

    def area(self) -> Real:
        """获取面积"""
        return self.width * self.height

    def empty(self) -> bool:
        """判定面积为零"""
        return self.area() == 0

    def positive(self) -> bool:
        """判定长宽为正"""
        return self.width > 0 and self.height > 0

    def center(self) -> Point:
        """获取中心坐标"""
        return Point(x=self.width / 2, y=self.height / 2)

    def aspect_ratio(self) -> float:
        """获取宽高比"""
        return self.width / self.height

    def contains(self, other: Self) -> bool:
        """是否包含目标尺寸"""
        return self.width >= other.width and self.height >= other.height

    def clone(self) -> Self:
        """克隆对象"""
        return copy(self)

    def set(self, other: Self) -> None:
        """设置为目标对象值"""
        self.width = other.width
        self.height = other.height

    def scale_me(self, n: Real1_2D) -> None:
        """缩放指定的倍数"""
        x, y = real_2d(n)
        self.width *= x
        self.height *= y

    def scale(self, n: Real1_2D) -> Self:
        """缩放指定的倍数"""
        s = self.clone()
        s.scale_me(n)
        return s

    def to_tuple(self) -> tuple[float, float]:
        """获取tuple"""
        return self.width, self.height

    def to_tuple_int(self) -> tuple[int, int]:
        """转换为tuple"""
        return int(self.width), int(self.height)

    def to_shape(self) -> tuple[int, int]:
        """转换为 2D Shape"""
        return int(self.height), int(self.width)

    def to_shape3d_i(self, channel: int) -> tuple[int, int, int]:
        """转换为 3D Shape交错格式"""
        return int(self.height), int(self.width), channel

    def to_shape3d_p(self, channel: int) -> tuple[int, int, int]:
        """转换为 3D Shape平坦格式"""
        return channel, int(self.height), int(self.width)

    def to_point(self) -> Point:
        """转换为Point"""
        return Point(x=self.width, y=self.height)

    def normalize_me(self, size: Self) -> None:
        """绝对坐标归一化"""
        self.width /= size.width
        self.height /= size.height

    def normalize(self, size: Self) -> Self:
        """获取绝对坐标归一化"""
        p = copy(self)
        p.normalize_me(size)
        return p

    def absolutize_me(self, size: Self) -> None:
        """归一化坐标绝对化"""
        self.width *= size.width
        self.height *= size.height
        self.round_me()  # 存在非整数可能

    def absolutize(self, size: Self) -> Self:
        """获取归一化坐标绝对化"""
        p = copy(self)
        p.absolutize_me(size)
        return p

    def round_me(self) -> None:
        """近似成整数"""
        self.width = round(self.width)
        self.height = round(self.height)

    def round(self) -> Self:
        """近似成整数"""
        s = copy(self)
        s.round_me()
        return s

    def is_normalized(self) -> bool:
        """判断坐标是否被归一化"""
        return is_normalized(self.width) and is_normalized(self.height)

    def __mul__(self, s: Self) -> "Size":
        """尺寸相乘"""
        return Size(width=self.width * s.width, height=self.height * s.height)

    def __truediv__(self, s: Self) -> "Size":
        """尺寸相除"""
        return Size(width=self.width / s.width, height=self.height / s.height)

    def __or__(self, s: Self) -> "Size":
        """尺寸并集"""
        return Size(width=max(self.width, s.width), height=max(self.height, s.height))

    def __and__(self, s: Self) -> "Size":
        """尺寸并集"""
        return Size(width=min(self.width, s.width), height=min(self.height, s.height))

    def scale_in(self, box_size: Self) -> "Size":
        """保证宽高比缩放到指定尺寸以内"""
        rx = box_size.width / self.width
        ry = box_size.height / self.height
        r = min(rx, ry)

        w = self.width * r
        h = self.height * r
        return Size(width=w, height=h)


def absolutize_points(points: Points, size: Size) -> Points:
    """点集归一化坐标绝对化"""
    arr = [p.absolutize(size) for p in points]
    return arr


# 参考：https://zh.wikipedia.org/wiki/%E6%98%BE%E7%A4%BA%E5%88%86%E8%BE%A8%E7%8E%87%E5%88%97%E8%A1%A8

SIZE_8K: Final = Size(width=8192, height=4320)
SIZE_8K_UHD: Final = Size(width=7680, height=4320)
SIZE_DCI_4K: Final = Size(width=4096, height=2160)
SIZE_4K_UHD: Final = Size(width=3840, height=2160)
SIZE_3K: Final = Size(width=2880, height=1620)
SIZE_2K: Final = Size(width=2048, height=1080)
SIZE_FHD: Final = Size(width=1920, height=1080)
SIZE_qHD: Final = Size(width=960, height=540)
SIZE_HD_PLUS: Final = Size(width=1600, height=900)
SIZE_HD: Final = Size(width=1280, height=720)
SIZE_nHD: Final = Size(width=640, height=360)
SIZE_VGA: Final = Size(width=640, height=480)
SIZE_QVGA: Final = Size(width=320, height=240)
SIZE_PAL: Final = Size(width=768, height=576)
SIZE_IM: Final = Size(width=224, height=224)

SIZE_640: Final = Size(width=640, height=640)
"""深度学习检测器常规尺寸"""
SIZE_720: Final = Size(width=720, height=720)
"""深度学习检测器常规尺寸"""
SIZE_1280: Final = Size(width=1280, height=1280)
"""深度学习检测器常规尺寸"""

resolutions: Final = {
    "8K": SIZE_8K,
    "8K_UHD": SIZE_8K_UHD,
    "DCI_4K": SIZE_DCI_4K,
    "4K_UHD": SIZE_4K_UHD,
    "3K": SIZE_3K,
    "2K": SIZE_2K,
    "FHD": SIZE_FHD,
    "qHD": SIZE_qHD,
    "HD+": SIZE_HD_PLUS,
    "HD": SIZE_HD,
    "nHD": SIZE_nHD,
    "VGA": SIZE_VGA,
    "QVGA": SIZE_QVGA,
    "PAL": SIZE_PAL,
    "IM": SIZE_IM,
}


def size_parse(s: str) -> Optional[Size]:
    """解析字符串获取尺寸"""

    size = resolutions.get(s)
    if size:
        return size

    p = re.compile(r"(\d+)x(\d+)")
    m = p.match(s.lower())
    if m:
        w = int(m.groups()[0])
        h = int(m.groups()[1])
        size = Size(width=w, height=h)
    else:
        size = None
    return size
