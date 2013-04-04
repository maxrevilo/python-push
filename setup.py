from distutils.core import setup

setup(
    name='python-push',
    version='0.1.0',
    author='Oliver Perez',
    author_email='oliver.a.perez.c@gmail.com',
    packages=['python-push'],
    url='http://pypi.python.org/pypi/python-push/',
    license='LICENSE.txt',
    description='Python server-side library for sending Push Notifications to multiple mobile platforms.',
    long_description=open('README.rst').read(),
    install_requires=[
        "python-asynchttp",
    ],
)
