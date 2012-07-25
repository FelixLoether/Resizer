from setuptools import setup

setup(
    name='Resizer',
    version='0.0.1',
    description='Resizer helps you generate thumbnails and '
                'load images from various sources.',
    packages=['resizer'],
    platforms='any',
    install_requires=['PIL>=1.1.6']
)
