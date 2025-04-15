from setuptools import setup, find_packages

setup(
    name='blockcoins',
    version='0.1.0',
    author='Vegeta',
    author_email='Gamma.scratch@gmail.com',
    description='A bot to automatically farm BlockCoins on blockcoin.vercel.app',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Gamma7113131/blockcoins',
    packages=find_packages(),
    install_requires=[
        'blockcoin',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12.8',
)
