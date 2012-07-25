from setuptools import setup

setup(
    name='TIP (title in progress)',
    version='0.0.1',
    description='TIP helps you generate thumbnails and '
                'load images from various sources.',
    packages=['tip'],
    platforms='any',
    install_requires=['PIL>=1.1.6']
)
