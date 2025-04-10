from setuptools import setup

setup(
    name="mypypack",
    version="1.0.1",
    packages=["cli"],
    entry_points={
        'console_scripts': ['my-test-command=cli.cli:hola'],
    },
    scripts=["bin/new.ps1"],
)