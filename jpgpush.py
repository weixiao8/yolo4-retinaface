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
import requests


def ToPush(filename):
    print(filename)
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K) tuhuAndroid 5.24.6',
               'content-type': 'application/json',
               "secretKey": "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"
               }

    f = open(filename, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    # 若yolo储存过程中出现读取图片文件失败的问题
    if not ls_f:
        return 0
    # 推送地址
    url = "http://njdt.njtjy.org.cn:10032/api/intelligentPrediction/save"
    # base64的encode转码过后是b'开头的bytes类型，需先转换成字符串去掉头尾之后才可以用
    jpgbase64 = "data:image/jpg;base64," + str(ls_f)[2:-1]  # "data:image/jpg;base64,"是java后端解析base64的格式前缀
    data = {"aiDeviceNo": "NJXQLYFZYXGS-001", "type": "1", "warningNum": "1", "imgBase64": jpgbase64}  # Post请求发送的数据，字典格式
    # data需要转化成json才能post
    res = requests.post(url=url, data=json.dumps(data), headers=headers)  # 这里使用post方法，参数和get方法一样
    print(res.text)
    response = res.text[8:11]
    f.close()
    # 返回值为200则添加数据成功，返回415 500等均为失败
    if response == "200":
        print("上传成功！")
        return 1
    else:
        print("上传失败！")
        return 0


def clear_dir(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            time.sleep(0.1)
            os.remove(path_file)
        else:
            for f in os.listdir(path_file):
                path_file2 = os.path.join(path_file, f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)


def start_push_image_to_web(interval):
    interval_flag = 0
    while 1:
        yearmonthdayfile = time.strftime("%Y_%m_%d", time.localtime())
        jpgpath = yearmonthdayfile + "/"
        if interval_flag == 1:
            for i in range(interval):
                time.sleep(1)
                print("等待{}秒".format(i))
                clear_dir(jpgpath)
        if not os.path.exists(jpgpath):
            interval_flag = 0
            # print("暂无预警")
            continue
        files = os.listdir(jpgpath)
        if len(files) == 0:
            interval_flag = 0
            # print("暂无预警")
            continue
        if len(files) > 0:
            print(files)
            time.sleep(1)
            filename = jpgpath + files[0]
            res = ToPush(filename)
            if res == 0:
                print("图片推流失败！")
            if res == 1:
                print("清空剩余的frame！")
                if not os.listdir(jpgpath):
                    print("文件夹已经清空！")
                interval_flag = 1


if __name__ == "__main__":
    interval = 10
    print("图片推送系统已开启！")
    start_push_image_to_web(interval)
