from setuptools import setup

setup(
    name='nk30',
    version='1.0.2',
    py_modules=['nk30'],
    description='✨ nk30: Hybrid base-30000 Hangul + Hanja encoder/decoder',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='blueradiance',
    author_email='none@example.com',
    url='https://github.com/dzbuit/nk30',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
