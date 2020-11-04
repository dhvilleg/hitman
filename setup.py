from setuptools import setup

setup(
    name='hitman',
    version='0.1',
    py_modules=['hitman'],
    install_requires=[
        'Click','pandas'
    ],
    entry_points='''
        [console_scripts]
        hitman=hitman:cli
    ''',
)