# -*- coding: utf-8 -*-
import os
import pdfkit
import logging
import sys

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("CreatePDF")
# 文件日志
file_handler = logging.FileHandler("CreatePDF.log")
# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

tag = True
for(root,dirs,files) in os.walk("./"):
    for filename in files:
        if tag and root.find("/medicalResult/国家发改委/部门规范性文件/2007.10.") <= 0:
            continue;
        else:
            tag = False
        try:
            if filename.find(".txt") > 0:
                print(os.path.join(root,filename))
                # print("find html:" + root)
                # print("fileName: " + filename[:filename.find(".html")])
                pdfPath = os.path.join(root, filename[:filename.find(".txt")] + '.pdf')
                options = {
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'custom-header': [
                        ('Accept-Encoding', 'gzip')
                    ],
                    'cookie': [
                        ('cookie-name1', 'cookie-value1'),
                        ('cookie-name2', 'cookie-value2'),
                    ],
                    'outline-depth': 20,
                    'zoom': 3,
                }

                pdfkit.from_file(os.path.join(root, filename), pdfPath, options=options)
        except IOError:
            logger.error('CreatePDF Error:', IOError)
            logger.error('Error File',os.path.join(root,filename))


    # for dirc in dirs:
    #     print(os.path.join(root,dirc))