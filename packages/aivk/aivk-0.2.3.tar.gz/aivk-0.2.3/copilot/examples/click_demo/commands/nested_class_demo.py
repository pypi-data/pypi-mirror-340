"""类中类重写示例模块

展示如何在 Python 中重写嵌套类
"""

import click
from typing import Optional


class Outer:
    """外部类"""
    
    class Inner:
        """内部类"""
        def __init__(self, value: str):
            self.value = value
            
        def display(self) -> str:
            return f"Inner: {self.value}"
    
    def __init__(self):
        self.inner = self.Inner("original")


class ExtendedOuter(Outer):
    """扩展的外部类"""
    
    class Inner(Outer.Inner):
        """重写的内部类"""
        def __init__(self, value: str, extra: Optional[str] = None):
            super().__init__(value)
            self.extra = extra or "default"
            
        def display(self) -> str:
            base_output = super().display()
            return f"{base_output} (Extra: {self.extra})"
    
    def __init__(self):
        self.inner = self.Inner("extended", "custom")


# 添加命令行接口来演示类中类的重写
@click.group()
def nested():
    """嵌套类演示命令组"""
    pass


@nested.command()
def demo():
    """演示类中类的重写"""
    # 创建原始类实例
    original = Outer()
    click.echo("原始类输出:")
    click.echo(original.inner.display())
    
    # 创建扩展类实例
    extended = ExtendedOuter()
    click.echo("\n扩展类输出:")
    click.echo(extended.inner.display())