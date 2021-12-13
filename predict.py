# -----------------------------------------------------------------------#
#   predict.py将单张图片预测、摄像头检测、FPS测试和目录遍历检测等功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
# -----------------------------------------------------------------------#
import datetime
import time

import cv2
import numpy as np
from PIL import Image

from jpgpush_face import ToPush
from yolo import YOLO
from retinaface import Retinaface

if __name__ == "__main__":
    yolo = YOLO()
    retinaface = Retinaface()
    # ----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'video'表示视频检测，可调用摄像头或者视频进行检测，详情查看下方注释。
    #   'fps'表示测试fps，使用的图片是img里面的street.jpg，详情查看下方注释。
    #   'dir_predict'表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    # ----------------------------------------------------------------------------------------------------------#
    mode = "video"
    # ----------------------------------------------------------------------------------------------------------#
    #   video_path用于指定视频的路径，当video_path=0时表示检测摄像头
    #   想要检测视频，则设置如video_path = "xxx.mp4"即可，代表读取出根目录下的xxx.mp4文件。
    #   video_save_path表示视频保存的路径，当video_save_path=""时表示不保存
    #   想要保存视频，则设置如video_save_path = "yyy.mp4"即可，代表保存为根目录下的yyy.mp4文件。
    #   video_fps用于保存的视频的fps
    #   video_path、video_save_path和video_fps仅在mode='video'时有效
    #   保存视频时需要ctrl+c退出或者运行到最后一帧才会完成完整的保存步骤。
    # ----------------------------------------------------------------------------------------------------------#
    video_path = 0
    video_save_path = ""
    video_fps = 25.0
    # -------------------------------------------------------------------------#
    #   test_interval用于指定测量fps的时候，图片检测的次数
    #   理论上test_interval越大，fps越准确。
    # -------------------------------------------------------------------------#
    test_interval = 100
    # -------------------------------------------------------------------------#
    #   dir_origin_path指定了用于检测的图片的文件夹路径
    #   dir_save_path指定了检测完图片的保存路径
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    # -------------------------------------------------------------------------#
    dir_origin_path = "img/"
    dir_save_path = "img_out/"
    # -------------------------------------------------------------------------#
    #   path指定了用于推流目标识别的文件夹路径
    #   path_face用于推流人脸识别文件夹
    #   face_recognize为是否打开人脸识别模块
    # -------------------------------------------------------------------------#
    path = "frame_out/"
    path_face = "frame_out_face/"
    face_recognize = 1
    # 人脸识别认证时间，单位秒
    interval_face = 3
    #cv.show的开关
    showcv = 1
    #眼镜检测开关
    object_dection = 1

    import os

    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
    folder = os.path.exists(path_face)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path_face)
    if mode == "predict":
        '''
        1、如果想要进行检测完的图片的保存，利用r_image.save("img.jpg")即可保存，直接在predict.py里进行修改即可。 
        2、如果想要获得预测框的坐标，可以进入yolo.detect_image函数，在绘图部分读取top，left，bottom，right这四个值。
        3、如果想要利用预测框截取下目标，可以进入yolo.detect_image函数，在绘图部分利用获取到的top，left，bottom，right这四个值
        在原图上利用矩阵的方式进行截取。
        4、如果想要在预测图上写额外的字，比如检测到的特定目标的数量，可以进入yolo.detect_image函数，在绘图部分对predicted_class进行判断，
        比如判断if predicted_class == 'car': 即可判断当前目标是否为车，然后记录数量即可。利用draw.text即可写字。
        '''
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image)
                r_image.show()

    elif mode == "video":
        capture = cv2.VideoCapture(video_path)
        if video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)
        count_flag = 0
        count_flag_face = 0
        fps = 0.0
        #人脸识别判定的初始时间
        temptime1 = time.time()
        while (True):

            t1 = time.time()
            # 读取某一帧
            ref, frame = capture.read()
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_face = frame
            if object_dection:
                object_dection += 1
                # 转变成Image
                frame = Image.fromarray(np.uint8(frame))
                # 进行检测
                frame = np.array(yolo.detect_image(frame))
                # RGBtoBGR满足opencv显示格式
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                fps = (fps + (1. / (time.time() - t1))) / 2
                print("fps= %.2f" % (fps))
                frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if showcv:
                    cv2.imshow("video", frame)
                    c = cv2.waitKey(1) & 0xff
                    if video_save_path != "":
                        out.write(frame)
                    if c == 27:
                        capture.release()
                        break
                if count_flag < 2:
                    savefile = "frame_out/" + str(count_flag) + "_out.npy"
                    if not os.path.exists(savefile):
                        np.save(savefile, frame)
                    count_flag += 1

            # -------------------------------------------------------------------------#
            #   当face_recognize为1打开人脸检测模块
            #   interval_face 是检测多少秒仍未检测到合法的人脸的时间阈值，超过时间阈值，上传人脸到监管平台
            #   目标检测为异步推送，人脸识别为同步推送，同步推送当遇到网络堵塞会导致检测效率变低甚至故障
            # -------------------------------------------------------------------------#
            if face_recognize:
                frame_face, flag = retinaface.detect_image(frame_face)
                # ------------------------------------------------------------#
                # flag == 2表示未检测到人脸或者人脸异常
                # flag == 1表示检测到数据集中的合法人脸
                # flag == 0表示检测到非法人脸
                #-------------------------------------------------------------#
                if flag == 2 or flag == 1:
                    temptime1 = t1
                if flag == 0:
                    if int(t1 - temptime1) > interval_face:
                        print("未通过人脸验证，上传预警")
                        ToPush(frame_face)
                        temptime1 = t1
                frame_face = np.array(frame_face)
                frame_face = cv2.cvtColor(frame_face, cv2.COLOR_RGB2BGR)
                fps = (fps + (1. / (time.time() - t1))) / 2
                frame_face = cv2.putText(frame_face, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                         (0, 255, 0), 2)
                if 1:
                    cv2.imshow("video_face", frame_face)
                    c = cv2.waitKey(1) & 0xff
                    if video_save_path != "":
                        out.write(frame)
                    if c == 27:
                        capture.release()
                        break
                if count_flag_face < 2:
                    savefile_face = "frame_out_face/" + str(count_flag_face) + "_out.npy"
                    if not os.path.exists(savefile_face):
                        np.save(savefile_face, frame_face)
                    count_flag_face += 1
                if count_flag_face == 2:
                    count_flag_face = 0

            if count_flag == 2:
                count_flag = 0
        capture.release()
        cv2.destroyAllWindows()

    elif mode == "fps":
        img = Image.open('img/street.jpg')
        tact_time = yolo.get_FPS(img, test_interval)
        print(str(tact_time) + ' seconds, ' + str(1 / tact_time) + 'FPS, @batch_size 1')

    elif mode == "dir_predict":
        import os
        from tqdm import tqdm

        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path = os.path.join(dir_origin_path, img_name)
                image = Image.open(image_path)
                r_image = yolo.detect_image(image)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name))

    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
