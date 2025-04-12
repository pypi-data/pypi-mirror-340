"""变量赋值和解包详解

此模块详细展示了 Python 中变量赋值和解包的规则：
1. 基本的变量赋值
2. 序列解包（Sequence Unpacking）
3. 部分赋值的限制
4. 正确的赋值方式
"""

import click
from typing import Tuple, List, Any


def demo_basic_unpacking():
    """基本解包演示"""
    # 完整解包 - 正确
    a, b, c, d = [1, 2, 3, 4]  # OK
    print(f"完整解包: a={a}, b={b}, c={c}, d={d}")
    
    try:
        # 部分赋值 - 错误
        1, 2, d = [1, 2, 3, 4]  # SyntaxError: 字面量不能作为赋值目标
    except SyntaxError as e:
        print(f"\n错误示例 1 - 使用字面量:")
        print(f"SyntaxError: 不能将值赋给字面量")
    
    try:
        # 数量不匹配 - 错误
        x, y, z = [1, 2, 3, 4]  # ValueError: 值太多
    except ValueError as e:
        print(f"\n错误示例 2 - 值的数量不匹配:")
        print(f"ValueError: {e}")


def demo_correct_unpacking():
    """正确的解包方式演示"""
    # 使用变量接收所有值
    w, x, y, z = [1, 2, 3, 4]
    print(f"接收所有值: w={w}, x={x}, y={y}, z={z}")
    
    # 使用 * 运算符接收剩余值
    a, b, *rest = [1, 2, 3, 4]
    print(f"\n使用 * 接收剩余值:")
    print(f"a={a}, b={b}, rest={rest}")
    
    # 忽略部分值
    first, *_, last = [1, 2, 3, 4, 5]
    print(f"\n忽略中间值:")
    print(f"first={first}, last={last}")


@click.group()
def unpacking():
    """变量赋值和解包演示命令组"""
    pass


@unpacking.command()
def demo_all():
    """运行所有解包演示"""
    print("=== 基本解包演示 ===")
    demo_basic_unpacking()
    
    print("\n=== 正确解包方式演示 ===")
    demo_correct_unpacking()


if __name__ == "__main__":
    unpacking()