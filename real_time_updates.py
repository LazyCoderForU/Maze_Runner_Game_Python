import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on('player_move')
async def handle_player_move(sid, data):
    await sio.emit('update_position', data, skip_sid=sid)

# To run: uvicorn real_time_updates:app_sio --host 0.0.0.0 --port 5002