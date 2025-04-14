from setuptools import setup

setup(
    name='nk20',
    version='1.0.1',
    py_modules=['nk20'],
    description='nk20: Hanja base-20000 numeral encoder/decoder',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='blueradiance',
    author_email='none@example.com',
    url='https://github.com/dzbuit/nk20',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
