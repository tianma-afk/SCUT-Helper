from langchain_deepseek import ChatDeepSeek
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from config.env_config import settings
import json
router = APIRouter(prefix="/chat" , tags=["智能"])
llm = ChatDeepSeek(
    model="deepseek-v4-pro",    # 指定模型
    temperature=0.7,            # 控制随机性
    streaming=True,              # 关键：开启流式
    api_key=settings.API_KEY  # 替换为你的 DeepSeek API 密钥
)
chain = llm
@router.post("/stream", summary="智能对话", description="智能对话入口")
async def chat_stream(message: str):
    async def event_generator():
        async for chunk in chain.astream([{"role": "user", "content": message}]):
            if chunk.content:
                event_data=json.dumps({
                    "type": "chunk",
                    "data": chunk.content
                },ensure_ascii=False)
                yield event_data
        end_data=json.dumps({
            "type": "end"
        },ensure_ascii=False)
        yield end_data
    return StreamingResponse(event_generator(), media_type="text/event-stream")