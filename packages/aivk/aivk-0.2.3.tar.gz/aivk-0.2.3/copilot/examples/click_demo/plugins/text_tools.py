"""文本处理工具插件

提供文本处理相关的命令
"""

import click

@click.group()
def text():
    """文本处理命令组"""
    pass

@text.command()
@click.argument('text')
@click.option('--reverse', '-r', is_flag=True, help='反转文本')
def transform(text: str, reverse: bool):
    """转换文本
    
    TEXT 参数指定要处理的文本
    """
    if reverse:
        text = text[::-1]
    click.echo(text)

@text.command()
@click.argument('text')
@click.option('--uppercase', '-u', is_flag=True, help='转换为大写')
@click.option('--lowercase', '-l', is_flag=True, help='转换为小写')
def case(text: str, uppercase: bool, lowercase: bool):
    """转换文本大小写
    
    TEXT 参数指定要转换的文本
    """
    if uppercase and lowercase:
        click.echo("错误：不能同时指定大写和小写选项", err=True)
        return
    
    if uppercase:
        result = text.upper()
    elif lowercase:
        result = text.lower()
    else:
        result = text
    
    click.echo(result)

@text.command()
@click.argument('texts', nargs=-1)
@click.option('--separator', '-s', default=' ', help='连接符')
def join(texts: tuple, separator: str):
    """连接多个文本
    
    TEXTS 参数指定要连接的文本列表
    """
    result = separator.join(texts)
    click.echo(result)