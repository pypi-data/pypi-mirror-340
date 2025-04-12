"""插件加载器模块

提供动态加载插件命令的功能
"""

import click
import importlib
import pkgutil
from pathlib import Path
import logging
from importlib.util import spec_from_file_location, module_from_spec

logger = logging.getLogger(__name__)

class PluginLoader:
    """插件加载器类"""
    
    @staticmethod
    def load_plugins(group: click.Group, plugin_path: str | Path) -> None:
        """从指定路径加载插件命令
        
        Args:
            group: 要添加命令的命令组
            plugin_path: 插件目录路径或包路径
        """
        plugin_path = Path(plugin_path)
        
        if not plugin_path.exists():
            logger.warning(f"插件路径不存在: {plugin_path}")
            return
            
        if plugin_path.is_dir():
            # 从目录加载
            for item in plugin_path.glob("*.py"):
                if item.name.startswith("_"):
                    continue
                    
                try:
                    # 动态导入模块
                    module_name = item.stem
                    spec = spec_from_file_location(module_name, str(item))
                    if spec and spec.loader:
                        module = module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # 查找并注册命令
                        for item_name in dir(module):
                            item = getattr(module, item_name)
                            if isinstance(item, click.Command):
                                group.add_command(item)
                                logger.info(f"已加载插件命令: {item.name}")
                                
                except Exception as e:
                    logger.error(f"无法加载插件 {item.name}: {e}")
        else:
            # 从Python包加载
            try:
                package = importlib.import_module(str(plugin_path))
                package_dir = Path(package.__file__).parent
                
                for _, name, _ in pkgutil.iter_modules([str(package_dir)]):
                    if name.startswith("_"):
                        continue
                        
                    try:
                        module = importlib.import_module(f"{plugin_path}.{name}")
                        
                        for item_name in dir(module):
                            item = getattr(module, item_name)
                            if isinstance(item, click.Command):
                                group.add_command(item)
                                logger.info(f"已加载插件命令: {item.name}")
                                
                    except ImportError as e:
                        logger.error(f"无法加载插件模块 {name}: {e}")
                        
            except ImportError as e:
                logger.error(f"无法加载插件包 {plugin_path}: {e}")
    
    @staticmethod
    def create_plugin_group(cli: click.Group) -> click.Group:
        """创建并注册插件命令组
        
        Args:
            cli: 主命令组
            
        Returns:
            创建的插件命令组
        """
        @cli.group()
        def plugins():
            """插件命令组"""
            pass
            
        return plugins