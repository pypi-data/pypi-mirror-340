import os
from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")

setup(
    name='coll-filter',
    packages=['cf'],
    description="Collaborative Filtering with multi-process parallelism.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.5.1',
    url='https://gitee.com/summry/myai',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['Collaborative Filtering', 'recommend'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)