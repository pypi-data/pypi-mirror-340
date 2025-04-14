from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

from .models import ChatRequest
from .file_handler import handle_file_upload
from .chat_handler import process_messages, generate_chat_response
from .utils import async_generator_to_json_stream

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 应用启动时的初始化
    yield
    # 应用关闭时的清理

# 创建FastAPI应用
app = FastAPI(title="LightPDF AI助手API", lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API根路径"""
    return {"message": "LightPDF AI助手 API已启动"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """处理文件上传请求"""
    return await handle_file_upload(file)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        # 处理消息
        processed_messages = await process_messages(request.messages)
        
        # 生成响应 - 修改响应头部，确保流式内容不被缓存或批处理
        return StreamingResponse(
            async_generator_to_json_stream(generate_chat_response(processed_messages)),
            media_type="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache, no-transform",
                "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
            }
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"LightPDF AI助手处理错误: {error_msg}") 