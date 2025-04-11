# setup.py

from setuptools import setup, find_packages

setup(
    name='CognitiveSDK',
    version='1.0.0.post2',
    description='Cognitive SDK',
    author='Turan Abdullah',
    author_email='turan.skt@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'loguru',
        'zmq==0.0.0',
        'pyyaml',
        'numpy==2.2.4',
        'brainflow==5.16.0',
        'httpx==0.28.1',
        'pika==1.3.2',
        'dotenv==0.9.9',
    ],
    include_package_data=True,
    zip_safe=False,
)