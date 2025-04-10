import os
import json
from typing import List, Dict, Any
from fastapi import HTTPException

from .state import get_mcp_session

async def get_tools() -> List[Dict]:
    """从MCP client获取工具列表
    
    Returns:
        List[Dict]: 工具列表
        
    Raises:
        HTTPException: MCP会话未初始化时抛出
    """
    mcp_session = get_mcp_session()
    if not mcp_session:
        raise HTTPException(status_code=500, detail="MCP session not initialized")
    
    tools_result = await mcp_session.list_tools()
    tools = []
    
    for tool in tools_result.tools:
        tool_dict = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        }
        tools.append(tool_dict)
    return tools

def format_tool_response(response_dict: Dict) -> str:
    """格式化工具响应，提取可能包含的Markdown内容
    
    Args:
        response_dict: 工具响应字典
        
    Returns:
        str: 格式化后的响应
    """
    print(response_dict)
    # 如果有 content 字段，优先使用它
    if 'content' in response_dict:
        return response_dict['content']
    
    # 如果有 markdown 字段，优先使用它
    if 'markdown' in response_dict:
        return response_dict['markdown']
    
    # 检查是否有返回文本字段
    if 'text' in response_dict:
        return response_dict['text']
    
    # 如果有结果字段，检查是否包含Markdown内容
    if 'result' in response_dict:
        result = response_dict['result']
        if isinstance(result, dict):
            # 优先查找markdown字段
            if 'markdown' in result:
                return result['markdown']
            elif 'text' in result:
                return result['text']
            elif 'content' in result:
                return result['content']
    
    # 否则返回格式化的JSON
    return f"工具返回结果：\n```json\n{json.dumps(response_dict, ensure_ascii=False, indent=2)}\n```"

async def process_tool_path(tool_args: Dict) -> Dict:
    """处理工具调用参数中的文件路径
    
    Args:
        tool_args: 工具调用参数
        
    Returns:
        Dict: 处理后的参数
    """
    if 'file_path' in tool_args:
        from .config import UPLOADS_DIR  # 避免循环导入
        
        file_path = tool_args['file_path']
        # 尝试确保文件路径正确
        if not os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            # 在uploads目录中查找
            for uploaded_file in os.listdir(UPLOADS_DIR):
                if file_name in uploaded_file:
                    full_path = os.path.join(UPLOADS_DIR, uploaded_file)
                    tool_args['file_path'] = full_path
                    break
    
    return tool_args 