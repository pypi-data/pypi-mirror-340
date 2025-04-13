from datetime import datetime as datetime2
from typing import Any
from pathlib import Path as lpath

import numpy as np
import pandas as pd
from pandas import Series


class Excel_Meta(type):
    def __truediv__(cls, path):
        return File(path=path)


class Excel(object, metaclass=Excel_Meta):
    ...


class File:
    def __init__(self, path):
        self.path = str(path)
        self.sheets = {}
        lfile = lpath(self.path)
        self.name = lfile.name
        self.out_dir = lfile.parent
    
    def __truediv__(self, sheet_name: str|int):
        assert type(sheet_name) in (str, int)
        if type(sheet_name) is int:
            assert sheet_name > 0
            sheet_name -= 1  # 转化为从 1 开始的索引
        sh = self.sheets.get(sheet_name)
        if sh is None:
            sh = self.sheets[sheet_name] = Sheet(file=self, sheet_name=sheet_name)
        return sh


class Sheet:
    def __init__(self, file: File, sheet_name: str|int):
        self.file = file
        self.sheet_name = sheet_name
        self.df = pd.read_excel(self.file.path, sheet_name=self.sheet_name)
        self.cs = Columns(sheet=self)
        self.列 = self.cs
    
    def __str__(self): return self.df.__str__()
    def __repr__(self): return self.df.__repr__()
    
    def __getattr__(self, name):
        return object.__getattribute__(self, name)
    
    def 另存(self):
        t = datetime2.now().strftime(r" _%m%d _%H%M%S")
        file_name = f"{self.file.name}{t}.xlsx"
        path = f"{self.file.out_dir}/{file_name}"
        self.df.to_excel(path, index=False)
        print(f"已另存到 {file_name}")
    
    save = 另存


oget = object.__getattribute__
oset = object.__setattr__


def get_column_core(obj):
    if isinstance(obj, Column):
        return obj.core
    else:
        return obj


class Column:
    def __init__(self, core: Series):
        self.core = core
    
    def __str__(self): return self.core.__str__()
    def __repr__(self): return self.core.__repr__()

    def __add__(self, other): return self.__class__(self.core + get_column_core(other))  # 加
    def __sub__(self, other): return self.__class__(self.core - get_column_core(other))  # 减
    def __mul__(self, other): return self.__class__(self.core * get_column_core(other))  # 乘
    def __truediv__(self, other): return self.__class__(self.core / get_column_core(other))  # 除
    def __pow__(self, other): return self.__class__(self.core ** get_column_core(other))  # 乘方

    def __gt__(self, other): return self.__class__(self.core > get_column_core(other))  # 大于
    def __ge__(self, other): return self.__class__(self.core >= get_column_core(other))  # 大于等于
    def __lt__(self, other): return self.__class__(self.core < get_column_core(other))  # 小于
    def __le__(self, other): return self.__class__(self.core <= get_column_core(other))  # 小于等于
    def __eq__(self, other): return self.__class__(self.core == get_column_core(other))  # 等于
    def __ne__(self, other): return self.__class__(self.core != get_column_core(other))  # 不等于

    def 应用(self, 函数):
        core = self.core.apply(函数)
        return self.__class__(core)
    
    def 判断(self, 真值, 假值):
        return self.应用(lambda x: 真值 if x else 假值)

    def 求和(self):
        return np.array([self.core.sum()]).tolist()[0]
    
    apply = 应用
    where = 判断
    sum = 求和


class Columns:
    sheet: Sheet

    def __init__(self, sheet: Sheet):
        oset(self, 'sheet', sheet)
    
    def __getattr__(self, column_name: str):
        assert type(column_name) is str
        sheet: Sheet = oget(self, 'sheet')
        return Column(sheet.df[column_name])
    
    def __setattr__(self, column_name: str, value):
        assert type(column_name) is str
        sheet: Sheet = oget(self, 'sheet')
        sheet.df[column_name] = get_column_core(value)
    
    __getitem__ = __getattr__
    __setitem__ = __setattr__
