import asyncio
import struct

import websockets


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = "admin:123456"
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True


# 向服务器端发送认证后的消息
async def send_msg(websocket):
    fmt = '128si'  # 文件名最长128 i表示文件大小 i的数据类型决定了最大能够传输多大的文件

    head = await websocket.recv()
    filename = struct.unpack(fmt, head)[0].decode().rstrip('\0')
    print(f"{head}")
    print(f"{filename}")
    filename = './model_data_face/' + "2" + filename
    print(f"{filename}")
    fd = open(filename, 'wb')
    data = await websocket.recv()
    print(f"{data}")
    fd.write(data)
    fd.close()

    head = await websocket.recv()
    filename = struct.unpack(fmt, head)[0].decode().rstrip('\0')
    print(f"{head}")
    print(f"{filename}")
    filename = './model_data_face/' + "2" + filename
    print(f"{filename}")
    fd = open(filename, 'wb')
    data = await websocket.recv()
    print(f"{data}")
    fd.write(data)
    fd.close()


# 客户端主逻辑
async def main_logic():
    async with websockets.connect('ws://10.2.13.4:5000') as websocket:
        await auth_system(websocket)
        await send_msg(websocket)


asyncio.get_event_loop().run_until_complete(main_logic())
