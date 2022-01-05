import base64
import os
import sys
from django.http import HttpResponse, JsonResponse
import json

secretKey = "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"


def is_base64_code(s):
    '''Check s is Base64.b64encode'''
    if not isinstance(s, str) or not s:
        raise ValueError("params s not string or None")

    _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                    '2', '3', '4', '5', '6', '7', '8', '9', '+',
                    '/', '=']

    # Check base64 OR codeCheck % 4
    code_fail = [i for i in s if i not in _base64_code]
    if code_fail or len(s) % 4 != 0:
        return False
    return True


# 增加人脸
def add_face(request):
    if request.method == "POST":
        key = request.META.get("HTTP_SECRETKEY", b'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        if len(name) < 2 or len(name) > 4:
            return JsonResponse({"state": "500", "msg": "人脸姓名字数异常！"})
        jpg_base64 = data["jpg"][22:]
        if not is_base64_code(jpg_base64):
            return JsonResponse({"state": "500", "msg": "编码异常！请检查传参！"})
        imagedata = base64.b64decode(jpg_base64)
        filename = "../face_dataset/" + name + "_1.jpg"
        file = open(filename, "wb")
        file.write(imagedata)
        file.close()
        if file:
            return JsonResponse({"state": "200", "msg": "添加人脸成功！"})
        else:
            return JsonResponse({"state": "500", "msg": "添加人脸失败！"})
#python manage.py runserver 10.2.13.4:8000

# 删除人脸
def delete_face(request):
    if request.method == "DELETE":
        key = request.META.get("HTTP_SECRETKEY", B'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        if len(name) < 2 or len(name) > 4:
            return JsonResponse({"state": "500", "msg": "人脸姓名字数异常！"})
        filename = "../face_dataset/" + name + "_1.jpg"
        if os.path.exists(filename):
            os.remove(filename)
            return JsonResponse({"state": "200", "msg": "删除人脸成功！"})
        else:
            return JsonResponse({"state": "500", "msg": "未找到该人脸！"})

# 增删人脸之后需要将整个检测模块重启！
def encode_face(request):
    if request.method == "GET":
        key = request.META.get("HTTP_SECRETKEY", B'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        os.system("chmod u+x /home/edgeb/od/new/yolo4-tiny/shell/restart.sh")
        os.system("shell/restart.sh")