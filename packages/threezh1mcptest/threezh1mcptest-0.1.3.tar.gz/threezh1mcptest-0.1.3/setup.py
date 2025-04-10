from setuptools import setup, find_packages

setup(
    name="threezh1mcptest",  # 包名
    version="0.1.3",  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 包的依赖项
       'mcp'
    ],
    author="Threezh1",
    author_email="xiaothreezhi@example.com",
    description="A simple example Python package",
    long_description=open("README.md").read(),  # 读取 README 作为长描述
    long_description_content_type="text/markdown",  # 说明 long_description 是 markdown 格式
    url="https://github.com/yourusername/my_package",  # 项目的 GitHub 地址或官网
    entry_points={"console_scripts": ["threezh1mcptest=threezh1mcptest.main:main"]},
    classifiers=[  # 用于 PyPI 分类
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定 Python 版本
)