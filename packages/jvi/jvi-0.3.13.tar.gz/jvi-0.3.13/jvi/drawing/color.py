import inspect
import sys
from random import randint
from typing import Final, Optional

from pydantic import BaseModel


class Color(BaseModel):
    """RGB颜色"""

    r: int = 0
    g: int = 0
    b: int = 0

    @classmethod
    def try_parse(cls, name: str) -> Optional["Color"]:
        """从颜色名称或者#RGB建立颜色"""
        if name.startswith("#"):
            s = name.replace("#", "0x")
            i = int(s, 16)
            b = i % 256
            i = i // 256
            g = i % 256
            r = i // 256
            return cls.new(r, g, b)
        else:
            name = name.upper().replace(" ", "_")
            return colors.get(name, None)

    @classmethod
    def parse(cls, name: str) -> "Color":
        """从颜色名称或者#RGB建立颜色"""
        c = cls.try_parse(name)
        assert c, f"Invalid color: {name}"
        return c

    @classmethod
    def new(cls, r: int, g: int, b: int) -> "Color":
        """从RGB建立颜色"""
        return Color(r=r, g=g, b=b)

    def rgb(self) -> tuple[int, int, int]:
        """获取RGB"""
        return self.r, self.g, self.b

    def bgr(self) -> tuple[int, int, int]:
        """获取BGR"""
        return self.b, self.g, self.r

    def inverse(self) -> "Color":
        """获取反色"""
        return Color(r=255 - self.r, g=255 - self.g, b=255 - self.b)

    def as_int(self) -> int:
        """颜色转换为单个整数"""
        return self.r << 16 | self.g << 8 | self.b

    def __str__(self) -> str:
        return "#%02X%02X%02X" % (self.r, self.g, self.b)

    def __len__(self) -> int:
        return 3


type Colors = list[Color]
"""颜色组"""

# 颜色定义

PINK: Final = Color.new(255, 192, 203)
"""粉红"""
CRIMSON: Final = Color.new(220, 20, 60)
"""猩红"""
LAVENDER_BLUSH: Final = Color.new(255, 240, 245)
"""淡紫红"""
PALE_VIOLET_RED: Final = Color.new(219, 112, 147)
"""苍白的紫罗兰红色"""
HOT_PINK: Final = Color.new(255, 105, 180)
"""热粉红"""
DEEP_PINK: Final = Color.new(255, 20, 147)
"""深粉红"""
MEDIUM_VIOLET_RED: Final = Color.new(199, 21, 133)
"""适中的紫罗兰红色"""
ORCHID: Final = Color.new(218, 112, 214)
"""兰花紫"""
THISTLE: Final = Color.new(216, 191, 216)
"""蓟"""
PLUM: Final = Color.new(221, 160, 221)
"""李子色"""
VIOLET: Final = Color.new(238, 130, 238)
"""紫罗兰"""
MAGENTA: Final = Color.new(255, 0, 255)
"""洋红"""
FUCHSIA: Final = Color.new(255, 0, 255)
"""紫红色"""
DARK_MAGENTA: Final = Color.new(139, 0, 139)
"""深洋红色"""
PURPLE: Final = Color.new(128, 0, 128)
"""紫色"""
MEDIUM_ORCHID: Final = Color.new(186, 85, 211)
"""适中的兰花紫"""
DARK_VIOLET: Final = Color.new(148, 0, 211)
"""深紫罗兰色"""
DARK_ORCHID: Final = Color.new(153, 50, 204)
"""深兰花紫"""
INDIGO: Final = Color.new(75, 0, 130)
"""靛青"""
BLUE_VIOLET: Final = Color.new(138, 43, 226)
"""紫罗兰的蓝色"""
MEDIUM_PURPLE: Final = Color.new(147, 112, 219)
"""适中的紫色"""
MEDIUM_SLATE_BLUE: Final = Color.new(123, 104, 238)
"""适中的板岩暗蓝灰色"""
SLATE_BLUE: Final = Color.new(106, 90, 205)
"""板岩暗蓝灰色"""
DARK_SLATE_BLUE: Final = Color.new(72, 61, 139)
"""深板岩暗蓝灰色"""
LAVENDER: Final = Color.new(230, 230, 250)
"""薰衣草花的淡紫色"""
GHOST_WHITE: Final = Color.new(248, 248, 255)
"""幽灵的白色"""
BLUE: Final = Color.new(0, 0, 255)
"""蓝"""
MEDIUM_BLUE: Final = Color.new(0, 0, 205)
"""适中的蓝色"""
MIDNIGHT_BLUE: Final = Color.new(25, 25, 112)
"""午夜的蓝色"""
DARK_BLUE: Final = Color.new(0, 0, 139)
"""深蓝色"""
NAVY: Final = Color.new(0, 0, 128)
"""海军蓝"""
ROYAL_BLUE: Final = Color.new(65, 105, 255)
"""皇家蓝"""
CORNFLOWER_BLUE: Final = Color.new(100, 149, 237)
"""矢车菊的蓝色"""
LIGHT_STEEL_BLUE: Final = Color.new(176, 196, 222)
"""淡钢蓝"""
LIGHT_SLATE_GRAY: Final = Color.new(119, 136, 153)
"""浅石板灰"""
SLATE_GRAY: Final = Color.new(112, 128, 144)
"""石板灰"""
DODGER_BLUE: Final = Color.new(30, 144, 255)
"""道奇蓝"""
ALICE_BLUE: Final = Color.new(240, 248, 255)
"""爱丽丝蓝"""
STEEL_BLUE: Final = Color.new(70, 130, 180)
"""钢蓝"""
LIGHT_SKY_BLUE: Final = Color.new(135, 206, 250)
"""淡天蓝色"""
SKY_BLUE: Final = Color.new(135, 206, 235)
"""天蓝色"""
DEEP_SKY_BLUE: Final = Color.new(0, 191, 255)
"""深天蓝"""
LIGHT_BLUE: Final = Color.new(173, 216, 230)
"""淡蓝色"""
POWDER_BLUE: Final = Color.new(176, 224, 230)
"""浅灰蓝"""
CADET_BLUE: Final = Color.new(95, 158, 160)
"""军校蓝"""
AZURE: Final = Color.new(240, 255, 255)
"""蔚蓝色"""
LIGHT_CYAN: Final = Color.new(224, 255, 255)
"""浅青色"""
PALE_TURQUOISE: Final = Color.new(175, 238, 238)
"""苍白的绿宝石"""
CYAN: Final = Color.new(0, 255, 255)
"""青色"""
AQUA: Final = Color.new(0, 255, 255)
"""水绿色"""
DARK_TURQUOISE: Final = Color.new(0, 206, 209)
"""深绿宝石"""
DARK_SLATE_GRAY: Final = Color.new(47, 79, 79)
"""深石板灰"""
DARK_CYAN: Final = Color.new(0, 139, 139)
"""深青色"""
TEAL: Final = Color.new(0, 128, 128)
"""水鸭色"""
MEDIUM_TURQUOISE: Final = Color.new(72, 209, 204)
"""适中的绿宝石"""
LIGHT_SEA_GREEN: Final = Color.new(32, 178, 170)
"""浅海洋绿"""
TURQUOISE: Final = Color.new(64, 224, 208)
"""绿宝石"""
AQUAMARINE: Final = Color.new(127, 255, 212)
"""绿玉，碧绿色"""
MEDIUM_AQUAMARINE: Final = Color.new(102, 205, 170)
"""适中的碧绿色"""
MEDIUM_SPRING_GREEN: Final = Color.new(0, 250, 154)
"""适中的春天的绿色"""
MINT_CREAM: Final = Color.new(245, 255, 250)
"""薄荷奶油"""
SPRING_GREEN: Final = Color.new(0, 255, 127)
"""春天的绿色"""
MEDIUM_SEA_GREEN: Final = Color.new(60, 179, 113)
"""适中的海洋绿"""
SEA_GREEN: Final = Color.new(46, 139, 87)
"""海洋绿"""
HONEYDEW: Final = Color.new(240, 255, 240)
"""蜂蜜"""
LIGHT_GREEN: Final = Color.new(144, 238, 144)
"""淡绿色"""
PALE_GREEN: Final = Color.new(152, 251, 152)
"""苍白的绿色"""
DARK_SEA_GREEN: Final = Color.new(143, 188, 143)
"""深海洋绿"""
LIME_GREEN: Final = Color.new(50, 205, 50)
"""酸橙绿"""
LIME: Final = Color.new(0, 255, 0)
"""酸橙色"""
FOREST_GREEN: Final = Color.new(34, 139, 34)
"""森林绿"""
GREEN: Final = Color.new(0, 128, 0)
"""绿"""
DARK_GREEN: Final = Color.new(1, 100, 0)
"""深绿色"""
CHARTREUSE: Final = Color.new(127, 255, 0)
"""查特酒绿，淡黄绿色"""
LAWN_GREEN: Final = Color.new(124, 252, 0)
"""草坪绿"""
GREEN_YELLOW: Final = Color.new(173, 255, 47)
"""绿黄色"""
DARK_OLIVE_GREEN: Final = Color.new(85, 107, 47)
"""深橄榄绿"""
YELLOW_GREEN: Final = Color.new(154, 205, 50)
"""黄绿"""
OLIVE_DRAB: Final = Color.new(107, 142, 35)
"""橄榄土褐色"""
BEIGE: Final = Color.new(245, 245, 220)
"""米色，浅褐色"""
LIGHT_GOLDENROD_YELLOW: Final = Color.new(250, 250, 210)
"""浅秋麒麟黄"""
IVORY: Final = Color.new(255, 255, 240)
"""象牙"""
LIGHT_YELLOW: Final = Color.new(255, 255, 224)
"""浅黄色"""
YELLOW: Final = Color.new(255, 255, 0)
"""黄"""
OLIVE: Final = Color.new(128, 128, 0)
"""橄榄色"""
DARK_KHAKI: Final = Color.new(189, 183, 107)
"""深卡其布"""
LEMON_CHIFFON: Final = Color.new(255, 250, 205)
"""柠檬薄纱"""
PALE_GOLDENROD: Final = Color.new(238, 232, 170)
"""灰秋麒麟"""
KHAKI: Final = Color.new(240, 230, 140)
"""卡其布"""
GOLD: Final = Color.new(255, 215, 0)
"""金色"""
CORNSILK: Final = Color.new(255, 248, 220)
"""玉米色"""
GOLDENROD: Final = Color.new(218, 165, 32)
"""秋麒麟色"""
DARK_GOLDENROD: Final = Color.new(184, 134, 11)
"""深秋麒麟"""
FLORAL_WHITE: Final = Color.new(255, 250, 240)
"""花卉白"""
OLDLACE: Final = Color.new(253, 245, 230)
"""老饰带"""
WHEAT: Final = Color.new(245, 222, 179)
"""小麦色"""
MOCCASIN: Final = Color.new(255, 228, 181)
"""鹿皮鞋"""
ORANGE: Final = Color.new(255, 165, 0)
"""橙色"""
PAPAYA_WHIP: Final = Color.new(255, 239, 213)
"""番木瓜色"""
BLANCHED_ALMOND: Final = Color.new(255, 235, 205)
"""漂白的杏仁"""
NAVAJO_WHITE: Final = Color.new(255, 222, 173)
"""纳瓦霍白"""
ANTIQUE_WHITE: Final = Color.new(250, 235, 215)
"""古典白"""
TAN: Final = Color.new(210, 180, 140)
"""棕褐色，茶色"""
BURLYWOOD: Final = Color.new(222, 184, 135)
"""原木色"""
BISQUE: Final = Color.new(255, 228, 196)
"""浓汤色"""
DARK_ORANGE: Final = Color.new(255, 140, 0)
"""深橙黄"""
LINEN: Final = Color.new(250, 240, 230)
"""亚麻布色"""
PERU: Final = Color.new(205, 133, 63)
"""秘鲁色"""
PEACH_PUFF: Final = Color.new(255, 218, 185)
"""桃色"""
SANDY_BROWN: Final = Color.new(244, 164, 96)
"""沙棕色"""
CHOCOLATE: Final = Color.new(210, 105, 30)
"""巧克力色"""
SADDLE_BROWN: Final = Color.new(139, 69, 19)
"""马鞍棕色"""
SEA_SHELL: Final = Color.new(255, 245, 238)
"""海贝色"""
SIENNA: Final = Color.new(160, 82, 45)
"""赭色"""
LIGHT_SALMON: Final = Color.new(255, 160, 122)
"""浅肉色"""
CORAL: Final = Color.new(255, 127, 80)
"""珊瑚色"""
ORANGE_RED: Final = Color.new(255, 69, 0)
"""橙红色"""
DARK_SALMON: Final = Color.new(233, 150, 122)
"""深肉色"""
TOMATO: Final = Color.new(255, 99, 71)
"""番茄色"""
MISTY_ROSE: Final = Color.new(255, 228, 225)
"""薄雾玫瑰色"""
SALMON: Final = Color.new(250, 128, 114)
"""鲜肉色"""
SNOW: Final = Color.new(255, 250, 250)
"""雪白"""
LIGHT_CORAL: Final = Color.new(240, 128, 128)
"""浅珊瑚色"""
ROSY_BROWN: Final = Color.new(188, 143, 143)
"""玫瑰棕色"""
INDIAN_RED: Final = Color.new(205, 92, 92)
"""印度红"""
RED: Final = Color.new(255, 0, 0)
"""红"""
BROWN: Final = Color.new(165, 42, 42)
"""褐色"""
FIRE_BRICK: Final = Color.new(178, 34, 34)
"""耐火砖色"""
DARK_RED: Final = Color.new(139, 0, 0)
"""深红"""
MAROON: Final = Color.new(128, 0, 0)
"""栗色"""
WHITE: Final = Color.new(255, 255, 255)
"""白"""
WHITE_SMOKE: Final = Color.new(245, 245, 245)
"""白烟"""
GAINSBORO: Final = Color.new(220, 220, 220)
"""淡灰色"""
LIGHT_GREY: Final = Color.new(211, 211, 211)
"""浅灰"""
SILVER: Final = Color.new(192, 192, 192)
"""银白"""
DARK_GRAY: Final = Color.new(169, 169, 169)
"""深灰"""
GRAY: Final = Color.new(128, 128, 128)
"""灰色"""
DIM_GRAY: Final = Color.new(105, 105, 105)
"""暗灰色"""
BLACK: Final = Color.new(0, 0, 0)
"""黑"""
YOLO_GRAY: Final = Color.new(114, 114, 114)  # /opt/ias/env/lib/yolo5/utils/general.py
"""YOLO灰色"""

COLORS7: Final = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]
"""七色"""

W3C16: Final = [
    BLACK,
    GREEN,
    SILVER,
    LIME,
    GRAY,
    OLIVE,
    WHITE,
    YELLOW,
    MAROON,
    NAVY,
    RED,
    BLUE,
    PURPLE,
    TEAL,
    FUCHSIA,
    AQUA,
]
"""W3C16色"""


def find_mod_colors() -> dict[str, Color]:
    """搜索模块内所有预定义颜色"""
    ns = inspect.getmembers(sys.modules[__name__])
    cs = {}
    for k, v in ns:
        if isinstance(v, Color):
            cs[k] = v
    return cs


colors = find_mod_colors()
"""预定义颜色字典"""


def random_color() -> Color:
    """获取随机颜色"""
    return Color.new(randint(0, 256), randint(0, 256), randint(0, 256))
