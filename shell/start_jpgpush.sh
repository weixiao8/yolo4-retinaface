# restart.sh
old_pid=$(ps ax|grep jpgpush.py|grep -v grep|awk '{print $1}')
echo "old_pid=${old_pid}"
if [ -z $old_pid ];then
    echo "Process Non-existent !"
    echo "Starting Process...."
    cd /home/edgeb/od/yolo4-retinaface/
    nohup python3 jpgpush.py >./my2.log 2>&1 &
else
    kill -9 ${old_pid}
    mid_pid=$(ps ax|grep jpgpush.py|grep -v grep|awk '{print $1}')
    if [ -z ${mid_pid} ];then
        echo "Process Close Success !"
        echo "Start Restarting....."
        cd /home/edgeb/od/yolo4-retinaface/
        nohup python3 jpgpush.py >./my.log 2>&1 &
    else
        echo "Process Close Fail !"
        exit 1
    fi
fi
new_pid=$(ps ax|grep jpgpush.py|grep -v grep|awk '{print $1}')

if [ -z ${new_pid} ];then
    echo "Restart Fail !"
else
    echo "Restart Success !"
    echo "new_pid=${new_pid}"
fi