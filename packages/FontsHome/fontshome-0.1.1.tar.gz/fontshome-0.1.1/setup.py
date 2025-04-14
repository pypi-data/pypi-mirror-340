from setuptools import setup, find_packages

setup(
    name="FontsHome",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
    ],
    package_data={
        '': ['FontsHome/fonts/*.otf'],
    },
    author="YanXinle",
    author_email="1020121123@qq.com",
    url="https://gitee.com/yanxinle1123/FontsHome",
)
