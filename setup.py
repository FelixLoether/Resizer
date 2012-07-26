from setuptools import setup

setup(
    name='Resizer',
    version='0.0.1',
    description='Resizer helps you generate thumbnails and '
                'load images from various sources.',
    packages=['resizer'],
    platforms='any',
    install_requires=['Pillow>=1.7.7']
)
