from typing import List

from fastapi import WebSocket, FastAPI, WebSocketDisconnect

from app.router import configure_routers
from app.services.groupchat import store_messages_to_db as group_storing
from app.services.private_chat import store_messages_to_db as private_storing
from app.services.globalchat import store_global_messages


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.group_chats = []
        self.new_group = []
        self.private_chats = []
        self.private_chat = []

    # GLOBAL PART

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                print("Message could not be sent...")

    # GROUP PART

    def create_group_chat(self, group_id: str):
        self.new_group = [group_id]
        self.group_chats.append(self.new_group)

    def check_exists(self, group_id: str):
        for connection in self.group_chats:
            if group_id in connection:
                return connection

    async def connect_to_group(self, group_id: str, websocket: WebSocket):
        for self.new_group in self.group_chats:
            if group_id in self.new_group:
                await websocket.accept()
                self.new_group.append(websocket)

    async def send_group_message(self, message: str, group_id: str):
        for connection in self.group_chats:
            if group_id in connection:
                for conn in connection:
                    try:
                        await conn.send_text(message)
                    except:
                        print("Message could not be sent")

    def disconnect_from_group(self, websocket: WebSocket, group_id: str):
        for self.new_group in self.group_chats:
            if group_id in self.new_group:
                self.new_group.remove(websocket)

    # PRIVATE PART
    def create_private_chat(self, chat_id: str):
        self.private_chat = [chat_id]
        self.private_chats.append(self.private_chat)

    def check_private_exists(self, chat_id: str):
        for connection in self.private_chats:
            if chat_id in connection:
                return connection

    async def connect_to_private_chat(self, chat_id: str, websocket: WebSocket):
        for self.private_chat in self.private_chats:
            if chat_id in self.private_chat:
                await websocket.accept()
                self.private_chat.append(websocket)

    async def send_private_message(self, message: str, chat_id: str):
        for connection in self.private_chats:
            if chat_id in connection:
                for conn in connection:
                    try:
                        await conn.send_text(message)
                    except:
                        print("Message could not be sent")

    def disconnect_from_private(self, websocket: WebSocket, chat_id: str):
        for self.private_chat in self.private_chats:
            if chat_id in self.private_chat:
                self.private_chat.remove(websocket)


app = FastAPI()
configure_routers(app)
manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            store_global_messages(message=f"{username}: {data}")
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{username} left the chat")


@app.websocket("/ws/{group_id}/{username}")
async def group_websocket_endpoint(websocket: WebSocket, group_id: str, username: str):
    group = manager.check_exists(group_id=group_id)
    if group:
        await manager.connect_to_group(group_id=group_id,
                                       websocket=websocket)
        try:
            while True:
                data = await websocket.receive_text()
                group_storing(group_id=group_id, message=f"{username}: {data}")
                await manager.send_group_message(message=f"{username}: {data}",
                                                 group_id=group_id)
        except WebSocketDisconnect:
            manager.disconnect_from_group(websocket=websocket, group_id=group_id)
            print(f"{username} DISCONNECTED")
    else:
        manager.create_group_chat(group_id=group_id)
        await manager.connect_to_group(group_id=group_id,
                                       websocket=websocket)
        try:
            while True:
                data = await websocket.receive_text()
                group_storing(group_id=group_id, message=f"{username}: {data}")
                await manager.send_group_message(message=f"{username}: {data}",
                                                 group_id=group_id)
        except WebSocketDisconnect:
            manager.disconnect_from_group(websocket=websocket, group_id=group_id)
            print(f"{username} DISCONNECTED")


@app.websocket("/ws/private_chat/{chat_id}/{username}")
async def private_websocket_endpoint(websocket: WebSocket, chat_id: str, username: str):
    chat = manager.check_private_exists(chat_id=chat_id)
    if chat:
        await manager.connect_to_private_chat(chat_id=chat_id,
                                              websocket=websocket)
        try:
            while True:
                data = await websocket.receive_text()
                private_storing(chat_id=chat_id, message=f"{username}: {data}")
                await manager.send_private_message(message=f"{username}: {data}",
                                                   chat_id=chat_id)
        except WebSocketDisconnect:
            manager.disconnect_from_private(websocket=websocket, chat_id=chat_id)
            print(f"{username} DISCONNECTED")
    else:
        manager.create_private_chat(chat_id=chat_id)
        await manager.connect_to_private_chat(chat_id=chat_id,
                                              websocket=websocket)
        try:
            while True:
                data = await websocket.receive_text()
                private_storing(chat_id=chat_id, message=f"{username}: {data}")
                await manager.send_private_message(message=f"{username}: {data}",
                                                   chat_id=chat_id)
        except WebSocketDisconnect:
            manager.disconnect_from_private(websocket=websocket, chat_id=chat_id)
            print(f"{username} DISCONNECTED")
