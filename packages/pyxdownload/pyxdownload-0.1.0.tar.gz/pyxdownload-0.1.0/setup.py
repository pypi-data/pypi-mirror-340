from setuptools import setup, find_packages

setup(
    name='pyxdownload',
    version='0.1.0',
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
    }
)