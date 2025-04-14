from setuptools import setup

setup(
    name='nk30',
    version='0.1.1',
    py_modules=['nk30'],
    description='One-function Hangul/Hanja 30,000-base encoder/decoder',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='blueradiance',
    author_email='your@email.com',
    url='https://github.com/dzbuit/nk30',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
