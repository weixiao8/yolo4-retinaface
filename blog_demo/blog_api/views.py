import base64
import os
import sys
from django.http import HttpResponse, JsonResponse
import json

secretKey = "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"


# 增加人脸
def add_face(request):
    if request.method == "POST":
        key = request.META.get("HTTP_SECRETKEY", b'')
        if key != secretKey:
            return JsonResponse({"state": "404", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        jpg_base64 = data["jpg"][22:]
        imagedata = base64.b64decode(jpg_base64)
        filename = "../face_dataset/" + name + "_1.jpg"
        file = open(filename, "wb")
        file.write(imagedata)
        file.close()
        if file:
            return JsonResponse({"state": "200", "msg": "添加人脸成功！"})
        else:
            return JsonResponse({"state": "500", "msg": "添加人脸失败！"})

#删除人脸
def delete_face(request):
    if request.method == "DELETE":
        key = request.META.get("HTTP_SECRETKEY", B'')
        if key != secretKey:
            return JsonResponse({"state": "404", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        filename = "../face_dataset/" + name + "_1.jpg"
        if os.path.exists(filename):
            os.remove(filename)
            return  JsonResponse({"state" : "200", "msg": "删除人脸成功！"})
        else:
            return JsonResponse({"state": "404", "msg": "未找到该人脸！"})

#增删人脸之后需要将整个检测模块重启！
