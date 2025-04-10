# -*- encoding: UTF-8 -*-

from setuptools import setup

setup(

    name="str_data_cleaner",  # 包名

    version="0.0.1b1",  # 版本信息

    packages=['data_cleaner_bonc'],  # 要打包的项目文件夹

    include_package_data=True,  # 自动打包文件夹内所有数据

    zip_safe=True,  # 设定项目包为安全，不用每次都检测其安全性

    install_requires=[  # 安装依赖的其他包（测试数据）
        "bs4==0.0.2"
    ],
    description="清理标讯工具包"

    # 设置程序的入口为path

    # 安装后，命令行执行path相当于调用get_path.py中的fun方法

    # entry_points={
    #
    #     'console_scripts': [
    #
    #         'path = demo.get_path:fun'
    #
    #     ]
    #
    # },

)
