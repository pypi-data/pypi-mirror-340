# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict, NoReturn
from ..logger import setup_logging
from ..base.utils import AivkExecuter
from ..base.cli import AivkCLI
setup_logging(style="panel")  # 使用面板样式
logger = logging.getLogger("aivk.onInstall")

async def install(
    **kwargs: Dict[str, Any]
) -> NoReturn:
    """安装模块入口点
    
    Args:
        **kwargs: id
        
    Returns:
        NoReturn
    """
    id = kwargs.get("id", "fs")

    AivkCLI._validate_id(id)

    logger.info("Installing ...")

    await AivkExecuter.aexec(command=f"uv pip install aivk-{id}")

    logger.info(f"Installation of aivk-{id} completed.")

if __name__ == "__main__":
    # pass
    import asyncio
    asyncio.run(install())