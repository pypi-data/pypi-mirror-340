"""类变量和实例变量详解

此模块详细展示了 Python 中类变量和实例变量的各种特性和用法：
1. 类变量与实例变量的区别
2. 变量的访问和修改规则
3. 类变量的继承特性
4. 类变量在多实例间的共享特性
5. 描述符和属性装饰器的使用
6. 变量的命名空间查找规则
"""

import click
from typing import Dict, List, Any, ClassVar
from dataclasses import dataclass
import weakref


class TemperatureDescriptor:
    """温度描述符，展示描述符与类变量的结合"""
    
    def __init__(self, default: float = 20.0):
        self.default = default
        # 使用弱引用字典存储实例特定的值，避免内存泄漏
        self.data: Dict[int, float] = weakref.WeakKeyDictionary()
        
    def __get__(self, instance: Any, owner: type) -> float:
        if instance is None:
            return self.default
        return self.data.get(id(instance), self.default)
        
    def __set__(self, instance: Any, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("温度必须是数字类型")
        if value < -273.15:  # 绝对零度检查
            raise ValueError("温度不能低于绝对零度")
        self.data[id(instance)] = float(value)


class Animal:
    """基础动物类，用于展示类变量的基本用法"""
    
    # 类变量 - 所有实例共享
    species_count = 0  # 追踪物种数量
    all_animals: List["Animal"] = []  # 追踪所有动物实例
    
    # 使用描述符定义类变量
    default_temperature = TemperatureDescriptor()
    
    def __init__(self, name: str):
        # 实例变量 - 每个实例独有
        self.name = name
        self._age = 0
        self._temperature = 37.0
        
        # 更新类变量
        Animal.species_count += 1
        Animal.all_animals.append(self)
        
    @property
    def age(self) -> int:
        """年龄属性"""
        return self._age
        
    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value
        
    @classmethod
    def get_species_count(cls) -> int:
        """获取物种数量的类方法"""
        return cls.species_count
        
    @staticmethod
    def is_adult(age: int) -> bool:
        """判断是否成年的静态方法"""
        return age >= 18
        
    def __str__(self) -> str:
        return f"{self.name} (年龄: {self.age})"


class Dog(Animal):
    """狗类，用于展示类变量的继承特性"""
    
    # 子类特有的类变量
    breed_count = 0  # 追踪品种数量
    default_temperature = TemperatureDescriptor(38.5)  # 重写父类的类变量
    
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed
        Dog.breed_count += 1
        
    @classmethod
    def get_breed_count(cls) -> int:
        """获取品种数量"""
        return cls.breed_count


@dataclass
class AnimalStats:
    """使用数据类展示类变量和实例变量的另一种模式"""
    
    # 实例变量 - 每个实例独有（必需参数放在前面）
    name: str
    age: int
    weight: float
    species: str = "unknown"
    
    # 类变量 - 使用 ClassVar 显式标记
    database: ClassVar[Dict[str, List[str]]] = None  # 将在 __post_init__ 中初始化
    
    def __post_init__(self):
        # 确保类变量 database 被正确初始化
        if self.database is None:
            # 使用类变量存储所有实例的数据
            type(self).database = {}
        
        # 将实例数据添加到类变量中
        if self.species not in self.database:
            self.database[self.species] = []
        self.database[self.species].append(self.name)


# 添加命令行接口来演示类变量和实例变量的使用
@click.group()
def variables():
    """类变量和实例变量演示命令组"""
    pass


@variables.command()
def basic_demo():
    """基本用法演示"""
    # 创建动物实例
    cat = Animal("Whiskers")
    cat.age = 5
    
    dog = Animal("Buddy")
    dog.age = 3
    
    # 展示类变量的共享特性
    click.echo(f"总物种数量: {Animal.species_count}")
    click.echo(f"通过实例访问: {cat.species_count}")
    
    # 展示实例变量的独立性
    click.echo("\n动物列表:")
    for animal in Animal.all_animals:
        click.echo(f"- {animal}")


@variables.command()
def inheritance_demo():
    """继承特性演示"""
    # 创建不同品种的狗
    dog1 = Dog("Max", "Golden Retriever")
    dog2 = Dog("Charlie", "Labrador")
    
    # 展示类变量的继承和独立性
    click.echo(f"总物种数量: {Animal.species_count}")
    click.echo(f"狗的品种数量: {Dog.breed_count}")
    
    # 展示类变量的重写
    click.echo("\n默认体温:")
    click.echo(f"普通动物: {Animal.default_temperature}")
    click.echo(f"狗: {Dog.default_temperature}")


@variables.command()
def advanced_demo():
    """高级特性演示"""
    # 创建带统计信息的动物实例
    stats1 = AnimalStats("Milo", 4, 5.5, "cat")
    stats2 = AnimalStats("Luna", 2, 4.2, "cat")
    stats3 = AnimalStats("Rocky", 6, 15.8, "dog")
    
    # 展示类变量的数据收集功能
    click.echo("物种数据库:")
    for species, names in AnimalStats.database.items():
        click.echo(f"{species}: {', '.join(names)}")


if __name__ == "__main__":
    variables()