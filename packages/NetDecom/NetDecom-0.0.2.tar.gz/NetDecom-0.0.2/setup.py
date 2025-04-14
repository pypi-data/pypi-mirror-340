from setuptools import setup, find_packages

setup(
    name='NetDecom',  # 包名
    version='0.0.2',  # 版本号
    description='Dimensionality Reduction and Decomposition of Undirected Graph Models and Bayesian Networks',  # 包的描述
    author='P. Heng',  # 作者
    author_email='peiheng@nenu.edu.cn',  # 作者邮箱
    packages=find_packages(),  # 查找所有包
    install_requires=['networkx'],  # 依赖包
    long_description=open('README.md').read(),  # 从README文件读取详细描述
    long_description_content_type='text/markdown',  # README文件的格式
    classifiers=[  # 选择适当的分类
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',  # 适用于Python 3.9
        'License :: OSI Approved :: MIT License',  # 许可证类型
        'Operating System :: OS Independent',  # 跨平台
    ],
)
