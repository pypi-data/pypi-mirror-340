"""Click CLI 演示项目

此项目用于展示 Click 框架的高级特性和最佳实践
"""

import click
from typing import Optional, Dict, Any
from pathlib import Path
import os
import logging
from .commands.cli import cli

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """CLI 入口函数"""
    cli()