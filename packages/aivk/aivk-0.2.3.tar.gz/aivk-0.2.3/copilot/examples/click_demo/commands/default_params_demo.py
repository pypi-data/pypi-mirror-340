"""默认参数详解

此模块详细展示了 Python 中默认参数的概念和最佳实践：
1. 默认参数的基本用法
2. 为什么默认参数必须在非默认参数之后
3. 默认参数的陷阱
4. 最佳实践
"""

import click
from typing import List, Dict, Any, Optional
from datetime import datetime


def greet(name: str, greeting: str = "你好") -> str:
    """基本的默认参数示例
    
    Args:
        name: 要问候的人名
        greeting: 问候语，默认为"你好"
    """
    return f"{greeting}, {name}!"


# 错误示例：这会导致 SyntaxError
# def wrong_order(greeting="你好", name):  # 这是错误的！
#     return f"{greeting}, {name}!"


def create_person(
    name: str,
    age: int,
    city: str = "北京",
    hobbies: Optional[List[str]] = None
) -> Dict[str, Any]:
    """多个默认参数示例
    
    Args:
        name: 姓名（必需参数）
        age: 年龄（必需参数）
        city: 城市（可选，默认为"北京"）
        hobbies: 爱好列表（可选，默认为None）
    """
    return {
        "name": name,
        "age": age,
        "city": city,
        "hobbies": hobbies or []
    }


# 默认参数的常见陷阱
def bad_append(value: int, items: List[int] = []) -> List[int]:
    """错误的默认参数用法 - 可变默认值
    
    不要使用可变对象作为默认值！
    每次调用都会使用同一个列表对象
    """
    items.append(value)
    return items


def good_append(value: int, items: Optional[List[int]] = None) -> List[int]:
    """正确的默认参数用法
    
    使用 None 作为默认值，在函数内部创建新的列表
    """
    if items is None:
        items = []
    items.append(value)
    return items


class Person:
    """使用默认参数的类示例"""
    
    def __init__(
        self,
        name: str,
        age: int,
        address: Optional[str] = None,
        created_at: datetime = datetime.now()  # 注意：这也是一个陷阱！
    ):
        self.name = name
        self.age = age
        self.address = address
        self.created_at = created_at


# 添加命令行接口来演示默认参数
@click.group()
def default_params():
    """默认参数演示命令组"""
    pass


@default_params.command()
@click.argument('name')
@click.option('--greeting', default="你好", help="自定义问候语")
def demo_greet(name: str, greeting: str):
    """基本默认参数演示"""
    result = greet(name, greeting)
    click.echo(result)


@default_params.command()
def demo_trap():
    """默认参数陷阱演示"""
    # 演示可变默认值的问题
    click.echo("错误示例 - 使用可变默认值:")
    click.echo(bad_append(1))  # [1]
    click.echo(bad_append(2))  # [1, 2] - 注意列表被共享了！
    click.echo(bad_append(3))  # [1, 2, 3]
    
    click.echo("\n正确示例 - 使用 None 作为默认值:")
    click.echo(good_append(1))  # [1]
    click.echo(good_append(2))  # [2]
    click.echo(good_append(3))  # [3]


@default_params.command()
@click.argument('name')
@click.argument('age', type=int)
@click.option('--city', default="北京", help="城市")
@click.option('--hobby', multiple=True, help="爱好（可多次指定）")
def create_profile(name: str, age: int, city: str, hobby: tuple):
    """创建个人信息示例"""
    person = create_person(name, age, city, list(hobby))
    click.echo("创建的个人信息:")
    for key, value in person.items():
        click.echo(f"{key}: {value}")


if __name__ == "__main__":
    default_params()