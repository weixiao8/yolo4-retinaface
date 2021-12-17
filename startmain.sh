cd /home/edgeb/od/yolo4-retinaface/
nohup python3 main.py >./startmain.log 2>&1 &
nohup python3 predict.py >./predict.log 2>&1 &
nohup python3 jpgpush.py >./jpgpush.log 2>&1 &