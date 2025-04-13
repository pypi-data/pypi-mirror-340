from typing import Self

from arrow import Arrow
from parse import parse  # type: ignore
from pydantic.dataclasses import dataclass
from rustshed import Option, Some, Null


# @total_ordering
@dataclass(frozen=True, order=True)
class ClockTime:
    """时钟时间（时分秒）"""

    hour: int = 0
    """小时"""
    minute: int = 0
    """分钟"""
    second: int = 0
    """秒"""

    class Config:
        allow_mutation = False

    @classmethod
    def new(cls, hour: int, minute: int, second: int) -> Self:
        """构造"""
        return ClockTime(hour=hour, minute=minute, second=second)

    @classmethod
    def from_secs(cls, secs: int) -> Self:
        """构造"""
        minute, second = divmod(secs, 60)
        hour, minute = divmod(minute, 60)
        return ClockTime(hour=hour, minute=minute, second=second)

    @staticmethod
    def from_time(t: Arrow) -> "ClockTime":
        """datetime转ClockTime"""
        return ClockTime(hour=t.hour, minute=t.minute, second=t.second)

    @staticmethod
    def parse(s: str) -> Option["ClockTime"]:
        """从字符串解析时间"""
        arr = parse("{:d}:{:d}:{:d}", s)
        if arr:
            return Some(ClockTime(hour=arr[0], minute=arr[1], second=arr[2]))
        return Null

    def __str__(self) -> str:
        return "%02d:%02d:%02d" % (self.hour, self.minute, self.second)

    def to_time(self) -> Arrow:
        """ClockTime转datetime"""
        t = Arrow.now()
        # now.date()
        return t.replace(
            hour=self.hour, minute=self.minute, second=self.second, microsecond=0
        )


type ClockTimes = list[ClockTime]  # 时钟时间列表


def to_clock_time(time: ClockTime | str | Arrow) -> Option[ClockTime]:
    """转化成ClockTime"""
    if isinstance(time, ClockTime):
        return Some(time)
    if isinstance(time, str):
        return ClockTime.parse(time)
    elif isinstance(time, Arrow):
        return Some(ClockTime.from_time(time))

    return Null
