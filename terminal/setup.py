from setuptools import setup

setup(
    name='purplemoon',
    version='0.1.0a0',
    py_modules=['client', 'server'], 
    entry_points={
        'console_scripts': [
            'purplemoon=client:start_connection',
            'purplemoon_server=server:handle_clients'
        ],
    },
    install_requires=[
        'pyaudio',
        'pyaes',
    ],
)