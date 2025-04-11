from setuptools import setup, find_packages

setup(
    name="yrspary",  # 包的名字
    version="1.0.0",  # 版本号
    packages=find_packages(),  # 自动找到所有包
    install_requires=[  # 列出你的依赖项
        'opcua'
    ],
    author="yrlab",
    author_email="2398603105@qq.com",
    description="Yueran Spray System Interface Library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # 如果你的 README 文件是 markdown 格式
    url="",  # GitHub 仓库或网站链接
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)