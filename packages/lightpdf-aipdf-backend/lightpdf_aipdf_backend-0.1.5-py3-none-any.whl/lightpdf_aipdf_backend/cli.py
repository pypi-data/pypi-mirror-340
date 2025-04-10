"""
CLI命令入口
"""
import asyncio
from .main import main

def run_server():
    """运行API服务器的命令行入口点"""
    asyncio.run(main()) 