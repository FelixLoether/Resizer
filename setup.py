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
    version='0.0.1',
    url='http://github.com/FelixLoether/resizer',
    author='Oskari Hiltunen',
    author_email='resizer@loethr.net',
    description='Resizer helps you generate thumbnails and '
                'load images from various sources.',
    long_description=open('README.md').read(),
    packages=['resizer'],
    platforms='any',
    install_requires=['Pillow>=1.7.7'],
    cmdclass={'test': PyTest}
)
