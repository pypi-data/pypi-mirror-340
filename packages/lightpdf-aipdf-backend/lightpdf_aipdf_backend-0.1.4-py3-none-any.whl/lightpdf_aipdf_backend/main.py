import os
import asyncio
import uvicorn
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .config import Config, UPLOADS_DIR
from .state import set_mcp_session, init_openai_client
from .app import app
from .tools import get_tools

async def main():
    """应用主入口"""
    # 初始化 OpenAI 客户端
    init_openai_client()
    
    # 准备 MCP 服务参数
    server_params = StdioServerParameters(
        command="uvx",
        args=["lightpdf_aipdf_mcp@latest"],
        # args=["-n", "../../../mcp_server/dist/lightpdf_aipdf_mcp-0.0.1-py3-none-any.whl"],
        cwd=UPLOADS_DIR,
        env={
            "API_KEY": os.getenv("API_KEY"),
        }
    )
    
    # 启动 MCP 会话
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # 设置全局 MCP 会话
            set_mcp_session(session)

            tools = await get_tools()
            print(tools)
            
            # 启动 FastAPI 服务器
            config = uvicorn.Config(app, port=3300)
            server = uvicorn.Server(config)
            await server.serve()

# 确保与原始 main 函数相同
if __name__ == "__main__":
    asyncio.run(main()) 