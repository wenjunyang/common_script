#!/bin/sh

##########################################################
# example. batch.sh 20150709 20150803 xxx.sh arg1 arg2 ...
# 如果arg包含ARGTIMESTR，将会替换成YYYY-mm-dd
# 如果arg包含ARGTIMEID,将会替换成YYYYmmdd
##########################################################

function print_useage()
{
    echo "useage: batch.sh <start_date> <end_date> <command> [arguments]..."
}

if [[ $# < 3 ]]; then
    print_useage
    exit 1
fi
beg_s=`date -d "$1" +%s`
end_s=`date -d "$2" +%s`

#两次shift，移出日期参数
shift
shift

#获取命令字符串
args=""
until [ $# -eq 0 ] 
do
    args="$args $1"
    shift
done

echo "==========开始批量处理$(date -d "@$beg_s" "+%Y-%m-%d")到$(date -d "@$end_s" "+%Y-%m-%d")的任务==========="

echo $args
while [ "$beg_s" -le "$end_s" ]
do
    time_s=$(date -d "@$beg_s" "+%Y-%m-%d")
    time_id=$(date -d "@$beg_s" "+%Y%m%d")
    comm=${args//ARGTIMESTR/$time_s}
    comm=${comm//ARGTIMEID/$time_id}
    echo +++++++++++$comm++++++++++++++++
    bash $comm
    beg_s=$((beg_s+86400))
done
