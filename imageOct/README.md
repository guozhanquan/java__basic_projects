
![输入图片说明](https://images.gitee.com/uploads/images/2020/0513/095829_dcb8f1c1_5200175.png "1.png")



### 安装依赖

将项目克隆到本地，然后:

1. 进入imageOct文件夹
2. pipenv shell(创建虚拟环境,如果已安装相应依赖可以不选)
3. pip install -r requirements.txt


### 运行

Linux or MacOS

1. export FLASK_APP=imageOct
2. export FLASK_ENV=development (可加可不加)
3. flask run

Windows

将上述命令中的export替换为set即可


在没有改变默认端口(5000)的情况下，打开http://127.0.0.1:5000/ 即可看到功能区域，直接点击浏览并上传图片即可


### 下载yolo-v3权重文件
1. 链接：https://share.weiyun.com/5MLGhDC 密码：f57ajd
2. 放入YOLOV3文件夹下即可