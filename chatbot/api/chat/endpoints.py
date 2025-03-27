import uuid
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from services.langchain import stream_response , session_history

router = APIRouter(
    prefix="/chat",
)
templates = Jinja2Templates(directory="chatbot/templates")
# templates = Jinja2Templates(directory="templates")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        session_id = str(uuid.uuid4())
        while True:
            input = await websocket.receive_text()
            await stream_response(
                user_input=input,
                session_id= session_id,
                ws=websocket
            )

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        del session_history[session_id]



@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html", context={})
