from pathlib import Path
from typing import Type, Self

from jcx.db.ivariant import IVariant
from jcx.sys.fs import StrPath
from jcx.text.txt_json import load_json, save_json, BMT


class JdbVariant(IVariant):
    """数据库变量"""

    @classmethod
    def open(cls, value_type: Type[BMT], folder, name: str) -> Self:
        """打开数据变量"""
        return JdbVariant(value_type, folder, name)

    def __init__(self, value_type: Type[BMT], folder: StrPath, name: str):
        self._type = value_type
        self._path = Path(folder, name + ".json")

    def name(self) -> str:
        """ "获取变量名"""
        return self._path.stem

    def value_type(self) -> Type[BMT]:
        """ "获取变量类型"""
        return self._type

    def exists(self) -> bool:
        """ "判断是否存在"""
        return self._path.exists()

    def get(self) -> BMT:
        """获取变量"""
        return load_json(self._path, self._type).unwrap()

    def set(self, value: BMT) -> None:
        """设置变量"""
        save_json(value, self._path)

    def remove(self) -> None:
        """删除变量"""
        Path.unlink(self._path)
