from setuptools import setup, find_packages

setup(
    name='killproc',
    version='1.0.0',
    author='Jeff Fischer',
    author_email='jeffrey.fischer@genforma.com',
    url='https://github.com/jfischer/killproc',
    packages=find_packages(),
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'killproc = killproc.killproc:main'
            ]},
    install_requires=[],
    license='Apache V2.0',
    description='Kill unix processes by name',
    long_description=open('README.rst').read(),
    )
