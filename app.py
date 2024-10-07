import asyncio
import websockets

connected = set()

async def chat(websocket, path):
    if len(connected) < 2:
        connected.add(websocket)
        try:
            async for message in websocket:
                for conn in connected:
                    if conn != websocket:
                        await conn.send(message)
        finally:
            connected.remove(websocket)
    else:
        await websocket.send("Chat room is full. Please try again later.")
        await websocket.close()

start_server = websockets.serve(chat, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()