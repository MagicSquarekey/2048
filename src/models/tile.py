# -*- coding: utf-8 -*-
# @Function: Tile 数据模型 - 方块值、位置、动画状态

from dataclasses import dataclass, field
from typing import Optional, Tuple
import time


@dataclass
class Tile:
    """方块数据模型 / Tile data model"""

    value: int                              # 方块数值（2, 4, 8, ...）
    row: int                                # 行位置（0-3）
    col: int                                # 列位置（0-3）
    prev_row: Optional[int] = None          # 动画：移动前行位置
    prev_col: Optional[int] = None          # 动画：移动前列位置
    merged_from: Optional[Tuple[int, int]] = None  # 合并来源（用于动画）
    is_new: bool = True                     # 是否新生成（用于生成动画）
    animation_start: float = field(default_factory=time.time)

    def get_position(self) -> Tuple[int, int]:
        """获取当前位置 / Get current position"""
        return (self.row, self.col)

    def set_position(self, row: int, col: int, save_prev: bool = True) -> None:
        """设置新位置，可选保存旧位置用于动画 / Set new position, optionally save old for animation"""
        if save_prev:
            self.prev_row = self.row
            self.prev_col = self.col
        self.row = row
        self.col = col

    def reset_animation(self) -> None:
        """重置动画状态 / Reset animation state"""
        self.prev_row = None
        self.prev_col = None
        self.merged_from = None
        self.is_new = False
        self.animation_start = time.time()

    def to_dict(self) -> dict:
        """序列化为字典 / Serialize to dict"""
        return {
            "value": self.value,
            "row": self.row,
            "col": self.col,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tile":
        """从字典反序列化 / Deserialize from dict"""
        tile = cls(
            value=data["value"],
            row=data["row"],
            col=data["col"],
        )
        tile.is_new = False
        return tile

    def __repr__(self) -> str:
        return f"Tile(value={self.value}, pos=({self.row},{self.col}))"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))
