from setuptools import setup, find_packages



with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyxdownload',
    version='0.2.0',
    packages=find_packages(),
    author='luffpyx',
    author_email='luffpyx@gmail.com',
    install_requires=[
        # Python 3.6+
        # pip install tqdm
    ],
    entry_points={
        'console_scripts': [
            'pyxdownload = pyxdownload.__main__:main',
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)