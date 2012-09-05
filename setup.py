from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='Resizer',
    version='0.1.0',
    url='http://github.com/FelixLoether/resizer',
    author='Oskari Hiltunen',
    author_email='resizer@loethr.net',
    description='Resizer helps you generate thumbnails and '
                'load images from various sources.',
    long_description=open('README.rst').read(),
    packages=['resizer'],
    platforms='any',
    install_requires=['Pillow>=1.7.7'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Graphics',
    ]
)
