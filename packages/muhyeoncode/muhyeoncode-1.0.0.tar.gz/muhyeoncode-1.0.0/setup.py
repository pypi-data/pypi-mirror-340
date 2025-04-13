from setuptools import setup

setup(
    name='muhyeoncode',
    version='1.0.0',
    py_modules=['무현코드'],
    entry_points={
        'console_scripts': [
            'muhyun=무현코드:main',
        ],
    },
    author='Donghyun Kim',
    author_email='your@email.com',
    description='🐉 무현 DSL 인터프리터',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)