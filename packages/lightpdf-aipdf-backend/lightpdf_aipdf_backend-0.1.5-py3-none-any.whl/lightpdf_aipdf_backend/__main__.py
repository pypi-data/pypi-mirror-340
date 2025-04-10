"""
后端应用主入口模块
"""
import asyncio
from .main import main

if __name__ == "__main__":
    asyncio.run(main()) 