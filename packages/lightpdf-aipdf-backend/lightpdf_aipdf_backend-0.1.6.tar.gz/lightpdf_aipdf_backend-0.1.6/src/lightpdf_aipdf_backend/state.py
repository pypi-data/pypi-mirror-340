from typing import Dict, List, Optional, Any
from collections import defaultdict
from openai import AsyncOpenAI
from mcp import ClientSession
from .config import Config

# 全局变量
mcp_session: Optional[ClientSession] = None
_openai_client = None
active_conversations = defaultdict(lambda: {"messages": [], "generator": None})
_session_history: List[Dict] = []
uploaded_files: Dict[str, Any] = {}

def get_openai_client():
    """获取OpenAI客户端，如果不存在则创建
    
    Returns:
        OpenAI: OpenAI客户端
    """
    global _openai_client
    if _openai_client is None:
        # 验证配置
        Config.validate()
        
        # 创建异步客户端
        _openai_client = AsyncOpenAI(
            api_key=Config.API_KEY,
            base_url=Config.BASE_URL
        )
    return _openai_client

def set_mcp_session(session: ClientSession):
    """设置MCP会话"""
    global mcp_session
    mcp_session = session

def get_mcp_session() -> Optional[ClientSession]:
    """获取MCP会话"""
    return mcp_session

def reset_session_history():
    """重置会话历史"""
    global _session_history
    _session_history = []

def get_session_history() -> List[Dict]:
    """获取会话历史"""
    return _session_history

def update_session_history(history: List[Dict]):
    """更新会话历史"""
    global _session_history
    _session_history = history 