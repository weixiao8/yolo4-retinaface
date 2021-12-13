import base64
import json
import os
import time

import cv2
import numpy as np
from flask import Flask, render_template, Response, request

secretKey = "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"
envr = "linux"  # 环境选择windows 或者 linux


class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # def get_frame(self):
    #     # success, image = self.video.read()
    #
    #     # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
    #     ret, jpeg = cv2.imencode('.jpg', image)
    #     return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')


def gen():
    count_flag = 0
    while True:

        if count_flag < 2:
            filename = "frame_out/" + str(count_flag) + "_out.npy"
            try:
                while not os.path.exists(filename):
                    pass
                time.sleep(0.05)
                image = np.load(filename)
            except:
                while not os.path.exists(filename):
                    pass
                time.sleep(0.05)
                image = np.load(filename)
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            count_flag += 1
        if count_flag == 2:
            count_flag = 0
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def face_recognize():
    count_flag = 0
    while True:
        if count_flag < 2:
            filename = "frame_out_face/" + str(count_flag) + "_out.npy"
            try:
                while not os.path.exists(filename):
                    pass
                time.sleep(0.1)
                image = np.load(filename)
            except:
                while not os.path.exists(filename):
                    pass
                time.sleep(0.05)
                image = np.load(filename)
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            count_flag += 1
        if count_flag == 2:
            count_flag = 0
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed_face')  # 这个地址返回视频流响应
def video_feed_face():
    return Response(face_recognize(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update', methods=['POST'])
def update():
    key = request.headers["secretKey"]
    if key != secretKey:
        return {"state": "404", "msg": "秘钥错误，请检查秘钥！"}
    data = json.loads(request.get_data(as_text=True))
    name = data["username"]
    jpg_base64 = data["jpg"][22:]
    imagedata = base64.b64decode(jpg_base64)
    filename = "face_dataset/" + name + "_1.jpg"
    file = open(filename, "wb")
    file.write(imagedata)
    file.close()
    if file:
        return {"state": "200", "msg": "添加人脸成功！"}
    else:
        return {"state": "500", "msg": "添加人脸失败！"}


@app.route('/delete', methods=['DELETE'])
def delete():
    key = request.headers["secretKey"]
    if key != secretKey:
        return {"state": "404", "msg": "秘钥错误，请检查秘钥！"}
    filename = "face_dataset/"
    data = json.loads(request.get_data(as_text=True))
    username = data["username"]
    name_list = os.listdir(filename)
    for fullname in name_list:
        name = fullname.split("_")[0]
        if username == name:
            os.remove(filename + fullname)
            return {"state": "200", "msg": "删除人脸成功！"}
    return {"state": "500", "msg": "删除人脸成功！"}


@app.route('/findAll', methods=['GET'])
def findAll():
    key = request.headers["secretKey"]
    if key != secretKey:
        return {"state": "404", "msg": "秘钥错误，请检查秘钥！"}
    filename = "face_dataset/"
    name_list = os.listdir(filename)
    username = []
    for fullname in name_list:
        name = fullname.split("_")[0]
        username.append(name)
    return str(username)


@app.route('/restartSystem', methods=['GET'])
def restartSystem():
    key = request.headers["secretKey"]
    if key != secretKey:
        return {"state": "404", "msg": "秘钥错误，请检查秘钥！"}
    if envr == "linux":
        os.system("chmod u+x /home/edgeb/od/new/yolo4-tiny/shell/restart.sh")
        os.system("shell/restart.sh")
    return {"state": "200", "msg": "系统初始化完成！系统将在40秒内完成启动！"}


@app.route('/startvideopush', methods=['GET'])
def startvideopush():
    key = request.headers["secretKey"]
    if key != secretKey:
        return {"state": "404", "msg": "秘钥错误，请检查秘钥！"}
    if envr == "linux":
        command_pushjpg = "chmod u+x " + os.getcwd() + "/shell/start_jpgpush.sh"
        os.system(command_pushjpg)
        os.system("shell/start_jpgpush.sh")
    return {"state": "200", "msg": "图片推送系统重启完成！"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
