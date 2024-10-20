from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from services.langchain import stream_response

router = APIRouter(
    prefix="/chat",
)
# templates = Jinja2Templates(directory="chatbot/templates")
templates = Jinja2Templates(directory="templates")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:

        while True:
            input = await websocket.receive_text()
            await stream_response(user_input=input, ws=websocket)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(f"Error: {str(e)}")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html", context={})
