from typing import Dict, List, Optional, Any
from collections import defaultdict
from openai import OpenAI
from mcp import ClientSession

from .config import Config

# 全局变量
mcp_session: Optional[ClientSession] = None
openai_client: Optional[OpenAI] = None
active_conversations = defaultdict(lambda: {"messages": [], "generator": None})
session_history: List[Dict] = []
uploaded_files: Dict[str, Any] = {}

def init_openai_client():
    """初始化OpenAI客户端"""
    global openai_client
    Config.validate()
    openai_client = OpenAI(
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL
    )
    return openai_client

def get_openai_client() -> OpenAI:
    """获取OpenAI客户端实例"""
    global openai_client
    if openai_client is None:
        openai_client = init_openai_client()
    return openai_client

def set_mcp_session(session: ClientSession):
    """设置MCP会话"""
    global mcp_session
    mcp_session = session

def get_mcp_session() -> Optional[ClientSession]:
    """获取MCP会话"""
    return mcp_session

def reset_session_history():
    """重置会话历史"""
    global session_history
    session_history = []

def get_session_history() -> List[Dict]:
    """获取会话历史"""
    return session_history

def update_session_history(history: List[Dict]):
    """更新会话历史"""
    global session_history
    session_history = history 