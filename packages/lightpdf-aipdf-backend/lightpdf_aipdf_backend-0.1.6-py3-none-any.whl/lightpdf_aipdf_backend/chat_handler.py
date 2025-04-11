import json
from typing import List, Dict, AsyncGenerator, Any, Tuple
from fastapi import HTTPException

from .state import get_openai_client, get_session_history, update_session_history, reset_session_history, get_mcp_session
from .models import Message
from .file_handler import get_file_references
from .tools import get_tools, format_tool_response, process_tool_path
from .utils import validate_and_fix_messages, async_generator_to_json_stream
from .config import Config

async def handle_tool_call(tool_call: Any, api_messages: List[Dict]) -> Tuple[Dict, Dict]:
    """处理单个工具调用
    
    Args:
        tool_call: 工具调用对象
        api_messages: API消息列表
    
    Returns:
        Tuple[Dict, Dict]: 工具响应消息和yield消息
    """
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    tool_args = await process_tool_path(tool_args)
    
    try:
        mcp_session = get_mcp_session()
        tool_response = await mcp_session.call_tool(tool_name, tool_args)
        formatted_response = format_tool_response(tool_response.model_dump())
        
        tool_response_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": formatted_response
        }
        
        yield_message = {
            "type": "step",
            "step_type": "result",
            "content": formatted_response
        }
        
    except Exception as e:
        error_msg = str(e)
        tool_response_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": f"Error: {error_msg}"
        }
        
        yield_message = {
            "type": "error",
            "content": f"工具 {tool_name} 调用失败：{error_msg}"
        }
    
    return tool_response_message, yield_message

async def collect_stream_content(response: Any) -> AsyncGenerator[Dict, Tuple[str, str, List[Dict], Any]]:
    """收集流式响应内容
    
    Args:
        response: OpenAI流式响应对象
    
    Yields:
        Dict: 处理后的消息
        
    Returns:
        Tuple[str, str, List[Dict], Any]: 完整内容、完成原因、工具调用数据和usage信息
    """
    full_content = ""
    finish_reason = None
    tool_calls_data = []
    usage_info = None
    yield_content = False
    
    # 添加用于token计数的变量，用于在无法获取usage时估算
    completion_tokens = 0
    
    # 使用异步方式处理流
    try:
        # 迭代处理流
        chunk_count = 0
        last_chunk = None
        
        async for chunk in response:
            chunk_count += 1
            last_chunk = chunk  # 保存最后一个chunk，因为usage信息可能在最后
            
            # 检查usage属性
            if hasattr(chunk, 'usage') and chunk.usage:
                usage_info = chunk.usage
            
            # 检查chunk是否有choices，防止索引错误
            if not hasattr(chunk, 'choices') or not chunk.choices:
                continue
            
            # 安全获取第一个choice
            try:
                choice = chunk.choices[0]
            except IndexError:
                continue
            
            # 检查choice的finish_reason
            if hasattr(choice, 'finish_reason') and choice.finish_reason:
                finish_reason = choice.finish_reason
            
            # 如果没有delta属性，跳过
            if not hasattr(choice, 'delta'):
                continue
            
            delta = choice.delta
            
            # 处理内容
            if delta.content:
                content_piece = delta.content
                full_content += content_piece
                completion_tokens += len(content_piece) // 4  # 粗略估计token数
                
                # 发送流式块
                yield {
                    "type": "stream_chunk",
                    "content": content_piece
                }
                yield_content = True
            
            # 处理工具调用
            if delta.tool_calls:
                for tool_call_delta in delta.tool_calls:
                    tc_index = tool_call_delta.index
                    while len(tool_calls_data) <= (tc_index or 0):
                        tool_calls_data.append({"id": None, "type": "function", "function": {"name": "", "arguments": ""}})
                    
                    tc_data = tool_calls_data[tc_index]
                    if tool_call_delta.id:
                        tc_data.update({"id": tool_call_delta.id})
                    
                    tc_function = tool_call_delta.function
                    if tc_function:
                        current_tool = tc_data["function"]
                        if tc_function.name:
                            current_tool["name"] = tc_function.name
                        if tc_function.arguments:
                            args_content = tc_function.arguments
                            current_tool["arguments"] = current_tool.get("arguments", "") + args_content
                            completion_tokens += len(args_content) // 4
        
        # 检查最后一个chunk是否包含usage信息
        if not usage_info and last_chunk and hasattr(last_chunk, 'usage') and last_chunk.usage:
            usage_info = last_chunk.usage
        
        # 如果仍然没有获取到usage信息，使用估算值
        if not usage_info:
            from openai.types.completion_usage import CompletionUsage
            
            # 估算提示token（通常是完成token的3倍）
            prompt_tokens = max(completion_tokens * 3, 1)
            total_tokens = prompt_tokens + completion_tokens
            
            usage_info = CompletionUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=max(completion_tokens, 1),
                total_tokens=max(total_tokens, 2)
            )
        
    except Exception as e:
        print(f"处理流式响应时出错: {str(e)}")
        import traceback
        print(traceback.format_exc())
    
    # 返回收集的完整内容信息
    yield (full_content, finish_reason, tool_calls_data, usage_info)

async def process_messages(messages: List[Message]) -> List[Dict]:
    """处理消息列表，包括文件处理和格式转换
    
    Args:
        messages: 消息列表
        
    Returns:
        List[Dict]: 处理后的消息列表
    """
    # 检查是否是新会话
    is_new_session = len(messages) <= 2  # 通常新会话只有系统消息和用户消息
    session_history = get_session_history()
    
    if is_new_session:
        reset_session_history()
    
    # 转换消息并处理文件
    processed_messages = []
    
    # 如果有会话历史且不是新会话，优先使用会话历史
    if session_history and not is_new_session:
        # 添加会话历史中的消息
        processed_messages.extend(session_history)
        
        # 只处理会话历史之后的新消息
        new_messages = messages[len(session_history):]
    else:
        new_messages = messages
    
    for msg in new_messages:
        # 基本消息结构
        message_dict = {"role": msg.role, "content": msg.content}
        
        # 处理assistant角色的工具调用
        if msg.role == "assistant" and msg.tool_calls:
            message_dict["tool_calls"] = msg.tool_calls
            # 当有工具调用时，content可以为空字符串
            if not message_dict["content"]:
                message_dict["content"] = ""
        
        # 处理tool角色的工具响应
        if msg.role == "tool":
            if msg.tool_call_id:
                message_dict["tool_call_id"] = msg.tool_call_id
            if msg.name:
                message_dict["name"] = msg.name
            # 确保tool角色必须有tool_call_id和name
            if "tool_call_id" not in message_dict or "name" not in message_dict:
                continue
        
        # 如果消息包含文件ID
        if msg.file_ids:
            file_urls = get_file_references(msg.file_ids)
            
            # 将文件引用添加到消息内容
            if file_urls:
                message_dict["content"] += "\n\n以下是文件附件的Markdown链接:\n\n" + "\n".join(file_urls)
        
        processed_messages.append(message_dict)
    
    # 限制消息历史长度
    MAX_MESSAGES = 50  # 增加消息历史长度以保留工具调用上下文
    if len(processed_messages) > MAX_MESSAGES:
        processed_messages = processed_messages[-MAX_MESSAGES:]
    
    # 检查工具调用和响应的匹配
    return validate_and_fix_messages(processed_messages)

async def generate_chat_response(messages: List[Dict]) -> AsyncGenerator:
    """生成聊天响应
    
    Args:
        messages: 处理后的消息列表
        
    Yields:
        Dict: 响应内容
    """
    openai_client = get_openai_client()
    
    try:
        tools = await get_tools()
        api_messages = messages.copy()
        
        # 完全依赖流式响应
        
        while True:
            # 使用流式请求 - 异步客户端
            from openai.types.chat import ChatCompletionStreamOptionsParam
            
            response = await openai_client.chat.completions.create(
                model=Config.MODEL_NAME,
                temperature=0.4,
                messages=api_messages,
                tools=tools,
                parallel_tool_calls=False,
                stream=True,
                stream_options=ChatCompletionStreamOptionsParam(include_usage=True)  # 使用类型化对象
            )
            
            full_content = ""
            finish_reason = None
            tool_calls_data = []
            yield_content = False
            usage_info = None  # 初始化usage_info变量，用于存储token统计信息
            
            # 收集流式响应内容
            async for item in collect_stream_content(response):
                if isinstance(item, tuple):
                    if len(item) == 4:
                        full_content, finish_reason, tool_calls_data, usage_info = item
                else:
                    if not yield_content:
                        # 第一次消息通知
                        yield {
                            "type": "stream_start",
                            "content": ""
                        }
                        yield_content = True
                    
                    yield item
            
            # 如果需要调用工具
            if finish_reason == 'tool_calls' and tool_calls_data:
                if yield_content:
                    # 停止当前流
                    yield {
                        "type": "stream_end",
                        "content": full_content
                    }
                
                # 转换工具调用格式并创建消息
                tool_calls = []
                for tc_data in tool_calls_data:
                    tc_function = tc_data["function"]
                    if tc_data["id"] and tc_function["name"]:
                        tool_calls.append(type('ToolCall', (), {
                            'id': tc_data["id"],
                            'function': type('Function', (), {
                                'name': tc_function["name"],
                                'arguments': tc_function["arguments"]
                            })
                        }))
                
                # 创建助手消息
                assistant_message = {
                    "role": "assistant",
                    "content": full_content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in tool_calls
                    ]
                }
                
                # 准备API消息列表
                api_messages.append(assistant_message)
                
                # 处理每个工具调用
                for tool_call in tool_calls:
                    # 发送工具调用信息
                    yield {
                        "type": "step",
                        "step_type": "call",
                        "content": f"调用工具 {tool_call.function.name}\n参数：{tool_call.function.arguments}"
                    }
                    
                    # 处理工具调用
                    tool_response_message, yield_message = await handle_tool_call(tool_call, api_messages)
                    api_messages.append(tool_response_message)
                    yield yield_message
                
            else:
                # 如果不需要调用工具，直接结束流
                stream_end_data = {
                    "type": "stream_end",
                    "content": full_content
                }
                
                # 如果有使用统计信息，添加到输出中
                if usage_info:
                    stream_end_data["usage"] = {
                        "prompt_tokens": usage_info.prompt_tokens,
                        "completion_tokens": usage_info.completion_tokens,
                        "total_tokens": usage_info.total_tokens
                    }
                
                yield stream_end_data
                
                # 更新会话历史
                api_messages.append({
                    "role": "assistant",
                    "content": full_content
                })
                update_session_history(api_messages)

                break

    except Exception as e:
        yield {
            "type": "error",
            "content": str(e)
        } 