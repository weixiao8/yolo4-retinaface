import asyncio
import time

import websockets
import socket, os, struct


# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    fmt = '128si'
    send_buffer = 4096
    # filepath = input("enter file path:")
    filepath = "./model_data_face/mobilenet_face_encoding.npy"
    if os.path.exists(filepath):
        filename = os.path.split(filepath)[1]
        filesize = os.path.getsize(filepath)
        print("filename:" + filename + "\nfilesize:" + str(filesize))
        head = struct.pack(fmt, filename.encode(), filesize)
        print(r"\nhead size:" + str(head.__len__()) + "\n" + str(head))
        await websocket.send(head)
        restSize = filesize
        fd = open(filepath, 'rb')
        count = 0
        while restSize >= send_buffer:
            data = fd.read(send_buffer)
            await websocket.send(data)
            restSize = restSize - send_buffer
            print(str(count) + " ")
            count = count + 1
        data = fd.read(restSize)
        await websocket.send(data)
        fd.close()
        print("successfully sent")
        os.remove(filepath)

        fmt = '128si'
        send_buffer = 4096
        # filepath = input("enter file path:")
        filepath = "./model_data_face/mobilenet_names.npy"
        filename = os.path.split(filepath)[1]
        filesize = os.path.getsize(filepath)
        print("filename:" + filename + "\nfilesize:" + str(filesize))
        head = struct.pack(fmt, filename.encode(), filesize)
        print(r"\nhead size:" + str(head.__len__()) + "\n" + str(head))
        await websocket.send(head)
        restSize = filesize
        fd = open(filepath, 'rb')
        count = 0
        while restSize >= send_buffer:
            data = fd.read(send_buffer)
            await websocket.send(data)
            restSize = restSize - send_buffer
            print(str(count) + " ")
            count = count + 1
        data = fd.read(restSize)
        await websocket.send(data)
        fd.close()
        print("successfully sent")
        os.remove(filepath)
    else:
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


# 把ip换成自己本地的ip
start_server = websockets.serve(main_logic, '0.0.0.0', 2022)
# 如果要给被回调的main_logic传递自定义参数，可使用以下形式
# 一、修改回调形式
# import functools
# start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
# 修改被回调函数定义，增加相应参数
# async def main_logic(websocket, path, other_param)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
