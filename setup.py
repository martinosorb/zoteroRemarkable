from setuptools import setup

setup(
    name='zoteroRemarkable',
    version='0.0.1',
    author='',
    author_email='martopix@gmail.com',
    packages=['zoteroRemarkable'],
    install_requires=['pyyaml', 'pyzotero'],
    package_data={'': ['config.ini']},
    include_package_data=True,
)
