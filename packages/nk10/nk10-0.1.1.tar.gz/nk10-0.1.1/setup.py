from setuptools import setup

setup(
    name='nk10',
    version='0.1.1',
    py_modules=['nk10'],
    description='✨ One-function nk10 encoder/decoder using Hangul syllables (base-10000)',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='blueradiance',
    author_email='your@email.com',
    url='https://github.com/dzbuit/nk10',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
