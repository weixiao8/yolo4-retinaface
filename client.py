import asyncio
import struct

import websockets


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True


# 向服务器端发送认证后的消息
async def send_msg(websocket):
    fmt = '128si'  # 文件名最长128 i表示文件大小 i的数据类型决定了最大能够传输多大的文件
    # recv_buffer = 4096
    # while True:
    #     headsize = struct.calcsize(fmt)
    #     head = websocket.recv(headsize)
    #     filename = struct.unpack(fmt, head)[0].decode().rstrip('\0')  # 要删掉用来补齐128个字节的空字符
    #     filename = './model_data_face/' + "2" + filename
    #     filesize = struct.unpack(fmt, head)[1]
    #     print("filename:" + filename + "\nfilesize:" + str(filesize))
    #     recved_size = 0
    #     fd = open(filename, 'wb')
    #     count = 0
    #     while True:
    #         data = websocket.recv(recv_buffer)
    #         recved_size = recved_size + len(data)  # 虽然buffer大小是4096，但不一定能收满4096
    #         fd.write(data)
    #         if recved_size == filesize:
    #             break
    #     fd.close()
    #     print("new file")
    # while True:
    #     _text = input("please enter your context: ")
    #     if _text == "exit":
    #         print(f'you have enter "exit", goodbye')
    #         await websocket.close(reason="user exit")
    #         return False
    #     await websocket.send(_text)
    headsize = struct.calcsize(fmt)
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
    async with websockets.connect('ws://127.0.0.1:5000') as websocket:
        await auth_system(websocket)

        await send_msg(websocket)


asyncio.get_event_loop().run_until_complete(main_logic())
