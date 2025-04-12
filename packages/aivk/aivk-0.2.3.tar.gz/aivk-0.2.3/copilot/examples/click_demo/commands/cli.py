"""CLI 命令模块

包含主要的命令组和基础命令实现
"""

import click
from pathlib import Path
from typing import Optional, List
import json
from .plugin_loader import PluginLoader
from .nested_class_demo import nested
from .variable_demo import variables


class Context:
    """CLI 上下文对象"""
    def __init__(self):
        self.verbose = False
        self.config = {}


class JsonType(click.ParamType):
    """JSON 参数类型"""
    name = 'json'
    
    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            self.fail(f"'{value}' 不是有效的 JSON 字符串", param, ctx)


# 创建参数类型实例
JSON = JsonType()


@click.group()  # 移除 chain=True
@click.option('--verbose', '-v', is_flag=True, help='启用详细输出模式')
@click.pass_context
def cli(ctx: click.Context, verbose: bool):
    """Click CLI 演示程序
    
    此程序展示了 Click 框架的各种高级特性和最佳实践。
    """
    # 初始化上下文
    ctx.obj = Context()
    ctx.obj.verbose = verbose
    
    if verbose:
        click.echo("详细模式已启用")


@cli.command()
@click.argument('text')
@click.option('--count', '-c', default=1, help='重复次数')
def echo(text: str, count: int):
    """回显文本
    
    TEXT 参数指定要回显的文本内容
    """
    for _ in range(count):
        click.echo(text)


@cli.command()
@click.argument('numbers', nargs=-1, type=float)
def calc(numbers: List[float]):
    """计算数字列表的总和
    
    NUMBERS 参数指定要计算的数字列表
    """
    total = sum(numbers)
    click.echo(f"总和: {total}")


@cli.group()
def config():
    """配置管理命令组"""
    pass


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.pass_obj
def config_set(obj: Context, key: str, value: str):
    """设置配置项
    
    KEY 参数指定配置项名称
    VALUE 参数指定配置项值
    """
    obj.config[key] = value
    click.echo(f"设置 {key}={value}")


@config.command('get')
@click.argument('key')
@click.pass_obj
def config_get(obj: Context, key: str):
    """获取配置项值
    
    KEY 参数指定配置项名称
    """
    value = obj.config.get(key)
    if value is None:
        click.echo(f"未找到配置项: {key}")
    else:
        click.echo(f"{key}={value}")


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径')
def process(input_path: str, output: Optional[str]):
    """处理文件内容
    
    INPUT_PATH 参数指定输入文件路径
    """
    with open(input_path) as f:
        content = f.read().upper()
        
    if output:
        with open(output, 'w') as f:
            f.write(content)
        click.echo(f"处理后的内容已写入: {output}")
    else:
        click.echo(content)


def init_cli():
    """初始化 CLI，包括加载插件"""
    # 创建插件命令组
    plugins_group = PluginLoader.create_plugin_group(cli)
    
    # 获取当前包的根目录
    current_dir = Path(__file__).parent.parent
    plugins_dir = current_dir / "plugins"
    
    # 加载插件
    PluginLoader.load_plugins(plugins_group, plugins_dir)
    
    # 添加演示命令组
    cli.add_command(nested)
    cli.add_command(variables)
    
    return cli

# 更新主命令组
cli = init_cli()