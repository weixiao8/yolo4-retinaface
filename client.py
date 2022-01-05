import asyncio
import os
import struct
import time

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
    if filename == "404":
        print("未检测到更新！")
    else:
        print("检测到更新！")
        filename = './model_data_face/' + filename
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
        filename = './model_data_face/'  + filename
        print(f"{filename}")
        fd = open(filename, 'wb')
        data = await websocket.recv()
        print(f"{data}")
        fd.write(data)
        fd.close()
        os.system("shell/restart.sh")

# 客户端主逻辑
async def main_logic():
    async with websockets.connect('ws://192.168.3.2:2022') as websocket:
        await auth_system(websocket)
        await send_msg(websocket)

while 1:
    time.sleep(10)
    asyncio.get_event_loop().run_until_complete(main_logic())
