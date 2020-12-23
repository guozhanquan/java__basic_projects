

import os


class Settings:

    SECRET_KEY = 'e50351efe80ddf91bf6c1d54a08db52f'


    # 图片上传后的保存路径
    UPLOAD_PATH = os.path.join(os.getcwd(), 'imageOct/static/upload')

    # 识别后的文件路径
    DOWNLOAD_PATH =         os.path.join(os.getcwd(), 'imageOct/static/download')

#scratches划痕保存路径
    DOWNLOAD_PATH_SCRATCH = os.path.join(os.getcwd(), 'imageOct/static/scratch')

    #bubble保存路径
    DOWNLOAD_PATH_BUBBLE =  os.path.join(os.getcwd(), 'imageOct/static/bubble')
    # 允许的文件类型
    ALLOWED_FILE = ['jpg', 'png', 'jpeg']
