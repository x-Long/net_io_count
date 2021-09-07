# net_io_count
在桌面动态显示实时网卡上传与下载流量

> **Motivation**: 一般的杀软类似360，火绒都会携带类似的小插件，非常美观易用，但是为了一个小插件专门去下载杀软没有必要，由此自己动手写一个并设为开机启动，非常方便。

## 1、终端运行
```shell script
pip install PyQt5 psutil
python3 run.py
```

## 2、图形界面运行
```shell script
cd ./dist/run
doubleclick the run.exe
# 建议可以设置为开机启动，会自动隐藏至托盘，不会出现在任务栏。
```
