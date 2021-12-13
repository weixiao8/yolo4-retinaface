############################
# 向管理平台推流：
# 将基于yolo4的待检测目标通过jetson nano的盒子推流到目标web上
# data数据中的deviceNo是需要在web平台上先注册的，非注册设备名称无法推流
# base64转码必须是jpg文件，否则无法在web平台上转码显示
########################
import base64
import json
import os
import time
from io import BytesIO

import requests
from PIL import Image


def frame2base64(frame):
    #-----------------------------------------------------------------
    # 在目标检测或者人脸识别中同步将frame转换为jpg储存在内存中的方式
    # 该方式速度快，但在发送请求时依赖于网络速度，若遭遇网络堵塞可能导致整个检测模块异常
    # 该方式可以选择save进BytesIO的格式
    # ----------------------------------------------------------------
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data  # 转码成功 返回base64编


def ToPush(filename):
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K) tuhuAndroid 5.24.6',
               'content-type': 'application/json',
               "secretKey": "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"
               }

    ls_f = frame2base64(filename)  # 读取文件内容，转换为base64编码
    # 若yolo储存过程中出现读取图片文件失败的问题
    if not ls_f:
        return 0
    # 推送地址
    url = "http://njdt.njtjy.org.cn:10032/api/intelligentPrediction/save"
    # base64的encode转码过后是b'开头的bytes类型，需先转换成字符串去掉头尾之后才可以用
    jpgbase64 = "data:image/jpg;base64," + str(ls_f)[2:-1]  # "data:image/jpg;base64,"是java后端解析base64的格式前缀
    print(jpgbase64)
    data = {"deviceNo": "MARK-42", "type": "2", "warningNum": "1", "imgBase64": jpgbase64}  # Post请求发送的数据，字典格式
    # data需要转化成json才能post
    res = requests.post(url=url, data=json.dumps(data), headers=headers)  # 这里使用post方法，参数和get方法一样
    print(res.text)
    response = res.text[8:11]

    # 返回值为200则添加数据成功，返回415 500等均为失败
    if response == "200":
        return 1
    else:
        return 0


